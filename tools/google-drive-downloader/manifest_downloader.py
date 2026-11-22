"""Download explicitly listed Google Drive files safely using yt-dlp.

Manifest JSON:
{
  "Course/Week 1": [
    {"id": "DRIVE_FILE_ID", "name": "lecture.mp4"}
  ]
}

Usage: python manifest_downloader.py manifest.json --output downloads
Use --dry-run to inspect destinations without invoking yt-dlp.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import uuid
from pathlib import Path, PurePosixPath
from typing import Iterator

DRIVE_ID = re.compile(r"^[A-Za-z0-9_-]{10,256}$")
WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def relative_destination(value: str, *, allow_subdirs: bool) -> Path:
    """Accept only safe, portable relative paths, without traversal."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Destination must be a nonempty string")
    if "\\" in value or "\x00" in value:
        raise ValueError("Backslashes and NUL bytes are not allowed in paths")
    parts = PurePosixPath(value).parts
    if value.startswith("/") or not parts or any(
        part in ("", ".", "..") for part in value.split("/")
    ):
        raise ValueError(f"Unsafe relative path: {value!r}")
    if any(
        part.endswith((" ", "."))
        or any(ord(char) < 32 or ord(char) == 127 or char in '<>:"|?*' for char in part)
        or part.split(".", 1)[0].upper() in WINDOWS_RESERVED
        for part in parts
    ):
        raise ValueError(f"Nonportable or reserved destination: {value!r}")
    if not allow_subdirs and len(parts) != 1:
        raise ValueError("File names cannot contain subdirectories")
    return Path(*parts)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def destination_is_safe(path: Path, root: Path) -> bool:
    cursor = path
    while cursor != root:
        if cursor.is_symlink() or cursor == cursor.parent:
            return False
        cursor = cursor.parent
    return not root.is_symlink()


