# CC-CFRS v1

This is the implementation scaffold for the new OrbitTrace methodology study:
**Canonical-Cell Cross-Fitted Recurrent Scan**.

It is deliberately separate from the historical OrbitTrace discovery and
validation scripts.  The package has no target coordinates, target IDs,
membership table, or truth-label dependency.

## Stage 0 scope

The current slice implements and tests:

- the fixed three-scale physical representation;
- deterministic canonical cell identity and half-open quantization;
- leave-one-year-out proposal generation using compact quarter-window cores,
  recurrence-aware local density modes, and one-bin physical neighborhoods at
  each scale;
- exact same-cell held-out evaluation;
- empirical held-out p-values and the at-least-two-of-three partial conjunction;
- fixed physical adjacency and deterministic local maxima; and
- complete-null score attachment and no-rerank annual capacity projection;
- frozen temporal-holdout execution that fits only on discovery years and
  records under-capacity in untouched years without reranking; and
- nuisance-preserving phase-permutation null generation plus the exact finite-
  sample Stage 0 gate helpers.

The bounded real-catalogue outcome is recorded in
`EXPLORATORY_RESULTS.md`. It is an exploratory method study, not a production
claim or a replacement for the frozen paper-facing methods.

The production contract is machine-readable in
`CC_CFRS_PREREGISTRATION.json`.  The 999 calibration replicates and 2,000
validation panels are not run by the repository smoke tests; a completed
Stage 0 result requires real endpoint inputs, frozen hashes, and the full
predeclared banks.

## Input adapter

`adapters.py` provides the strict local-table adapter.  Raw decoded source
tables should use `adapt_raw_frame` or `load_csv`: the adapter first selects
only physical event fields and records every dropped raw column.  It then
accepts common
GMN/SonotaCo-style aliases, converts ecliptic or equatorial radiants into the
Sun-centred convention, prefixes event IDs with the source, and emits a
provenance manifest including hashes.  It rejects columns whose names expose
shower, target, truth, membership, background, or known-source information.

The normalized table has unique `event_id` values and these columns:

`year`, `sol_lon_deg`, `radiant_lon_deg`, `radiant_lat_deg`, `speed_km_s`.

The discovery and holdout paths retain the full valid solar-longitude domain,
including 20–55 degrees.  An interval-excluded table may be supplied to
`PhasePermutationNull(..., require_target_interval_excluded=True)` only for a
separately declared control; it is never the discovery default.

## Local checks

From the repository root:

```bash
python -m unittest discover -s tests -p 'test_cc_cfrs.py'
python scripts/verify_repository.py
```

Passing these checks means the implementation scaffold is internally
consistent.  It does not mean that the scientific Stage 0 gate has passed.

The exact bank is intentionally guarded:

```bash
python -m pipeline.cc_cfrs_v1.run_stage0 \
  --source SonotaCo \
  --input 2012=/path/to/S12.csv \
  --input 2013=/path/to/S13.csv \
  --input 2014=/path/to/S14.csv \
  --delimiter ';' \
  --confirm-expensive
```

This runs the complete 999-replicate calibration and fixed 2,000-panel
validation bank.  The method must stop on any source/hash/row firewall error;
there is no partial-bank success mode.

For a single ordinary scan before running that bank:

```bash
python -m pipeline.cc_cfrs_v1.run_scan \
  --source SonotaCo \
  --input 2012=/path/to/S12.csv \
  --input 2013=/path/to/S13.csv \
  --input 2014=/path/to/S14.csv \
  --delimiter ';' \
  --output cc-cfrs-scan.json
```

The scan retains the full valid solar-longitude domain and reports the
selected canonical cells; it does not use truth labels or run Stage 0.
