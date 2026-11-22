# Google Drive Downloader

## Manifest-based downloader (new)

For new download lists, use `manifest_downloader.py` instead of editing
`COURSE_STRUCTURE` in the historical script. Requires Python 3.9+ and yt-dlp.

Create a local `manifest.json`:

```json
{
  "Course/Week 1": [
    {"id": "YOUR_GOOGLE_DRIVE_FILE_ID", "name": "lecture.mp4", "size": 1048576}
  ]
}
```

Each file may include an optional positive integer `"size"` in bytes and an
optional 64-character hexadecimal `"sha256"` checksum. Existing files with
mismatched sizes or checksums are **not overwritten**. New downloads are also
checked against any supplied expectations. Size alone can detect truncation,
but does not prove file integrity.

Reserve available storage during large batches:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --min-free-space 10737418240 --failed-manifest failed.json
```

`--min-free-space` accepts a nonnegative byte count; the example reserves
10 GiB. Before invoking yt-dlp for each new file, the downloader checks
the destination filesystem's free bytes. If the manifest provides a
`size`, it requires enough free space for the **estimated remaining**
bytes plus the reserve. For an interrupted transfer with an existing regular
`.part` file, the downloader subtracts the bytes already present in that
partial file from the expected size. If no expected size is provided, only
the reserve can be checked before downloading. The check runs before **each
retry**, and a symlinked or non-regular partial-download path is rejected.
Insufficient space is recorded as a per-file failure and can be retried later.
This is a preflight safeguard, not a guarantee: concurrent processes can
consume space during downloads, and yt-dlp may use other temporary files.

For integrity-sensitive archives, require SHA-256 checksums on every selected
file:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --require-sha256 --verify-only
```

`--require-sha256` rejects the selected batch before file operations if
any entry lacks `sha256`. It works with downloads, `--verify-only`,
`--dry-run`, and file/folder selection filters. Entries excluded from the
current batch are not required to carry checksums. Without this flag, the
existing optional-checksum behavior is unchanged.

### Portable destination paths

Manifest folder names and filenames must be relative and use forward slashes
for nested folders. Path traversal, control characters, Windows-invalid
characters (`< > : " / \\ | ? *` where `/` is only a folder separator),
and Windows-reserved names such as `CON`, `NUL`, `COM1`, and `LPT1`
are rejected, including names with extensions (for example `CON.txt`).
Output roots that are themselves symbolic links are also rejected; existing
symlinked paths inside the output directory remain prohibited. The manifest
also rejects duplicate destinations after Unicode NFC normalization and
case folding, and refuses file/directory conflicts (for example, a file
named `Week1` alongside the folder `Week1/`). These checks protect against
filesystem naming differences across macOS, Windows, and Linux.

Preview the destinations:

```bash
python manifest_downloader.py manifest.json --output downloads --dry-run
```

Audit existing files without downloading or requiring cookies:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --verify-only --failed-manifest missing-or-invalid.json
```

This reads existing local files only. An empty or absent file is reported as
missing; a file with an expected SHA-256 is fully hashed. Without a checksum,
the audit can confirm presence, nonzero size and any supplied expected
size but **cannot** establish cryptographic integrity. The resulting report is another valid manifest containing entries
that need attention. The `--verify-only` and `--dry-run` modes are mutually
exclusive.

Select a specific folder, or cap the number of selected files:

```bash
python manifest_downloader.py manifest.json --folder "Course/Week 1" --limit 10
python manifest_downloader.py manifest.json --folder "Course/Week 1" \
  --folder "Other Course" --verify-only
```

Select individual files by their complete relative manifest destinations:

```bash
python manifest_downloader.py manifest.json \
  --file "Course/Week 1/lecture.mp4" \
  --file "Course/Week 2/lecture.mp4" --verify-only
