# GhostStream recovery status

Updated: 2026-08-01

## Current state

- Original core GMN analysis source recovered: **yes**
- Recovery source: **immutable `brandonlign/remotion-worker` PR commits**
- Recovery/discovery tree preserved: **13 files from commit `4175e5187fcc6faf3d1befb099a9e35be96850f2`**
- Novel-search/downstream tree preserved: **35 files from commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`**
- File-level SHA-256 manifest committed: **yes**
- Exact original primary validator rerun: **passed**
- Exact 101-member annual counts: **passed**
- Exact committed 95-event 2022–2026 timestamp set: **passed**
- Missing preserved timestamps: **0**
- Additional timestamps: **0**
- Original validator verdict: **`APRIL_STREAM_DISCOVERY_CANDIDATE_SURVIVES_AUDIT`**
- Internal GMN downstream clean rerun: **passed and committed**
- External CAMS/SonotaCo clean rerun: **passed and committed**
- Historical v2 method-control gate: **`NO_GO_DEGENERATE_PARENT_CLUSTER` preserved**
- Corrected independent-year 2024 method controls: **passed 3/3**
- Actual January–July 2026 blind-discovery matrix: **running from recovered source**
- Current JPL parent screen: **passed; zero objects at D ≤ 0.15**
- Publication hold active: **yes, pending blind-lineage result, final package build, and independent review**
- Formal MDC hold active: **yes**
- Prior expert bundle sendable: **no; it must be rebuilt from the recovered implementation**

## Authoritative recovery evidence

- `pilots/ghoststream/recovered_pipeline/SOURCE_MANIFEST.json`
- `pilots/ghoststream/reconstruction/exact_recovered/EXACT_REPRODUCTION.md`
- `pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json`
- `pilots/ghoststream/reconstruction/exact_downstream/downstream_reproduction.json`
- `pilots/ghoststream/reconstruction/exact_downstream/DOWNSTREAM_REPRODUCTION.md`
- `pilots/ghoststream/reconstruction/exact_external/external_reproduction.json`
- `pilots/ghoststream/reconstruction/exact_external/EXTERNAL_REPRODUCTION.md`
- `pilots/ghoststream/reconstruction/exact_method_controls_v3/method_controls_v3.json`
- `pilots/ghoststream/reconstruction/exact_method_controls_v3/METHOD_CONTROLS_V3.md`

## Exact primary result

The unchanged recovered `validate_april_candidate.py` was run from immutable commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e` under Python 3.9.25 and the recovered pinned direct dependencies.

It regenerated:

- 2019: 1 member
- 2020: 4
- 2021: 1
- 2022: 10
- 2023: 8
- 2024: 14
- 2025: 34
- 2026: 29
- total: 101

The 95 events from 2022–2026 matched the committed lookup timestamp-for-timestamp.

## Exact internal downstream reproduction

The recovered source reran and matched the preserved evidence boundary for:

1. source-preserving expanded-antihelion and source/time orbit-null audit;
2. 20,000-replicate year/night cluster bootstrap;
3. corrected March–May exposure-normalized activity profile;
4. three-way disjoint geographic replication; and
5. frozen 81-cell specification curve.

Key regenerated results:

- untouched pooled activity p = `1.857134041807409e-05`
- untouched shifted-window p = `0.017543859649122806`
- untouched orbit-null p = `0.0001`
- bootstrap: 95 members, 29 nights, 20,000 replicates per scheme
- RA and Dec drift exclude zero; speed drift does not
- activity core: solar longitude 35.902°–39.902°
- geographic members: 30 / 22 / 44
- maximum cross-region medoid D = `0.040536830930146595`
- specification curve: 81/81 eligible cells passed

## Exact external reproduction

The recovered external scripts regenerated the preserved member sets and statistics:

- CAMS: 6 members in 2011–2012; supportive but not individually decisive
- SonotaCo: 4 members in 2022, 2023, and 2025; supportive but below the minimum count
- pooled CAMS+SonotaCo synthesis: exact preserved 10-event ID set
- pooled activity p = `0.0001621843884718582`
- pooled orbit-null p = `5e-05`
- pooled medoid distance to the refined GMN orbit = `0.017230503215407457`

The current JPL screen evaluated 729 valid broad-compatible orbits:

- objects at D ≤ 0.15: 0
- objects at D ≤ 0.25: 2
- nearest: 2023 HJ7 at D = 0.15939456567933025
- nearest orbit condition code: 8
- nearest observational arc: 11 days
- parent claimed: no

EDMOND remains provenance-limited supplementary evidence. The advertised 2024 attachment is still unavailable and the surviving linked annual files are not a complete v6.01 release.

## Method-control reconciliation

The unchanged recovered v2 method gate individually recovered all three untouched named showers and the weak-stream injection gate passed, but its aggregate verdict was `NO_GO_DEGENERATE_PARENT_CLUSTER`. That historical verdict remains preserved.

The no-go arose because the v2 30% largest-cluster ceiling included the real target cluster. Eta Aquariids itself occupied more than 30% of its holdout sample, making full ETA recovery mathematically incompatible with the rule.

A correction was frozen before inspecting independent 2024 seasons. It retained the exact HDBSCAN setting, recovery thresholds, hidden labels, and 30% threshold, but applied the ceiling to the largest non-target cluster—the unrelated-cluster failure mode the rule was intended to detect.

The corrected prospective holdout passed:

| Control | Precision | Recall | F1 | Largest non-target cluster |
|---|---:|---:|---:|---:|
| Lyrids | 0.821 | 1.000 | 0.902 | 0.130 |
| Eta Aquariids | 0.917 | 1.000 | 0.957 | 0.156 |
| Southern Delta Aquariids | 0.864 | 1.000 | 0.927 | 0.140 |

All three values were below the unchanged 0.30 ceiling. This resolves the specific v2 gate-design contradiction without rewriting its historical outcome.

## Why an earlier reconstruction returned 103

A separately reconstructed later radiant-speed template omitted the original validator's frozen orbit-distance membership cuts. It was therefore a different analysis, not evidence that the official monthly catalogues or signal had changed. Running the recovered original source removed the discrepancy completely.

## Remaining work

1. complete and preserve the actual January–July 2026 blind-discovery matrix from `run_month_year_v3.py`;
2. integrate the blind and corrected method-control evidence into the recovered MDC package audit and code-inclusive expert bundle;
3. obtain independent scientific and duplicate review; and
4. keep journal and formal MDC submission blocked until those steps pass.
