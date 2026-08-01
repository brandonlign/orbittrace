# GhostStream January–July 2026 blind rediscovery

**Verdict:** `EXACT_2026_BLIND_REDISCOVERY`

The recovered drift-aware month/year scanner was run for every month from January through July 2026. It used 2025 and 2024 as the two untouched validation years. The original arbitrary-year wrapper crashed after completing April's scientific gate because one report/CSV lookup remained hardcoded to the 2023 validation key. The original wrapper remains preserved unchanged; the rerun used a separately documented minimal year-key/reporting repair that did not change catalogue acquisition, clustering, candidate ranking, validation, orbital tests, clone trials, or IAU matching.

## Matrix result

| Month | Quality sporadics | Clusters | Prevalidation candidates | Full-gate survivors |
|---|---:|---:|---:|---:|
| 2026-01 | 39,867 | 475 | 0 | 0 |
| 2026-02 | 37,762 | 440 | 0 | 0 |
| 2026-03 | 51,173 | 568 | 0 | 0 |
| 2026-04 | 52,506 | 600 | 2 | 1 |
| 2026-05 | 52,102 | 581 | 0 | 0 |
| 2026-06 | 52,647 | 607 | 1 | 0 |
| 2026-07 | 65,478 | 689 | 1 | 0 |

- Months scanned: **7**
- Total full-gate survivors: **1**
- Additional non-April survivors: **0**
- IAU solutions parsed: **2,143** in every monthly run

## April survivor

- Blind cluster: **429**
- 2026 discovery members: **26**
- Frozen discovery center: `[-149.297555, 7.450070, 37.422240, 36.901963]`
- Regenerated center distance from frozen record: **2.86 × 10⁻¹⁵** in the verifier's normalized coordinates
- Orbit medoid: `[e=0.950783, q=0.073747 AU, i=25.286643°, ω=334.338586°, Ω=37.363391°]`
- Median orbital D: **0.037988**
- q90 orbital D: **0.094446**
- Source/time orbit-null p: **0.005**
- Clone trials: **500**
- Clone pass fraction: **1.000**

### Untouched 2025 validation

- Members: **36**
- Nights: **7**
- Participating stations: **104**
- Activity/local-null p: **0.002**
- Median orbital D: **0.041608**
- Passed: **yes**

### Untouched 2024 validation

- Members: **14**
- Nights: **4**
- Participating stations: **44**
- Activity/local-null p: **0.002**
- Median orbital D: **0.051316**
- Passed: **yes**

### Catalogue veto

The nearest automated IAU comparison was phi-Ophiuchids (`USG`), but it was inactive at the candidate epoch and did not match:

- activity-epoch separation from mean: **13.798°** solar longitude
- drifted sky separation: **3.072°**
- speed difference: **1.692 km/s**
- orbital D: **0.3672**
- matched: **false**

The later checksum-locked full MDC audit remains the authoritative current novelty comparison.

## Provenance

- Recovered source commit: `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`
- Discovery entrypoint: `ghoststream_novel/run_month_year_v3.py`
- Wrapper repair commit: `38582b848b0ba730a292e48116a476c04df221d0`
- Original wrapper SHA-256: `9681b11f97546589689f39af9e2ebe956185a5956de58d37538a1bd1e74b78ed`
- Repaired wrapper SHA-256: `94f04270aca54d1056841390fd6bbb0cdfc25187c065c6bf886307c8effab217`
- Worker PR: `brandonlign/remotion-worker#59`
- Workflow run: `30685257519`
- Job: `91329624924`
- Artifact: `8813808115`
- Artifact ZIP SHA-256: `60a175bd766ae02294d8469d22d22e59b7536378a7d0d79654835d536f158fcc`

## Claim boundary

The actual January–July 2026 blind discovery lineage is reproduced: April was the only month with a full-gate survivor, and that survivor independently passed 2025 and 2024 validation, orbital compactness, clone stability, and the automated IAU veto.

The rerun is not described as an entirely unchanged execution of the original arbitrary-year wrapper. The wrapper required a minimal, separately preserved reporting/year-key repair after the scientific decision had already completed. No scientific threshold or algorithm was changed.

This result supports the discovery lineage of an uncatalogued candidate. It is not official IAU recognition and does not replace independent expert duplicate-shower review.
