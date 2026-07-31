# GhostStream results

## Current verdict

**GO — GhostStream has produced a high-confidence uncatalogued meteor-stream discovery candidate.**

The primary result is no longer only confirmation of a working-list shower. A blind scan of 2026 Global Meteor Network trajectories found a compact April stream that:

- is absent from all **2,174** parsable IAU Meteor Data Center shower solutions used in the audit;
- appears independently in GMN data from **2022–2026**;
- survives a source-preserving antihelion-background test that does not use any orbital element to select the activity enhancement;
- remains orbitally compact after **1,000/1,000** measurement-uncertainty clone trials;
- is supported by **10 additional meteors** in the independent legacy CAMS and SonotaCo archives, spanning 2011, 2012, 2022, 2023, and 2025.

The correct claim is currently:

> **GhostStream identified and independently supported an uncatalogued annual April meteor stream.**

It is not yet an official IAU discovery. Formal submission, expert review, and publication remain required.

## Primary result: uncatalogued April stream

### Frozen stream solution

At solar longitude **36.902°** (approximately late April), the refined GMN solution is:

| Parameter | Value |
|---|---:|
| Sun-centered ecliptic longitude | −149.376° |
| Geocentric ecliptic latitude | +7.323° |
| Approximate geocentric RA | 247.1° |
| Approximate geocentric Dec | −14.2° |
| Geocentric speed | 37.642 km/s |
| Perihelion distance, q | 0.079202 AU |
| Eccentricity, e | 0.946296 |
| Inclination, i | 24.709° |
| Argument of perihelion, ω | 333.494° |
| Encounter node, Ω | 37.937° |
| Semimajor axis | 1.475 AU |
| Orbital period | 1.79 years |
| Tisserand parameter relative to Jupiter | 3.84 |

Measured radiant/speed drift per degree of solar longitude:

- Sun-centered longitude: **−0.10295°**
- Ecliptic latitude: **−0.02305°**
- Geocentric speed: **−0.02935 km/s**

### GMN evidence

The frozen template selected **101 deduplicated GMN meteors** from April catalogs spanning 2019–2026. The stream was individually significant in five consecutive years:

| Year | Members | Activity p-value | Orbit-null p-value | Significant |
|---:|---:|---:|---:|:---:|
| 2019 | 1 | 0.3532 | — | No |
| 2020 | 4 | 0.1319 | — | No |
| 2021 | 1 | 0.3436 | — | No |
| 2022 | 10 | 0.003970 | 0.0001 | Yes |
| 2023 | 8 | 0.002168 | 0.0001 | Yes |
| 2024 | 14 | 0.00004888 | 0.0001 | Yes |
| 2025 | 34 | 9.42×10⁻⁹ | 0.0001 | Yes |
| 2026 | 29 | 4.13×10⁻⁶ | 0.0001 | Yes |

The two untouched years, 2022 and 2023, jointly passed the twelve-month familywise-corrected activity test:

- Pooled activity p-value: **1.857×10⁻⁵**
- Shifted-window empirical p-value: **0.01754**
- Source-matched orbit-null p-value: **0.0001**

No orbital elements were used to select the activity enhancement in this audit. Orbit coherence was tested only after radiant-speed-time selection, removing the orbital-node/date circularity concern.

The deduplicated GMN orbit distribution had:

- Median orbital distance: **0.04398**
- 90th-percentile orbital distance: **0.09232**
- Maximum distance between significant-year orbital medoids: **0.05044**
- Measurement-uncertainty clone stability: **1,000/1,000 passed**

### Independent archive support

The GMN solution was frozen before inspecting the independent archives.

#### Legacy CAMS

The official CAMS orbit catalog from 2010–2013 contained six strict matches:

- 2011: 2
- 2012: 4

Their orbit distribution had median D = **0.05068** and source-matched orbit-null p = **0.0001**. The activity test was suggestive but narrowly missed its preregistered individual-catalog threshold: p = **0.01251**.

#### SonotaCo

Permanent SonotaCo catalogs contained four strict matches:

- 2022: 2
- 2023: 1
- 2025: 1

Their activity p-value was **0.00715**, shifted-window p = **0.02041**, median orbital D = **0.03614**, and orbit-null p = **0.0001**. The catalog had too few members to pass the original minimum-count rule by itself.

#### Exploratory pooled synthesis

Because the two independent archives were individually sparse, they were pooled in an explicitly post-hoc synthesis. This is supporting evidence, not a substitute for a new preregistered network test.

- Independent members: **10**
- Years represented: **2011, 2012, 2022, 2023, 2025**
- Pooled activity p-value: **1.6218×10⁻⁴**
- Pooled shifted-window p-value: **0.02041**
- Pooled median orbital D: **0.04879**
- Pooled orbit-null p-value: **5×10⁻⁵**
- Independent pooled medoid distance from the refined GMN orbit: **0.01723**

No independent archive meteor duplicates a GMN event by UTC time.

### Novelty audit

- Official IAU shower solutions checked: **2,174**
- Hard matches: **0**
- Nearest official orbit: Northern May Ophiuchids, D ≈ **0.235**, inactive at the candidate epoch and substantially separated in radiant.
- A targeted literature search did not identify a published shower matching the full epoch, radiant, speed, and orbit.
- A NASA/JPL small-body screen evaluated **6,284** broadly compatible objects. None had D ≤ 0.15; the nearest object had D ≈ 0.159 but an uncertainty-code-8, 11-day orbit and is not credible parent-body evidence.

No parent body is claimed.

## Secondary result: Northern March gamma-Virginids

The earlier blind pipeline independently recovered the IAU working-list shower **NMV — Northern March gamma-Virginids** and confirmed it in five consecutive GMN years from 2021–2025. This remains an important positive control and secondary scientific result, but it is no longer the main GhostStream claim.

## Method validation

### Known-shower recovery

| Untouched shower | Precision | Recall | F1 |
|---|---:|---:|---:|
| Lyrids | 0.810 | 1.000 | 0.895 |
| Eta Aquariids | 0.904 | 1.000 | 0.950 |
| Southern Delta Aquariids | 0.856 | 1.000 | 0.922 |

### Weak-stream sensitivity

| Injected members | Recovered | Recovery rate | Median F1 |
|---|---:|---:|---:|
| 20 | 4/9 | 44.4% | 0.526 |
| 40 | 7/9 | 77.8% | 0.800 |
| 80 | 8/9 | 88.9% | 0.870 |

## Claim boundary

### Supported now

- A repeatable, orbitally coherent April stream is present in GMN data.
- It is not represented by the current IAU shower solutions checked.
- Its activity survives a widened antihelion-source null without using orbit to select members.
- Two older independent video-orbit archives contain a small but jointly significant set of matching meteors.

### Not supported yet

- Official IAU recognition.
- An official shower name.
- Established-shower status.
- A parent-body association.
- A causal dynamical history.

## Next stage

1. Prepare the IAU MDC shower-mean submission template and a full methods manuscript.
2. Obtain a fresh analysis from an independent meteor-network team using its own selection pipeline.
3. Request expert review of the orbit convention, radiant drift, antihelion null, and possible duplicate showers.
4. Perform dynamical integrations only after a credible parent-body shortlist exists.

**Overall status: high-confidence discovery candidate; proceed toward external expert validation and IAU MDC submission.**
