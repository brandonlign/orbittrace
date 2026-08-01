# GhostStream IAU MDC pre-submission package

Generated: 2026-07-31  
Last scientific update: 2026-08-01

This folder is a **draft internal-results package**. Nothing has been submitted to the IAU Meteor Data Center or a journal.

## Critical reproducibility status

The committed package is internally consistent and its later MDC/EDMOND/package audits are reproducible. However, the current branch does **not** contain the core GMN discovery and validation software or exact source-input manifests that produced the principal scientific results.

Missing end-to-end implementations include the blind GMN search, expanded-antihelion activity test, shifted-window and orbital nulls, uncertainty clones, year/night bootstrap, geographic split, March–May activity profile, and 81-cell specification curve.

Therefore:

- the 111/111 package audit is an internal consistency/provenance check, not end-to-end scientific reproduction;
- the current branch cannot regenerate the 95-member lookup from the original GMN catalogues;
- the current expert-review bundle is superseded and must not be sent as a code-complete reproducibility package;
- no public reproducibility DOI should be minted from this branch; and
- journal or formal MDC submission is blocked until the original pipeline is recovered or independently reconstructed and cleanly rerun.

See `../../REPRODUCIBILITY_GAP_AUDIT.md`.

## Submission files

- `GhostStream_April_95_GMN_lookup.csv` — the 95 GMN meteors from the five significant years, formatted to the current MDC lookup-table columns.
- `GhostStream_April_mean_submission.json` — a pre-submission mean record matching the current MDC database JSON field structure.
- `GhostStream_April_mean_legacy.txt` — a compatibility record for the February 20, 2026 legacy text template.
- `calculation_audit.json` — exact values and rules used to generate the mean record, including separate full-precision and submitted-precision semimajor-axis derivations.
- `MDC_OFFICIAL_CHECKER_REPORT.md` — exact rerun of the current official MDC radiant/orbit consistency programs on the committed mean; the distributed binaries and a fresh build of the distributed Fortran source produced identical comparison files and zero errors.
- `exact_official_checker_summary.json` — machine-readable provenance and result for that exact checker rerun.
- `live_mdc_novelty_refresh_summary.json` — checksum-locked comparison against the official catalogue version 2026-06-25.
- `MDC_PACKAGE_CONSISTENCY_AUDIT.md` — fail-closed internal package audit; all 111 checks passed.
- `mdc_package_consistency_summary.json` — machine-readable internal package verdict, recomputed lookup quantities, semimajor-axis precision audit, hashes, and CI evidence.
- `MANUSCRIPT_DRAFT.md` — current manuscript draft, not ready for submission while the core pipeline is missing.
- `SUBMISSION_CHECKLIST.md` — completed bounded checks and remaining reproducibility/external blockers.

## Supporting evidence elsewhere in `april_stream/`

- `BOOTSTRAP_UNCERTAINTY.md` — preserved report of 20,000 year/night cluster-bootstrap replicates and confidence intervals; producing core code is not currently committed.
- `SPECIFICATION_CURVE.md` — preserved report of the frozen 81-cell threshold grid; producing core code is not currently committed.
- `ACTIVITY_PROFILE.md` — preserved corrected March–May source-normalized activity report; producing core code is not currently committed.
- `GEOGRAPHIC_SPLIT_VALIDATION.md` — preserved three-group validation report; producing core code is not currently committed.
- `ALL_EXTERNAL_ZERO_SPEED.md` — uniform external-archive synthesis.
- `all_external_members_zero_speed.csv` — all 16 selected CAMS, SonotaCo, and Shober EDMOND events.
- `shober_edmond/SHOBER_EDMOND_VALIDATION.md` — archive-specific EDMOND audit and provenance boundary.
- `edmond_2024/EDMOND_CURRENT_RELEASE_AUDIT.md` — integrity audit showing that the currently linked annual files are incomplete or stale relative to the advertised v6.01 release.
- `candidate_solution.json` — machine-readable frozen solution and evidence summary.
- `flux/` — tested RMS handoff tools and the exact data required for an absolute flux analysis using consented GMN Level 2 station-night data.

## Mean record

The mean record is calculated from exactly **95** preserved GMN member rows in 2022–2026. The lookup table contains exactly **95** data rows, satisfying the MDC N-consistency requirement.

The record uses unweighted arithmetic means (`Flags = A`). The submitted six-decimal `q = 0.080114 AU` and `e = 0.943593` imply `a = 1.420284716... AU`; the submitted record uses `a = 1.420285 AU` after six-decimal rounding. The separate full-precision means imply `a = 1.420295780... AU` and remain preserved in `calculation_audit.json`.

The current package verifies arithmetic consistency of the preserved rows. It does not independently verify that those 95 rows can be regenerated from the original source catalogues until the core pipeline is restored and rerun.

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

1. the core source-to-result pipeline and exact input manifests are recovered or independently reconstructed;
2. a clean fail-closed rerun regenerates the 95-member lookup and primary reported statistics;
3. every discrepancy from the preserved package is documented;
4. the manuscript is reviewed by a meteor-science expert with access to the reproducible pipeline;
5. a duplicate-shower review confirms the novelty result;
6. GMN data-use and authorship/acknowledgment language is confirmed;
7. authorship, affiliation, journal, and timetable are final; and
8. the final edited code/data/manuscript package is regenerated and checksum-locked.

The MDC one-year publication clock must not begin while the core analysis is unreproducible.
