# Whisper transcription helpers (macOS compatible)

Original: https://github.com/MeiRR17/Video_to_text (main). Four executable/code scripts only were imported. **No videos, audio recordings, subtitle/transcript outputs, large models or collected user files were imported.**

The three Bash scripts used the original developer's hard-coded macOS desktop path; here they resolve their own directory by default and support an explicit `BASE_DIR` environment variable. Example:

```bash
BASE_DIR="$HOME/Videos" bash tools/whisper-transcription/transcribe_all.sh
```

The Python cleanup script now accepts `VIDEO_TO_TEXT_OUTPUT_DIR` (defaults to the `output/` directory beside the script). These are adapted source snapshots rather than byte-identical copies. The original source Git hashes are documented in `tools/IMPORT_PROVENANCE.json`; runtime execution and whisper.cpp model compatibility have not been tested. Keep all recordings and output folders outside this public repository.