```

Repeat `--file` to include multiple exact destinations in manifest order.
Unknown paths cause an error. When `--file` and `--folder` are both
specified, a file must match both filters; `--exclude-file` and
`--exclude-folder` still take precedence. All selection filters apply
before pagination and `--only-failed` intersects the resulting set with
unresolved retries. Checkpoints include `selected_files` and reject a
different `--file` selection when resuming. Checkpoints created before
this field existed represent an unrestricted file selection.

Folders are matched as complete relative paths, including their descendants,
not arbitrary string prefixes. Repeating `--folder` combines selections.
Use `--exclude-folder` to omit entire subtrees, including when they fall
inside a selected parent:

```bash
python manifest_downloader.py manifest.json --folder "Course" \
  --exclude-folder "Course/Archived" --exclude-folder "Course/Drafts" \
  --limit 20 --cursor-out checkpoint.json
```

Exclusions are applied after folder inclusion but before `--offset`,
`--after`, `--cursor-in`, and `--limit`. Thus pagination counts only
files that remain eligible. Checkpoints record `excluded_folders` and
reject resume attempts where `--exclude-folder` differs from the original
run. Older checkpoints lacking this field imply no exclusions. Use repeatable
`--exclude-file` for an exact target instead of excluding a whole subtree:

```bash
python manifest_downloader.py manifest.json --folder "Course" \
  --exclude-file "Course/Week 1/lecture.mp4" --limit 20 \
  --cursor-out checkpoint.json
```

The file path must exist in the manifest, and must match the complete
relative destination. Checkpoints also record `excluded_files` and require
the same file exclusions when resuming with `--cursor-in`. Older checkpoints
without `excluded_files` are treated as having no excluded files. All manifest
entries are still validated and protected against output/report collisions,
including excluded files.
Use `--offset` together with `--limit` to page through matching entries
in stable manifest order (the default offset is zero):

```bash
python manifest_downloader.py manifest.json --limit 10 --offset 0
python manifest_downloader.py manifest.json --limit 10 --offset 10
python manifest_downloader.py manifest.json --limit 10 --offset 20
```

Alternatively, resume directly after a known file destination using
`--after`. This is useful if entries were inserted before your previous
batch, because it does not depend on their numeric positions:

```bash
python manifest_downloader.py manifest.json --after "Course/Week 1/lecture.mp4" --limit 10
```

The path must exactly match a file destination in the currently selected
manifest (using forward slashes). That file itself is excluded from the
new batch. Folder filtering is applied before the cursor lookup; if the
cursor is missing, the command fails rather than silently starting over.
`--after` and `--offset` cannot be combined. Reordering entries or removing
the cursor from the manifest can still change which files follow it.

Save a machine-readable checkpoint at the end of a batch:

```bash
python manifest_downloader.py manifest.json --limit 10 \
  --failed-manifest failed.json --cursor-out checkpoint.json
```

`checkpoint.json` includes `after` (the last selected destination),
`processed`, `failed`, `matching_entries`, `has_more`, and
`manifest_sha256`. Use `after` in the next invocation:

```bash
python manifest_downloader.py manifest.json \
  --after "Course/Week 1/lecture.mp4" --limit 10 \
  --failed-manifest failed-next.json --cursor-out checkpoint-next.json
```

You can now resume directly from the checkpoint without manually copying
the `after` value:

```bash
python manifest_downloader.py manifest.json --limit 10 \
  --cursor-in checkpoint.json --cursor-out checkpoint.json \
  --failed-manifest failed-next.json
