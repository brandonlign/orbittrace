# IAU MDC duplicate screen

OrbitTrace was compared with every submitted solution in the IAU Meteor Data Center catalogue downloaded on 2026-08-14 at 20:00 UTC. The file contains 2,179 solution rows and has SHA-256 `418365d3f005bc6a2ead6e8bc0548dafdc4cc378843c8c2bf351f79af5293dbf`.

## Screen

A hard match requires all of the following:

- compatible activity timing (or a fixed ±8° fallback when no interval is published);
- drifted radiant separation ≤ 5°;
- geocentric-speed difference ≤ 5 km s⁻¹;
- `D_SH ≤ 0.15`;
- a complete orbit.

The OrbitTrace radiant and speed are propagated to each solution's mean solar longitude before the comparison.

Of the 2,179 catalogue rows, 2,150 contain the timing, radiant, and speed fields needed for that part of the screen. 1,888 also contain a complete five-element orbit. The remaining 29 rows were checked separately. Only AVB-003 is timing-compatible, but its drifted radiant is 49.09° from OrbitTrace and it has no published geocentric speed.

**Result: 0 hard duplicates, 0 timing/radiant/speed near matches, and 0 plausible matches hidden by incomplete fields.** The same conclusion was obtained with the 2026-06-25 catalogue snapshot.

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

NOP-004 is the nearest complete-orbit solution at `D_SH = 0.23445`. Its published activity begins at solar longitude 45°, after OrbitTrace, and its drifted radiant is 9.59° away.

## NOP-004 population comparison

The supported OrbitTrace interval used in Figure 3A is 35.902°–39.902°. For the population-level comparison, the observed canonical span is 32.958°–40.269° and the NOP-004 span is 45.007°–74.869°, leaving a 4.738° gap.

The median OrbitTrace residual from the fitted NOP radiant trend is 11.233°, larger than the maximum residual inside the NOP sample, and all 95 OrbitTrace meteors lie above the NOP 99th-percentile radiant residual. None of 100,000 bootstrap draws reached the observed separation.

Among 118 publicly recoverable complete NOP orbits, the within-NOP 99th-percentile nearest-neighbour `D_SH` is 0.0878. The closest OrbitTrace–NOP pair is 0.0929 and the median OrbitTrace-to-NOP distance is 0.1569.

Under this catalogue screen, OrbitTrace is not a duplicate of NOP-004 or any other submitted MDC solution. This test does not rule out a broader dynamical relationship to a known complex.
