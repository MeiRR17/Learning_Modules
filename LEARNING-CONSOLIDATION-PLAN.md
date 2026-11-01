# Learning repository consolidation — review checklist

## Goal
Keep one visible learning hub (`Learning_Modules`) instead of maintaining many tiny tutorial repositories. Avoid combining educational code with production applications, business IP, academic research or confidential Cisco operational work.

## Staged workflow
1. Inventory candidate practice exercises from the private DvirOS portfolio catalog; separately assess whether each is truly a lesson, usable app or finished coursework.
2. Classify by domain: languages (Java, C/C++, Android), API/backend (FastAPI), DevOps (Docker), algorithms (Sudoku), and UI/game exercises.
3. For each source, run secret/license scan and identify binary artifacts, local databases, IDE outputs and generated builds. Document the source Git SHA, original repo, owners and any external attribution.
4. Create track-based folders and import selected lessons. Prefer `git subtree` or a traceable scripted import if retaining commit history matters; test each imported example. Do not blindly concatenate branches or remove original repos.
5. Update navigation, replace hardcoded relative paths, and verify Linux/macOS/Windows execution where practical.
6. Once tests, links and source snapshots match, archive redundant small exercise repos; preserve standout capstones as independent portfolio projects.
7. Keep the Cisco guide in review. Move any organization-specific content only into the private DevTeam1770 knowledge system after redaction/authorization; do not simply copy private material into this public repo.

## Public learning links initially in scope
- `MeiRR17/JAVA`
- `MeiRR17/AirRaid`
- `MeiRR17/Sudoku`
- `MeiRR17/GalaxyFlare`
- `MeiRR17/Learning_FastAPI`
- existing REST, Docker and Cisco guides already in this repository (Cisco guide pending screening).

## Non-goals
No archive, copy, branch merge, secret disclosure or transfer has occurred. A research notebook, complete product or proprietary project should **not** be recategorized as a tutorial merely to lower the repository count.