```

`--cursor-in` is mutually exclusive with `--after` and `--offset`.
Before processing files, the downloader compares the checkpoint's
`manifest_sha256` with the current manifest and checks that the
`--folder` selection is unchanged. It rejects stale or incompatible
checkpoints rather than silently restarting. The checkpoint may be updated
in place with `--cursor-out`. Previous failures are reported as a warning;
they still need to be retried using their own failure manifest.

The checkpoint is atomically updated after each completed file, including
files that failed. If the process stops during a file, the checkpoint remains
at the last completed entry rather than skipping an unfinished file. This
makes `--cursor-in` useful after interrupted batches, not only completed
batches. A nonzero `failed` count means some selected
entries were unsuccessful: retry them using `failed.json` before considering
the batch fully complete. The fingerprint can be compared to detect changes
in the input manifest between batches. The checkpoint is not written in
`--dry-run` mode, and its path cannot be the input or failure manifest.

When a selection is empty (for example, a cursor already past the final
file), the command does not invoke yt-dlp. If report paths were supplied,
it replaces the retry manifest with `{}`, writes a zero-entry status report,
and writes a checkpoint with `has_more: false`. An existing input cursor is
carried forward into the output checkpoint; if the offset has passed the
last eligible file, that file becomes the checkpoint cursor. Only a manifest
selection with zero matching entries produces `after: null`. Such a
checkpoint can be supplied to `--cursor-in` again without an error and
will remain complete as long as the manifest and filters are unchanged.
No reports are
written for an empty `--dry-run`. As with nonempty batches, using the same
report paths replaces their prior contents.

Folder filtering happens before offset and limit are applied. All manifest
entries are validated before selection, and retry reports include only
failures from the selected page. If the input manifest changes between
runs, offsets may no longer refer to the same files. To cover the full
manifest, run every page or finish with an unfiltered, unlimited run.

Create a machine-readable report of each selected file's result:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --status-out status.json --failed-manifest failed.json
```

`status.json` contains a `files` array with each relative `path`, its
`status`, and a `reason` for failures. It also includes aggregate `counts`
and `selected`. Download runs use `downloaded` or `skipped` for successful
files; offline verification uses `verified`, `size-checked`, or `present`
depending on the available integrity metadata. Errors appear as `failed`.
The status report does not include Google Drive IDs or cookies. The report
is atomically updated after each selected file, including failures; it is not
produced in dry-run mode. If interrupted, the report preserves outcomes written
so far, but does not itself resume the batch. Use `--cursor-in` for completed
batch checkpoints or rerun the original manifest to skip eligible files.
If a progress report cannot be written (for example, because the disk is
full or permissions deny the update), the downloader prints an error and
terminates with a nonzero exit status rather than moving on to more files.
The last successfully written reports remain on disk. Fix the storage issue
and resume from the last valid checkpoint, or rerun the manifest; unfinished
files may be skipped only when they satisfy the existing-file checks.

Report files cannot overwrite the manifest, cookies, or input checkpoint.
Before downloading or generating reports, the tool also rejects collisions
between any declared download destination and the input manifest, cookie
file, input checkpoint, or report paths. This check uses the complete
manifest, even when `--folder`, `--offset`, `--after`, or `--limit` selects
only part of it. Keep report files outside the download destination tree
when names could overlap with files in the manifest.

Stop a large batch when repeated failures suggest unavailable files or
network trouble:

```bash
python manifest_downloader.py manifest.json --limit 50 --max-failures 3 \
  --status-out status.json --failed-manifest failed.json \
  --cursor-out checkpoint.json
```

`--max-failures` accepts a positive integer and counts failed **files**,
not individual yt-dlp retry attempts. The default is to process the entire
selected batch. When the threshold is reached, no further files are started;
the JSON status report contains results only for processed entries, and the
checkpoint's `after` and `processed` fields identify the last processed
entry and actual progress. The `has_more` field remains true when entries
are still waiting. The failed-entry manifest contains all failures observed
before stopping. It is initialized at batch start and atomically updated
after each processed file, so a crash or interruption preserves failures
recorded so far. By default, every new run starts a fresh failure list at the supplied
path; save old retry manifests elsewhere before reusing that path, or
use `--retain-failures` to preserve unresolved entries. Those
failed entries must be retried separately; resuming from the checkpoint
moves forward and does not retry them automatically.

Limit how long an individual yt-dlp attempt may run:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --timeout 300 --attempts 3 --retry-delay 2 \
  --failed-manifest failed.json --status-out status.json
