# Exhaustive IAU MDC duplicate-screening audit for OrbitTrace

This paper-facing audit resolves the duplicate-screening concern without changing the OrbitTrace candidate, validation thresholds, or ACRF method.

## Current catalogue and all-solution screen

The official IAU Meteor Data Center text catalogue reports **Last update: 2026-08-14 20:00 UTC**. The downloaded file is 1,545,850 bytes with SHA-256 `418365d3f005bc6a2ead6e8bc0548dafdc4cc378843c8c2bf351f79af5293dbf` and contains **2,179 submitted solution rows**.

The duplicate rules were held fixed from the earlier audit:

- OrbitTrace activity interval: solar longitude 32.901963°–40.901963°;
- if a solution lacks a published activity interval, mean-epoch compatibility uses a fixed ±8° fallback;
- drifted radiant separation ≤ 5°;
- geocentric-speed difference ≤ 5 km s⁻¹;
- `D_SH ≤ 0.15` for a hard match;
- a hard match requires a complete orbit.

The candidate radiant and speed are propagated to each catalogue solution's mean solar longitude using the fitted OrbitTrace drifts before radiant/speed comparison. Southworth–Hawkins distance is then evaluated for complete orbits.

## Completeness audit

Of the 2,179 submitted rows, **2,150** contain solar longitude, Sun-centred radiant longitude, radiant latitude and geocentric speed and therefore permit the complete timing/radiant/speed screen. **1,888** of these also contain a complete five-element orbit for `D_SH`.

The remaining 29 rows were inspected separately rather than silently discarded. Only one is timing-compatible with OrbitTrace: alpha-Virginids solution AVB-003 at mean solar longitude 32.5°. It lacks a geocentric speed, but its drifted radiant is **49.09°** from OrbitTrace, so it fails the fixed 5° radiant condition by a wide margin regardless of the missing speed/orbit fields. None of the other incomplete rows is activity-compatible.

## Result

Across the **entire 2,179-row current catalogue**:

- hard duplicate matches: **0**;
- timing/radiant/speed near matches among parameter-complete rows: **0**;
- plausible matches hidden by incomplete fields: **0**.

The result is unchanged from the earlier 2026-06-25 audit even though the catalogue has since been updated.

## Nearest complete-orbit alternatives

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

No complete-orbit alternative is inside the fixed `D_SH ≤ 0.15` boundary. The nearest remains NOP-004 at `D_SH = 0.23445`; its published activity begins at solar longitude 45° and its drifted radiant is 9.59° from OrbitTrace.

## Population-level follow-up of NOP-004

The official NOP-004 observational lookup contains 567 rows. OrbitTrace spans solar longitude 32.958°–40.269° and NOP-004 45.007°–74.869°, leaving a 4.738° gap. The median OrbitTrace residual from the fitted NOP radiant trend is 11.233°, above the maximum residual within the NOP sample; all 95 OrbitTrace meteors exceed the NOP 99th-percentile radiant residual. In 100,000 bootstrap draws, none reached the observed separation. Among 118 publicly recoverable complete NOP orbits, the within-NOP 99th-percentile nearest-neighbour `D_SH` is 0.0878, while the closest OrbitTrace–NOP pair is 0.0929 and the median OrbitTrace-to-NOP distance is 0.1569.

Therefore the current exhaustive catalogue screen and the dedicated population-level test agree: **OrbitTrace is not a duplicate of any solution in the 2026-08-14 MDC catalogue.** This does not exclude a broader dynamical relationship to a known complex.
