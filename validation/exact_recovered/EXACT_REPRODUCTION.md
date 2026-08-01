# Primary reproduction

The candidate validator was recovered from immutable commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e` and rerun with the same source and parameters. It reproduced the primary GMN selection exactly.

## Membership

| Year | Members |
|---:|---:|
| 2019 | 1 |
| 2020 | 4 |
| 2021 | 1 |
| 2022 | 10 |
| 2023 | 8 |
| 2024 | 14 |
| 2025 | 34 |
| 2026 | 29 |

The total was 101 deduplicated events. The 95 events from 2022–2026 matched the committed MDC lookup table timestamp for timestamp. The recovered set matched all 95 preserved timestamps exactly.

## Reproduced values

- Significant years: 2022–2026
- Overall median orbital distance: 0.04398
- Largest significant-year medoid distance: 0.05044
- Measurement-error pass fraction: 1.0
- Matching IAU catalogue solutions: 0

## Run record

- Python: 3.9.25
- Workflow run: `30682932931`
- Source script SHA-256: `4a29b4c3bde528be2523b627f7e8a22d3c836f45981cc77aefd7d4c694c844ac`
- Artifact ZIP SHA-256: `7a507f3858fddbc181323b7838dd83f11e6224393b5045a6c3d69373e6f437d0`
- Regenerated 101-member CSV SHA-256: `e0e1ec7dca981cc656ac458ce5fce8c825a7f8914460e023808b966e7ca51e6b`
- Committed 95-member lookup SHA-256: `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3`

An earlier reconstruction returned 103 events because it used a later radiant/speed template and omitted the original orbit-distance membership cuts. Running the recovered validator resolved the difference and restored the exact 101-event set.

The published event set can be regenerated from the recovered implementation.