```

`--timeout` is an optional positive number of seconds. If omitted, there
is no subprocess timeout. Each timed-out attempt counts toward
`--attempts` and follows the same exponential retry delay as a nonzero
downloader exit. Once attempts are exhausted, the file is marked failed
and appears in both status and retry manifests when enabled. This is a
**per-attempt** deadline rather than a timeout for the entire batch.
Timeouts can leave partial downloads on disk, which yt-dlp may resume.

Keep unresolved failures from earlier batches in a single retry manifest:

```bash
python manifest_downloader.py manifest.json --limit 20 \
  --failed-manifest failed.json --retain-failures \
  --cursor-in checkpoint.json --cursor-out checkpoint.json
```

`--retain-failures` requires `--failed-manifest`. If the retry report
already exists, it is loaded and validated before downloads begin. Failures
from earlier batches are retained; when an entry is processed again, a
successful outcome removes its old retry record, while a failed outcome
replaces that record without duplicates. An interrupted pending item keeps
its previous record. A `--dry-run` preview never changes
retained failure records. An empty selection does not clear the retained retry
manifest. Checkpoints now include `unresolved_failures`, the total number of
entries still requiring a retry across all retained batches, distinct from
`failed` (failures encountered in the current batch). With
`--retain-failures`, the program exits nonzero while that unresolved count
is positive, even for an empty or otherwise successful batch. Without
`--retain-failures`, each run replaces the retry list as before. Use a separate input manifest when retrying failures, since an
output retry manifest cannot overwrite the active input manifest.

Retry only outstanding entries using the original manifest:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --failed-manifest failed.json --retain-failures --only-failed \
  --limit 10 --status-out retry-status.json
```

`--only-failed` requires both `--retain-failures` and an existing
`--failed-manifest`. It selects only paths recorded as unresolved in that
report, in the original manifest's order. As each selected file succeeds,
its entry is removed from the retained failure report; unsuccessful entries
remain. A failure referring to a file no longer in the original manifest is
rejected instead of silently ignored. Each retained failure must also
match the original manifest's Drive file ID, optional SHA-256 digest, and
optional expected byte size; mismatches require an explicit correction of
the retry record or a fresh retry manifest before using `--only-failed`. Folder selection and exclusions still
apply, and `--limit` allows bounded retry batches. Run the command again
to attempt remaining failures. Because the eligible selection changes as
files are resolved, `--only-failed` cannot be combined with `--offset`,
`--after`, `--cursor-in`, or `--cursor-out`. The command exits nonzero
until the retained retry manifest is empty.

Download files you are authorized to access:

```bash
python manifest_downloader.py manifest.json --output downloads \
  --cookies /path/to/cookies.txt --attempts 3 --retry-delay 2 \
  --failed-manifest failed.json
```

The cookie argument is optional for publicly accessible files. Failed entries
are collected in `failed.json`, which uses the same schema as the input and
can be supplied as the next run's manifest. The retry report is published
atomically and cannot use the same path as the input manifest. The downloader preserves partial
downloads using yt-dlp's normal resume behavior and backs off on process
failures. A checksum mismatch is not retried automatically, to avoid
silently overwriting corrupted content. Keep manifests containing private
file IDs and cookie files outside public version control.

---

A Python script to automatically download video courses from Google Drive using yt-dlp with cookie-based authentication. Maintains the exact folder hierarchy structure locally.

## Features

- Downloads videos from Google Drive using file IDs
- Preserves original folder structure
- Resumable downloads (skips existing files)
- Progress tracking with detailed logs
- Error handling and failed download reporting
- Random throttling to avoid rate limiting

## Prerequisites

- Python 3.7 or higher
- yt-dlp library
- Google Drive cookies (Netscape format)

## Installation

### 1. Install Python

Download and install Python from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation.

### 2. Install yt-dlp

Open a terminal/command prompt and run:

```bash
pip install yt-dlp
```

### 3. Export Google Drive Cookies

You need to export your browser cookies to authenticate with Google Drive:

**Option A: Using Chrome Extension (Recommended)**
1. Install the "Get cookies.txt LOCALLY" Chrome extension
2. Go to drive.google.com and log in
3. Click the extension icon and export cookies
4. Save the file as `cookies.txt` in the same folder as this script

