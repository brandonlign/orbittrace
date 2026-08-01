# Internal analysis reproduction

The recovered analysis source from commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e` was used to repeat the main GMN analyses after event selection. The regenerated results matched the saved evidence.

- Primary selection: 101 total events and the same 95-event 2022–2026 lookup.
- Untouched 2022–2023 activity p-value: 1.857134 × 10⁻⁵.
- Untouched shifted-window p-value: 0.0175439.
- Untouched source/time-matched orbit-null p-value: 0.0001.
- Bootstrap: 95 members, 29 nights, 20,000 replicates for each resampling scheme.
- Drift result: RA and declination drift resolved; speed drift unresolved.
- Activity interval: solar longitude 35.902°–39.902°, pooled p = 6.507 × 10⁻¹⁹.
- Geographic member counts: 30, 22, and 44; largest cross-region medoid D = 0.04054.
- Sensitivity analysis: all 81 settings passed.

These reruns reproduce the internal analyses from the preserved source. The external-catalogue rerun is recorded in `../exact_external/`.
