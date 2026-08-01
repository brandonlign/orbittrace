# GhostStream results

## Current verdict

**GO — GhostStream has produced a high-confidence uncatalogued meteor-stream discovery candidate.**

A blind scan of 2026 Global Meteor Network trajectories found a compact annual April stream that:

- is absent from all **2,174** parsable IAU Meteor Data Center shower solutions used in the audit;
- appears in GMN data from **2022–2026**;
- survives a source-preserving antihelion-background test that does not use orbital elements to select the activity enhancement;
- remains orbitally compact after **1,000/1,000** measurement-uncertainty clone trials;
- reproduces in **three disjoint geographic GMN station groups**;
- has a corrected March–May source-normalized activity core spanning solar longitude **35.90°–39.90°**;
- remains significant under **all 81 of 81** frozen combinations of fit-error, station-count, radiant-width, and activity-window rules;
- has stable mean radiant and orbit under a **20,000-replicate year/night cluster bootstrap**;
- is supported primarily by **10 CAMS and SonotaCo meteors** across five historical years;
- receives additional orbitally strong support from **six non-overlapping meteors** in a shower-removed EDMOND subset;
- reproduces exactly those six and no additional members when the unchanged template is applied to every usable linked EDMOND v6.01 annual archive from 2001–2023; and
- passes the official MDC radiant/orbit consistency programs with **zero flagged errors**.

The correct claim is currently:

> **GhostStream identified and externally supported an uncatalogued annual April meteor-stream candidate.**

It is not yet an official IAU discovery. Formal submission, expert review, and publication remain required.

## Primary result: uncatalogued April stream

### Frozen stream solution

At solar longitude **36.902°**, the refined GMN solution is:

| Parameter | Value |
|---|---:|
| Sun-centered ecliptic longitude | −149.376° |
| Geocentric ecliptic latitude | +7.323° |
| Approximate geocentric RA | 247° |
| Approximate geocentric Dec | −14.3° |
| Geocentric speed | 37.642 km/s |
| Perihelion distance, q | 0.079202 AU |
| Eccentricity, e | 0.946296 |
| Inclination, i | 24.709° |
| Argument of perihelion, ω | 333.494° |
| Encounter node, Ω | 37.937° |
| Semimajor axis | 1.475 AU |
| Orbital period | 1.79 years |
| Tisserand parameter relative to Jupiter | 3.84 |

Fitted radiant/speed drift per degree of solar longitude:

- Sun-centered longitude: **−0.10295°**
- Ecliptic latitude: **−0.02305°**
- Geocentric speed: **−0.02935 km/s**

The fitted speed slope is **not resolved from zero**. Its year/night-bootstrap 95% interval is **−0.178 to +0.221 km/s per degree**. It is retained for reproducibility but is not claimed as a detected physical drift. Uniform external validation was rerun with the speed slope fixed to zero.

### GMN recurrence

The frozen template selected **101 deduplicated GMN meteors** from 2019–2026. Five consecutive years passed the individual confirmation gate:

| Year | Members | Activity p | Orbit-null p | Significant |
|---:|---:|---:|---:|:---:|
| 2019 | 1 | 0.3532 | — | No |
| 2020 | 4 | 0.1319 | — | No |
| 2021 | 1 | 0.3436 | — | No |
| 2022 | 10 | 0.003970 | 0.0001 | Yes |
| 2023 | 8 | 0.002168 | 0.0001 | Yes |
| 2024 | 14 | 4.888×10⁻⁵ | 0.0001 | Yes |
| 2025 | 34 | 9.42×10⁻⁹ | 0.0001 | Yes |
| 2026 | 29 | 4.13×10⁻⁶ | 0.0001 | Yes |

The two untouched years, 2022 and 2023, jointly passed the twelve-month familywise-corrected audit:

- pooled activity p = **1.857×10⁻⁵**;
- shifted-window p = **0.01754**;
- source-matched orbit-null p = **0.0001**.

No orbital elements were used to select the activity enhancement in this audit. Orbit was tested only afterward.

The GMN orbit distribution had:

- median orbital D = **0.04398**;
- 90th-percentile orbital D = **0.09232**;
- maximum significant-year medoid separation = **0.05044**;
- uncertainty-clone stability = **1,000/1,000 passed**.

