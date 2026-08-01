# GhostStream primary-pipeline reconstruction protocol

**Status:** Frozen before inspecting any reconstruction result.

**Purpose:** Independently rebuild the missing source-to-result GMN analysis from the official live GMN catalogue and compare it with the preserved GhostStream evidence package. This is a reproduction attempt, not an effort to tune a new pipeline until it matches old numbers.

## Non-negotiable rule

No threshold in this document may be changed because a reconstruction result misses the preserved result. Any correction required by an implementation error must be documented in a separate discrepancy log with the old code, corrected code, reason, and effects.

## Official source

The reconstruction uses the public Global Meteor Network Data Explorer and its underlying official GMN tables:

- `meteor`
- `participating_station`
- `meteor_sigma` when uncertainty cloning is reconstructed

Every query, response byte count, response SHA-256, access time, and returned row count must be recorded. Source records used in a result must be committed or retained as checksum-locked artifacts.

## Frozen central-quality rules

A trajectory is eligible only when all of the following are true:

1. `shower_iau_no = -1` (GMN sporadic label);
2. at least two participating stations;
3. median trajectory-fit error no greater than 180 arcsec;
4. finite geocentric radiant, geocentric speed, and orbit fields;
5. geocentric speed from 5 through 75 km/s, inclusive.

Exact-second duplicate trajectory solutions are collapsed before candidate selection. The retained solution is ranked by:

1. lowest median fit error;
2. highest participating-station count;
3. lexicographically smallest unique trajectory identifier as a deterministic final tie-break.

The tie-break in item 3 is a reconstruction-only determinism rule and must be reported if it ever decides a retained row.

## Frozen candidate template

Reference solar longitude:

- `36.901963 deg`

Radiant and speed at the reference epoch:

- Sun-centered geocentric ecliptic longitude: `-149.3763247 deg`, equivalent to `210.6236753 deg` on `[0, 360)`;
- geocentric ecliptic latitude: `7.3230377 deg`;
- geocentric speed: `37.641692 km/s`.

Linear drift per degree of solar longitude:

- Sun-centered longitude: `-0.1029483 deg/deg`;
- latitude: `-0.0230546 deg/deg`;
- speed: `-0.0293492 km/s/deg` for the primary GMN reproduction.

Residual scales:

- longitude: `0.7369 deg`;
- latitude: `0.6250 deg`;
- speed: `1.1596 km/s`.

For each eligible trajectory, the squared standardized radiant-speed score is

`S = (delta_lon / 0.7369)^2 + (delta_lat / 0.6250)^2 + (delta_v / 1.1596)^2`.

The central core requires `S <= 9`. The central activity interval requires circular solar-longitude distance from `36.901963 deg` no greater than `4 deg`.

No orbital element enters this member selection.

## Frozen broad-source null

The expanded antihelion source contains eligible trajectories satisfying:

- Sun-centered geocentric ecliptic longitude from `120 deg` through `240 deg`;
- absolute geocentric ecliptic latitude no greater than `35 deg`;
- geocentric speed from `15` through `50 km/s`.

Within each year, the one-sided Fisher/hypergeometric activity test compares:

| | Core | Non-core |
|---|---:|---:|
| Inside the ±4 deg activity interval | a | b |
| Outside the activity interval | c | d |

The pooled untouched-year result combines the 2022 and 2023 cells before computing the same one-sided test.

Orbit is tested only after radiant-speed-time selection.

## Preserved values tested without tuning

### Membership

Expected frozen-template counts:

| Year | Expected members |
|---:|---:|
| 2019 | 1 |
| 2020 | 4 |
| 2021 | 1 |
| 2022 | 10 |
| 2023 | 8 |
| 2024 | 14 |
| 2025 | 34 |
| 2026 | 29 |

Expected total: `101`.

The 95 selected records from 2022 through 2026 must be compared by exact UTC second against `april_stream/mdc/GhostStream_April_95_GMN_lookup.csv`.

### Activity

Expected annual one-sided activity p-values:

- 2019: `0.3532`
- 2020: `0.1319`
- 2021: `0.3436`
- 2022: `0.003970`
- 2023: `0.002168`
- 2024: `4.888e-5`
- 2025: `9.42e-9`
- 2026: `4.131e-6`

Expected pooled 2022–2023 p-value: `1.857134041807409e-5`.

P-values are compared numerically and by scientific conclusion. Small differences can result from source-catalogue revisions; every difference must be quantified rather than hidden.

### Post-selection orbit

Reference robust orbit:

- `q = 0.079202 AU`
- `e = 0.946296`
- `i = 24.709376 deg`
- `omega = 333.493819 deg`
- `Omega = 37.937477 deg`

Preserved selected-sample diagnostics:

- median Southworth-Hawkins distance: `0.0439834`;
- 90th percentile distance: `0.0923211`;
- maximum significant-year medoid separation: `0.0504401`.

## Reconstruction stages

1. **Source reconnection:** Match all 95 preserved lookup rows to official live GMN source records and recover full quality, orbit, station, and uncertainty metadata.
2. **Frozen-template reproduction:** Apply the rules above to 2019–2026 and test membership, untouched-year activity, and post-selection orbit.
3. **Primary robustness:** Rebuild shifted windows, source/time-matched orbital nulls, measurement-error clones, year/night bootstrap, geographic split, March–May activity profile, and the 81-cell specification curve.
4. **Blind-discovery reconstruction:** Rebuild positive controls, injection tests, known-shower vetoes, and month-by-month blind candidate generation. This is required to reproduce the discovery process, but it must remain analytically separate from the frozen-template confirmation.
5. **External archives:** Rebuild original CAMS and SonotaCo acquisition and frozen selection. The already committed EDMOND evaluator remains a later bounded reproducible stage.

## Verdict labels

- `EXACT_REPRODUCTION`: the source rows, membership, and statistics agree within declared numerical precision.
- `SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT`: live catalogue revisions produce documented row/value changes, but the frozen test reaches the same scientific conclusion.
- `PARTIAL_REPRODUCTION`: only some primary claims can be regenerated.
- `FAILED_REPRODUCTION`: the frozen analysis does not regenerate the candidate or its decisive validation.
- `BLOCKED`: official source access or missing required fields prevents the test.

No publication or formal IAU MDC submission hold is lifted until stages 1–3 pass and stage 4 has a fully committed, auditable implementation.