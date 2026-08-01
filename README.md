# GhostStream

GhostStream is a reproducible search for weak meteor streams hidden in large public meteor-trajectory archives. The analysis identified a high-confidence late-April stream candidate in Global Meteor Network data, recovered it in a blind month-by-month search, reproduced it across multiple years, and found supporting events in CAMS and SonotaCo.

The result is a **meteor-stream discovery candidate**, not an officially recognized IAU meteor shower. Independent meteor-science review and a final duplicate-shower assessment are still required before publication or submission to the IAU Meteor Data Center.

## Repository layout

- `pipeline/pr57_novel/` — discovery, validation, external-archive, activity-profile, and submission-support source
- `pipeline/pr56_runner/` — the original blind-search and method-gate source preserved for exact reproducibility
- `candidate/` — final candidate solution, event lookup table, orbit solution, manuscript materials, and review documents
- `validation/` — exact reproduction, blind rediscovery, external-support, and method-control results
- `results/ghoststream_final_summary.json` — canonical machine-readable project summary
- `scripts/verify_repository.py` — structural, scientific-consistency, and repository-hygiene checks

## Current scientific result

The supported claim is:

> A computationally reproduced, high-confidence, apparently uncatalogued late-April meteor-stream candidate.

Key evidence includes:

- 95 confirmed GMN members across 2022–2026;
- exact reproduction of the preserved event set;
- one full-gate survivor in the blind January–July 2026 search;
- recurrence in untouched 2025 and 2024 data;
- 500/500 blind-search uncertainty-clone passes and 1,000/1,000 final-solution clone passes;
- 81/81 passing specification-grid cells;
- supporting CAMS and SonotaCo events;
- no hard automated match in the checked IAU Meteor Data Center catalogue.

## Repository hygiene

The active repository contains no tracked logs, caches, editor files, ZIP archives, temporary files, or abandoned cleanup workflows. The verifier rejects these artifacts if they are introduced later.

Some files under `pipeline/` have versioned names or end in `_fixed.py`. They are not unfinished temporary files. That directory is an immutable source snapshot of the exact historical execution trees, and those names document which compatibility or determinism fixes were actually applied. Renaming or deleting them would weaken the computational provenance.

## Verification

```bash
python -m pip install -r requirements.txt
python scripts/verify_repository.py
```

The complete computational environments and exact historical execution records are preserved under `validation/` and `pipeline/SOURCE_MANIFEST.json`.

## Provenance

The canonical evidence source is commit `af9a21e10d8c365cf4ca75f945b9c04bdde137e0` from the earlier development history. The final repository layout changes organization only; it does not alter the frozen candidate, event lists, statistics, or scientific claim boundary.

Canonical package SHA-256: `716b70313465d5df4bfb092a85a81680e6f618606b71e25470c63c480b6449f5`  
Expert-review bundle SHA-256: `60c0a77ed8852277f949a0296ccafc91ae4947277011cb1d6247b9be4b173e22`
