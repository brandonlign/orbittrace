# Corrected exposure-normalized activity profile

March, April, and May catalogues were loaded for every year, removing the April-month boundary artifact in the first run. Bins with fewer than 40 simultaneous non-core antihelion meteors are unavailable rather than assigned a rate.

This is a relative source-normalized activity profile, not an absolute flux or ZHR estimate.

- Years: **2022, 2023, 2024, 2025, 2026**
- Bin width: **0.50°**
- Baseline rate: **1.604 per 1000 antihelion-background meteors**
- Peak solar longitude: **38.652°**
- Peak counts: **15 stream / 1021 background**
- Peak relative rate: **15.17 per 1000 background**
- Background-subtracted weighted center: **35.421°**
- FWHM interval: **[38.401963, 38.901963]°**
- FWHM width: **0.50°**
- Aggregate inside-versus-baseline p: **6.50745e-19**

## Year-level tests

| Year | Stream inside | Background inside | Stream baseline | Background baseline | p |
|---:|---:|---:|---:|---:|---:|
| 2022 | 10 | 1086 | 6 | 2239 | 0.013947 |
| 2023 | 8 | 1525 | 3 | 4064 | 0.0022412 |
| 2024 | 14 | 2181 | 15 | 10410 | 0.00012599 |
| 2025 | 35 | 5277 | 15 | 9267 | 1.3777e-06 |
| 2026 | 29 | 4471 | 25 | 14366 | 2.0668e-06 |

## Leave-one-year-out stability

| Omitted | Peak delta | Weighted center delta | FWHM | Aggregate p |
|---:|---:|---:|---:|---:|
| 2022 | 1.75° | -1.15° | 0.50° | 2.2994e-17 |
| 2023 | 1.75° | -1.76° | 0.50° | 5.8205e-17 |
| 2024 | 0.75° | -1.50° | 1.50° | 2.9336e-15 |
| 2025 | 0.25° | -1.56° | 2.00° | 2.167e-13 |
| 2026 | 1.75° | -0.30° | 0.50° | 4.7721e-14 |

The profile remains conditional on catalogue-level detection and the expanded antihelion denominator. Weather, limiting magnitude, radiant elevation, and collecting area are not modeled explicitly.