**Option B: Using Browser Export Tool**
1. Use a tool like [cookies.txt](https://github.com/kairi003/Get-cookies.txt-LOCALLY)
2. Export cookies from drive.google.com
3. Save as `cookies.txt`

**Important:** The `cookies.txt` file should be in the same directory as `auto_downloader.py`. It's already in `.gitignore` to prevent accidental commits.

## Project Structure

```
Google Drive Downloader/
├── auto_downloader.py    # Main script
├── cookies.txt           # Browser cookies (NOT in git)
├── .gitignore            # Ignores cookies.txt
└── README.md             # This file
```

## Configuration

### Setting Up Your Course Structure

Edit the `COURSE_STRUCTURE` dictionary in `auto_downloader.py` to add your courses:

```python
COURSE_STRUCTURE = {
    "Folder/Subfolder": [
        ("FILE_ID_HERE", "filename.mp4"),
        ("ANOTHER_FILE_ID", "another_video.mp4")
    ]
}
```

### Finding Google Drive File IDs

1. Open the file in Google Drive
2. The URL format is: `https://drive.google.com/file/d/[FILE_ID]/view`
3. Copy the `[FILE_ID]` part (the long alphanumeric string)

### Changing Output Directory

Edit the `BASE_DIR` variable at the top of the script:

```python
BASE_DIR = os.path.abspath("Your_Custom_Folder_Name")
```

## Usage

### Basic Usage

1. Place `cookies.txt` in the same folder as the script
2. Run the script:

```bash
python auto_downloader.py
```

### What Happens During Execution

1. The script checks for `cookies.txt`
2. Creates the base directory structure
3. Iterates through each folder and file in `COURSE_STRUCTURE`
4. Downloads each file using yt-dlp
5. Skips files that already exist (resumable)
6. Adds random delays between downloads (0.5-1.5 seconds)
7. Reports progress and any failed downloads

### Output Structure

After running, you'll have:

```
University_Course_Data/
├── 01-Linux/
│   ├── 01-intro.mp4
│   ├── 02-HPC.mp4
│   └── ...
├── 02-Python/
│   ├── part1/
│   │   ├── 01-intro_to_Python.mp4
│   │   └── ...
│   └── part2/
│       ├── part1.mp4
│       └── ...
└── ...
```

## Troubleshooting

### "cookies.txt file not found!"

- Ensure `cookies.txt` is in the same directory as the script
- Check that the filename is exactly `cookies.txt` (not `cookies.txt.txt`)

### Download Failed Errors

- Your cookies may have expired - re-export them
- Check your internet connection
- Verify the file ID is correct
- Some files may require additional permissions

### Files Not Downloading

- Check if files already exist in the output directory (script skips existing files)
- Delete existing files if you want to re-download them
- Verify the file IDs are still valid (files may have been deleted or moved)

### Permission Errors

- Ensure you have write permissions in the output directory
- On Windows, run the terminal as Administrator if needed

## Advanced Usage

### Adding Speed Adjustment and Video Processing

Based on your requirements to adjust video speed and extract to a separate folder, you can extend the script with FFmpeg:

1. Install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add FFmpeg to your system PATH
3. Create a secondary script that:
   - Reads the downloaded videos
   - Uses FFmpeg to adjust playback speed
   - Maintains the same folder hierarchy in a new output directory

Example FFmpeg command for speed adjustment:
```bash
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" output.mp4
```

## Security Notes

- **Never commit `cookies.txt` to version control** - it contains your authentication tokens
- The `.gitignore` file is configured to ignore `cookies.txt`
- Re-export cookies periodically as they may expire
- Only use cookies from accounts you own or have permission to access

## License

This script is provided as-is for educational purposes.

## Support

For issues with:
- **yt-dlp**: Visit [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- **Cookie export**: Use the Chrome extension mentioned above
- **Script errors**: Check the error messages in the terminal output
