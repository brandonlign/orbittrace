# An Uncatalogued Annual April Meteor Stream Identified in Global Meteor Network Trajectories

**Draft manuscript — not submitted**

**Author:** Brandon Li  
**Affiliation:** John L. Miller Great Neck North High School, Great Neck, New York, USA  
**Corresponding author:** [email to be added]

## Abstract

A blind search for weak meteor streams was conducted using public Global Meteor Network (GMN) trajectory catalogues. Candidate structures were detected in a joint radiant–speed–time representation and then evaluated with orbital coherence, independent-year replication, measurement-uncertainty cloning, source-preserving null tests, geographic station-network splits, clustered bootstrap uncertainty, a frozen 81-cell specification curve, external meteor-orbit archives, and comparison against the International Astronomical Union Meteor Data Center (IAU MDC) shower catalogue. One compact structure discovered in April 2026 survived the complete audit. A frozen template identified 95 members in five significant GMN years from 2022 through 2026. In the two untouched confirmation years, 2022 and 2023, the pooled activity enhancement remained significant after a twelve-month familywise correction (p = 1.86 × 10⁻⁵), while a source- and time-matched orbital null gave p = 1.0 × 10⁻⁴. No orbital element was used to select the final activity enhancement. A March–May source-normalized profile supported a contiguous activity core from solar longitude 35.90° to 39.90° (pooled p = 6.51 × 10⁻¹⁹). Three disjoint GMN geographic station groups independently reproduced the activity excess and compact orbit; their medoid orbits differed by at most D = 0.0405. All 81 frozen combinations of trajectory-fit error, station count, radiant-core width, and activity-window width passed. A 20,000-replicate year/night bootstrap resolved right-ascension and declination drift but not geocentric-speed drift. The robust GMN orbit is q = 0.0792 AU, e = 0.9463, i = 24.71°, ω = 333.49°, and Ω = 37.94°. Ten CAMS and SonotaCo meteors provide the primary external support. Six additional non-overlapping meteors occur in a shower-removed EDMOND subset; their orbital evidence is strong, although EDMOND is a compiled archive and is not treated as a fully independent third instrument. No matching solution was found among 2,174 parsed IAU MDC shower solutions. These results support an uncatalogued annual meteor-stream candidate active in late April. The stream is not claimed as established pending expert duplicate review, publication, and IAU MDC evaluation.

## 1. Introduction

Meteor streams are commonly identified as concentrations in radiant, velocity, encounter time, and orbital-element space. Weak streams are difficult to distinguish from the structured sporadic background, especially near the broad helion and antihelion sources. A clustering method can therefore generate convincing false positives if its null model destroys real source correlations, if orbital node is used both to select and test activity, or if a result depends on one favorable quality threshold.

The Global Meteor Network provides a large, public, multi-station trajectory catalogue with sufficient precision for meteor-shower studies. Its wide geographic coverage and repeated annual observations make it suitable for blind discovery followed by independent-year validation. The present study developed an uncertainty-aware search in which candidate generation was separated from confirmatory testing.

The goals were to:

1. recover established showers and injected weak streams before beginning a novelty search;
2. identify residual structures without using known-shower labels as positive training targets;
3. reject known and working-list showers using activity-aware catalogue matching;
4. require replication in data not used to choose the candidate;
5. test activity inside a source-preserving background without using orbital elements;
6. test whether the signal persists across disjoint geographic station groups;
7. quantify sampling uncertainty by resampling years and observing nights;
8. test robustness across a frozen grid of reasonable analysis choices; and
9. seek support in separately assembled meteor-orbit archives.

## 2. Data

### 2.1 Global Meteor Network

Monthly GMN trajectory catalogues from 2019 through July 2026 were accessed through the public GMN data service. Only multi-station trajectories were retained. The principal quality requirements were:

- at least two participating stations;
- median trajectory-fit error no greater than 180 arcsec;
- finite geocentric radiant, speed, and orbital elements;
- geocentric speed between 5 and 75 km s⁻¹; and
- a GMN shower label corresponding to sporadic activity.

Multiple trajectory solutions with the same event time were deduplicated. The solution with the lowest fit error was retained, with station count used as a secondary criterion.

### 2.2 External archives

The frozen candidate was later tested in:

- the official legacy CAMS orbit catalogue covering 2010–2013;
- permanent SonotaCo annual catalogues for 2022–2025; and
- a shower-removed EDMOND subset published in a 2026 Zenodo record associated with Shober (2026).

