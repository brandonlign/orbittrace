# Preserved analysis code

This directory contains the executable source used for discovery and validation.

The `pr56_runner/` snapshot contains the early method controls and blind-search code. The `pr57_novel/` snapshot contains the all-season search, candidate validation, uncertainty tests, external-catalogue work, and submission-support scripts.

The `cc_cfrs_v1/` package is a separate, new methodology study. It contains
the Canonical-Cell Cross-Fitted Recurrent Scan implementation scaffold and its
label-free Stage 0 contract. It does not modify the historical snapshots or
the frozen paper evidence.

The `unified_v2/` package is the active exploratory revision: a partitioned
exposure-normalized recurrent tree, cross-fitted halo propagation, and fixed
orbital-coherence gate. Its results are kept separate from the frozen v1
evidence and include checksummed seed/expansion artifacts for the fresh
target-label-sealed run.

The programs are standalone scripts. `SOURCE_MANIFEST.json` records the exact files and hashes, and the reproduction notes under `validation/` identify the entry points that were rerun.

The scripts expect public catalogue downloads and can be computationally expensive. `scripts/verify_repository.py` only checks repository structure, fixed metadata, and Python syntax.

The snapshots are kept unchanged. Small compatibility repairs used in later reruns are documented separately under `validation/`.
