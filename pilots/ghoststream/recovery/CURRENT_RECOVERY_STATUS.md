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
- Internal GMN downstream clean rerun: **in progress under fail-closed CI**
- Publication hold active: **yes, pending remaining downstream/external reruns and independent review**
- Formal MDC hold active: **yes**
- Prior expert bundle sendable: **no; it must be rebuilt from the recovered implementation**

## Authoritative recovery evidence

- `pilots/ghoststream/recovered_pipeline/SOURCE_MANIFEST.json`
- `pilots/ghoststream/reconstruction/exact_recovered/EXACT_REPRODUCTION.md`
- `pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json`
- `.github/workflows/ghoststream-primary-reproduction-pr.yml`
- `.github/workflows/ghoststream-recovered-downstream-reproduction.yml`

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

## Why an earlier reconstruction returned 103

A separately reconstructed later radiant-speed template omitted the original validator's frozen orbit-distance membership cuts. It was therefore a different analysis, not evidence that the official monthly catalogues or signal had changed. Running the recovered original source removed the discrepancy completely.

## Remaining executable gate

The current fail-closed workflow reruns the recovered:

1. source-preserving expanded-antihelion and source/time orbit-null audit;
2. 20,000-replicate year/night cluster bootstrap;
3. corrected March–May exposure-normalized activity profile;
4. three-way disjoint geographic replication; and
5. frozen 81-cell specification curve.

It compares each regenerated result against the preserved evidence boundary and commits the complete machine-readable output only if every check passes.

After the internal GMN chain, the remaining work is the clean external-archive/parent-screen reproduction and reconstruction of the manuscript and expert-review bundle.