The Shober EDMOND file was verified against its published MD5 before analysis. EDMOND aggregates observations from contributing video networks and can share provenance with other historical compilations. It was therefore treated as additional robustness evidence rather than a fully independent third instrument.

The public EDMOND v6.01 page advertises a 2024 annual file containing 13,513 refined orbits, but its live attachment returned HTTP 404. A networked recovery audit tested 434 candidate URLs, direct and alternate site paths, the WordPress media API, Wayback, and recent Common Crawl indexes without locating a CRC-valid 2024 ZIP; the neighboring official 2023 attachment passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed. The frozen candidate was instead evaluated in every usable annual ZIP linked by the same page, covering 2001–2023. No result was inferred from the missing 2024 file.

### 2.3 Shower catalogue

Candidate solutions were compared with all parsable IAU MDC solutions available during the audit, including working-list and removed solutions. Duplicate rejection considered activity epoch, drifted radiant, geocentric speed, and orbital similarity rather than a static radiant alone.

## 3. Methods

### 3.1 Positive controls and sensitivity gate

Before the blind search, the method was required to recover three untouched major-shower controls: the Lyrids, Eta Aquariids, and Southern Delta Aquariids. Their F1 scores were 0.895, 0.950, and 0.922, respectively.

Weak synthetic streams were inserted into real sporadic backgrounds. Recovery increased with injected membership:

| Injected members | Recovery |
|---:|---:|
| 20 | 4/9 |
| 40 | 7/9 |
| 80 | 8/9 |

These tests established useful, though incomplete, sensitivity to diffuse low-member streams.

### 3.2 Blind candidate generation

The blind scan operated month by month. Meteors were represented using Sun-centered ecliptic radiant longitude, ecliptic latitude, geocentric speed, encounter time, and orbital information. Density-based clustering generated candidate structures. Static catalogue matching was rejected after it misidentified radiant-drifted known showers; the final veto propagated known-shower radiants to the candidate solar longitude.

The initial 2025 full-year search produced no defensible uncatalogued annual shower. A subsequent untouched scan of January–July 2026 produced one candidate in April.

### 3.3 Frozen April template

The discovery-stage center was frozen before historical validation. The confirmatory selection used a narrow radiant–speed core around a drifted template and an activity interval centered near solar longitude 36.9°. Exact-time duplicate solutions were collapsed before testing.

A year was considered individually confirmed only when it contained at least eight selected members, passed the activity test at p ≤ 0.01, and passed the orbital compactness threshold.

### 3.4 Source-preserving activity test

Because the candidate lies near the edge of the conventional antihelion-source region, the final audit deliberately widened the antihelion background to:

- Sun-centered ecliptic longitude 120°–240°;
- absolute ecliptic latitude ≤ 35°; and
- geocentric speed 15–50 km s⁻¹.

The activity test used only radiant, speed, and solar longitude. It did not use eccentricity, perihelion distance, inclination, argument of perihelion, or node. Orbital coherence was evaluated only after radiant–speed–time selection.

A Fisher exact test compared the fraction of expanded-antihelion meteors inside the narrow radiant–speed core during the candidate interval with the same fraction outside the interval. Shifted activity windows provided an empirical time-localization check.

### 3.5 Source-normalized activity profile

A first exploratory profile was rejected because it loaded April catalogues only; bins after the end of April contained zero exposure and were incorrectly assigned a posterior rate. The corrected analysis loaded March, April, and May for every year from 2022–2026.

Frozen stream-core counts were divided by simultaneous non-core counts inside the same expanded antihelion source in 0.5° solar-longitude bins. Bins with fewer than 40 background meteors were treated as unavailable. The outer region |Δλ⊙| > 6° and ≤ 18° defined the source-normalized baseline. Jeffreys posterior intervals were calculated for the stream fraction in each bin. This procedure estimates relative activity but not absolute flux or ZHR.

### 3.6 Orbital coherence and measurement uncertainty

Orbital compactness was measured with a five-element orbital dissimilarity statistic based on eccentricity, perihelion distance, orbital-plane angle, and perihelion-direction angle. Null groups were drawn from meteors observed in the same time and broad antihelion source but outside the narrow radiant–speed core.

Reported trajectory uncertainties were propagated through 1,000 clone trials. A clone trial passed only if the median and 90th-percentile orbital dispersions remained below frozen thresholds.

### 3.7 Year/night cluster bootstrap

