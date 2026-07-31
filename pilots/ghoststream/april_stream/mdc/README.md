# GhostStream IAU MDC pre-submission package

Generated: 2026-07-31

This folder is a **draft package**. Nothing has been submitted to the IAU Meteor Data Center.

## Files

- `GhostStream_April_95_GMN_lookup.csv` — the 95 GMN meteors from the five significant years, formatted to the current MDC lookup-table columns.
- `GhostStream_April_mean_submission.json` — a pre-submission mean record matching the current MDC database JSON field structure.
- `GhostStream_April_mean_legacy.txt` — a compatibility record for the February 20, 2026 legacy text template.
- `calculation_audit.json` — exact values and rules used to generate the mean record.
- `MDC_OFFICIAL_CHECKER_REPORT.md` — results from the official MDC radiant/orbit consistency programs; zero errors flagged.
- `MANUSCRIPT_DRAFT.md` — first complete manuscript draft.
- `SUBMISSION_CHECKLIST.md` — blockers that must be resolved before sending.

## Mean record

The mean record is calculated from exactly **95** deduplicated GMN members in 2022–2026. The lookup table contains exactly **95** data rows, satisfying the MDC N-consistency requirement.

The record uses unweighted arithmetic means (`Flags = A`). Semimajor axis is derived from the mean q and e rather than averaged independently, so `q = a(1-e)` is internally consistent.

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
5. the target journal and submission timetable are realistic.

The MDC states that a mean-data template, one lookup table per shower, and a manuscript are required. The final paper must be published within one year of MDC submission or the shower may be moved to the Removed list.
