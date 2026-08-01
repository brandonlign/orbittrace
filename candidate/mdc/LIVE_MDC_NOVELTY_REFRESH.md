# Comparison with the IAU Meteor Data Center catalogue

I compared the candidate with the official IAU MDC full shower-data catalogue downloaded on 2026-08-01. The file identifies itself as version 2026-06-25.

## Catalogue used

- Shower records: 1,072
- Submitted solutions: 2,174
- Download size: 3,308,032 bytes
- SHA-256: `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`

Before matching, the file passed the expected count and schema checks.

## Matching rule

A shower was counted as a direct match only when all of the following were true:

1. its published activity interval overlapped the candidate interval of solar longitude 32.901963°–40.901963°, or its mean epoch was within 8° when bounds were unavailable;
2. its radiant, propagated to the candidate epoch when drift information was available, was within 5°;
3. its geocentric speed differed by no more than 5 km/s; and
4. its complete orbit had D_SH ≤ 0.15.

Solutions missing orbital elements were listed separately if their timing, radiant, and speed were close.

## Result

- Direct matches: 0
- Activity-compatible radiant/speed near matches: 0
- Near matches with incomplete orbits: 0

The nearest complete orbit was Northern May Ophiuchids solution 004:

- D_SH = 0.2344515;
- published activity interval = 45°–75°;
- mean epoch = 58.6°;
- drifted-radiant separation = 9.5879°; and
- speed difference = 1.0049 km/s.

Its speed is similar, but its timing, radiant, and orbit do not satisfy the comparison rule.

No current catalogue solution met the fixed criteria. A specialist should next compare the candidate with older literature, alternate coordinate conventions, removed solutions, and local shower lists.

The full machine-readable output is in `live_mdc_novelty_refresh_summary.json`.