Individual meteors from the same year and observing night are not fully independent. Sampling uncertainty was therefore estimated with 20,000 hierarchical bootstrap replicates. Each replicate sampled the five confirmed years with replacement and, within every selected year, sampled observing nights with replacement while retaining all meteors from each sampled night. Circular means were used for angular quantities. A second bootstrap retained every year exactly once and resampled nights only.

The bootstrap quantified uncertainty in the mean radiant, speed, orbit, and linear radiant/speed drift. It addresses sampling variability and is distinct from the measurement-error clone audit.

### 3.8 Disjoint geographic station groups

Each GMN trajectory was assigned to exactly one geographic group according to the unique majority of its parsed participating-station country prefixes. Ties and unknown prefixes were excluded. The groups were:

- Americas;
- Europe and West Asia; and
- Oceania, East Asia, and Africa.

The frozen radiant–speed–time activity test and post-selection orbital null were repeated independently in each group. No trajectory contributed to more than one regional test. This is a geographically disjoint robustness test within the common GMN reduction system, not a fully independent reduction pipeline.

### 3.9 Frozen specification curve

A prespecified 81-cell grid varied four defensible analysis choices:

- median trajectory-fit-error maximum: 120, 180, or 240 arcsec;
- minimum station count: 2, 3, or 4;
- radiant-core radius: 2.5σ, 3.0σ, or 3.5σ; and
- activity half-width: 3°, 4°, or 5°.

Every cell used the same March–May data, expanded antihelion background, frozen candidate center, and non-orbital activity test. Orbit was evaluated only after radiant–speed–time selection. A cell passed when its activity enhancement and post-selection orbit satisfied the frozen significance and compactness rules. The grid was evaluated in full; no specification was selected after seeing its outcome.

### 3.10 External-archive tests

CAMS, SonotaCo, and Shober EDMOND meteors were selected using the frozen GMN radiant center, resolved radiant drift, widths, and activity interval. The year/night bootstrap did not resolve geocentric-speed drift, so the final uniform external analysis fixed dVg/dλ⊙ = 0. Orbit was tested afterward and was not used to select external members.

CAMS and SonotaCo form the primary cross-network external comparison. Their archive-specific thresholds were defined before examining each result. Because both samples were sparse, their pooled synthesis is explicitly post-hoc. The EDMOND extension is also exploratory and is reported separately because EDMOND is a compiled archive that may share upstream network provenance with other historical catalogues. Exact UTC overlaps were audited across selected external events.

## 4. Results

### 4.1 GMN recurrence

The frozen template selected 101 deduplicated GMN meteors in 2019–2026. Five consecutive years passed the individual confirmation gate.

| Year | Members | Activity p | Orbit-null p | Confirmed |
|---:|---:|---:|---:|:---:|
| 2019 | 1 | 0.3532 | — | No |
| 2020 | 4 | 0.1319 | — | No |
| 2021 | 1 | 0.3436 | — | No |
| 2022 | 10 | 0.003970 | 0.0001 | Yes |
| 2023 | 8 | 0.002168 | 0.0001 | Yes |
| 2024 | 14 | 4.888 × 10⁻⁵ | 0.0001 | Yes |
| 2025 | 34 | 9.42 × 10⁻⁹ | 0.0001 | Yes |
| 2026 | 29 | 4.131 × 10⁻⁶ | 0.0001 | Yes |

The submission lookup table uses the 95 members from the five significant years.

### 4.2 Source-preserving confirmation

For the untouched 2022–2023 sample:

- pooled activity p = 1.857 × 10⁻⁵;
- shifted-window p = 0.01754; and
- source-matched orbital-null p = 0.0001.

The result remains localized in time and orbit when the broad antihelion source is preserved and orbital elements are excluded from activity selection.

### 4.3 Activity profile

The corrected March–May profile had a baseline rate of 1.604 stream-core meteors per 1000 non-core antihelion meteors. The highest 0.5° bin occurred at solar longitude 38.652°, with 15 stream-core and 1021 background meteors, corresponding to 15.17 per 1000 background meteors (95% interval 8.56–23.72).

The contiguous interval with posterior probability at least 0.95 of exceeding the out-of-window baseline extended from solar longitude **35.902° to 39.902°**. The pooled inside-versus-baseline odds ratio was 4.162, with p = 6.51 × 10⁻¹⁹.

