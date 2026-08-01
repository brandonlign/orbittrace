# Independent Shober EDMOND validation

**Verdict:** `SHOBER_EDMOND_PROVIDES_SPEED_SLOPE_ROBUST_ORBITAL_SUPPORT`

The open Zenodo file is a shower-removed EDMOND subset published independently of GhostStream. Its MD5 was verified before analysis. The unchanged frozen template was evaluated with both the original fitted velocity slope and a zero velocity slope.

- Zenodo record: **18664293**
- Record title: **Asteroidal non-shower meteor orbit subsets (CAMS, GMN, EDMOND, SonotaCo) used in Shober (2026, ApJ)**
- Publication date: **2026-02-16**
- License: **CC BY 4.0**
- File: `EDMOND_shober_2026_subset.csv`
- File size: **24,428,864 bytes**
- Verified MD5: `c5a3ee2c89cdff792bd114a39179350b`
- Raw rows: **30,341**
- Deduplicated valid rows: **29,812**
- Candidate members: **6**
- Years: **2014, 2016, 2017, 2022**
- Activity p with zero speed slope: **0.0120609**
- Activity odds ratio: **7.013**
- Median orbital D: **0.036695**
- q90 orbital D: **0.098150**
- Orbit-null p: **0.0001**
- Maximum member distance to refined GMN orbit: **0.106375**
- Same six members under fitted and zero speed-slope variants: **True**
- Exact-time overlap with prior CAMS/SonotaCo members: **none**

The result is supportive rather than a standalone catalogue pass. It narrowly misses the original activity threshold of p ≤ 0.01 and contains six rather than eight members. Its orbital evidence is independently decisive and is not sensitive to the unresolved speed drift.

The Shober EDMOND subset may contain observations contributed by networks that also appear in other historical compilations. It is therefore preserved as a separate robustness result and is not automatically counted as a fully independent third observing network.

## Later full linked-series audit

The unchanged zero-speed-drift template was later applied to all 23 usable annual ZIPs linked by the public EDMOND v6.01 page from 2001–2023. The linked 2024 ZIP remained unavailable. The full annual series selected exactly these same six UTC events and no additional events. Its one-sided activity p was 3.3785×10⁻⁴, the 48-position shifted-window p was 0.06122, and the 20,000-trial post-selection orbit-null p was 4.99975×10⁻⁵. This confirms the six-member extraction in the full usable public series without changing the interpretation: supportive, orbitally strong, provenance-limited evidence rather than an independent standalone pass.
