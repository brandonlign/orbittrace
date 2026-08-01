# Uniform zero-speed-drift external archive synthesis

**Verdict:** `EXTERNAL_EVIDENCE_STABLE_WITH_ZERO_SPEED_DRIFT_AND_EDMOND_EXTENSION`

The clustered year/night bootstrap did not resolve a geocentric-speed drift, so every external archive was rerun with `dVg/dλ⊙ = 0`. All radiant centers, radiant drift terms, dispersions, activity bounds, and orbital rules remained frozen.

## Primary cross-network evidence: CAMS + SonotaCo

- Members: **10**
- Years: **2011, 2012, 2022, 2023, 2025**
- Activity p: **1.6218439 × 10⁻⁴**
- Shifted-window p: **0.0204082**
- Median orbital D: **0.048791**
- q90 orbital D: **0.077081**
- Orbit-null p: **5 × 10⁻⁵**
- Medoid distance to refined GMN orbit: **0.017231**
- Frozen family gate: **passed**

This is the primary external result because CAMS and SonotaCo provide distinct historical observing/reduction contexts from the GMN discovery sample. The pooled test remains explicitly post-hoc because it was motivated by the two sparse archive-specific outcomes.

## Extended exploratory evidence: adding the Shober EDMOND subset

- Members: **16**
- Years: **2011, 2012, 2014, 2016, 2017, 2022, 2023, 2025**
- Member counts:
  - CAMS 2011: 2
  - CAMS 2012: 4
  - Shober-EDMOND 2014: 1
  - Shober-EDMOND 2016: 2
  - Shober-EDMOND 2017: 2
  - Shober-EDMOND 2022: 1
  - SonotaCo 2022: 2
  - SonotaCo 2023: 1
  - SonotaCo 2025: 1
- Activity p: **1.4638728 × 10⁻⁶**
- Shifted-window p: **0.0204082**
- Median orbital D: **0.048433**
- q90 orbital D: **0.087006**
- Orbit-null p: **5 × 10⁻⁵**
- Medoid distance to refined GMN orbit: **0.017231**
- Exact cross-source UTC duplicate groups: **0**

The EDMOND extension is supporting, explicitly exploratory evidence. EDMOND is a compiled historical archive and may share contributing networks or reduction ancestry with other video-meteor compilations. The absence of exact UTC duplicates prevents simple double-counting of the same selected events, but the three archive labels must not be interpreted as three fully independent instruments.

## Interpretation

The independent-archive result is not an artifact of the fitted GMN speed slope. Setting that unresolved slope to zero leaves the primary CAMS+SonotaCo evidence unchanged and preserves all 16 external radiant-time members in the extended audit. Orbit was not used to select members; their orbital compactness was tested only afterward against source- and time-matched null samples.