The raw 0.5° half-maximum width was not interpreted as the physical stream width because the highest bin shifted between adjacent bins in leave-one-year-out analyses. The four-degree posterior-supported interval is the more defensible characterization. The pooled activity excess remained highly significant when any one year was omitted, with p-values from 2.17 × 10⁻¹³ to 2.30 × 10⁻¹⁷.

### 4.4 Radiant, speed, and clustered uncertainty

At solar longitude 36.902°, the fitted drift-corrected solution is:

- Sun-centered ecliptic longitude = −149.376°;
- ecliptic latitude = +7.323°;
- geocentric right ascension ≈ 246.96°;
- geocentric declination ≈ −14.34°; and
- geocentric speed = 37.642 km s⁻¹.

The fitted drift per degree of solar longitude is:

- −0.10295° in Sun-centered ecliptic longitude;
- −0.02305° in ecliptic latitude; and
- −0.02935 km s⁻¹ in geocentric speed.

The 20,000-replicate year/night cluster bootstrap gave:

| Quantity | Point estimate | 95% interval |
|---|---:|---:|
| dRA/dλ⊙ | +0.887°/° | +0.672 to +1.040 |
| dDec/dλ⊙ | −0.158°/° | −0.248 to −0.037 |
| dVg/dλ⊙ | −0.029 km s⁻¹/° | −0.178 to +0.221 |

Right-ascension and declination drift were resolved from zero. The speed slope was not; it is retained as a fitted descriptive value but is not interpreted as a detected physical deceleration. External validation was therefore repeated with dVg/dλ⊙ fixed to zero.

The arithmetic-mean MDC record calculated directly from the 95 lookup-table meteors has solar longitude 37.150°, RA 247.170°, Dec −14.343°, and Vg 37.618 km s⁻¹. Its clustered 95% intervals are RA 246.428°–247.894°, Dec −14.565° to −14.159°, and Vg 37.201–37.865 km s⁻¹.

### 4.5 Orbit

The robust GMN medoid orbit is:

| Element | Value | 95% year/night bootstrap interval for arithmetic mean |
|---|---:|---:|
| a | 1.475 AU | 1.3725–1.4549 AU |
| q | 0.0792 AU | 0.078358–0.082575 AU |
| e | 0.9463 | 0.940369–0.945591 |
| i | 24.709° | 23.448°–24.961° |
| ω | 333.494° | 333.262°–333.946° |
| Ω | 37.937° | 36.341°–38.052° |

The medoid and arithmetic-mean rows serve different purposes: the medoid is used for robust membership/similarity calculations, whereas the arithmetic mean and clustered intervals are used for the MDC submission record. The full GMN sample has median orbital D = 0.04398 and 90th-percentile D = 0.09232. All 1,000 uncertainty-clone trials passed the frozen compactness requirements.

### 4.6 Geographic replication

The candidate passed in all three disjoint geographic station groups:

| Region | Members | Years | Activity p | Median D | Orbit-null p |
|---|---:|---|---:|---:|---:|
| Americas | 30 | 2022–2026 | 6.41 × 10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2022–2026 | 2.26 × 10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2023–2026 | 2.16 × 10⁻¹⁰ | 0.04795 | 0.0001 |

The maximum orbital distance between regional medoids was D = 0.04054. The signal is therefore not attributable to one regional camera network or station cluster.

### 4.7 Specification-curve robustness

All **81 of 81** frozen specification cells passed. Selected membership ranged from 29 in the strictest cells to 129 in the broadest cells. Across the grid:

- activity p-values ranged from approximately 8.95 × 10⁻²⁵ to 8.55 × 10⁻⁷;
- median orbital D ranged from 0.0364 to 0.0555; and
- every post-selection orbit passed the frozen compactness requirement.

The candidate therefore does not depend on the originally chosen 180-arcsec fit-error limit, two-station minimum, 3σ radiant core, or four-degree activity half-width.

### 4.8 External archives

#### Primary CAMS + SonotaCo result

Legacy CAMS contained six strict matches in 2011–2012. Their median orbital D was 0.05068, and their source-matched orbit-null p-value was 0.0001. The archive-specific activity test gave p = 0.01251, narrowly above the frozen p ≤ 0.01 threshold.

SonotaCo contained four strict matches in 2022, 2023, and 2025. Their activity p-value was 0.00715, median orbital D was 0.03614, and orbit-null p-value was 0.0001, but the sample did not reach the frozen minimum member count.

Under the corrected uniform zero-speed-drift template, the explicitly post-hoc pooled CAMS + SonotaCo synthesis remained unchanged:

