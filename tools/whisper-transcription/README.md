# Whisper transcription helpers (macOS compatible)

Original: https://github.com/MeiRR17/Video_to_text (main). Four executable/code scripts only were imported. **No videos, audio recordings, subtitle/transcript outputs, large models or collected user files were imported.**

The three Bash scripts used the original developer's hard-coded macOS desktop path; here they resolve their own directory by default and support an explicit `BASE_DIR` environment variable. Example:

```bash
BASE_DIR="$HOME/Videos" bash tools/whisper-transcription/transcribe_all.sh
```

The Python cleanup script now accepts `VIDEO_TO_TEXT_OUTPUT_DIR` (defaults to the `output/` directory beside the script). These are adapted source snapshots rather than byte-identical copies. The original source Git hashes are documented in `tools/IMPORT_PROVENANCE.json`; runtime execution and whisper.cpp model compatibility have not been tested. Keep all recordings and output folders outside this public repository.

## Optional faster-whisper adapter (development branch)

This directory now also includes `transcribe_faster_whisper.py`. It is an
**optional real transcription implementation**, not a replacement for the
existing whisper.cpp workflow or Kolmud Studio's MLX model. It runs on an
operator-owned local audio/video file using a **pre-downloaded local** faster-
whisper CTranslate2 model. No model downloads or API keys are requested.

In an isolated Python environment, install the MIT code package after
reviewing model-weight terms:

    python -m pip install faster-whisper
    mkdir -p "$HOME/Transcripts/pilot"
    python tools/whisper-transcription/transcribe_faster_whisper.py \
      "$HOME/Recordings/owned_lecture.wav" \
      --model-dir "$HOME/Models/faster-whisper-he" \
      --output-dir "$HOME/Transcripts/pilot"

The model directory must actually contain a compatible offline model
(download and license approval are manual, separate steps). All output folders
and model weights **must stay outside this public GitHub repository**.

The result is `owned_lecture.faster-whisper.txt`,
`owned_lecture.faster-whisper.srt` and
`owned_lecture.faster-whisper.json`, with source hash, detected language and
output checksums. The script refuses to overwrite existing outputs, mutate
the original, use symlinks or download missing models. Cloud transcription and
automatic corpus indexing are out of scope.

No real acoustic quality/benchmark claim has been established yet. Compare
Hebrew WER/CER and elapsed time against the already present whisper.cpp
backend on the same *authorized* 1-3 minute lecture clip before switching
backend.

    python -m unittest discover -s tools/whisper-transcription -p 'test_transcribe_faster_whisper.py' -v

The tests use a fake local model; no heavy dependencies or downloads.
