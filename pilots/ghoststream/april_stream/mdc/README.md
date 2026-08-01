# GhostStream IAU MDC pre-submission package

Generated: 2026-07-31  
Last scientific update: 2026-08-01

This folder is a **draft package**. Nothing has been submitted to the IAU Meteor Data Center.

## Submission files

- `GhostStream_April_95_GMN_lookup.csv` — the 95 GMN meteors from the five significant years, formatted to the current MDC lookup-table columns.
- `GhostStream_April_mean_submission.json` — a pre-submission mean record matching the current MDC database JSON field structure.
- `GhostStream_April_mean_legacy.txt` — a compatibility record for the February 20, 2026 legacy text template.
- `calculation_audit.json` — exact values and rules used to generate the mean record.
- `MDC_OFFICIAL_CHECKER_REPORT.md` — results from the official MDC radiant/orbit consistency programs; zero errors flagged.
- `MANUSCRIPT_DRAFT.md` — complete current manuscript draft.
- `SUBMISSION_CHECKLIST.md` — remaining blockers before external delivery.

## Supporting evidence elsewhere in `april_stream/`

- `BOOTSTRAP_UNCERTAINTY.md` — 20,000 year/night cluster-bootstrap replicates and confidence intervals.
- `SPECIFICATION_CURVE.md` — frozen 81-cell threshold grid; all 81 cells passed.
- `ACTIVITY_PROFILE.md` — corrected March–May source-normalized activity profile.
- `GEOGRAPHIC_SPLIT_VALIDATION.md` — three disjoint GMN geographic station-group tests.
- `ALL_EXTERNAL_ZERO_SPEED.md` — uniform external-archive rerun with unresolved speed drift fixed to zero.
- `all_external_members_zero_speed.csv` — all 16 selected CAMS, SonotaCo, and Shober EDMOND events.
- `shober_edmond/SHOBER_EDMOND_VALIDATION.md` — archive-specific EDMOND audit and provenance boundary.
- `candidate_solution.json` — machine-readable frozen solution, bootstrap intervals, claim boundary, and evidence summary.
- `flux/` — tested RMS handoff tools and the exact data required for an absolute flux analysis using consented GMN Level 2 station-night data.

## Mean record

The mean record is calculated from exactly **95** deduplicated GMN members in 2022–2026. The lookup table contains exactly **95** data rows, satisfying the MDC N-consistency requirement.

The record uses unweighted arithmetic means (`Flags = A`). Semimajor axis is derived from the mean q and e rather than averaged independently, so `q = a(1-e)` is internally consistent.

The robust medoid orbit is used for membership and similarity tests. The arithmetic-mean orbit is used for the MDC mean record. Cluster-bootstrap intervals quantify sampling variability across years and observing nights.

The fitted geocentric-speed drift is retained for reproducibility, but its clustered 95% interval crosses zero. It must not be presented as a detected physical drift. External archive validation was rerun uniformly with `dVg/dλ⊙ = 0` and remained positive.

## Deliberate placeholders

The following are intentionally blank or provisional:

- IAU numerical code;
- three-letter code;
- provisional MDC designation;
- official shower name;
- final journal reference;
- corresponding-author email.

The MDC assigns the numerical code and provisional designation. An official name must not be invented at this stage.

## Submission boundary

Do not send the package until:

1. the manuscript is reviewed by a meteor-science expert;
2. a duplicate-shower review confirms the novelty result;
3. the GMN data-use and authorship/acknowledgment language is confirmed;
4. the author and affiliation fields are final;
5. the target journal and submission timetable are realistic; and
6. the final edited package is regenerated and checksum-locked.

The MDC requires a mean-data record, one lookup table per shower, and a manuscript. The final paper must be published within one year of MDC submission or the shower may be moved to the Removed list.
