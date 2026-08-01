# GhostStream IAU MDC pre-submission package

Generated: 2026-07-31  
Last scientific update: 2026-08-01

This folder is a **draft package** for internal checking and external expert review. Nothing has been submitted to the IAU Meteor Data Center or a journal.

## Current reproducibility status

The original GhostStream implementation was recovered from immutable temporary runner commits and is now preserved under `../../recovered_pipeline/` with file-level SHA-256 provenance.

The recovered source has completed clean fail-closed reruns of the scientific analysis chain:

- exact primary GMN reproduction: **101 total selected events** and the committed **95-event 2022–2026 lookup** matched timestamp-for-timestamp;
- source-preserving activity and source/time-matched orbital nulls;
- 20,000-replicate year/night cluster bootstrap;
- corrected March–May activity profile;
- three disjoint GMN geographic groups;
- frozen 81-cell specification curve;
- CAMS and SonotaCo archive checks and the exact pooled ten-event ID set; and
- a current JPL parent screen, with zero objects at Southworth–Hawkins D ≤ 0.15.

Authoritative evidence:

- `../../recovered_pipeline/SOURCE_MANIFEST.json`
- `../../reconstruction/exact_recovered/EXACT_REPRODUCTION.md`
- `../../reconstruction/exact_downstream/DOWNSTREAM_REPRODUCTION.md`
- `../../reconstruction/exact_external/EXTERNAL_REPRODUCTION.md`
- `../../results/ghoststream_final_summary.json`

The recovered package audit recomputes the MDC lookup quantities and verifies the source manifest plus primary, internal-downstream, and external clean-rerun records. The remaining hold is not that the code is missing. The remaining hold is package completion, final human review, and independent meteor-science/duplicate-shower review.

Raw monthly GMN catalogue bytes have not been vendored as a complete immutable archive. The exact recovered implementation successfully regenerated the reported results from the current official monthly source, but long-term raw-input preservation remains a disclosed limitation.

## Submission files

- `GhostStream_April_95_GMN_lookup.csv` — the 95 GMN meteors from the five significant years, formatted to the current MDC lookup-table columns.
- `GhostStream_April_mean_submission.json` — a draft mean record matching the current MDC database JSON field structure.
- `GhostStream_April_mean_legacy.txt` — a compatibility record for the February 20, 2026 legacy text template.
- `calculation_audit.json` — exact values and rules used to generate the mean record, including separate full-precision and submitted-precision semimajor-axis derivations.
- `MDC_OFFICIAL_CHECKER_REPORT.md` — exact rerun of the current official MDC radiant/orbit consistency programs on the committed mean; the distributed binaries and a fresh build of the distributed Fortran source produced identical comparison files and zero errors.
- `exact_official_checker_summary.json` — machine-readable provenance and result for that checker rerun.
- `live_mdc_novelty_refresh_summary.json` — checksum-locked comparison against official catalogue version 2026-06-25.
- `MDC_PACKAGE_CONSISTENCY_AUDIT.md` — recovered, fail-closed package audit.
- `mdc_package_consistency_summary.json` — machine-readable package verdict, recomputed lookup quantities, hashes, and recovered-analysis evidence.
- `MANUSCRIPT_DRAFT.md` — current manuscript draft; it still requires final human and expert review.
- `SUBMISSION_CHECKLIST.md` — completed computational checks and remaining external-review/submission blockers.
- `AI_AND_SOFTWARE_PROVENANCE.md` — disclosure of substantive generative-AI and software assistance.

## Supporting evidence elsewhere in the project

- `../../recovered_pipeline/` — exact preserved source snapshots from the immutable runner commits.
- `../../reconstruction/exact_recovered/` — exact primary reproduction evidence.
- `../../reconstruction/exact_downstream/` — regenerated source-null, bootstrap, activity, geographic, and specification outputs.
- `../../reconstruction/exact_external/` — regenerated CAMS, SonotaCo, pooled archive, EDMOND-link, and JPL evidence.
- `../BOOTSTRAP_UNCERTAINTY.md` — 20,000-replicate year/night cluster-bootstrap report.
- `../SPECIFICATION_CURVE.md` — frozen 81-cell threshold-grid report.
- `../ACTIVITY_PROFILE.md` — corrected March–May source-normalized activity report.
- `../GEOGRAPHIC_SPLIT_VALIDATION.md` — three-group GMN validation report.
- `../ALL_EXTERNAL_ZERO_SPEED.md` — uniform external-archive synthesis.
- `../all_external_members_zero_speed.csv` — all 16 selected CAMS, SonotaCo, and Shober EDMOND events.
- `../shober_edmond/SHOBER_EDMOND_VALIDATION.md` — archive-specific EDMOND audit and provenance boundary.
- `../edmond_2024/EDMOND_CURRENT_RELEASE_AUDIT.md` — integrity audit showing that the currently linked annual files are incomplete or stale relative to advertised v6.01.
- `../candidate_solution.json` — machine-readable frozen solution and evidence summary.
- `../flux/` — tested RMS handoff tools and the data requirements for an absolute-flux analysis using consented GMN Level 2 station-night data.

## Mean record

The mean record is calculated from exactly **95** GMN member rows in 2022–2026. The lookup table contains exactly **95** data rows, satisfying the MDC N-consistency requirement.

The record uses unweighted arithmetic means (`Flags = A`). The submitted six-decimal `q = 0.080114 AU` and `e = 0.943593` imply `a = 1.420284716... AU`; the draft record uses `a = 1.420285 AU` after six-decimal rounding. The separate full-precision means imply `a = 1.420295780... AU` and remain preserved in `calculation_audit.json`.

The package verifies arithmetic consistency of the lookup rows and links them to the exact recovered primary rerun.

## Deliberate placeholders

The following are intentionally blank or provisional:

- IAU numerical code;
- three-letter code;
- provisional MDC designation;
- official shower name;
- final journal reference;
- corresponding-author email.

The MDC assigns the numerical code and provisional designation. An official name must not be invented at this stage.

## Current claim boundary

Supported:

- recovery and preservation of the original executable source;
- exact primary 101-event and 95-event reproduction;
- clean internal downstream reproduction;
- exact CAMS/SonotaCo supporting-member reproduction;
- current official-catalogue novelty and MDC consistency-checker evidence; and
- a high-confidence uncatalogued annual late-April meteor-stream candidate.

Not claimed:

- official IAU recognition or established-shower status;
- a complete current EDMOND v6.01 replication;
- a fully independent third-network replication;
- absolute flux or ZHR;
- a parent-body identification; or
- submission readiness before independent review.

## Submission boundary

Do not send or submit the package until:

1. the recovered package audit passes against the current branch;
2. the code-inclusive expert-review bundle is built and checksum-validated;
3. the recovered all-season blind rediscovery and method-control evidence are included when complete;
4. a meteor-science expert reviews the coordinates, orbit conventions, null models, and duplicate-shower risk;
5. GMN data-use and authorship/acknowledgment language is confirmed;
6. authorship, affiliation, journal, and timetable are final; and
7. the final edited code/data/manuscript package is regenerated and checksum-locked.

The MDC one-year publication clock must not begin before those review and submission steps are complete.