def write_retry_manifest(path: Path, manifest: object) -> None:
    """Atomically publish retry entries without exposing a partial JSON report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError("Failed-manifest path must not be a symlink")

    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            json.dump(manifest, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        if path.is_symlink():
            raise ValueError("Failed-manifest path became a symlink")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def entries(manifest: object) -> Iterator[tuple[str, Path, str | None, int | None]]:
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be an object mapping folders to file lists")
    seen: set[str] = set()
    for folder, files in manifest.items():
        folder_path = relative_destination(folder, allow_subdirs=True)
        if not isinstance(files, list):
            raise ValueError(f"Folder {folder!r} must contain a list")
        for item in files:
            if not isinstance(item, dict) or not {"id", "name"} <= set(item) or set(item) - {"id", "name", "sha256", "size"}:
                raise ValueError("Each file requires 'id', 'name'; optionally 'sha256'")
            file_id = item["id"]
            if not isinstance(file_id, str) or not DRIVE_ID.fullmatch(file_id):
                raise ValueError(f"Invalid Drive file ID in {folder!r}")
            checksum = item.get("sha256")
            if checksum is not None and (not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", checksum)):
                raise ValueError(f"Invalid SHA-256 in {folder!r}")
            size = item.get("size")
            if size is not None and (type(size) is not int or size < 1):
                raise ValueError(f"Invalid expected file size in {folder!r}")
            filename = relative_destination(item["name"], allow_subdirs=False)
            target = folder_path / filename
            # Case-insensitive or Unicode-normalizing filesystems can alias
            # differently encoded names. A file cannot also be a directory.
            identity = unicodedata.normalize("NFC", target.as_posix()).casefold()
            if identity in seen:
                raise ValueError(f"Duplicate destination: {target}")
            if any(
                identity.startswith(existing + "/")
                or existing.startswith(identity + "/")
                for existing in seen
            ):
                raise ValueError(f"File/directory destination collision: {target}")
            seen.add(identity)
            yield file_id, target, checksum.lower() if checksum else None, size


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON file listing authorized downloads")
    parser.add_argument("--output", type=Path, default=Path("downloads"))
    parser.add_argument("--cookies", type=Path, help="Optional Netscape cookies.txt file")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true",
                      help="Preview destinations without downloading or verifying")
    mode.add_argument("--verify-only", action="store_true",
                      help="Audit local files without network access or downloading")
    parser.add_argument("--require-sha256", action="store_true",
                        help="Reject selected files without an expected SHA-256 digest")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--max-total-attempts", type=int, metavar="COUNT",
                        help="Cap total yt-dlp subprocess attempts across the batch")
    parser.add_argument("--max-download-seconds", type=float, metavar="SECONDS",
                        help="Cap cumulative yt-dlp subprocess time across the batch")
    parser.add_argument("--max-batch-wall-seconds", type=float, metavar="SECONDS",
                        help="Cap total elapsed batch time, including retries and local work")
    parser.add_argument("--max-failures", type=int,
                        help="Stop the batch after N failed files (default: no limit)")
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--timeout", type=float,
                        help="Maximum seconds per yt-dlp attempt (default: unlimited)")
    parser.add_argument("--min-free-space", type=int, default=0, metavar="BYTES",
                        help="Reserve this many free bytes in the download filesystem")
    parser.add_argument("--rate-limit", type=int, metavar="BYTES_PER_SECOND",
                        help="Limit yt-dlp transfer rate per download (default: unlimited)")
    parser.add_argument("--max-file-size", type=int, metavar="BYTES",
                        help="Refuse files larger than this byte limit")
    parser.add_argument("--max-batch-size", type=int, metavar="BYTES",
                        help="Reject selected batches whose declared file sizes exceed this total")
    parser.add_argument("--quarantine-invalid", action="store_true",
                        help="Move invalid existing files aside before redownloading")
    parser.add_argument("--restore-quarantine-on-failure", action="store_true",
                        help="Restore quarantined originals after failed replacement when paths are free")
    parser.add_argument("--failed-manifest", type=Path)
    parser.add_argument("--retain-failures", action="store_true",
                        help="Carry forward unresolved entries from an existing failed manifest")
    parser.add_argument("--only-failed", action="store_true",
                        help="Process only unresolved entries recorded in --failed-manifest")
    parser.add_argument("--status-out", type=Path,
                        help="Write a JSON report of individual file outcomes")
    parser.add_argument("--plan-out", type=Path,
                        help="Write selected files and declared metadata to JSON (also in dry-run)")
    parser.add_argument("--plan-inspect-local", action="store_true",
                        help="Inspect local destinations and partial files in --plan-out")
    parser.add_argument("--fail-on-missing-checksum-plan", action="store_true",
                        help="In dry-run, reject selected files without SHA-256 metadata")
    parser.add_argument("--fail-on-unverified-local-plan", action="store_true",
                        help="In dry-run, reject local skip/verify actions without SHA-256 validation")
    parser.add_argument("--fail-on-blocked-plan", action="store_true",
                        help="In dry-run, exit nonzero if the inspected plan contains blocked files")
    parser.add_argument("--fail-on-quarantine-plan", action="store_true",
                        help="In dry-run, reject plans requiring quarantine of existing files")
    parser.add_argument("--max-quarantine-bytes", type=int, metavar="BYTES",
                        help="In dry-run, cap total existing data that would be quarantined")
    parser.add_argument("--max-planned-transfers", type=int, metavar="COUNT",
                        help="In dry-run, cap the number of files needing download or resume")
    parser.add_argument("--fail-on-disk-space-plan", action="store_true",
                        help="In dry-run, reject a plan that cannot fit with --min-free-space reserve")
    parser.add_argument("--fail-on-unknown-size-plan", action="store_true",
                        help="In dry-run, exit nonzero if actionable files have unknown transfer sizes")
    parser.add_argument("--max-estimated-transfer", type=int, metavar="BYTES",
                        help="In dry-run, reject inspected plans exceeding this remaining-byte budget")
    parser.add_argument("--cursor-out", type=Path,
                        help="Write a JSON checkpoint containing the last processed path")
    parser.add_argument("--folder", action="append", default=[],
                        help="Only process this folder and its descendants (repeatable)")
    parser.add_argument("--file", action="append", default=[],
                        help="Only process this exact manifest destination (repeatable)")
    parser.add_argument("--exclude-folder", action="append", default=[],
                        help="Skip this folder and its descendants (repeatable)")
    parser.add_argument("--exclude-file", action="append", default=[],
                        help="Skip this exact relative file destination (repeatable)")
    parser.add_argument("--limit", type=int,
                        help="Process at most N selected files")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--offset", type=int, default=0,
                           help="Skip first N matching entries before --limit")
    selection.add_argument("--after", type=str,
                           help="Resume after this exact relative destination path")
    selection.add_argument("--cursor-in", type=Path,
                           help="Resume using a checkpoint from --cursor-out")
    args = parser.parse_args(argv)
    if args.retain_failures and not args.failed_manifest:
        parser.error("--retain-failures requires --failed-manifest")
    if args.restore_quarantine_on_failure and not args.quarantine_invalid:
        parser.error("--restore-quarantine-on-failure requires --quarantine-invalid")
    if args.plan_inspect_local and not args.plan_out:
        parser.error("--plan-inspect-local requires --plan-out")
    if args.fail_on_missing_checksum_plan and not (args.plan_out and args.dry_run):
        parser.error("--fail-on-missing-checksum-plan requires --plan-out and --dry-run")
    if args.fail_on_unverified_local_plan and not (args.plan_inspect_local and args.dry_run):
        parser.error("--fail-on-unverified-local-plan requires --plan-inspect-local and --dry-run")
    if args.fail_on_blocked_plan and not (args.plan_inspect_local and args.dry_run):
        parser.error("--fail-on-blocked-plan requires --plan-inspect-local and --dry-run")
    if args.fail_on_unknown_size_plan and not (args.plan_inspect_local and args.dry_run):
        parser.error("--fail-on-unknown-size-plan requires --plan-inspect-local and --dry-run")
    if args.fail_on_quarantine_plan and not (args.plan_inspect_local and args.dry_run):
        parser.error("--fail-on-quarantine-plan requires --plan-inspect-local and --dry-run")
    if args.max_quarantine_bytes is not None:
        if args.max_quarantine_bytes < 0:
            parser.error("--max-quarantine-bytes must be zero or greater")
        if not (args.plan_inspect_local and args.dry_run):
            parser.error("--max-quarantine-bytes requires --plan-inspect-local and --dry-run")
    if args.max_planned_transfers is not None:
        if args.max_planned_transfers < 0:
            parser.error("--max-planned-transfers must be zero or greater")
        if not (args.plan_inspect_local and args.dry_run):
            parser.error("--max-planned-transfers requires --plan-inspect-local and --dry-run")
    if args.fail_on_disk_space_plan and not (args.plan_inspect_local and args.dry_run):
        parser.error("--fail-on-disk-space-plan requires --plan-inspect-local and --dry-run")
    if args.max_estimated_transfer is not None:
        if args.max_estimated_transfer < 0:
            parser.error("--max-estimated-transfer must be zero or greater")
        if not (args.plan_inspect_local and args.dry_run):
            parser.error("--max-estimated-transfer requires --plan-inspect-local and --dry-run")
    if args.only_failed and not args.retain_failures:
        parser.error("--only-failed requires --retain-failures")
    if args.only_failed and (args.after is not None or args.cursor_in or args.offset or args.cursor_out):
        parser.error("--only-failed cannot be combined with cursor or offset options")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")
    if args.max_failures is not None and args.max_failures < 1:
        parser.error("--max-failures must be a positive integer")
    if args.offset < 0:
        parser.error("--offset must be zero or greater")
    if args.after is not None:
        try:
            resume_after = relative_destination(args.after, allow_subdirs=True)
        except ValueError as exc:
            parser.error(f"Invalid --after: {exc}")
    else:
        resume_after = None
    try:
        selected_folders = [
            relative_destination(folder, allow_subdirs=True)
            for folder in args.folder
        ]
        selected_files = [
            relative_destination(filename, allow_subdirs=True)
            for filename in args.file
        ]
        excluded_folders = [
            relative_destination(folder, allow_subdirs=True)
            for folder in args.exclude_folder
        ]
        excluded_files = [
            relative_destination(filename, allow_subdirs=True)
            for filename in args.exclude_file
        ]
    except ValueError as exc:
        parser.error(f"Invalid file or folder selection: {exc}")
    if args.cursor_in:
        try:
            checkpoint = json.loads(args.cursor_in.expanduser().read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            parser.error(f"Cannot read checkpoint: {exc}")
        if not isinstance(checkpoint, dict) or checkpoint.get("schema_version") != 1:
            parser.error("Unsupported checkpoint format")
        try:
            current_manifest_hash = sha256_file(args.manifest.expanduser())
        except OSError as exc:
            parser.error(f"Cannot read input manifest for checkpoint verification: {exc}")
        if checkpoint.get("manifest_sha256") != current_manifest_hash:
            parser.error("Checkpoint does not match the current manifest")
        expected_folders = sorted(folder.as_posix() for folder in selected_folders)
        # Checkpoints produced before folder metadata was introduced imply
        # that no folder filter was used.
        if checkpoint.get("folders", []) != expected_folders:
            parser.error("Checkpoint folder selection does not match --folder arguments")
        expected_selected_files = sorted(path.as_posix() for path in selected_files)
        if checkpoint.get("selected_files", []) != expected_selected_files:
            parser.error("Checkpoint file selection does not match --file arguments")
        expected_exclusions = sorted(folder.as_posix() for folder in excluded_folders)
        if checkpoint.get("excluded_folders", []) != expected_exclusions:
            parser.error("Checkpoint exclusion selection does not match --exclude-folder arguments")
        expected_files = sorted(path.as_posix() for path in excluded_files)
        if checkpoint.get("excluded_files", []) != expected_files:
            parser.error("Checkpoint file exclusions do not match --exclude-file arguments")
        if checkpoint.get("failed", 0):
            print("Warning: checkpoint has failed entries; retry them separately.", file=sys.stderr)
        if checkpoint.get("after") is None:
            # A genuinely empty filtered manifest has no last file.
            if checkpoint.get("matching_entries") != 0 or checkpoint.get("has_more") is not False:
                parser.error("Null checkpoint cursor is valid only for an empty selection")
            resume_after = None
        else:
            try:
                resume_after = relative_destination(checkpoint["after"], allow_subdirs=True)
            except (TypeError, ValueError) as exc:
                parser.error(f"Invalid checkpoint cursor: {exc}")
    if args.attempts < 1 or not math.isfinite(args.retry_delay) or not 0 <= args.retry_delay <= 3600:
        parser.error("Require --attempts >= 1 and 0 <= --retry-delay <= 3600")
    if args.max_total_attempts is not None and args.max_total_attempts < 1:
        parser.error("--max-total-attempts must be a positive integer")
    if args.max_download_seconds is not None and (
        not math.isfinite(args.max_download_seconds) or args.max_download_seconds <= 0
    ):
        parser.error("--max-download-seconds must be finite and greater than zero")
    if args.max_batch_wall_seconds is not None and (
        not math.isfinite(args.max_batch_wall_seconds) or args.max_batch_wall_seconds <= 0
    ):
        parser.error("--max-batch-wall-seconds must be finite and greater than zero")
    if args.timeout is not None and (not math.isfinite(args.timeout) or args.timeout <= 0):
        parser.error("--timeout must be a finite number greater than zero")
    if args.min_free_space < 0:
        parser.error("--min-free-space must be zero or greater")
    if args.rate_limit is not None and args.rate_limit < 1:
        parser.error("--rate-limit must be a positive integer of bytes per second")
    if args.max_file_size is not None and args.max_file_size < 1:
        parser.error("--max-file-size must be a positive integer of bytes")
    if args.max_batch_size is not None and args.max_batch_size < 1:
        parser.error("--max-batch-size must be a positive integer of bytes")

    failed_entries = {}
    if args.retain_failures and args.failed_manifest:
        retry_path = args.failed_manifest.expanduser()
        if args.only_failed and not retry_path.is_file():
            parser.error("--only-failed requires an existing --failed-manifest")
        if retry_path.exists():
            try:
                previous = json.loads(retry_path.read_text(encoding="utf-8"))
                list(entries(previous))
                failed_entries = {
                    folder: [dict(item) for item in items]
                    for folder, items in previous.items()
                }
            except (OSError, ValueError) as exc:
                parser.error(f"Invalid retained failure manifest: {exc}")
    failed_records = {
        target: (file_id, checksum, size)
        for file_id, target, checksum, size in entries(failed_entries)
    }
    failed_targets = set(failed_records)

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        downloads = list(entries(manifest))  # Validate everything before writing.
        # Protect every declared destination, including unselected batches.
        all_destinations = [entry[1] for entry in downloads]
        if args.only_failed:
            original_records = {
                target: (file_id, checksum, size)
                for file_id, target, checksum, size in downloads
            }
            missing = failed_targets - set(original_records)
            if missing:
                parser.error(
                    "Retained failures absent from input manifest: "
                    + ", ".join(sorted(path.as_posix() for path in missing))
                )
            changed = [
                target for target, recorded in failed_records.items()
                if original_records[target] != recorded
            ]
            if changed:
                parser.error(
                    "Retained failure metadata differs from input manifest: "
                    + ", ".join(sorted(path.as_posix() for path in changed))
                )
        unknown_selections = set(selected_files) - set(all_destinations)
        if unknown_selections:
            parser.error(
                "--file destination not found: "
                + ", ".join(sorted(path.as_posix() for path in unknown_selections))
            )
        unknown_exclusions = set(excluded_files) - set(all_destinations)
        if unknown_exclusions:
            parser.error(
                "--exclude-file destination not found: "
                + ", ".join(sorted(path.as_posix() for path in unknown_exclusions))
            )
        if selected_folders:
            downloads = [
                entry for entry in downloads
                if any(
                    entry[1].parent == folder or folder in entry[1].parents
                    for folder in selected_folders
                )
            ]
        if selected_files:
            selected_targets = set(selected_files)
            downloads = [
                entry for entry in downloads if entry[1] in selected_targets
            ]
        if excluded_folders:
            downloads = [
                entry for entry in downloads
                if not any(
                    entry[1].parent == folder or folder in entry[1].parents
                    for folder in excluded_folders
                )
            ]
        if excluded_files:
            excluded_targets = set(excluded_files)
            downloads = [
                entry for entry in downloads if entry[1] not in excluded_targets
            ]
        if args.only_failed:
            downloads = [entry for entry in downloads if entry[1] in failed_targets]
        # Preserve stable manifest order across successive batch invocations.
        # Inclusion and exclusion precede slicing, so cursors and offsets
        # refer only to entries that satisfy both selection rules.
        total_matching = len(downloads)
        last_matching_path = downloads[-1][1] if downloads else None
        if args.cursor_in and checkpoint.get("after") is None and total_matching != 0:
            parser.error("Checkpoint empty selection no longer matches the manifest")
        start = args.offset
        if resume_after is not None:
            matches = [
                i for i, entry in enumerate(downloads)
                if entry[1] == resume_after
            ]
            if not matches:
                parser.error(
                    f"--after path not found among matching entries: {args.after}"
                )
            start = matches[0] + 1
        if args.limit is not None:
            downloads = downloads[start:start + args.limit]
        else:
            downloads = downloads[start:]
        if args.max_batch_size is not None:
            unsized = [relative.as_posix() for _, relative, _, size in downloads if size is None]
            if unsized:
                parser.error(
                    "--max-batch-size requires declared size for each selected file: "
                    + ", ".join(unsized)
                )
            declared_total = sum(size for _, _, _, size in downloads)
            if declared_total > args.max_batch_size:
                parser.error(
                    f"Selected batch declares {declared_total} bytes, "
                    f"exceeding --max-batch-size {args.max_batch_size}"
                )
        if args.require_sha256:
            missing_checksums = [
                relative.as_posix() for _, relative, checksum, _ in downloads
                if checksum is None
            ]
            if missing_checksums:
                parser.error(
                    "--require-sha256: missing checksum for "
                    + ", ".join(missing_checksums)
                )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(f"Invalid manifest: {exc}")

    # Compare resolved paths before downloading: the retry output must never
    # replace the user's original manifest (including through symlink aliases).
    if not args.dry_run or args.plan_out:
        reports = [
            path.expanduser()
            for path in (
                args.plan_out,
                *(() if args.dry_run else (args.failed_manifest, args.cursor_out, args.status_out)),
            )
            if path is not None
        ]
        resolved_reports = [path.resolve() for path in reports]
        if any(path.is_symlink() for path in reports):
            parser.error("Report destination must not be a symlink")
        if len(set(resolved_reports)) != len(resolved_reports):
            parser.error("Report destinations must all be distinct")
        if args.manifest.expanduser().resolve() in resolved_reports:
            parser.error("Report destination must differ from input manifest")
        if args.cookies and args.cookies.expanduser().resolve() in resolved_reports:
            parser.error("Report destination must differ from cookies file")
        if args.cursor_in and args.cursor_out is None and (
            args.cursor_in.expanduser().resolve() in resolved_reports
        ):
            parser.error("Reports cannot overwrite the input checkpoint")
        if args.cursor_in and args.cursor_in.expanduser().resolve() in [
            path.expanduser().resolve()
            for path in (args.failed_manifest, args.status_out, args.plan_out)
            if path is not None and (path == args.plan_out or not args.dry_run)
        ]:
            parser.error("Retry, status, and plan reports cannot overwrite the input checkpoint")

    output_path = args.output.expanduser()
    if output_path.is_symlink():
        parser.error("--output must not be a symlink")
    root = output_path.resolve()
    # Refuse any collision between a generated file and sensitive inputs or
    # reports before initializing the retry manifest or invoking yt-dlp.
    declared_paths = {(root / relative).resolve() for relative in all_destinations}
    inputs = [
        path.expanduser().resolve()
        for path in (args.manifest, args.cookies, args.cursor_in)
        if path is not None
    ]
    if any(path in declared_paths for path in inputs):
        parser.error("A manifest destination overlaps an input or credentials file")
    if (not args.dry_run or args.plan_out) and any(
        path in declared_paths for path in resolved_reports
    ):
        parser.error("A report destination overlaps a manifest download destination")
    if args.plan_out:
        def inspect_local(relative: Path, checksum: str | None, size: int | None) -> dict:
            destination = root / relative
            if not destination_is_safe(destination, root):
                return {
                    "local_state": "unsafe", "planned_action": "blocked",
                    "estimated_remaining_bytes": None,
                }
            try:
                # Runtime checks manifest-declared size before either download
                # or verification; keep both planning modes consistent.
                if (
                    args.max_file_size is not None
                    and size is not None
                    and size > args.max_file_size
                ):
                    return {
                        "local_state": "oversized",
                        "planned_action": "blocked",
                        "blocked_reason": "file_size_limit",
                        "estimated_remaining_bytes": None,
                    }
                # Verification never downloads, resumes, or quarantines files.
                # Keep the plan's actions aligned with --verify-only rather
                # than suggesting network work that the command will not do.
                if args.verify_only:
                    if not destination.is_file():
                        return {
                            "local_state": "missing" if not destination.exists() else "unsafe",
                            "planned_action": "blocked",
                            "estimated_remaining_bytes": 0,
                        }
                    local_bytes = destination.stat().st_size
                    reason = (
                        "empty_file" if local_bytes == 0
                        else "file_size_limit"
                        if args.max_file_size is not None and local_bytes > args.max_file_size
                        else "size_mismatch"
                        if size is not None and local_bytes != size
                        else "checksum_mismatch"
                        if checksum is not None and sha256_file(destination) != checksum
                        else None
                    )
                    return {
                        "local_state": "invalid" if reason else "matching",
                        "planned_action": "blocked" if reason else "verify",
                        "local_bytes": local_bytes,
                        "estimated_remaining_bytes": 0,
                        "integrity_verified": checksum is not None and reason is None,
                        **({"integrity_issue": reason} if reason else {}),
                    }
                if destination.is_file():
                    local_bytes = destination.stat().st_size
                    if args.max_file_size is not None and local_bytes > args.max_file_size:
                        return {
                            "local_state": "oversized", "planned_action": "blocked",
                            "local_bytes": local_bytes, "estimated_remaining_bytes": None,
                        }
                    issue = (
                        "empty_file" if local_bytes == 0
                        else "size_mismatch"
                        if size is not None and local_bytes != size
                        else "checksum_mismatch"
                        if checksum is not None and sha256_file(destination) != checksum
                        else None
                    )
                    if issue is None:
                        return {
                            "local_state": "matching", "planned_action": "skip",
                            "local_bytes": local_bytes, "estimated_remaining_bytes": 0,
                            "integrity_verified": checksum is not None,
                        }
                    # A zero-byte destination can be downloaded in-place;
                    # nonempty mismatches require explicit quarantine.
                    if local_bytes > 0 and not args.quarantine_invalid:
                        return {
                            "local_state": "invalid", "planned_action": "blocked",
                            "local_bytes": local_bytes, "estimated_remaining_bytes": None,
                            "integrity_issue": issue,
                        }
                    if local_bytes > 0:
                        action = "quarantine_and_download"
                        state = "invalid"
                    else:
                        action = "download"
                        state = "empty"
                elif destination.exists():
                    return {
                        "local_state": "unsafe", "planned_action": "blocked",
                        "estimated_remaining_bytes": None,
                    }
                else:
                    action = "download"
                    state = "missing"
                part_path = destination.with_name(destination.name + ".part")
                if part_path.is_symlink() or (part_path.exists() and not part_path.is_file()):
                    return {
                        "local_state": "unsafe_partial", "planned_action": "blocked",
                        "estimated_remaining_bytes": None,
                    }
                part_bytes = part_path.stat().st_size if part_path.is_file() else 0
                if action != "quarantine_and_download" and (
                    (size is not None and part_bytes > size)
                    or (args.max_file_size is not None and part_bytes > args.max_file_size)
                ):
                    return {
                        "local_state": "oversized_partial",
                        "planned_action": "blocked",
                        "partial_bytes": part_bytes,
                        "estimated_remaining_bytes": None,
                        "integrity_issue": (
                            "partial_size_mismatch"
                            if size is not None and part_bytes > size
                            else "partial_file_size_limit"
                        ),
                    }
                # When quarantining, even a partial file must be moved aside
                # and the replacement starts from scratch.
                if action == "quarantine_and_download":
                    estimate = size
                else:
                    estimate = max(size - part_bytes, 0) if size is not None else None
                    if part_path.is_file():
                        action = "resume"
                        state = "partial"
                result = {
                    "local_state": state, "planned_action": action,
                    "estimated_remaining_bytes": estimate,
                }
                if part_path.is_file():
                    result["partial_bytes"] = part_bytes
                if destination.is_file():
                    result["local_bytes"] = destination.stat().st_size
                    result["integrity_issue"] = issue
                return result
            except OSError as exc:
                return {
                    "local_state": "unreadable", "planned_action": "blocked",
                    "error": str(exc), "estimated_remaining_bytes": None,
                }

        def planned_entry(
            file_id: str, relative: Path, checksum: str | None, size: int | None
        ) -> dict:
            entry = {
                "path": relative.as_posix(), "id": file_id,
                "size": size, "sha256": checksum,
            }
            if not args.plan_inspect_local:
                return entry
            inspection = inspect_local(relative, checksum, size)
            if inspection["planned_action"] == "blocked":
                inspection["blocked_reason"] = {
                    "unsafe": "unsafe_destination",
                    "unsafe_partial": "unsafe_partial",
                    "unreadable": "local_read_error",
                    "oversized": "file_size_limit",
                    "oversized_partial": inspection.get("integrity_issue", "partial_size_mismatch"),
                    "missing": "missing_for_verification",
                    "invalid": inspection.get("integrity_issue", "existing_file_mismatch"),
                }.get(inspection["local_state"], "unavailable")
            if inspection["planned_action"] == "quarantine_and_download":
                inspection["quarantine_bytes"] = (
                    inspection.get("local_bytes", 0)
                    + inspection.get("partial_bytes", 0)
                )
            entry.update(inspection)
            return entry

        planned_files = [
            planned_entry(file_id, relative, checksum, size)
            for file_id, relative, checksum, size in downloads
        ]
        plan = {
            "schema_version": 1,
            "manifest_sha256": sha256_file(args.manifest),
            "matching_entries": total_matching,
            "start_index": start,
            "selected": len(downloads),
            "declared_bytes": sum(size or 0 for _, _, _, size in downloads),
            "unknown_size_count": sum(size is None for _, _, _, size in downloads),
            "missing_checksum_count": sum(checksum is None for _, _, checksum, _ in downloads),
            "files": planned_files,
            "mode": "verify-only" if args.verify_only else (
                "dry-run" if args.dry_run else "download"
            ),
        }
        if args.plan_inspect_local:
            estimates = [
                item["estimated_remaining_bytes"] for item in planned_files
                if item["planned_action"] != "blocked"
            ]
            actions = {
                action: sum(item["planned_action"] == action for item in planned_files)
                for action in ("verify", "skip", "download", "resume", "quarantine_and_download", "blocked")
            }
            plan["local_inspection"] = {
                "actions": actions,
                "planned_transfers": sum(
                    actions[action]
                    for action in ("download", "resume", "quarantine_and_download")
                ),
                "matching": sum(item["local_state"] == "matching" for item in planned_files),
                "unverified_local_count": sum(
                    item["planned_action"] in ("skip", "verify")
                    and not item.get("integrity_verified", False)
                    for item in planned_files
                ),
                "partial": sum(item["local_state"] == "partial" for item in planned_files),
                "quarantine_bytes": sum(
                    item.get("quarantine_bytes", 0) for item in planned_files
                ),
                "blocked_or_invalid": sum(
                    item["planned_action"] == "blocked" for item in planned_files
                ),
                "blocked_reasons": {
                    reason: sum(
                        item.get("blocked_reason") == reason for item in planned_files
                    )
                    for reason in sorted({
                        item["blocked_reason"] for item in planned_files
                        if "blocked_reason" in item
                    })
                },
                "estimated_remaining_bytes_known": sum(
                    value for value in estimates if value is not None
                ),
                "unknown_estimate_count": sum(value is None for value in estimates),
            }
        # Persist preflight decisions in the plan itself, including rejected
        # batches. Callers can inspect stable reason codes instead of
        # depending on stderr wording or exit status alone.
        checks = []
        if args.fail_on_missing_checksum_plan:
            missing_checksums = plan["missing_checksum_count"]
            checks.append({
                "code": "missing_sha256",
                "passed": missing_checksums == 0,
                "observed": missing_checksums,
                "limit": 0,
            })
        if args.plan_inspect_local:
            inspection = plan["local_inspection"]
            blocked = inspection["blocked_or_invalid"]
            unknown = inspection["unknown_estimate_count"]
            estimate = inspection["estimated_remaining_bytes_known"]
            if args.fail_on_unverified_local_plan:
                unverified = inspection["unverified_local_count"]
                checks.append({
                    "code": "unverified_local_files",
                    "passed": unverified == 0,
                    "observed": unverified,
                    "limit": 0,
                })
            if args.fail_on_blocked_plan:
                checks.append({
                    "code": "blocked_files",
                    "passed": blocked == 0,
                    "observed": blocked,
                    "limit": 0,
                })
            if args.fail_on_quarantine_plan:
                quarantine_count = inspection["actions"]["quarantine_and_download"]
                checks.append({
                    "code": "quarantine_required",
                    "passed": quarantine_count == 0,
                    "observed": quarantine_count,
                    "limit": 0,
                })
            if args.max_quarantine_bytes is not None:
                quarantine_bytes = inspection["quarantine_bytes"]
                checks.append({
                    "code": "quarantine_bytes_budget",
                    "passed": quarantine_bytes <= args.max_quarantine_bytes,
                    "observed": quarantine_bytes,
                    "limit": args.max_quarantine_bytes,
                })
            if args.max_planned_transfers is not None:
                planned_transfers = inspection["planned_transfers"]
                checks.append({
                    "code": "planned_transfer_count",
                    "passed": planned_transfers <= args.max_planned_transfers,
                    "observed": planned_transfers,
                    "limit": args.max_planned_transfers,
                })
            if args.fail_on_unknown_size_plan:
                checks.append({
                    "code": "unknown_transfer_size",
                    "passed": unknown == 0,
                    "observed": unknown,
                    "limit": 0,
                })
            if args.fail_on_disk_space_plan:
                # The destination directory may not exist during dry-run.
                # Query its closest existing ancestor on the same filesystem.
                usage_path = root
                while not usage_path.exists() and usage_path != usage_path.parent:
                    usage_path = usage_path.parent
                try:
                    free_bytes = shutil.disk_usage(usage_path).free
                except OSError as exc:
                    plan["disk_space"] = {
                        "error": str(exc),
                        "free_bytes": None,
                        "required_bytes": None,
                    }
                    checks.append({
                        "code": "disk_space_available",
                        "passed": False,
                        "observed": None,
                        "limit": None,
                    })
                else:
                    required_bytes = estimate + args.min_free_space
                    plan["disk_space"] = {
                        "free_bytes": free_bytes,
                        "estimated_remaining_bytes": estimate,
                        "reserved_bytes": args.min_free_space,
                        "required_bytes": required_bytes,
                        "filesystem_path": str(usage_path),
                    }
                    checks.append({
                        "code": "disk_space_available",
                        "passed": free_bytes >= required_bytes,
                        "observed": free_bytes,
                        "limit": required_bytes,
                    })
                checks.append({
                    "code": "disk_space_estimate_known",
                    "passed": unknown == 0,
                    "observed": unknown,
                    "limit": 0,
                })
            if args.max_estimated_transfer is not None:
                checks.append({
                    "code": "transfer_size_known",
                    "passed": unknown == 0,
                    "observed": unknown,
                    "limit": 0,
                })
                checks.append({
                    "code": "estimated_transfer_budget",
                    "passed": estimate <= args.max_estimated_transfer,
                    "observed": estimate,
                    "limit": args.max_estimated_transfer,
                })
        plan["preflight"] = {
            "passed": all(check["passed"] for check in checks),
            "checks": checks,
            "failed_codes": [check["code"] for check in checks if not check["passed"]],
        }
        try:
            write_retry_manifest(args.plan_out.expanduser(), plan)
        except (OSError, ValueError) as exc:
            print(f"Failed to write batch plan: {exc}", file=sys.stderr)
            return 1
        print(f"Batch plan written: {args.plan_out}")
        if not plan["preflight"]["passed"]:
            for check in checks:
                if not check["passed"]:
                    print(
                        f"Preflight blocked: {check['code']} "
                        f"(observed={check['observed']}, limit={check['limit']}).",
                        file=sys.stderr,
                    )
            return 1
    cookies = args.cookies.expanduser().resolve() if args.cookies else None
    if cookies and not args.verify_only and not args.dry_run and not cookies.is_file():
        parser.error(f"Cookies file does not exist: {cookies}")

    failed = 0
    attempts_used = 0
    download_seconds_used = 0.0
    attempt_budget_stopped = False
    download_time_budget_stopped = False
    wall_time_budget_stopped = False
    stop_reason = None
    outcomes = []
    batch_started = time.monotonic()

    def wall_remaining() -> float | None:
        if args.max_batch_wall_seconds is None:
            return None
        return args.max_batch_wall_seconds - (time.monotonic() - batch_started)
    def unresolved_failure_count() -> int:
        return sum(len(items) for items in failed_entries.values())

    if not downloads:
        print(f"No downloads selected (matched {total_matching}; start index {start}).")
        if not args.dry_run:
            # Do not leave reports from an earlier batch looking current.
            # Keep a usable last-file cursor when the batch is exhausted.
            try:
                if args.failed_manifest and not args.retain_failures:
                    write_retry_manifest(args.failed_manifest.expanduser(), {})
                if args.status_out:
                    write_retry_manifest(args.status_out.expanduser(), {
                        "schema_version": 1,
                        "selected": 0, "processed": 0, "counts": {}, "files": [],
                    })
                if args.cursor_out:
                    write_retry_manifest(args.cursor_out.expanduser(), {
                        "schema_version": 1,
                        "manifest_sha256": sha256_file(args.manifest),
                        "folders": sorted(folder.as_posix() for folder in selected_folders),
                        "selected_files": sorted(path.as_posix() for path in selected_files),
                        "excluded_folders": sorted(folder.as_posix() for folder in excluded_folders),
                        "excluded_files": sorted(path.as_posix() for path in excluded_files),
                        "after": (
                            resume_after or last_matching_path
                        ).as_posix() if (resume_after or last_matching_path) else None,
                        "processed": 0,
                        "failed": 0,
                        "unresolved_failures": unresolved_failure_count(),
                        "matching_entries": total_matching,
                        "has_more": False,
                    })
            except (OSError, ValueError) as exc:
                print(f"Failed to write empty-batch reports: {exc}", file=sys.stderr)
                return 1
        return 1 if args.retain_failures and unresolved_failure_count() else 0
    print(
        f"Selected {len(downloads)} of {total_matching} matching entries "
        f"(start index {start})."
    )

    if args.failed_manifest and not args.dry_run:
        # Retain previously unresolved entries only when explicitly requested.
        try:
            write_retry_manifest(args.failed_manifest.expanduser(), failed_entries)
        except (OSError, ValueError) as exc:
            print(f"Failed to initialize retry manifest: {exc}", file=sys.stderr)
            return 1

    def publish_status() -> None:
        if not args.status_out or args.dry_run:
            return
        counts = {}
        for item in outcomes:
            status = item["status"]
            counts[status] = counts.get(status, 0) + 1
        report = {
            "schema_version": 1,
            "selected": len(downloads),
            "processed": len(outcomes),
            "counts": counts,
            "quarantined": sum("quarantined_backup" in item for item in outcomes),
            "recovered": sum(
                item.get("status") == "downloaded" and "quarantined_backup" in item
                for item in outcomes
            ),
            "successful_output_bytes": sum(
                item.get("output_bytes", 0) for item in outcomes
            ),
            "sha256_verified_files": sum(
                item.get("integrity_verified") is True for item in outcomes
            ),
            "download_attempts": sum(item.get("download_attempts", 0) for item in outcomes),
            "max_total_attempts": args.max_total_attempts,
            "attempt_budget_exhausted": attempt_budget_stopped,
            "max_download_seconds": args.max_download_seconds,
            "download_time_budget_exhausted": download_time_budget_stopped,
            "max_batch_wall_seconds": args.max_batch_wall_seconds,
            "batch_wall_seconds_elapsed": round(time.monotonic() - batch_started, 3),
            "wall_time_budget_exhausted": wall_time_budget_stopped,
            "stop_reason": stop_reason,
            "unprocessed": len(downloads) - len(outcomes),
            "attempt_outcomes": {
                status: sum(
                    attempt["outcome"] == status
                    for item in outcomes for attempt in item.get("attempt_history", [])
                )
                for status in (
                    "completed", "verification_failed", "nonzero_exit",
                    "timeout", "launch_failed"
                )
            },
            "download_elapsed_seconds": round(
                sum(item.get("download_elapsed_seconds", 0) for item in outcomes), 3
            ),
            "files": outcomes,
        }
        write_retry_manifest(args.status_out.expanduser(), report)

    checkpoint_hash = None
    if args.cursor_out and not args.dry_run:
        try:
            checkpoint_hash = sha256_file(args.manifest)
        except OSError as exc:
            parser.error(f"Cannot read manifest for checkpoint: {exc}")

    def publish_checkpoint() -> None:
        if not args.cursor_out or args.dry_run or not outcomes:
            return
        # A pending item was interrupted; do not skip it on resumption.
        if outcomes[-1]["status"] == "pending":
            return
        checkpoint = {
            "schema_version": 1,
            "manifest_sha256": checkpoint_hash,
            "folders": sorted(folder.as_posix() for folder in selected_folders),
            "selected_files": sorted(path.as_posix() for path in selected_files),
            "excluded_folders": sorted(folder.as_posix() for folder in excluded_folders),
            "excluded_files": sorted(path.as_posix() for path in excluded_files),
            "after": outcomes[-1]["path"],
            "processed": len(outcomes),
            "failed": failed,
            "unresolved_failures": unresolved_failure_count(),
            "download_attempts": attempts_used,
            "max_total_attempts": args.max_total_attempts,
            "attempt_budget_exhausted": attempt_budget_stopped,
            "max_download_seconds": args.max_download_seconds,
            "download_seconds_used": round(download_seconds_used, 3),
            "download_time_budget_exhausted": download_time_budget_stopped,
            "max_batch_wall_seconds": args.max_batch_wall_seconds,
            "batch_wall_seconds_elapsed": round(time.monotonic() - batch_started, 3),
            "wall_time_budget_exhausted": wall_time_budget_stopped,
            "stop_reason": stop_reason,
            "matching_entries": total_matching,
            "has_more": start + len(outcomes) < total_matching,
        }
        write_retry_manifest(args.cursor_out.expanduser(), checkpoint)

    def restore_backup_without_overwrite(backup: Path, target: Path) -> str | None:
        """Install the backup at target without clobbering; report cleanup errors.

        An exclusive hard link fails when another process creates the target
        concurrently. Once the link succeeds, the restored target exists even
        if removing the old backup name fails.
        """
        if backup.is_symlink() or not backup.is_file():
            raise OSError(f"Quarantine backup is not a regular file: {backup}")
        os.link(backup, target, follow_symlinks=False)
        try:
            backup.unlink()
        except OSError as exc:
            return str(exc)
        return None

    def restore_quarantine_after_failure(outcome: dict, destination: Path) -> None:
        """Restore preserved originals after any per-file failure, if safe."""
        if not args.restore_quarantine_on_failure or "quarantined_backup" not in outcome:
            return
        original_backup = root / outcome["quarantined_backup"]
        partial_backup = (
            root / outcome["quarantined_partial_backup"]
            if "quarantined_partial_backup" in outcome else None
        )
        part_path = destination.with_name(destination.name + ".part")
        # Preserve both sets of evidence if the failed attempt wrote
        # anything. Never overwrite a new output, even a zero-byte file.
        if (
            destination.exists() or destination.is_symlink()
            or part_path.exists() or part_path.is_symlink()
        ):
            outcome["quarantine_restore"] = "deferred_outputs_present"
            return
        try:
            original_cleanup_error = restore_backup_without_overwrite(
                original_backup, destination
            )
        except OSError as exc:
            outcome["quarantine_restore"] = "original_restore_failed"
            outcome["quarantine_restore_error"] = str(exc)
            return
        outcome["quarantine_restore"] = "original_restored"
        cleanup_errors = {}
        if original_cleanup_error is None:
            outcome.pop("quarantined_backup", None)
        else:
            cleanup_errors["original"] = original_cleanup_error
        if partial_backup is not None:
            try:
                partial_cleanup_error = restore_backup_without_overwrite(
                    partial_backup, part_path
                )
            except OSError as exc:
                outcome["quarantine_restore"] = "partial_restore_failed"
                outcome["quarantine_restore_error"] = str(exc)
                if cleanup_errors:
                    outcome["quarantine_cleanup_errors"] = cleanup_errors
                return
            if partial_cleanup_error is None:
                outcome.pop("quarantined_partial_backup", None)
            else:
                cleanup_errors["partial"] = partial_cleanup_error
        if cleanup_errors:
            outcome["quarantine_restore"] = "restored_backup_retained"
            outcome["quarantine_cleanup_errors"] = cleanup_errors
        else:
            outcome["quarantine_restore"] = "restored"

    try:
        for index, (file_id, relative, checksum, size) in enumerate(downloads, start=1):
            # Check before selecting the next file: all previous outcomes have
            # already been atomically journaled by the per-file finally block.
            if args.max_failures is not None and failed >= args.max_failures:
                stop_reason = "max_failures"
                print(f"Stopping batch after {failed} failed files.", file=sys.stderr)
                break
            if args.max_total_attempts is not None and attempts_used >= args.max_total_attempts:
                attempt_budget_stopped = True
                stop_reason = "max_total_attempts"
                print(
                    f"Stopping batch after {attempts_used} downloader attempts.",
                    file=sys.stderr,
                )
                break
            if (
                args.max_download_seconds is not None
                and download_seconds_used >= args.max_download_seconds
            ):
                download_time_budget_stopped = True
                stop_reason = "max_download_seconds"
                print("Stopping batch: downloader time budget exhausted.", file=sys.stderr)
                break
            if wall_remaining() is not None and wall_remaining() <= 0:
                wall_time_budget_stopped = True
                stop_reason = "max_batch_wall_seconds"
                print("Stopping batch: wall-clock time budget exhausted.", file=sys.stderr)
                break
            destination = root / relative
            outcome = {"path": relative.as_posix(), "status": "pending"}
            outcomes.append(outcome)
            print(f"[{index}/{len(downloads)}] {relative}", flush=True)
            def fail(reason):
                nonlocal failed
                failed += 1
                outcome["status"] = "failed"
                outcome["reason"] = reason
                item = {"id": file_id, "name": relative.name}
                if checksum:
                    item["sha256"] = checksum
                if size is not None:
                    item["size"] = size
                failed_entries.setdefault(relative.parent.as_posix(), []).append(item)
                print(f"  {reason}", file=sys.stderr)

            try:
                if args.dry_run:
                    outcome["status"] = "planned"
                    continue
                if not destination_is_safe(destination, root):
                    fail("Symlink destination refused.")
                    continue
                if args.max_file_size is not None and size is not None and size > args.max_file_size:
                    fail(
                        f"Expected file size {size} exceeds --max-file-size "
                        f"{args.max_file_size} bytes."
                    )
                    continue
                if args.verify_only:
                    if not destination.is_file():
                        fail("Missing or non-regular local file.")
                    elif destination.stat().st_size == 0:
                        fail("Local file is empty.")
                    elif args.max_file_size is not None and destination.stat().st_size > args.max_file_size:
                        fail(f"Local file exceeds --max-file-size {args.max_file_size} bytes.")
                    elif size is not None and destination.stat().st_size != size:
                        fail(f"Local file size mismatch (expected {size} bytes).")
                    elif checksum and sha256_file(destination) != checksum:
                        fail("Local file SHA-256 mismatch.")
                    elif checksum:
                        outcome["status"] = "verified"
                        print("  SHA-256 verified.")
                    elif size is not None:
                        outcome["status"] = "size-checked"
                        print("  File size verified; no checksum provided (integrity unverified).")
                    else:
                        outcome["status"] = "present"
                        print("  File present; no checksum provided (integrity unverified).")
                    if outcome["status"] != "failed":
                        outcome["output_bytes"] = destination.stat().st_size
                        outcome["integrity_verified"] = bool(checksum)
                    continue
                if destination.is_file() and destination.stat().st_size > 0:
                    if args.max_file_size is not None and destination.stat().st_size > args.max_file_size:
                        fail(f"Existing file exceeds --max-file-size {args.max_file_size} bytes.")
                        continue
                    if (size is None or destination.stat().st_size == size) and (
                        checksum is None or sha256_file(destination) == checksum
                    ):
                        outcome["status"] = "skipped"
                        outcome["output_bytes"] = destination.stat().st_size
                        outcome["integrity_verified"] = bool(checksum)
                        print("  Already exists; skipped.")
                        continue
                    if not args.quarantine_invalid:
                        fail("Existing file size or checksum mismatch; refusing overwrite.")
                        continue
                    # Validate the partial file before moving any original.
                    # Reusing a stale .part could reconstruct the same corrupt
                    # content and defeat the clean replacement attempt.
                    part_path = destination.with_name(destination.name + ".part")
                    if part_path.is_symlink() or (
                        part_path.exists() and not part_path.is_file()
                    ):
                        fail("Unsafe partial download path; refusing quarantine.")
                        continue
                    suffix = f".invalid-{uuid.uuid4().hex}"
                    backup = destination.with_name(destination.name + suffix)
                    part_backup = part_path.with_name(part_path.name + suffix)
                    if any(
                        path.exists() or path.is_symlink()
                        for path in (backup, part_backup)
                    ):
                        fail("Quarantine destination already exists.")
                        continue
                    # Treat the pair as one operation as far as possible:
                    # restore the partial file if moving the original fails.
                    # Never claim the original was quarantined before rename
                    # has succeeded.
                    part_moved = False
                    try:
                        if part_path.is_file():
                            part_path.rename(part_backup)
                            part_moved = True
                        destination.rename(backup)
                    except OSError as exc:
                        rollback_error = None
                        if part_moved:
                            try:
                                part_backup.rename(part_path)
                            except OSError as rollback_exc:
                                rollback_error = rollback_exc
                                outcome["quarantined_partial_backup"] = (
                                    part_backup.relative_to(root).as_posix()
                                )
                        if rollback_error is not None:
                            fail(
                                "Could not quarantine original file "
                                f"({exc}); could not restore partial ({rollback_error})."
                            )
                        else:
                            fail(f"Could not quarantine original file: {exc}")
                        continue
                    if part_moved:
                        outcome["quarantined_partial_backup"] = (
                            part_backup.relative_to(root).as_posix()
                        )
                        print(f"  Partial download quarantined: {part_backup}", flush=True)
                    outcome["quarantined_backup"] = backup.relative_to(root).as_posix()
                    print(f"  Invalid file quarantined: {backup}", flush=True)
                if destination.exists() and not destination.is_file():
                    fail("Destination is not a regular file; skipped.")
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                part_path = destination.with_name(destination.name + ".part")
                if part_path.is_symlink():
                    fail("Symlinked partial download refused.")
                    continue
                if part_path.exists() and not part_path.is_file():
                    fail("Partial download path is not a regular file.")
                    continue
                if part_path.is_file():
                    partial_bytes = part_path.stat().st_size
                    if size is not None and partial_bytes > size:
                        fail(
                            f"Partial download exceeds expected file size "
                            f"({partial_bytes} > {size} bytes); refusing unsafe resume."
                        )
                        continue
                    if args.max_file_size is not None and partial_bytes > args.max_file_size:
                        fail(
                            f"Partial download exceeds --max-file-size "
                            f"({partial_bytes} > {args.max_file_size} bytes); "
                            "refusing unsafe resume."
                        )
                        continue
                command = [
                    sys.executable, "-m", "yt_dlp",
                    "--continue",
                    "--no-playlist",
                    "--format", "best[ext=mp4]/best",
                    "--output", str(destination),
                ]
                if cookies:
                    command.extend(["--cookies", str(cookies)])
                if args.rate_limit is not None:
                    command.extend(["--limit-rate", str(args.rate_limit)])
                if args.max_file_size is not None:
                    command.extend(["--max-filesize", str(args.max_file_size)])
                command.append(f"https://drive.google.com/file/d/{file_id}/view")
                failure = None
                outcome["download_attempts"] = 0
                outcome["download_elapsed_seconds"] = 0.0
                outcome["attempt_history"] = []
                for attempt in range(1, args.attempts + 1):
                    if (
                        args.max_total_attempts is not None
                        and attempts_used >= args.max_total_attempts
                    ):
                        failure = (
                            f"Batch attempt budget exhausted after {attempts_used} "
                            "downloader attempts."
                        )
                        outcome["retry_suppressed_reason"] = "max_total_attempts"
                        outcome["attempt_budget_exhausted"] = True
                        attempt_budget_stopped = True
                        stop_reason = "max_total_attempts"
                        break
                    if (
                        args.max_download_seconds is not None
                        and download_seconds_used >= args.max_download_seconds
                    ):
                        failure = "Batch downloader time budget exhausted."
                        outcome["retry_suppressed_reason"] = "max_download_seconds"
                        download_time_budget_stopped = True
                        stop_reason = "max_download_seconds"
                        break
                    if wall_remaining() is not None and wall_remaining() <= 0:
                        failure = "Batch wall-clock time budget exhausted."
                        outcome["retry_suppressed_reason"] = "max_batch_wall_seconds"
                        wall_time_budget_stopped = True
                        stop_reason = "max_batch_wall_seconds"
                        break
                    # A failed attempt may have left a larger partial file.
                    # Reject that state even if the free-space reserve is off.
                    if part_path.is_symlink() or (
                        part_path.exists() and not part_path.is_file()
                    ):
                        failure = "Unsafe partial download path; refusing resume."
                        break
                    if part_path.is_file():
                        partial_bytes = part_path.stat().st_size
                        if size is not None and partial_bytes > size:
                            failure = (
                                "Partial download exceeds expected file size "
                                f"({partial_bytes} > {size} bytes); refusing unsafe resume."
                            )
                            break
                        if args.max_file_size is not None and partial_bytes > args.max_file_size:
                            failure = (
                                "Partial download exceeds --max-file-size "
                                f"({partial_bytes} > {args.max_file_size} bytes); "
                                "refusing unsafe resume."
                            )
                            break
                    if args.min_free_space:
                        # yt-dlp uses a .part file for resumed downloads. Count
                        # only bytes already stored in that file; recheck space
                        # before every retry, not just the first attempt.
                        if part_path.is_symlink():
                            failure = "Symlinked partial download refused."
                            break
                        if part_path.exists() and not part_path.is_file():
                            failure = "Partial download path is not a regular file."
                            break
                        partial_bytes = part_path.stat().st_size if part_path.is_file() else 0
                        remaining_bytes = max(size - partial_bytes, 0) if size is not None else 0
                        required = args.min_free_space + remaining_bytes
                        free_bytes = shutil.disk_usage(destination.parent).free
                        if free_bytes < required:
                            failure = (
                                "Insufficient free disk space: "
                                f"{free_bytes} bytes available, {required} required "
                                "(reserve plus estimated remaining bytes)."
                            )
                            break
                    result = None
                    remaining_budget = (
                        args.max_download_seconds - download_seconds_used
                        if args.max_download_seconds is not None else None
                    )
                    remaining_wall = wall_remaining()
                    timeout_candidates = [
                        value for value in (args.timeout, remaining_budget, remaining_wall)
                        if value is not None
                    ]
                    effective_timeout = min(timeout_candidates) if timeout_candidates else None
                    attempt_started = time.monotonic()
                    attempt_record = {"attempt": attempt, "outcome": "launch_failed"}
                    if effective_timeout is not None:
                        attempt_record["effective_timeout_seconds"] = effective_timeout
                    outcome["download_attempts"] += 1
                    attempts_used += 1
                    try:
                        result = subprocess.run(
                            command, check=False, timeout=effective_timeout,
                        )
                    except subprocess.TimeoutExpired:
                        attempt_record["outcome"] = "timeout"
                        batch_timeout = (
                            remaining_budget is not None
                            and (args.timeout is None or remaining_budget <= args.timeout)
                        )
                        wall_timeout = (
                            remaining_wall is not None
                            and (args.timeout is None or remaining_wall <= args.timeout)
                            and (remaining_budget is None or remaining_wall <= remaining_budget)
                        )
                        attempt_record["timeout_source"] = (
                            "max_batch_wall_seconds" if wall_timeout
                            else "max_download_seconds" if batch_timeout else "timeout"
                        )
                        failure = f"Download attempt timed out after {effective_timeout:g}s."
                        attempt_record["failure_reason"] = failure
                    except OSError as exc:
                        failure = f"Could not launch downloader: {exc}"
                        attempt_record["failure_reason"] = failure
                        break
                    finally:
                        precise_elapsed = time.monotonic() - attempt_started
                        download_seconds_used += precise_elapsed
                        elapsed = round(precise_elapsed, 3)
                        attempt_record["elapsed_seconds"] = elapsed
                        outcome["attempt_history"].append(attempt_record)
                        outcome["download_elapsed_seconds"] = round(
                            outcome["download_elapsed_seconds"] + elapsed, 3
                        )
                    if result is not None:
                        outcome["last_downloader_exit_code"] = result.returncode
                        attempt_record["exit_code"] = result.returncode
                        if result.returncode == 0:
                            # A downloader subprocess can replace its output.
                            # Recheck path safety before reading file metadata
                            # or hashing content that may now be a symlink.
                            verification_issue = None
                            if not destination_is_safe(destination, root):
                                verification_issue = "unsafe_output_path"
                                failure = "Downloader output is a symlink or has an unsafe parent."
                            elif not destination.is_file():
                                verification_issue = "missing_output"
                                failure = "Downloader succeeded but output file is missing or not regular."
                            else:
                                actual_size = destination.stat().st_size
                                attempt_record["output_bytes"] = actual_size
                                if actual_size == 0:
                                    verification_issue = "empty_output"
                                    failure = "Downloader succeeded but output file is empty."
                                elif args.max_file_size is not None and actual_size > args.max_file_size:
                                    verification_issue = "file_size_limit"
                                    failure = f"Downloaded file exceeds --max-file-size {args.max_file_size} bytes."
                                elif size is not None and actual_size != size:
                                    verification_issue = "size_mismatch"
                                    failure = f"Downloaded file size mismatch (expected {size} bytes)."
                                elif checksum and sha256_file(destination) != checksum:
                                    verification_issue = "checksum_mismatch"
                                    failure = "Downloaded file SHA-256 mismatch."
                                else:
                                    failure = None
                            attempt_record["outcome"] = (
                                "completed" if failure is None else "verification_failed"
                            )
                            if failure is not None:
                                attempt_record["failure_reason"] = failure
                                attempt_record["verification_issue"] = verification_issue
                                outcome["verification_issue"] = verification_issue
                            break
                        attempt_record["outcome"] = "nonzero_exit"
                        failure = f"Download failed (exit {result.returncode})."
                        attempt_record["failure_reason"] = failure
                    # The OS may report a subprocess timeout just before the
                    # monotonic sum reaches the configured budget. Treat a
                    # batch-capped timeout as decisive rather than attempting
                    # another launch on a tiny apparent remainder.
                    if attempt_record.get("timeout_source") == "max_batch_wall_seconds":
                        if attempt < args.attempts:
                            attempt_record["retry_suppressed_reason"] = "max_batch_wall_seconds"
                            outcome["retry_suppressed_reason"] = "max_batch_wall_seconds"
                        if attempt < args.attempts or index < len(downloads):
                            wall_time_budget_stopped = True
                            stop_reason = "max_batch_wall_seconds"
                        break
                    if attempt_record.get("timeout_source") == "max_download_seconds":
                        if attempt < args.attempts:
                            attempt_record["retry_suppressed_reason"] = "max_download_seconds"
                            outcome["retry_suppressed_reason"] = "max_download_seconds"
                        if attempt < args.attempts or index < len(downloads):
                            download_time_budget_stopped = True
                            stop_reason = "max_download_seconds"
                        break
                    if attempt < args.attempts:
                        if (
                            args.max_total_attempts is not None
                            and attempts_used >= args.max_total_attempts
                        ):
                            # Preserve the downloader's actual failure and
                            # explain why the next retry was not scheduled.
                            # This avoids replacing a timeout/exit-code error
                            # with an artificial budget failure.
                            attempt_record["retry_suppressed_reason"] = "max_total_attempts"
                            outcome["retry_suppressed_reason"] = "max_total_attempts"
                            outcome["attempt_budget_exhausted"] = True
                            attempt_budget_stopped = True
                            stop_reason = "max_total_attempts"
                            break
                        if (
                            args.max_download_seconds is not None
                            and download_seconds_used >= args.max_download_seconds
                        ):
                            attempt_record["retry_suppressed_reason"] = "max_download_seconds"
                            outcome["retry_suppressed_reason"] = "max_download_seconds"
                            download_time_budget_stopped = True
                            stop_reason = "max_download_seconds"
                            break
                        if wall_remaining() is not None and wall_remaining() <= 0:
                            attempt_record["retry_suppressed_reason"] = "max_batch_wall_seconds"
                            outcome["retry_suppressed_reason"] = "max_batch_wall_seconds"
                            wall_time_budget_stopped = True
                            stop_reason = "max_batch_wall_seconds"
                            break
                        delay = min(args.retry_delay * (2 ** (attempt - 1)), 60.0)
                        remaining_wall = wall_remaining()
                        if remaining_wall is not None and delay >= remaining_wall:
                            attempt_record["retry_suppressed_reason"] = "max_batch_wall_seconds"
                            outcome["retry_suppressed_reason"] = "max_batch_wall_seconds"
                            wall_time_budget_stopped = True
                            stop_reason = "max_batch_wall_seconds"
                            break
                        attempt_record["retry_delay_seconds"] = delay
                        print(f"  Retry {attempt + 1}/{args.attempts} in {delay:g}s.", flush=True)
                        time.sleep(delay)
                if failure:
                    fail(failure)
                else:
                    outcome["status"] = "downloaded"
                    outcome["output_bytes"] = destination.stat().st_size
                    outcome["integrity_verified"] = bool(checksum)
            except OSError as exc:
                fail(f"File operation failed: {exc}")
            finally:
                # Resolve the effective batch-stop reason before persisting
                # reports. Failure cap takes precedence when both limits
                # are reached after the same file; no more retry was denied.
                if index < len(downloads) and not (
                    attempt_budget_stopped or download_time_budget_stopped
                    or wall_time_budget_stopped
                ):
                    if args.max_failures is not None and failed >= args.max_failures:
                        stop_reason = "max_failures"
                    elif (
                        args.max_total_attempts is not None
                        and attempts_used >= args.max_total_attempts
                    ):
                        attempt_budget_stopped = True
                        stop_reason = "max_total_attempts"
                    elif (
                        args.max_download_seconds is not None
                        and download_seconds_used >= args.max_download_seconds
                    ):
                        download_time_budget_stopped = True
                        stop_reason = "max_download_seconds"
                    elif wall_remaining() is not None and wall_remaining() <= 0:
                        wall_time_budget_stopped = True
                        stop_reason = "max_batch_wall_seconds"
                # Run recovery even if a filesystem exception interrupted the
                # download path after quarantine succeeded.
                if outcome["status"] == "failed":
                    restore_quarantine_after_failure(outcome, destination)
                # Only reconcile retained failures once this entry has a
                # definitive outcome. An interrupted pending entry must keep
                # its earlier retry record.
                if args.retain_failures and not args.dry_run and outcome["status"] != "pending":
                    folder_key = relative.parent.as_posix()
                    existing = failed_entries.get(folder_key, [])
                    matching = [item for item in existing if item["name"] == relative.name]
                    retained = [item for item in existing if item["name"] != relative.name]
                    if outcome["status"] == "failed" and matching:
                        retained.append(matching[-1])
                    if retained:
                        failed_entries[folder_key] = retained
                    else:
                        failed_entries.pop(folder_key, None)
                # Persist failure information before advancing the cursor.
                # A pending entry must never be marked complete.
                if args.failed_manifest and not args.dry_run:
                    write_retry_manifest(args.failed_manifest.expanduser(), failed_entries)
                publish_status()
                publish_checkpoint()

    except (OSError, ValueError) as exc:
        # A report write failure must abort instead of silently advancing
        # to files whose recovery state cannot be persisted.
        print(f"Failed to persist download progress: {exc}", file=sys.stderr)
        return 1

    if args.status_out and not args.dry_run:
        print(f"Status report written: {args.status_out}")

    if args.failed_manifest and not args.dry_run:
        print(f"Retry manifest written: {args.failed_manifest}")

    if args.cursor_out and not args.dry_run:
        print(f"Batch checkpoint written: {args.cursor_out}")

    processed = len(outcomes)
    if args.verify_only:
        print(f"Local verification completed: {processed - failed}/{processed} checked; {len(downloads) - processed} unprocessed.")
    else:
        print(f"Completed: {processed - failed}/{processed} entries successful or skipped; {len(downloads) - processed} unprocessed.")
    unresolved = unresolved_failure_count()
    if args.retain_failures and unresolved:
        print(f"Unresolved retry entries: {unresolved}.", file=sys.stderr)
    return 1 if failed or (args.retain_failures and unresolved) or stop_reason is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
