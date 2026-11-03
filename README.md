# Learning Hub · מרכז הלמידה

This repository is the **single entry point for reusable programming lessons and exercises**. It is not a monorepo for production products, research datasets, private documents or organization-specific operational code.

## Learning tracks

| Track | Current material | Destination in future hub |
|---|---|---|
| REST APIs | [REST API Complete Tutorial](REST_API_Complete_Tutorial.md), [FastAPI tutorial (imported)](tracks/backend/fastapi/) | `tracks/backend/fastapi/` |
| Containers | [Docker complete guide](docker-complete-guide-hebrew.md) | `tracks/devops/docker/` |
| Java exercises | [Java anagram example (imported)](tracks/languages/java/) | `tracks/languages/java/` |
| C and algorithms | [C Sudoku example (imported)](tracks/languages/c/sudoku/) | `tracks/languages/c/algorithms/` |
| GUI/game experiments | [AirRaid](https://github.com/MeiRR17/AirRaid), [GalaxyFlare](https://github.com/MeiRR17/GalaxyFlare) | `tracks/game-dev/` |

## Cisco-specific material

Cisco/telephony training documentation is maintained by `DevTeam1770/Knowledge-Base` (private organizational repository), rather than this public personal learning hub. Reusable general REST API and Docker tutorials remain here. Access to organization-private documentation requires authorized GitHub membership; no internal content should be copied into this public repository.

## Migration rules
- First **link** the existing labs here; never delete/move historical repos before confirming their full content and git history.
- Import reusable educational code only after testing, code/asset licensing review and secret scanning; preserve meaningful attribution and provenance.
- Keep independent products, capstones, thesis work, Torah/AI experiments, datasets and deployed systems in their own repositories.
- Use one consistent track layout: `tracks/<domain>/<topic>/{README.md,examples,exercises,solutions,resources}`.
- Each exercise needs goal, prerequisites, run/test commands, expected outcome and source. Do not commit `node_modules`, virtual environments, local IDE builds, secret files or generated databases.
- Mark original repositories as superseded or archive them **only after** matching content and documenting which hub path replaced them.

This initial PR creates the public navigation point only. Physical history-preserving imports and archival are **not** performed.

See [consolidation checklist](LEARNING-CONSOLIDATION-PLAN.md).

## Imported public examples

The FastAPI tutorial, Java anagram example, and C Sudoku exercise now have tracked copies under [`tracks/`](tracks/) with immutable [source provenance](tracks/IMPORT_PROVENANCE.md). Original repositories are retained for their full Git history and unimported material. Build/runtime verification and archival decisions are separate follow-ups.

## Small utilities — one consolidated toolbox

Reusable standalone scripts from five public personal repositories now live under **[`tools/`](tools/README.md)**: Google Drive downloads, YouTube downloads, TaamAI, Sefaria/Neo4j and portable Whisper transcription. These are organized modules, not a single combined executable. The [provenance manifest](tools/IMPORT_PROVENANCE.json) pins all 18 imported source files; syntax and content-integrity CI gates were added. No media, private user input lists, transcript outputs or historical Neo4j hardcoded authentication settings were brought in.

The earlier `tracks/` teaching content remains independent; legacy source repos are not deleted by the import.
