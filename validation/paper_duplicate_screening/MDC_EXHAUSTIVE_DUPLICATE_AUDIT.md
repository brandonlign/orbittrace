# Exhaustive IAU MDC duplicate-screening audit for OrbitTrace

This paper-facing audit resolves the duplicate-screening concern without changing the OrbitTrace candidate, validation thresholds, or ACRF method.

## Frozen catalogue and all-solution screen

The comparison uses the fixed **2026-06-25 IAU Meteor Data Center snapshot**, SHA-256 `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`. The file contains **1,072 shower records and 2,174 submitted solutions**, including working-list and removed entries. Every parsable solution was screened; this was not a nearest-name or confirmed-shower-only search.

The duplicate rules were frozen before the comparison:

- OrbitTrace activity interval: solar longitude 32.901963°–40.901963°;
- if an MDC solution lacked a published activity interval, mean-epoch compatibility used a fixed ±8° fallback;
- drifted radiant separation ≤ 5°;
- geocentric-speed difference ≤ 5 km s⁻¹;
- `D_SH ≤ 0.15` for a hard match;
- a hard match required a complete orbit.

## Result

Across all **2,174** solutions:

- hard duplicate matches: **0**;
- timing/radiant/speed near matches: **0**;
- near matches hidden only by incomplete orbital elements: **0**.

The archived live rerun verdict is `NO_CURRENT_IAU_MDC_HARD_DUPLICATE` (workflow `30678572191`, artifact `8811375826`, artifact SHA-256 `d7a88515dcc97762812dd4df6b431a2c65805928969ad114b3636809254ae393`).

## Nearest alternatives

The table below lists the ten smallest complete-orbit `D_SH` alternatives from the exhaustive screen. These are descriptive nearest neighbours; none passes the fixed duplicate rule.

| IAU solution | Activity compatible | Drifted radiant sep. | ΔVg | D_SH | Why it fails |
|---|---:|---:|---:|---:|---|
| 149 NOP 004 | No | 9.59° | 1.00 km/s | 0.234 | timing, radiant and orbit |
| 1060 NSE 000 | No | 9.18° | 1.12 km/s | 0.247 | timing, radiant and orbit |
| 809 USG 000 | No | 8.29° | 1.51 km/s | 0.335 | timing, radiant and orbit |
| 352 ZOP 000 | No | 11.38° | 14.55 km/s | 0.378 | timing, radiant, speed and orbit |
| 55 ASC 002 | No | 11.14° | 0.59 km/s | 0.392 | timing, radiant and orbit |
| 140 XLI 000 | No | 6.16° | 3.69 km/s | 0.422 | timing, radiant and orbit |
| 149 NOP 002 | No | 11.99° | 8.51 km/s | 0.423 | timing, radiant, speed and orbit |
| 1061 EPO 000 | Yes | 13.60° | 1.98 km/s | 0.434 | radiant and orbit |
| 167 NSS 001 | No | 14.49° | 9.70 km/s | 0.465 | timing, radiant, speed and orbit |
| 358 TOP 000 | No | 11.47° | 0.11 km/s | 0.474 | timing, radiant and orbit |

No complete-orbit alternative is even inside the fixed `D_SH ≤ 0.15` hard-match boundary. The nearest complete orbit, NOP-004, has `D_SH = 0.23445`, begins at solar longitude 45° rather than overlapping OrbitTrace, and is separated by 9.59° in the drifted radiant at the candidate epoch.

## Population-level follow-up of the only serious neighbour

Because NOP-004 is the nearest complete catalogue orbit, it was also tested beyond its catalogue mean. The official NOP-004 observational lookup contains 567 rows. OrbitTrace spans solar longitude 32.958°–40.269° and NOP-004 45.007°–74.869°, leaving a 4.738° gap. The median OrbitTrace residual from the fitted NOP radiant trend is 11.233°, above the maximum residual within the NOP sample; all 95 OrbitTrace meteors exceed the NOP 99th-percentile radiant residual. In 100,000 bootstrap draws, none reached the observed separation. Among 118 publicly recoverable complete NOP orbits, the within-NOP 99th-percentile nearest-neighbour `D_SH` is 0.0878, while the closest OrbitTrace–NOP pair is 0.0929 and the median OrbitTrace-to-NOP distance is 0.1569.

Therefore the exhaustive catalogue screen and the dedicated population-level test agree: **OrbitTrace is not a duplicate of any solution in the frozen 2026-06-25 MDC snapshot.** This does not exclude a broader dynamical relationship to a known complex; it addresses the narrower duplicate-stream question.
