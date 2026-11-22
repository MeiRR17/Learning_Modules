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
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Iterator

DRIVE_ID = re.compile(r"^[A-Za-z0-9_-]{10,256}$")


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
    if any(":" in part or part.endswith((" ", ".")) for part in parts):
        raise ValueError(f"Nonportable destination: {value!r}")
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
            # Windows and macOS may treat distinct spellings as the same file.
            identity = target.as_posix().casefold()
            if identity in seen:
                raise ValueError(f"Duplicate destination: {target}")
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
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--failed-manifest", type=Path)
    parser.add_argument("--status-out", type=Path,
                        help="Write a JSON report of individual file outcomes")
    parser.add_argument("--cursor-out", type=Path,
                        help="Write a JSON checkpoint containing the last processed path")
    parser.add_argument("--folder", action="append", default=[],
                        help="Only process this folder and its descendants (repeatable)")
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
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")
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
    except ValueError as exc:
        parser.error(f"Invalid --folder: {exc}")
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
        if checkpoint.get("failed", 0):
            print("Warning: checkpoint has failed entries; retry them separately.", file=sys.stderr)
        try:
            resume_after = relative_destination(checkpoint["after"], allow_subdirs=True)
        except (KeyError, TypeError, ValueError) as exc:
            parser.error(f"Invalid checkpoint cursor: {exc}")
    if args.attempts < 1 or not 0 <= args.retry_delay <= 3600:
        parser.error("Require --attempts >= 1 and 0 <= --retry-delay <= 3600")

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        downloads = list(entries(manifest))  # Validate everything before writing.
        if selected_folders:
            downloads = [
                entry for entry in downloads
                if any(
                    entry[1].parent == folder or folder in entry[1].parents
                    for folder in selected_folders
                )
            ]
        # Preserve stable manifest order across successive batch invocations.
        # Filtering precedes slicing, so offsets refer to matching entries.
        total_matching = len(downloads)
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
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(f"Invalid manifest: {exc}")

    # Compare resolved paths before downloading: the retry output must never
    # replace the user's original manifest (including through symlink aliases).
    if not args.dry_run:
        reports = [
            path.expanduser() for path in (args.failed_manifest, args.cursor_out, args.status_out)
            if path is not None
        ]
        resolved_reports = [path.resolve() for path in reports]
        if any(path.is_symlink() for path in reports):
            parser.error("Report destination must not be a symlink")
        if len(set(resolved_reports)) != len(resolved_reports):
            parser.error("Report destinations must all be distinct")
        if args.manifest.expanduser().resolve() in resolved_reports:
            parser.error("Report destination must differ from input manifest")

    root = args.output.expanduser().resolve()
    cookies = args.cookies.expanduser().resolve() if args.cookies else None
    if cookies and not args.verify_only and not args.dry_run and not cookies.is_file():
        parser.error(f"Cookies file does not exist: {cookies}")

    if not downloads:
        print(f"No downloads selected (matched {total_matching}; start index {start}).")
        return 0
    print(
        f"Selected {len(downloads)} of {total_matching} matching entries "
        f"(start index {start})."
    )

    failed = 0
    failed_entries = {}
    outcomes = []
    for index, (file_id, relative, checksum, size) in enumerate(downloads, start=1):
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

        if args.dry_run:
            outcome["status"] = "planned"
            continue
        if not destination_is_safe(destination, root):
            fail("Symlink destination refused.")
            continue
        if args.verify_only:
            if not destination.is_file():
                fail("Missing or non-regular local file.")
            elif destination.stat().st_size == 0:
                fail("Local file is empty.")
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
            continue
        if destination.is_file() and destination.stat().st_size > 0:
            if (size is None or destination.stat().st_size == size) and (
                checksum is None or sha256_file(destination) == checksum
            ):
                outcome["status"] = "skipped"
                print("  Already exists; skipped.")
                continue
            fail("Existing file size or checksum mismatch; refusing overwrite.")
            continue
        if destination.exists() and not destination.is_file():
            fail("Destination is not a regular file; skipped.")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable, "-m", "yt_dlp",
            "--continue",
            "--no-playlist",
            "--format", "best[ext=mp4]/best",
            "--output", str(destination),
        ]
        if cookies:
            command.extend(["--cookies", str(cookies)])
        command.append(f"https://drive.google.com/file/d/{file_id}/view")
        failure = None
        for attempt in range(1, args.attempts + 1):
            try:
                result = subprocess.run(command, check=False)
            except OSError as exc:
                failure = f"Could not launch downloader: {exc}"
                break
            if result.returncode == 0:
                if not destination.is_file() or destination.stat().st_size == 0:
                    failure = "Downloader succeeded but output file is missing or empty."
                elif size is not None and destination.stat().st_size != size:
                    failure = f"Downloaded file size mismatch (expected {size} bytes)."
                elif checksum and sha256_file(destination) != checksum:
                    failure = "Downloaded file SHA-256 mismatch."
                else:
                    failure = None
                break
            failure = f"Download failed (exit {result.returncode})."
            if attempt < args.attempts:
                delay = min(args.retry_delay * (2 ** (attempt - 1)), 60.0)
                print(f"  Retry {attempt + 1}/{args.attempts} in {delay:g}s.", flush=True)
                time.sleep(delay)
        if failure:
            fail(failure)
        else:
            outcome["status"] = "downloaded"

    if args.status_out and not args.dry_run:
        counts = {}
        for item in outcomes:
            status = item["status"]
            counts[status] = counts.get(status, 0) + 1
        report = {"schema_version": 1, "selected": len(downloads),
                  "counts": counts, "files": outcomes}
        try:
            write_retry_manifest(args.status_out.expanduser(), report)
        except (OSError, ValueError) as exc:
            print(f"Failed to write status report: {exc}", file=sys.stderr)
            return 1
        print(f"Status report written: {args.status_out}")

    if args.failed_manifest and not args.dry_run:
        report = args.failed_manifest.expanduser()
        try:
            write_retry_manifest(report, failed_entries)
        except (OSError, ValueError) as exc:
            print(f"Failed to write retry manifest: {exc}", file=sys.stderr)
            return 1
        print(f"Retry manifest written: {report}")

    if args.cursor_out and not args.dry_run:
        checkpoint = {
            "schema_version": 1,
            "manifest_sha256": sha256_file(args.manifest),
            "folders": sorted(folder.as_posix() for folder in selected_folders),
            "after": downloads[-1][1].as_posix(),
            "processed": len(downloads),
            "failed": failed,
            "matching_entries": total_matching,
            "has_more": start + len(downloads) < total_matching,
        }
        try:
            write_retry_manifest(args.cursor_out.expanduser(), checkpoint)
        except (OSError, ValueError) as exc:
            print(f"Failed to write batch checkpoint: {exc}", file=sys.stderr)
            return 1
        print(f"Batch checkpoint written: {args.cursor_out}")

    if args.verify_only:
        print(f"Local verification completed: {len(downloads) - failed}/{len(downloads)} files present and acceptable.")
    else:
        print(f"Completed: {len(downloads) - failed}/{len(downloads)} entries successful or skipped.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
