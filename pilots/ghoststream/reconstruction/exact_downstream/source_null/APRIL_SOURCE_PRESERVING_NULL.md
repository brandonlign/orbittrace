# April stream source-preserving null audit

**Verdict:** `APRIL_STREAM_SURVIVES_SOURCE_PRESERVING_NULL`

The activity test uses only Sun-centered radiant, ecliptic latitude, geocentric speed, and solar longitude. No orbit element or node is used to select the activity enhancement. Orbit coherence is tested separately afterward.

- Untouched years individually confirmed: **[2022, 2023]**
- Pooled untouched activity p: **1.85713e-05** (12-month threshold 0.000833333)
- Pooled untouched shifted-window p: **0.0175439**
- Pooled untouched orbit-null p: **0.0001**
- Expanded antihelion longitude range: **120° to 240°**

| Year | Core in window | Antihelion in window | Activity p | Shift p | Core orbit n | Orbit p | Confirmed |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 2019 | 1 | 95 | 0.3532 | 0.01754 | 1 | — | False |
| 2020 | 4 | 599 | 0.1319 | 0.01818 | 4 | — | False |
| 2021 | 1 | 287 | 0.3436 | 0.01786 | 1 | — | False |
| 2022 | 10 | 995 | 0.00397 | 0.01754 | 10 | 0.0001 | True |
| 2023 | 8 | 1426 | 0.002168 | 0.01754 | 8 | 0.0001 | True |
| 2024 | 14 | 2166 | 4.888e-05 | 0.01887 | 14 | 0.0001 | True |
| 2025 | 34 | 5098 | 9.42e-09 | 0.01786 | 34 | 0.0001 | True |
| 2026 | 29 | 4315 | 4.131e-06 | 0.01852 | 29 | 0.0001 | True |

A passing result removes the orbital-node circularity and broad antihelion-boundary objection. It still requires external network/catalog and literature validation before a discovery claim.
