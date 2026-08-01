# Results

A blind search of GMN trajectories found one late-April structure that remained convincing after the candidate definition was fixed and tested in other years. The project refers to it internally as `GhostStream-April-36.9`.

## Candidate at a glance

| Quantity | Result |
|---|---:|
| Significant GMN years | 2022–2026 |
| Confirmed GMN members | 95 |
| Total selected GMN members, 2019–2026 | 101 |
| Untouched confirmation years | 2022 and 2023 |
| Pooled untouched-year activity p-value | 1.857 × 10⁻⁵ |
| Shifted-window p-value | 0.01754 |
| Source/time-matched orbit-null p-value | 0.0001 |
| Measurement-error trials passed | 1,000 / 1,000 |
| Geographic groups passing | 3 / 3 |
| Sensitivity-grid settings passing | 81 / 81 |
| Official MDC solutions checked | 2,174 |
| Matching official solutions | 0 |

The evidence supports a recurring meteor stream. The remaining scientific question is whether specialists agree that it is distinct from every known minor shower and from narrower structure within the antihelion source.

## Discovery and recurrence

The search used public GMN trajectories labelled as sporadic. Meteors were represented by Sun-centered radiant longitude, radiant latitude, geocentric speed, and solar longitude. HDBSCAN generated candidate clusters, and candidates then had to pass requirements for observing nights, participating stations, compactness, orbital coherence, split-sample recurrence, and separation from known showers.

A January–July 2026 blind rerun independently selected April as the only full-gate survivor. The fixed April definition was then evaluated in earlier years.

| Year | Selected members | Activity p-value | Orbit-null p-value | Individually significant |
|---:|---:|---:|---:|:---:|
| 2019 | 1 | 0.3532 | — | No |
| 2020 | 4 | 0.1319 | — | No |
| 2021 | 1 | 0.3436 | — | No |
| 2022 | 10 | 0.003970 | 0.0001 | Yes |
| 2023 | 8 | 0.002168 | 0.0001 | Yes |
| 2024 | 14 | 4.888 × 10⁻⁵ | 0.0001 | Yes |
| 2025 | 34 | 9.42 × 10⁻⁹ | 0.0001 | Yes |
| 2026 | 29 | 4.13 × 10⁻⁶ | 0.0001 | Yes |

The pooled 2022–2023 test was reserved as an untouched confirmation. It gave an activity p-value of 1.857 × 10⁻⁵ after the twelve-month familywise rule, a shifted-window p-value of 0.01754, and a source/time-matched orbit-null p-value of 0.0001.

## Mean solution

The robust solution used for matching is evaluated near solar longitude 36.902°.

| Parameter | Value |
|---|---:|
| Sun-centered ecliptic longitude | −149.376° |
| Geocentric ecliptic latitude | +7.323° |
| Approximate geocentric RA | 247.06° |
| Approximate geocentric Dec | −14.22° |
| Geocentric speed | 37.642 km/s |
| Perihelion distance, q | 0.079202 AU |
| Eccentricity, e | 0.946296 |
| Inclination, i | 24.709° |
| Argument of perihelion, ω | 333.494° |
| Encounter node, Ω | 37.937° |
| Semimajor axis, a | 1.475 AU |
| Orbital period | 1.79 years |
| Tisserand parameter with respect to Jupiter | 3.84 |

The 95-member arithmetic mean prepared for the draft MDC record is slightly different because it is a direct unweighted mean of the submitted rows. Both forms are kept, with their separate uses explained in the manuscript and MDC folder.

## Timing and uncertainty

A March–May profile normalized stream-core counts by the simultaneous non-core antihelion population. The supported activity interval is solar longitude 35.902°–39.902°. The highest half-degree bin occurred at 38.652°, but that exact peak shifted when individual years were removed, so the four-degree interval is the more stable description.

A 20,000-replicate bootstrap resampled years and observing nights. The mean radiant and orbit remained stable. Right-ascension and declination drift were resolved, while the fitted speed drift remained unresolved. External-catalogue tests were therefore repeated with the speed drift set to zero.

## Geographic checks

The GMN sample was split into three non-overlapping station groups. All three contained a significant activity enhancement and a compact orbit.

| Region | Members | Activity p-value | Median orbital D | Orbit-null p-value |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41 × 10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26 × 10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16 × 10⁻¹⁰ | 0.04795 | 0.0001 |

The largest distance between regional medoid orbits was 0.04054. This argues against a single region or station group creating the signal, although all three groups still share the GMN reduction system.

## Sensitivity to analysis choices

The candidate was re-evaluated under 81 combinations of:

- trajectory-fit error limit: 120, 180, or 240 arcsec;
- minimum station count: 2, 3, or 4;
- radiant/speed core radius: 2.5σ, 3.0σ, or 3.5σ; and
- activity half-width: 3°, 4°, or 5°.

All 81 settings passed. Membership ranged from 29 to 129, while median orbital D remained between 0.0364 and 0.0555. Together, the 81 settings form one sensitivity analysis.

## External catalogues

The GMN solution was fixed before the external catalogues were examined.

CAMS contributed six matches from 2011–2012. SonotaCo contributed four from 2022, 2023, and 2025. Each catalogue is individually small: CAMS narrowly missed the activity cutoff, while SonotaCo was below the minimum member count. Their combined ten-event result is therefore useful supporting evidence, but the pooled test is post-hoc.

| External result | Value |
|---|---:|
| CAMS + SonotaCo members | 10 |
| Years represented | 2011, 2012, 2022, 2023, 2025 |
| Pooled activity p-value | 1.622 × 10⁻⁴ |
| Shifted-window p-value | 0.02041 |
| Median orbital D | 0.04879 |
| Orbit-null p-value | 5 × 10⁻⁵ |
| Medoid distance from GMN orbit | 0.01723 |

A shower-removed EDMOND subset added six non-overlapping meteors from 2014, 2016, 2017, and 2022. The sample falls below the project’s standalone size and timing thresholds. Because EDMOND may share upstream observations with other catalogues, it is treated as supplementary evidence.

## Known-shower and parent-body checks

A checksum-locked copy of IAU MDC catalogue version 2026-06-25 contained 1,072 shower records and 2,174 submitted solutions. None matched the candidate under the activity, drifted-radiant, speed, and orbital criteria. The nearest complete orbit was Northern May Ophiuchids solution 004 at D_SH = 0.23445; its activity period and radiant do not match the late-April candidate.

A NASA/JPL search evaluated 729 broadly compatible valid orbits. The nearest object, 2023 HJ7, had D = 0.15939, an uncertainty code of 8, and an observational arc of only 11 days. The search did not identify a credible parent-body candidate.

## What remains uncertain

The main limitations are straightforward:

- the analysis uses catalogue trajectories rather than new reductions of raw images;
- the antihelion source has real internal structure that may not be fully captured by the background model;
- the three geographic groups share the GMN processing system;
- the external samples are small, and the pooled analysis was decided after the separate results were known;
- EDMOND is a compiled archive with incomplete currently linked release files;
- specialist comparison with obscure or differently parameterized shower literature remains the most important external check.

The next step is independent scientific review of the coordinate conventions, antihelion background, event table, and possible historical shower matches.
