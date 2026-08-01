# GhostStream exact recovered reproduction

## Verdict

**EXACT REPRODUCTION PASSED.**

On 2026-08-01 UTC, GitHub Actions ran the recovered original validator directly from immutable `brandonlign/remotion-worker` commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`, with no parameter changes or source edits. The run regenerated the preserved primary GMN membership exactly.

- Original script: `ghoststream_novel/validate_april_candidate.py`
- Script SHA-256: `4a29b4c3bde528be2523b627f7e8a22d3c836f45981cc77aefd7d4c694c844ac`
- Requirements SHA-256: `8c9ceaf71ad2ed87bbf2141a399a582feb9a09e48e52ee740cf024d68bd54ab2`
- Python: 3.9.25
- Workflow run: `30682932931`
- Exact-evidence artifact: `8812912880`
- Artifact ZIP SHA-256: `7a507f3858fddbc181323b7838dd83f11e6224393b5045a6c3d69373e6f437d0`

## Exact membership result

The regenerated catalogue contained **101 total deduplicated members**, matching the preserved annual counts exactly:

| Year | Reproduced members |
|---:|---:|
| 2019 | 1 |
| 2020 | 4 |
| 2021 | 1 |
| 2022 | 10 |
| 2023 | 8 |
| 2024 | 14 |
| 2025 | 34 |
| 2026 | 29 |

The **95 events from the significant years 2022–2026 matched the committed MDC lookup timestamp-for-timestamp**:

- missing preserved timestamps: none
- additional timestamps: none
- lookup exact: true
- annual counts exact: true
- total count exact: true

Checksums:

- regenerated 101-member CSV: `e0e1ec7dca981cc656ac458ce5fce8c825a7f8914460e023808b966e7ca51e6b`
- regenerated validation JSON: `6cfee8a5651a3e739fd09d9b886426499b7d6bed4148362e6bff5f1bf9189a04`
- committed 95-member lookup: `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3`

## Reproduced scientific audit

The unchanged validator returned:

`APRIL_STREAM_DISCOVERY_CANDIDATE_SURVIVES_AUDIT`

- significant years: 2022, 2023, 2024, 2025, 2026
- untouched significant years: 2022 and 2023
- overall median orbital distance: 0.04398
- maximum significant-year medoid distance: 0.05044
- measurement-error clone pass fraction: 1.0
- hard IAU catalogue matches: 0

## Why the earlier 103-member run differed

The first reconstruction used a later drifted radiant-speed template and omitted the recovered validator's frozen orbit-distance membership cuts. It returned 103 members, missing two preserved timestamps and adding four others. That run is retained only as a robustness diagnostic. It was not an exact implementation of the original selection rule.

Running the actual recovered source resolved the discrepancy completely. The GMN monthly catalogues and preserved primary result are stable under the original frozen analysis.

## Updated claim boundary

The primary code-loss and exact-GMN-reproduction gap is resolved: the source trees are committed under `pilots/ghoststream/recovered_pipeline/`, file-level hashes are recorded in `SOURCE_MANIFEST.json`, and fail-closed CI reruns the exact validator from its immutable source commit.

This does **not** by itself make GhostStream an official discovery or automatically make the project ready for journal publication or formal IAU MDC submission. Independent scientific review, careful manuscript rebuilding from the recovered implementation, and review of the external-network evidence remain required.
