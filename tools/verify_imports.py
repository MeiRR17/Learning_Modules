#!/usr/bin/env python3
"""Offline Git object verification of the consolidated tools (no network/actions)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools/IMPORT_PROVENANCE.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> int:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    rows = m["files"]
    if len(rows) != 18 or m["source_count"] != 5:
        errors.append("Unexpected source count or file count")
    if sum(bool(x["transformed"]) for x in rows) != 4:
        errors.append("Expected four path-portability transformations")
    seen = set()
    for row in rows:
        location = pathlib.PurePosixPath(row["destination"])
        path = location.as_posix()
        if location.is_absolute() or ".." in location.parts or not path.startswith("tools/") or path in seen:
            errors.append(f"Invalid destination: {path}")
            continue
        seen.add(path)
        original = row["source_blob_sha"]
        expected = row["destination_blob_sha"]
        if not row["transformed"] and original != expected:
            errors.append(f"Unexpected source change: {path}")
        if row["transformed"] and original == expected:
            errors.append(f"Missing expected sanitization: {path}")
        local = ROOT / path
        if not local.is_file() or local.is_symlink():
            errors.append(f"Not a regular source file: {path}")
            continue
        data = local.read_bytes()
        if git_blob_sha(data) != expected:
            errors.append(f"Destination Git blob differs: {path}")
        if b"-----BEGIN OPENSSH PRIVATE KEY-----" in data or b"-----BEGIN RSA PRIVATE KEY-----" in data:
            errors.append(f"Private key detected: {path}")
        if path.startswith("tools/whisper-transcription/") and b"/Users/" in data:
            errors.append(f"Unredacted user home directory: {path}")
    for item in errors:
        print("FAIL:", item, file=sys.stderr)
    if errors:
        return 1
    print("PASS: 18 imported file Git object hashes, 14 exact and 4 portable adaptations.")
    print("No dependency, deployment, external API or license compliance assertion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
