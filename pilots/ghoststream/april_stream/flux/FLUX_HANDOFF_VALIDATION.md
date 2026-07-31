# GhostStream flux handoff validation

Validation date: 2026-07-31

## Verdict

**PASS — the RMS custom-shower generator and Level 2 preflight validator executed successfully in both local and GitHub Actions tests.**

This validates the handoff tooling. It does not provide an absolute flux measurement because the required consented GMN Level 2 station-night data have not been supplied.

## Custom shower-catalogue generator

The generator was executed at all required mass-index sensitivity values:

| Mass index s | Population index r |
|---:|---:|
| 1.7 | 1.90546072 |
| 1.8 | 2.08929613 |
| 1.9 | 2.29086765 |
| 2.0 | 2.51188643 |
| 2.1 | 2.75422870 |

For every value, the generated candidate row:

- contained exactly 21 pipe-delimited RMS flux-shower fields;
- used the internal code `GSA`;
- preserved activity bounds 35.902°–39.902°;
- preserved the reference epoch 38.652°;
- converted mass index to population index using `r = 10^((s-1)/2.5)`; and
- retained the warning that its code, ZHR, and activity-shape fields are operational placeholders rather than official or measured values.

## Level 2 preflight validator

Three synthetic station-night fixtures were tested:

1. A complete raw-data directory containing `FTPdetectinfo`, station config, platepar, mask, CALSTARS, and FF data was classified as `READY_RAW_RECOMPUTE`.
2. A complete metadata route containing `FTPdetectinfo`, config, recalibrated platepars, mask, flux time intervals, sensor characterization, and collection-area metadata was classified as `READY_PRECOMPUTED_METADATA`.
3. An intentionally incomplete directory containing only `FTPdetectinfo` was classified as `INCOMPLETE` and caused the validator to return its documented nonzero status.

## Independent execution

The test was reproduced in GitHub Actions on the trusted compute repository:

- workflow run: `30673545661`;
- job: `test-flux-handoff`;
- compile step: pass;
- five-value catalogue-generation grid: pass;
- three-class preflight fixture test: pass;
- artifact SHA-256: `7f68843386c9ca7509b4577d4783a059c44c299f820dbf2ca3ec6157814582bd`.

## Remaining blocker

The physical flux computation still requires either:

- an internal GMN run using all eligible station nights, including valid zero-detection nights; or
- consented Level 2 station-night directories that pass the preflight validator.

The public Level 3 trajectory catalogue cannot supply an unbiased time-area-product denominator.
