# Draft MDC material

This folder collects the event table, mean records, catalogue comparison, consistency checks, manuscript, and submission checklist.

## Main files

- `GhostStream_April_95_GMN_lookup.csv` contains the 95 GMN members from 2022–2026.
- `GhostStream_April_mean_submission.json` is the draft arithmetic-mean record.
- `GhostStream_April_mean_legacy.txt` is a compatibility version of the same record.
- `MANUSCRIPT_DRAFT.md` is the working paper draft.
- `LIVE_MDC_NOVELTY_REFRESH.md` records the comparison with the current official shower catalogue.
- `MDC_OFFICIAL_CHECKER_REPORT.md` records the official radiant/orbit consistency check.
- `MDC_PACKAGE_CONSISTENCY_AUDIT.md` summarizes the internal consistency check.
- `SUBMISSION_CHECKLIST.md` tracks the remaining work.

The numerical code, provisional designation, shower name, journal reference, and corresponding-author email remain blank until the submission process supplies them.

## Two related solutions

The project keeps two representations of the candidate:

1. A robust solution used for event matching and orbital-distance comparisons.
2. An unweighted arithmetic mean of the 95 lookup rows, prepared in the format expected for a draft MDC record.

Using the six-decimal draft values q = 0.080114 AU and e = 0.943593 gives a = 1.420285 AU. Using the full-precision means gives a = 1.420296 AU. Both calculations are recorded in `calculation_audit.json`.

## Remaining work

The remaining work is specialist review, confirmation of GMN data-use and acknowledgment language, and revision of the manuscript in response to that review.