### Cluster-bootstrap uncertainty

The 95 confirmed meteors span 29 observing nights. A hierarchical bootstrap sampled years and then observing nights within years for **20,000 replicates**.

| Drift | Point estimate | 95% interval | Result |
|---|---:|---:|---|
| dRA/dλ⊙ | +0.887°/° | +0.672 to +1.040 | resolved |
| dDec/dλ⊙ | −0.158°/° | −0.248 to −0.037 | resolved |
| dVg/dλ⊙ | −0.029 km/s/° | −0.178 to +0.221 | unresolved |

The arithmetic-mean solution, orbit, and resolved angular radiant drifts remained stable when entire years were omitted.

### Corrected activity profile

The first profile attempt was rejected because April-only files created zero-exposure bins after the end of the month. The corrected run loaded March, April, and May for 2022–2026 and discarded low-exposure bins.

- Baseline rate: **1.604 per 1000 antihelion-background meteors**
- Highest observed bin: **solar longitude 38.652°**
- Peak-bin counts: **15 stream / 1021 background**
- Peak relative rate: **15.17 per 1000 background**
- Contiguous posterior-supported activity core: **35.902°–39.902°**
- Pooled odds ratio: **4.162**
- Pooled p = **6.51×10⁻¹⁹**

The raw 0.5° FWHM is not treated as a physical duration because the highest half-degree bin moves when individual years are omitted. The robust result is the approximately four-degree relative activity core. Absolute flux and ZHR remain unmeasured.

### Disjoint geographic replication

| Region | Members | Years | Activity p | Median D | Orbit-null p |
|---|---:|---|---:|---:|---:|
| Americas | 30 | 2022–2026 | 6.41×10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2022–2026 | 2.26×10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2023–2026 | 2.16×10⁻¹⁰ | 0.04795 | 0.0001 |

Maximum cross-region medoid distance: **D = 0.04054**.

This substantially weakens the possibility of a single regional network or station-cluster artifact, although the groups still share the GMN processing system.

### Frozen specification curve

All **81 of 81** prespecified threshold combinations passed. The grid varied:

- maximum fit error: 120, 180, or 240 arcsec;
- minimum station count: 2, 3, or 4;
- radiant-core radius: 2.5σ, 3.0σ, or 3.5σ; and
- activity half-width: 3°, 4°, or 5°.

Selected membership ranged from 29 to 129. Activity p-values ranged from approximately **8.95×10⁻²⁵ to 8.55×10⁻⁷**, and median orbital D ranged from **0.0364 to 0.0555**. Every post-selection orbit passed.

### External archive support

The GMN solution was frozen before inspecting the external archives. After the clustered bootstrap showed that speed drift was unresolved, all external archives were rerun with `dVg/dλ⊙ = 0`.

#### Primary CAMS + SonotaCo evidence

CAMS contributed six strict matches in 2011–2012. SonotaCo contributed four in 2022, 2023, and 2025.

The explicitly post-hoc pooled result remained unchanged under zero speed drift:

- 10 meteors across 2011, 2012, 2022, 2023, and 2025;
- activity p = **1.6218×10⁻⁴**;
- shifted-window p = **0.02041**;
- median D = **0.04879**;
- q90 D = **0.07708**;
- orbit-null p = **5×10⁻⁵**;
- medoid distance from GMN = **0.01723**.

#### Supporting Shober EDMOND subset

A 2026 Zenodo shower-removed EDMOND subset was verified by MD5 before analysis. It added six non-overlapping members in 2014, 2016, 2017, and 2022:

- archive-specific activity p = **0.01206**;
- activity odds ratio = **7.013**;
- median D = **0.03669**;
- q90 D = **0.09815**;
- orbit-null p = **0.0001**;
- maximum member distance from GMN = **0.10638**.

The EDMOND subset narrowly missed the standalone N ≥ 8 and p ≤ 0.01 rules. It is supportive rather than independently decisive.

#### Extended exploratory synthesis

Combining CAMS, SonotaCo, and the Shober EDMOND subset produced:

