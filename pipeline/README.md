# Preserved analysis code

This directory preserves the executable source used across the discovery and validation stages.

The `pr56_runner/` snapshot contains the early method controls and blind-search code. The `pr57_novel/` snapshot contains the all-season search, candidate validation, uncertainty tests, external-catalogue work, and submission-support scripts.

The programs were written as standalone scripts. The exact file list and hashes are recorded in `SOURCE_MANIFEST.json`; the clean reproduction records under `validation/` show which entry points were rerun.

The scripts expect public catalogue downloads and can be computationally expensive. `scripts/verify_repository.py` only checks repository structure, fixed metadata, and Python syntax.

These snapshots remain unchanged for provenance. Small compatibility repairs used in later reruns are documented separately under `validation/`.