- 10 meteors across 2011, 2012, 2022, 2023, and 2025;
- activity p = 1.622 × 10⁻⁴;
- shifted-window p = 0.02041;
- median orbital D = 0.04879;
- q90 orbital D = 0.07708;
- orbit-null p = 5 × 10⁻⁵; and
- medoid distance from the GMN orbit = 0.01723.

#### Exploratory Shober EDMOND extension

The MD5-verified shower-removed EDMOND subset contained six additional members in 2014, 2016, 2017, and 2022. The same six were selected with the fitted and zero speed-slope templates. Under zero speed drift:

- archive-specific activity p = 0.01206;
- activity odds ratio = 7.013;
- median orbital D = 0.03669;
- q90 orbital D = 0.09815;
- orbit-null p = 0.0001; and
- maximum member distance from the refined GMN orbit = 0.10638.

The EDMOND sample narrowly missed the standalone p ≤ 0.01 and N ≥ 8 rules, so it is supportive rather than independently decisive.

#### Full linked EDMOND v6.01 audit

The unchanged zero-speed-drift template was subsequently applied to all 23 usable annual archives linked by the public EDMOND v6.01 page from 2001 through 2023; the linked 2024 archive remained unavailable. The full annual series selected exactly the same six UTC events as the Shober subset and no additional events. Within the expanded antihelion source, the frozen inside-versus-outside activity test gave p = 3.3785 × 10⁻⁴ and a Haldane–Anscombe odds ratio of 7.455. A 48-position shifted-window audit gave a plus-one empirical p = 0.06122. The six post-selection orbits had median Southworth–Hawkins D = 0.03601, q90 D = 0.07344, and a 20,000-trial source/time-matched orbit-null p = 4.99975 × 10⁻⁵. This full-series check confirms that the six selected events are reproducible in the public annual archives, but it does not create an independent sample and does not pass the frozen N ≥ 8 or shifted-window localization gates.

The uniform exploratory synthesis of CAMS, SonotaCo, and Shober EDMOND contained 16 non-overlapping events across eight years:

- activity p = 1.464 × 10⁻⁶;
- shifted-window p = 0.02041;
- median orbital D = 0.04843;
- q90 orbital D = 0.08701;
- orbit-null p = 5 × 10⁻⁵;
- medoid distance from the GMN orbit = 0.01723; and
- exact cross-source UTC duplicate groups = 0.

This extended result is explicitly exploratory. The EDMOND label does not imply a wholly independent observing instrument because EDMOND is a compilation and may share contributing-network provenance with other video-meteor archives.

### 4.9 Catalogue and parent-body checks

No hard match was found among 2,174 parsed IAU MDC shower solutions. The nearest official orbit was the Northern May Ophiuchids at D ≈ 0.235, but its activity epoch and radiant do not match the candidate.

A NASA/JPL Small-Body Database screen found no credible parent. The nearest listed object had D ≈ 0.159 but an uncertainty-code-8 orbit based on an 11-day observational arc. No parent-body association is proposed.

## 5. Discussion

The strongest evidence for a real stream is the conjunction of recurrence across five GMN years, confirmation in untouched years, a source-preserving activity excess, orbital coherence after non-orbital selection, recurrence in three geographically disjoint station groups, stability under year/night resampling, survival across all 81 frozen specifications, and matching historical meteors in separately assembled archives.

The candidate is not merely defined by an orbital node near the date of observation. The final activity test excludes all orbital elements, and the orbit remains far more compact than source- and time-matched null samples. The candidate also survives when embedded inside a deliberately expanded antihelion background, reducing the risk that it is an artifact of a conventional source boundary.

The geographic split further reduces the possibility of a station-specific or regional reduction artifact. The Americas, Europe/West Asia, and Oceania/East Asia/Africa independently show significant activity enhancements and mutually consistent orbital medoids. Because all three still use the GMN processing system, this test complements rather than replaces external-network validation.

The specification curve addresses another common false-positive route: favorable threshold choice. The activity signal remains highly significant and orbitally compact under stricter and broader fit-error limits, station-count requirements, core radii, and activity windows. The bootstrap further shows that the mean solution and angular radiant drift are stable at the year/night level. Conversely, it prevents overstatement of the fitted speed slope, whose interval includes zero.

The source-normalized activity profile supports a concentrated four-degree late-April core. It should not be interpreted as an absolute flux curve because station uptime, weather, limiting magnitude, radiant elevation, and collecting area were not modeled directly. The exact 0.5° highest bin is also not stable enough to warrant a precise annual maximum claim.

