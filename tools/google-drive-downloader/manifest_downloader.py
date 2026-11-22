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
import re
import subprocess
import sys
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


def entries(manifest: object) -> Iterator[tuple[str, Path, str | None]]:
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be an object mapping folders to file lists")
    seen: set[str] = set()
    for folder, files in manifest.items():
        folder_path = relative_destination(folder, allow_subdirs=True)
        if not isinstance(files, list):
            raise ValueError(f"Folder {folder!r} must contain a list")
        for item in files:
            if not isinstance(item, dict) or not {"id", "name"} <= set(item) or set(item) - {"id", "name", "sha256"}:
                raise ValueError("Each file requires 'id', 'name'; optionally 'sha256'")
            file_id = item["id"]
            if not isinstance(file_id, str) or not DRIVE_ID.fullmatch(file_id):
                raise ValueError(f"Invalid Drive file ID in {folder!r}")
            checksum = item.get("sha256")
            if checksum is not None and (not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", checksum)):
                raise ValueError(f"Invalid SHA-256 in {folder!r}")
            filename = relative_destination(item["name"], allow_subdirs=False)
            target = folder_path / filename
            # Windows and macOS may treat distinct spellings as the same file.
            identity = target.as_posix().casefold()
            if identity in seen:
                raise ValueError(f"Duplicate destination: {target}")
            seen.add(identity)
            yield file_id, target, checksum.lower() if checksum else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON file listing authorized downloads")
    parser.add_argument("--output", type=Path, default=Path("downloads"))
    parser.add_argument("--cookies", type=Path, help="Optional Netscape cookies.txt file")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--failed-manifest", type=Path)
    args = parser.parse_args(argv)
    if args.attempts < 1 or not 0 <= args.retry_delay <= 3600:
        parser.error("Require --attempts >= 1 and 0 <= --retry-delay <= 3600")

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        downloads = list(entries(manifest))  # Validate everything before writing.
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(f"Invalid manifest: {exc}")

    root = args.output.expanduser().resolve()
    cookies = args.cookies.expanduser().resolve() if args.cookies else None
    if cookies and not cookies.is_file():
        parser.error(f"Cookies file does not exist: {cookies}")

    if not downloads:
        print("Manifest contains no downloads.")
        return 0

    failed = 0
    failed_entries = {}
    for index, (file_id, relative, checksum) in enumerate(downloads, start=1):
        destination = root / relative
        print(f"[{index}/{len(downloads)}] {relative}", flush=True)
        def fail(reason):
            nonlocal failed
            failed += 1
            item = {"id": file_id, "name": relative.name}
            if checksum:
                item["sha256"] = checksum
            failed_entries.setdefault(relative.parent.as_posix(), []).append(item)
            print(f"  {reason}", file=sys.stderr)

        if args.dry_run:
            continue
        if not destination_is_safe(destination, root):
            fail("Symlink destination refused.")
            continue
        if destination.is_file() and destination.stat().st_size > 0:
            if checksum is None or sha256_file(destination) == checksum:
                print("  Already exists; skipped.")
                continue
            fail("Existing file checksum mismatch; refusing overwrite.")
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
                if checksum and (
                    not destination.is_file() or sha256_file(destination) != checksum
                ):
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

    if args.failed_manifest and not args.dry_run:
        report = args.failed_manifest.expanduser()
        if report.is_symlink():
            parser.error("Failed-manifest path must not be a symlink")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            json.dumps(failed_entries, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Retry manifest written: {report}")

    print(f"Completed: {len(downloads) - failed}/{len(downloads)} entries successful or skipped.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
