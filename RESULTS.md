# Results

A blind search of GMN trajectories found one compact late-April group. After its centre and selection rules were fixed, the same pattern appeared in earlier years. The internal label is `OrbitTrace-April-36.9`.

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
| External network passing all frozen gates | SonotaCo |

The recurrence and orbital coherence make a random grouping unlikely. The main unresolved issue is classification: a distinct stream, a branch of a known minor shower, or narrow structure within the antihelion source.

## GMN recurrence

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

The pooled 2022–2023 sample was reserved as an untouched confirmation. It gave an activity p-value of 1.857 × 10⁻⁵ after the twelve-month familywise rule, a shifted-window p-value of 0.01754, and a source/time-matched orbit-null p-value of 0.0001.

## Mean solution

The robust solution used for matching is evaluated near solar longitude 36.902°.

| Parameter | Value |
|---|---:|
| Sun-centred ecliptic longitude | −149.376° |
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

The draft MDC record uses a direct unweighted mean of the 95 event rows, so its values differ slightly from the robust matching solution.

## Internal robustness

A March–May profile supports an activity interval of solar longitude 35.902°–39.902°. A 20,000-replicate bootstrap resampled years and observing nights. The mean radiant and orbit were stable; right-ascension and declination drift were resolved, while speed drift was not.

The GMN sample was also split into three non-overlapping station groups:

| Region | Members | Activity p-value | Median orbital D | Orbit-null p-value |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41 × 10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26 × 10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16 × 10⁻¹⁰ | 0.04795 | 0.0001 |

All 81 nearby combinations of trajectory-fit limit, station count, core width, and activity-window width passed. Membership ranged from 29 to 129, while median orbital D remained between 0.0364 and 0.0555.

## Complete external-catalogue replication

The fixed GMN centre, drifts, widths, activity interval, orbit, and decision gates were applied without refitting to the complete usable IAU MDC 2026 yearly catalogues. The full machine-readable result, catalogue hashes, and selected events are under [`validation/full_external_replication/`](validation/full_external_replication/).

### SonotaCo — formal independent replication

| Quantity | Result |
|---|---:|
| Valid seasonal rows | 52,565 |
| Frozen-template members | 11 |
| Represented years | 2007, 2009, 2010, 2013, 2018, 2020, 2022, 2023 |
| Active years with at least two members | 2009 and 2022 |
| Activity p-value | 5.484 × 10⁻⁵ |
| Shifted-window p-value | 0.02041 |
| Median orbital D | 0.02998 |
| 90th-percentile orbital D | 0.05632 |
| Orbit-null p-value | 0.0001 |
| Preserved full gate | **Pass** |

SonotaCo therefore constitutes an independent external-network replication under the frozen GMN solution.

### CAMS — strong independent corroboration

| Quantity | Result |
|---|---:|
| Valid seasonal rows | 64,830 |
| Frozen-template members | 9 |
| Represented years | 2011, 2012, 2014, 2015, 2016 |
| Active years with at least two members | 2011 and 2012 |
| Activity p-value | 0.01526 |
| Shifted-window p-value | 0.02041 |
| Median orbital D | 0.05630 |
| 90th-percentile orbital D | 0.11642 |
| Orbit-null p-value | 0.0001 |
| Preserved full gate | **No — activity p exceeded 0.01** |

CAMS is statistically significant under the conventional 5% standard and passes the member-count, multi-year, shifted-window, and orbital gates. It is described as strong independent corroboration rather than a second formal pass because the pre-established activity threshold was 0.01.

### EDMOND — supplementary evidence

EDMOND supplied four frozen-template members in 2013, 2014, and 2016. Its activity p-value was 0.00939, median orbital D was 0.06054, and orbit-null p-value was 0.0006. It did not meet the member-count or multi-year gate. EDMOND is also treated as supplementary because it compiles observations from contributing video networks.

## Known-shower and parent-body checks

The checked IAU MDC catalogue contained 2,174 submitted solutions. None matched the candidate under the fixed activity, drifted-radiant, speed, and orbital rules. The nearest complete orbit was Northern May Ophiuchids solution 004 at D_SH = 0.23445; its activity period and radiant do not match the late-April candidate.

A NASA/JPL search evaluated 729 broadly compatible valid orbits. The nearest object, 2023 HJ7, had D = 0.15939, an uncertainty code of 8, and an observational arc of only 11 days. No credible parent body was identified.

## Main uncertainty

The external-confirmation weakness is substantially reduced: one independent network passes the complete frozen protocol and a second independently provides conventionally significant activity and highly significant orbital coherence.

The largest remaining uncertainty is classification. The candidate could still be a distinct stream, a branch of a poorly represented minor shower, or narrow structure within the antihelion source. Specialist review should focus on coordinate conventions, the antihelion background, historical shower lists, and whether the 95-event GMN orbit is distinct enough to justify a separate stream interpretation.
