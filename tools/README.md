# Small utilities — consolidated source

Five previously standalone or script-focused public repositories now have selected scripts under this **one** existing `MeiRR17/Learning_Modules` repository. These are isolated **utilities**, not one combined executable.

| Folder | Source | Included |
|---|---|---|
| [google-drive-downloader](google-drive-downloader/) | `MeiRR17/Google-Drive-Downloader` | Python downloader, README, gitignore |
| [youtube-downloader](youtube-downloader/) | `MeiRR17/Youtube-Downloader` | Python downloader, requirements, README (no personal URL list) |
| [taam-cantillation](taam-cantillation/) | `MeiRR17/TaamAI` | Python cantillation pipeline and requirements |
| [neo4j-sefaria](neo4j-sefaria/) | `MeiRR17/Neo4j` | Cypher and PowerShell/Python helpers (no insecure historical Compose) |
| [whisper-transcription](whisper-transcription/) | `MeiRR17/Video_to_text` | Four scripts, with personal macOS paths replaced by configurable paths; no transcripts or audio |

Exact source Git blob IDs and explicit portability edits are pinned in [IMPORT_PROVENANCE.json](IMPORT_PROVENANCE.json). Run `python3 tools/verify_imports.py` for the local source snapshot integrity check. The GitHub CI checks source hashes and Python/Bash syntax only; **it does not execute downloaders, run Neo4j, call Sefaria, transcribe recordings or prove end-to-end behavior.**

The original source repositories remain unchanged to preserve full Git history, stars, issues and existing links. This consolidation does not authorize deleting them; decide separately after confirming all code, dependencies, legal rights and consumer links. Empty or large dataset projects were excluded rather than importing irrelevant data.

The separate private organizational [DevTeam1770/Scripts](https://github.com/DevTeam1770/Scripts) and Cisco monorepo were **not** touched; organizational operational scripts must stay within their own access boundaries.

Usage respects third-party terms and applicable copyright, particularly downloading video/audio and consuming data APIs.