- 16 non-overlapping events across eight years;
- activity p = **1.4639×10⁻⁶**;
- shifted-window p = **0.02041**;
- median D = **0.04843**;
- q90 D = **0.08701**;
- orbit-null p = **5×10⁻⁵**;
- medoid distance from GMN = **0.01723**;
- exact cross-source UTC duplicate groups = **0**.

This extension is explicitly exploratory. EDMOND is a compiled archive and may share contributing-network provenance with other historical catalogues, so it is not counted as a clean third independent instrument.

The advertised public EDMOND 2024 annual attachment remains unavailable. A networked recovery audit tested 434 candidate URLs, direct and alternate site paths, the WordPress media API, Wayback, and recent Common Crawl indexes without finding a CRC-valid 2024 ZIP; the neighboring official 2023 archive passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed.

The unchanged zero-speed-drift template was then applied to all **23 usable linked annual archives from 2001–2023**. It selected exactly the same six 2014, 2016, 2017, and 2022 events already preserved from the Shober subset and no additional events. The full-series activity enrichment was strong (one-sided Fisher p = **3.3785×10⁻⁴**, odds ratio **7.455**) and the post-selection orbit remained decisive (median Southworth–Hawkins D = **0.03601**, q90 = **0.07344**, 20,000-trial orbit-null p = **4.99975×10⁻⁵**). The 48-position shifted-window audit gave p = **0.06122**. This is therefore supporting evidence rather than a standalone frozen pass: the sample remains below the preexisting N ≥ 8 rule and the supplemental localization audit is slightly above 0.05. No scientific inference is drawn from the absent 2024 attachment.

### Novelty and parent-body audit

- IAU shower solutions checked: **2,174**
- Hard matches: **0**
- Nearest official orbit: Northern May Ophiuchids, D ≈ **0.235**, with the wrong activity epoch and radiant
- JPL small bodies screened: **6,284**
- Credible objects at D ≤ 0.15: **0**
- Nearest object: D ≈ 0.159, but uncertainty code 8 and only an 11-day observational arc

No parent body is claimed.

### IAU MDC package

The draft MDC package includes:

- a **95-row** lookup table containing the members from the five significant GMN years;
- arithmetic-mean JSON and legacy text records;
- a calculation audit;
- a full manuscript draft;
- a submission checklist; and
- the official MDC consistency-checker report.

The official `elements.f` and `radiants.f` programs reported **zero flagged consistency errors**. This validates compatibility of the mean radiant, speed, solar longitude, and orbit, not novelty or official recognition.

## Secondary result: Northern March gamma-Virginids

The earlier blind pipeline independently recovered the IAU working-list shower **NMV — Northern March gamma-Virginids** and confirmed it in five consecutive GMN years from 2021–2025. This remains a method-validation and secondary scientific result.

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

- A repeatable, orbitally coherent annual April stream is present in GMN data.
- It survives a widened antihelion-source null without orbital selection.
- It appears in three disjoint geographic GMN station groups.
- It survives all 81 frozen reasonable specification choices.
- Its mean solution and resolved angular radiant drift are stable under year/night resampling.
- Its relative activity is concentrated primarily between solar longitudes 35.90° and 39.90°.
- It is not represented by the IAU shower solutions checked.
- CAMS and SonotaCo contain a small but jointly significant historical sample with the same orbit.
- Six additional EDMOND meteors provide non-overlapping, orbitally strong supporting evidence.

### Not supported yet

- Official IAU recognition.
- An official shower name.
- Established-shower status.
- A detected geocentric-speed drift.
- Absolute flux or ZHR.
- A parent-body association.
- A demonstrated dynamical history.
- A fully preregistered third-network replication.

## Remaining external stage

1. Obtain expert review of coordinate conventions, duplicate audit, antihelion null, and membership table.
2. Obtain a fresh independent-network analysis using a separate reduction pipeline.
3. Obtain consented GMN Level 2 data for absolute flux and mass-index estimation.
4. Resolve authorship, GMN acknowledgment, affiliation, and journal plans.
5. Refresh the MDC catalogue immediately before submission.
6. Regenerate and checksum-lock the final package after all edits.
7. Submit the lookup table, mean record, and manuscript together only after those checks.

**Overall status: high-confidence discovery candidate with a technically complete draft package; external scientific review is now the principal remaining barrier.**
