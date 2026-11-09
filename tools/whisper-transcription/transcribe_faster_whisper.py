#!/usr/bin/env python3
"""Optional OFFLINE faster-whisper transcriber for authorized local audio.

Keeps the existing whisper.cpp script unchanged. Requires a pre-downloaded,
locally licensed CTranslate2 model and an operator-installed faster-whisper.
Generates TXT, SRT and JSON provenance without touching the original.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MEDIA = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".mp4", ".mov", ".webm", ".mkv"}


def hash_file(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def srt_timestamp(seconds: float) -> str:
    if seconds < 0:
        raise ValueError("Negative timestamps")
    milliseconds = round(seconds * 1000)
    hours, remaining = divmod(milliseconds, 3600000)
    minutes, remaining = divmod(remaining, 60000)
    secs, milliseconds = divmod(remaining, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def transcribe(media: Path, model_dir: Path, output_dir: Path, *,
               language: str = "he", device: str = "cpu",
               compute_type: str = "int8", beam_size: int = 5,
               model_factory=None) -> dict:
    if not media.is_file() or media.is_symlink() or media.suffix.lower() not in MEDIA:
        raise ValueError("Authorized local media file required")
    if media.stat().st_size > 2 * 1024 * 1024 * 1024:
        raise ValueError("Input larger than 2 GiB; split first")
    if not model_dir.is_dir() or model_dir.is_symlink():
        raise ValueError("A pre-downloaded local model directory is required")
    if not output_dir.is_dir() or output_dir.is_symlink():
        raise ValueError("Output directory must already exist")
    repo_root = Path(__file__).resolve().parents[2]
    if repo_root in output_dir.resolve().parents or output_dir.resolve() == repo_root:
        raise ValueError("Keep transcripts outside this public GitHub checkout")
    if repo_root in model_dir.resolve().parents or model_dir.resolve() == repo_root:
        raise ValueError("Keep model weights outside this public GitHub checkout")
    if language not in ("he", "en", "auto"):
        raise ValueError("Language must be he, en or auto")
    if beam_size not in range(1, 11):
        raise ValueError("Beam size must be 1–10")
    # Output names are based on the explicitly provided local filename.
    base = media.stem + ".faster-whisper"
    output = {
        "txt": output_dir / (base + ".txt"),
        "srt": output_dir / (base + ".srt"),
        "manifest": output_dir / (base + ".json"),
    }
    if any(p.exists() or p.is_symlink() for p in output.values()):
        raise FileExistsError("Output exists; input and existing outputs will not be overwritten")
    before = hash_file(media)
    if model_factory is None:
        from faster_whisper import WhisperModel  # type: ignore[import-not-found]
        model_factory = WhisperModel
    model = model_factory(str(model_dir), device=device, compute_type=compute_type,
                          local_files_only=True)
    segments, info = model.transcribe(str(media), language=None if language == "auto" else language,
                                      beam_size=beam_size, vad_filter=False)
    texts, captions = [], []
    for segment in segments:
        message = str(segment.text).strip()
        if not message:
            continue
        start, end = float(segment.start), float(segment.end)
        if not (0 <= start <= end < 24 * 3600 * 7):
            raise ValueError("Invalid segment timing")
        texts.append(message)
        captions.append(
            f"{len(captions)+1}\n{srt_timestamp(start)} --> {srt_timestamp(end)}\n{message}\n"
        )
        if len(captions) > 100_000:
            raise ValueError("Too many segments")
    if not texts:
        raise ValueError("No transcription detected")
    txt = "\n".join(texts) + "\n"
    srt = "\n".join(captions) + "\n"
    if max(len(txt.encode("utf-8")), len(srt.encode("utf-8"))) > 32 * 1024 * 1024:
        raise ValueError("Transcript exceeds size cap")
    if hash_file(media) != before:
        raise RuntimeError("Media changed during transcription; outputs refused")
    manifest = {
        "schema_version": 1, "engine": "faster-whisper",
        "source_name": media.name, "source_sha256": before,
        "local_model_directory_name": model_dir.name,
        "model_distribution_rights": "OPERATOR_MUST_CONFIRM",
        "language_requested": language, "language_observed": getattr(info, "language", None),
        "segment_count": len(captions), "duration_seconds": getattr(info, "duration", None),
        "device": device, "compute_type": compute_type,
        "external_upload": False, "indexing_performed": False,
        "txt_sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
        "srt_sha256": hashlib.sha256(srt.encode("utf-8")).hexdigest(),
    }
    payloads = {"txt": txt, "srt": srt,
                "manifest": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"}
    made = []
    try:
        for key, path in output.items():
            with path.open("x", encoding="utf-8") as file:
                made.append(path)
                file.write(payloads[key])
    except BaseException:
        for path in made:
            path.unlink(missing_ok=True)
        raise
    return {"outputs": {name: str(p) for name, p in output.items()}, **manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", type=Path)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--language", choices=("he", "en", "auto"), default="he")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()
    try:
        print(json.dumps(transcribe(args.media, args.model_dir, args.output_dir,
                                    language=args.language, device=args.device,
                                    compute_type=args.compute_type),
                         ensure_ascii=False, indent=2))
    except (ValueError, FileExistsError, ImportError, RuntimeError, OSError) as exc:
        parser.exit(1, "Transcription refused: " + str(exc) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
