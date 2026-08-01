# Draft MDC material

This folder contains the event table, mean records, catalogue comparison, consistency checks, manuscript, and checklist prepared for a possible IAU Meteor Data Center submission.

## Main files

- `GhostStream_April_95_GMN_lookup.csv` contains the 95 GMN members from 2022–2026.
- `GhostStream_April_mean_submission.json` is the draft arithmetic-mean record.
- `GhostStream_April_mean_legacy.txt` is a compatibility version of the same record.
- `MANUSCRIPT_DRAFT.md` is the working paper draft.
- `LIVE_MDC_NOVELTY_REFRESH.md` records the comparison with the current official shower catalogue.
- `MDC_OFFICIAL_CHECKER_REPORT.md` records the official radiant/orbit consistency check.
- `MDC_PACKAGE_CONSISTENCY_AUDIT.md` summarizes the internal consistency check.
- `SUBMISSION_CHECKLIST.md` lists completed preparation and remaining work.

The numerical code, provisional designation, shower name, journal reference, and corresponding-author email are fields completed during the appropriate submission process.

## Two related solutions

The project keeps two representations of the candidate:

1. A robust solution used for event matching and orbital-distance comparisons.
2. An unweighted arithmetic mean of the 95 lookup rows, prepared in the format expected for a draft MDC record.

The draft six-decimal values q = 0.080114 AU and e = 0.943593 imply a = 1.420285 AU after rounding. The full-precision means imply a = 1.420296 AU. Both calculations are preserved in `calculation_audit.json`.

## Next steps

The event table, mean records, official consistency check, and current catalogue comparison are prepared. The remaining work is specialist review, confirmation of GMN data-use and acknowledgment language, and revision of the manuscript in response to that review.
