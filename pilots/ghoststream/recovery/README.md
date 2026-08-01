# Recovering the missing GhostStream core pipeline

## Purpose

The current GitHub branch preserves the GhostStream results package but not the software that generated the central GMN analyses. This directory contains a read-only local inventory tool to search Brandon's Mac for the original implementation before attempting a reconstruction.

The tool does not modify Git, restore objects, copy files, upload data, or use the network.

## Run on Brandon's Mac

From the local repository:

```bash
cd /Users/Brandon/Desktop/isef
python3 pilots/ghoststream/recovery/audit_local_workspace.py \
  --repo /Users/Brandon/Desktop/isef \
  --output-dir /Users/Brandon/Desktop/ghoststream_recovery_audit
```

The default search window is July 24 through August 2, 2026 UTC. To widen it:

```bash
python3 pilots/ghoststream/recovery/audit_local_workspace.py \
  --repo /Users/Brandon/Desktop/isef \
  --output-dir /Users/Brandon/Desktop/ghoststream_recovery_audit_wide \
  --start 2026-07-01T00:00:00-04:00 \
  --end 2026-08-05T23:59:59-04:00
```

Add another likely storage root by repeating `--root`:

```bash
python3 pilots/ghoststream/recovery/audit_local_workspace.py \
  --repo /Users/Brandon/Desktop/isef \
  --output-dir /Users/Brandon/Desktop/ghoststream_recovery_audit \
  --root /Users/Brandon/Desktop \
  --root /Users/Brandon/Downloads \
  --root '/Users/Brandon/Library/Application Support/OpenCode'
```

## Outputs

- `GHOSTSTREAM_LOCAL_RECOVERY_AUDIT.md` — readable list of highest-priority source/notebook/archive candidates.
- `ghoststream_local_recovery_audit.json` — complete machine-readable inventory.
- `git_results.json` — Git status, branches, worktrees, reflogs, stashes, unreachable objects, and dated file history.

The report may contain personal paths and command-history snippets. Review it locally before sharing or committing anything.

## What it searches

### Files and archives

- `.py`, `.ipynb`, shell, R, Julia, MATLAB, JSON/YAML, Markdown, CSV, and other text files;
- ZIP/TAR/GZIP/7z/RAR archives modified near the GhostStream work period;
- names and content matching GhostStream, GMN, antihelion, bootstrap, geographic split, specification curve, clone, activity-profile, and related terms;
- common OpenCode storage locations, Desktop, Downloads, Documents, and the local `isef` directory.

### Git recovery sources

- untracked files;
- all local/remote branches;
- worktrees;
- reflogs;
- stashes;
- unreachable/dangling commits and blobs;
- files changed during the likely work interval; and
- ignored versus untracked state.

### Shell history

The tool records matching commands from `.zsh_history` and `.bash_history`, with common inline secret assignments redacted.

## Privacy and secret handling

- Files with secret-like names are never content-inspected or hashed.
- The tool does not upload anything.
- It does not run `git reset`, `git checkout`, `git restore`, `git clean`, or any other modifying Git command.
- It does not restore dangling objects automatically.
- It does not copy candidate files.
- Do not commit `.env`, credentials, API keys, session databases, browser data, or full private chat histories.

## Candidate review procedure

1. Copy the entire audit-output directory to a safe location.
2. Start with source/notebook candidates that contain multiple matching terms and were modified during July 24–August 2.
3. Review Git worktrees, stashes, and reflogs before inspecting dangling objects.
4. For a promising directory, copy it to a separate recovery directory before editing.
5. Record original path, modification time, byte count, and SHA-256.
6. Search for hard-coded result values, manual membership lists, and post-result parameter changes.
7. Determine whether the code can acquire or verify exact source catalogues.
8. Run only a small non-scientific smoke test first.
9. Never treat numerical agreement with preserved reports as independent validation if parameters were adjusted to achieve it.

## If the original code is recovered

Do not immediately merge it into the paper package. First:

- preserve a raw hash-locked copy;
- document chronology and original environment;
- remove credentials and machine-specific paths without changing scientific logic;
- identify discovery versus confirmation stages;
- freeze a clean configuration;
- add deterministic tests and fail-closed input validation; and
- rerun from immutable source manifests.

## If the original code is not recovered

Reconstruction is allowed only as a new, explicitly documented reproducibility project. Use the preserved reports to recover definitions, not to tune the implementation until target values match. A valid reconstruction must begin from source catalogues and independently regenerate the membership and statistics under frozen rules.
