# Preserved analysis code

This directory contains the executable source used for discovery and validation.

The `pr56_runner/` snapshot contains the early method controls and blind-search code. The `pr57_novel/` snapshot contains the all-season search, candidate validation, uncertainty tests, external-catalogue work, and submission-support scripts.

The programs are standalone scripts. `SOURCE_MANIFEST.json` records the exact files and hashes, and the reproduction notes under `validation/` identify the entry points that were rerun.

The scripts expect public catalogue downloads and can be computationally expensive. `scripts/verify_repository.py` only checks repository structure, fixed metadata, and Python syntax.

The snapshots are kept unchanged. Small compatibility repairs used in later reruns are documented separately under `validation/`.