The external evidence is supportive but not definitive. CAMS and SonotaCo contain ten matching meteors in total. Each archive is individually underpowered under at least one frozen rule, and their pooled analysis was motivated after observing the separate sparse results. The six EDMOND meteors increase the breadth of historical support and are orbitally compelling, but EDMOND's compiled provenance prevents treating them as a clean third-network replication. A fresh independent network analysis using a preregistered pipeline remains the most valuable next validation.

The absence of a credible known parent is not evidence against the stream. Weak meteoroid streams may have unrecognized, poorly determined, dormant, or dynamically evolved parents. Dynamical integrations would be premature until a plausible parent-body shortlist exists.

## 6. Limitations

1. The discovery and confirmatory analyses use public catalogue-level trajectories rather than raw image re-reductions.
2. The broad antihelion source has complex internal structure that may not be captured completely by the chosen null.
3. The activity profile is normalized to the simultaneous antihelion source rather than an explicit collecting-area and limiting-magnitude exposure model; it is not an absolute flux or ZHR profile.
4. The geographic split uses disjoint station groups but a shared GMN reduction system.
5. The pooled CAMS–SonotaCo analysis and the three-archive extension are post-hoc.
6. EDMOND is a compiled archive and may share upstream observing-network provenance with other historical catalogues.
7. The advertised official EDMOND 2024 annual attachment was unavailable during the audit.
8. The literature and duplicate-shower audit cannot guarantee that no obscure historical solution uses a different convention or incomplete orbit.
9. No dynamical parent-body connection has been demonstrated.
10. The fitted geocentric-speed drift is not resolved from zero under clustered resampling.

## 7. Conclusion

A blind search of GMN trajectories identified an annual late-April meteor-stream candidate with a compact radiant and orbit. The candidate is significant in five consecutive GMN years, survives a node-independent source-preserving test, appears across three disjoint geographic station groups, remains stable in 20,000 year/night bootstrap replicates, and passes all 81 frozen specification choices. Its source-normalized activity is concentrated primarily between solar longitudes 35.90° and 39.90°. Ten CAMS/SonotaCo meteors provide the primary external support, while six non-overlapping EDMOND meteors provide additional orbitally strong but provenance-limited evidence. No matching IAU MDC solution or credible parent body was found. The result warrants submission to the IAU MDC and independent expert review, but it should remain described as an uncatalogued discovery candidate until publication and formal evaluation.

## Data and code availability

The GMN trajectory catalogues are publicly available through the Global Meteor Network. The frozen search, validation scripts, lookup table, candidate solution, source-preserving null, activity profile, geographic split, bootstrap intervals, specification curve, external-member tables, and audit outputs are preserved in the project repository. The IAU MDC lookup table accompanying this draft contains the 95 GMN meteors used for the arithmetic-mean submission record. The Shober EDMOND subset is available through Zenodo record 18664293 under CC BY 4.0.

## References

Campello, R. J. G. B., Moulavi, D., & Sander, J. (2013). Density-based clustering based on hierarchical density estimates. *Advances in Knowledge Discovery and Data Mining*, 160–172. https://doi.org/10.1007/978-3-642-37456-2_14

Jenniskens, P., Jopek, T. J., Janches, D., Hajduková, M., Kokhirova, G. I., & Rudawska, R. (2020). On removing showers from the IAU Working List of Meteor Showers. *Planetary and Space Science, 182*, 104821. https://doi.org/10.1016/j.pss.2019.104821

Jopek, T. J., & Kaňuchová, Z. (2017). IAU Meteor Data Center—the shower database: a status report. *Planetary and Space Science, 143*, 3–6.

Shober, P. M. (2026). *Asteroidal non-shower meteor orbit subsets (CAMS, GMN, EDMOND, SonotaCo) used in Shober (2026, ApJ)* [Data set]. Zenodo. Record 18664293.

Southworth, R. B., & Hawkins, G. S. (1963). Statistics of meteor streams. *Smithsonian Contributions to Astrophysics, 7*, 261–285.

Vida, D., Šegon, D., Gural, P. S., Brown, P. G., McIntyre, M. J. M., Dijkema, T. J., et al. (2021). The Global Meteor Network—Methodology and first results. *Monthly Notices of the Royal Astronomical Society, 506*(4), 5046–5074. https://doi.org/10.1093/mnras/stab2008
