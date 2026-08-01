# GhostStream reproducibility recovery audit

Audit opened: 2026-08-01  
Current update: 2026-08-01

## Current verdict

**`CORE_SOURCE_RECOVERED_AND_PRIMARY_RESULT_EXACTLY_REPRODUCED`**

The earlier audit correctly established that the principal GMN source-to-result implementation was absent from the `isef` branch. Its conclusion that the software had not been preserved anywhere accessible was incomplete.

The original executable source survived in two temporary `brandonlign/remotion-worker` pull-request commits and has now been copied unchanged into this branch with file-level SHA-256 provenance:

- PR #56 recovery/discovery tree: 13 files at commit `4175e5187fcc6faf3d1befb099a9e35be96850f2`
- PR #57 novel-search/downstream tree: 35 files at commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`

Authoritative manifest:

`pilots/ghoststream/recovered_pipeline/SOURCE_MANIFEST.json`

## What was recovered

The preserved source includes implementations for:

- official GMN monthly catalogue acquisition and parsing;
- quality filtering and exact-time trajectory deduplication;
- known-shower recovery and injection controls;
- blind candidate scans;
- frozen April member selection;
- Southworth–Hawkins orbital distance and post-selection compactness tests;
- expanded-antihelion source-preserving activity and shifted-window tests;
- source/time-matched orbital nulls;
- measurement-uncertainty clone trials;
- year/night cluster bootstrap;
- disjoint geographic station-group validation;
- corrected March–May exposure-normalized activity profiling;
- the frozen 81-cell specification curve;
- CAMS, SonotaCo, and EDMOND archive checks;
- IAU catalogue/official-checker support;
- parent-body screening; and
- flux-handoff utilities.

The exact recovered snapshots are preserved separately from all later reconstruction or repair work.

## Exact primary clean rerun

GitHub Actions reran the unchanged original `validate_april_candidate.py` from immutable commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e` under Python 3.9.25 and the recovered pinned direct dependencies.

Source identity:

- validator SHA-256: `4a29b4c3bde528be2523b627f7e8a22d3c836f45981cc77aefd7d4c694c844ac`
- requirements SHA-256: `8c9ceaf71ad2ed87bbf2141a399a582feb9a09e48e52ee740cf024d68bd54ab2`
- workflow run: `30682932931`

Result:

- verdict: `EXACT_REPRODUCTION`
- validator verdict: `APRIL_STREAM_DISCOVERY_CANDIDATE_SURVIVES_AUDIT`
- total members: 101
- annual counts: 1, 4, 1, 10, 8, 14, 34, 29 for 2019–2026
- exact committed 2022–2026 lookup: 95/95 timestamps
- missing preserved timestamps: 0
- additional timestamps: 0
- overall median orbital distance: 0.04398
- maximum significant-year medoid distance: 0.05044
- measurement-error clone pass fraction: 1.0
- hard IAU catalogue matches: 0

Durable evidence:

- `pilots/ghoststream/reconstruction/exact_recovered/EXACT_REPRODUCTION.md`
- `pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json`
- `.github/workflows/ghoststream-primary-reproduction-pr.yml`

## Reconciliation of the 103-member diagnostic

Before the original source was located, a later radiant-speed template was reconstructed from reports and returned 103 members. It omitted the original validator's frozen orbit-distance membership cuts and therefore was not the original analysis.

The mismatch was not hidden or tuned away. Running the actual recovered implementation regenerated the preserved 101-member annual counts and 95-member significant-year timestamp set exactly. The 103-member output is retained only as a robustness diagnostic.

## Resolution status by component

- [x] original core source code recovered and committed
- [x] file-level source provenance and SHA-256 manifest committed
- [x] environment, seeds, rules, and replicate counts recovered
- [x] official GMN monthly acquisition path operational
- [x] exact 101-member primary rerun
- [x] exact 95-event significant-year lookup rerun
- [x] primary validation, compactness, clone, and IAU-veto verdict reproduced
- [ ] internal GMN downstream null/bootstrap/activity/geographic/specification chain committed from a fresh clean rerun
- [ ] external CAMS/SonotaCo stages freshly rerun and reconciled
- [ ] parent-screen stage freshly rerun and reconciled
- [ ] code-inclusive manuscript and expert-review bundle rebuilt
- [ ] independent scientific/duplicate review completed

The fail-closed internal downstream workflow is:

`.github/workflows/ghoststream-recovered-downstream-reproduction.yml`

It commits regenerated evidence only after all preserved numerical and qualitative gates pass.

## Updated interpretation

The former statement that GhostStream's primary GMN result could not be computationally regenerated is no longer true. The central source-loss gap is resolved, and the preserved primary result has been independently regenerated from current official monthly GMN catalogues by the original unchanged implementation.

That does not make the candidate an officially recognized meteor shower, prove a parent body, supply absolute flux/ZHR, or eliminate the need for expert review. It also does not automatically validate every external archive claim until those recovered stages receive the same clean rerun-and-compare treatment.

## Current submission boundary

Continue scientific development and manuscript reconstruction. Keep journal submission and formal IAU MDC submission on hold until the remaining downstream/external stages are committed from clean runs and independent expert review is completed.
