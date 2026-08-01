# An Uncatalogued Annual April Meteor-Stream Candidate in Global Meteor Network Data

**Working manuscript**

**Author:** Brandon Li  
**Affiliation:** John L. Miller Great Neck North High School, Great Neck, New York, USA  
**Corresponding author:** [to be added]

## Abstract

I searched public Global Meteor Network (GMN) trajectory catalogues for weak meteor streams outside the solutions represented in the IAU Meteor Data Center (MDC) shower catalogue. Candidate groups were found in Sun-centered radiant, speed, and encounter-time space and then tested using orbital coherence, historical recurrence, source-matched backgrounds, measurement-error simulations, geographic station splits, clustered bootstrap resampling, a sensitivity analysis over 81 nearby specifications, and external meteor-orbit catalogues.

One late-April group survived the complete analysis. The final GMN sample contains 95 meteors in five significant years from 2022 through 2026. The pooled 2022–2023 confirmation was reserved until after the candidate definition had been fixed and gave an activity p-value of 1.86 × 10⁻⁵ after a twelve-month familywise rule and a source/time-matched orbit-null p-value of 1.0 × 10⁻⁴. The activity enhancement was selected from radiant, speed, and solar longitude, with orbit evaluated afterward. A March–May profile supports an activity interval from solar longitude 35.90° to 39.90°. The candidate appears in three non-overlapping GMN geographic station groups, passes all 81 tested combinations of nearby quality and window choices, and remains stable in 20,000 year/night bootstrap samples. The bootstrap resolves angular radiant drift while leaving geocentric-speed drift unresolved.

Six CAMS meteors and four SonotaCo meteors provide the main external support. Six additional meteors occur in a shower-removed EDMOND subset, although EDMOND’s compiled provenance limits its independence. A checksum-locked comparison with 2,174 official MDC solutions found no direct match or timing/radiant/speed near match. The original analysis code was recovered from immutable commits and reproduced the primary event list and downstream results without retuning. The evidence supports a recurring, apparently uncatalogued late-April meteor-stream candidate. Specialist review will focus on its distinctness from minor-shower branches and antihelion structure.

## 1. Introduction

Meteor showers are usually recognized as concentrations in radiant position, speed, encounter date, and heliocentric orbit. Strong annual showers are easy to see, but weak streams can be difficult to separate from the structured sporadic background. The problem is especially difficult near the broad helion and antihelion sources, where genuine correlations already exist in radiant, speed, and time.

A convincing weak-stream search therefore needs more than a compact cluster. It should show annual recurrence, stability across reasonable analysis choices, geographic consistency, orbital compactness relative to a local background, and separation from known shower solutions.

The Global Meteor Network provides public multi-station trajectory catalogues with broad geographic coverage and repeated annual observations. I used those catalogues for a blind search followed by tests in years that were not used to choose the candidate. The analysis was designed around four principles:

1. demonstrate that the method can recover known showers and injected weak streams;
2. separate candidate generation from later confirmation;
3. test activity without using orbital elements, then test orbit afterward; and
4. keep external catalogues and untouched years out of the candidate-tuning stage.

This paper describes the one late-April candidate that survived those tests.

## 2. Data

### 2.1 Global Meteor Network

Monthly GMN trajectory catalogues from 2019 through July 2026 were downloaded from the public GMN service. The discovery search used trajectories labelled as sporadic by GMN and required:

- at least two participating stations;
- median trajectory-fit error no greater than 180 arcsec;
- finite radiant, speed, and orbital quantities; and
- geocentric speed between 5 and 75 km/s.

When more than one solution shared the same event time, the lowest-fit-error solution was kept, with station count used as a secondary criterion.

The 2026 January–July data were used for the blind rediscovery. The April candidate definition was fixed before the earlier years were evaluated.

### 2.2 External catalogues

The candidate was later applied to:

- the legacy CAMS orbit catalogue for 2010–2013;
- permanent SonotaCo annual catalogues for 2022–2025; and
- a shower-removed EDMOND subset published with Shober (2026).

The EDMOND subset was checked against its published MD5 before use. Because EDMOND combines observations from contributing video networks, it was treated as supplementary evidence rather than as a wholly independent third instrument.

The public EDMOND page also linked annual ZIP files for 2001–2024. The 2024 link returned 404. Twenty-three files for 2001–2023 passed ZIP, CRC, and schema checks. Their row counts and embedded version fields differ from the advertised v6.01 release, so they are described as the currently linked files and used only to reproduce the six EDMOND events.

### 2.3 Shower catalogue and parent-body data

The candidate was compared with every parsable solution in the official IAU MDC full shower-data catalogue, including working-list entries. A NASA/JPL Small-Body Database query was used for a broad parent-body screen after the meteor-stream solution had been established.

## 3. Methods

### 3.1 Method controls

Three named showers were used as positive controls: the Lyrids, Eta Aquariids, and Southern Delta Aquariids. Their F1 scores were 0.895, 0.950, and 0.922.

The original combined control gate contained a flawed rule that rejected any cluster larger than 30% of the sample. Eta Aquariids themselves made up more than 30% of their control sample, making the rule impossible to satisfy at high recall. I retained that failed gate rather than relabelling it. A correction was specified before independent 2024 holdouts were examined: the same 30% limit was applied to the largest non-target cluster. All three showers then passed, with 2024 F1 scores of 0.902, 0.957, and 0.927.

Synthetic weak streams were also inserted into real sporadic backgrounds. Four of nine 20-member injections, seven of nine 40-member injections, and eight of nine 80-member injections were recovered.

### 3.2 Blind search

Each meteor was represented by four quantities:

- Sun-centered geocentric ecliptic radiant longitude;
- geocentric ecliptic radiant latitude;
- geocentric speed; and
- solar longitude.

The feature scales were 3.5°, 3.0°, 2.5 km/s, and 2.5°, respectively. HDBSCAN was run with `min_cluster_size = 12`, `min_samples = 4`, and leaf cluster selection.

Candidate groups had to contain 12–300 members, appear on at least four nights and at least six stations, avoid domination by one night or station set, and have at least 80% valid orbits. Their median and 90th-percentile orbital distances also had to remain below fixed limits. Alternating-night split tests and local time-permutation tests were used to check recurrence. Broad sporadic-source regions and known MDC showers were screened before a candidate could proceed.

The January–July 2026 rerun selected April as the only full-gate candidate.

### 3.3 Historical confirmation

The April center, drift, widths, and activity interval were fixed before the earlier years were tested. A year was counted as individually significant only when both the activity and post-selection orbital tests passed.

The pooled 2022–2023 sample was reserved as the untouched confirmation. Its activity p-value was evaluated under a twelve-month familywise rule. A shifted-window test compared the observed activity interval with nearby positions, and a source/time-matched orbit null tested whether the selected meteors were unusually compact in orbital space.

### 3.4 Source-matched activity test

The candidate lies near the antihelion source. The final background therefore used a deliberately broad region in Sun-centered radiant longitude, latitude, and speed. Candidate selection depended only on radiant, speed, and solar longitude. Orbital elements, including node, were evaluated afterward.

Orbital compactness was compared with local source- and time-matched groups. This separation avoids using encounter geometry both to select the events and to claim significance.

### 3.5 Activity profile

For each half-degree solar-longitude bin, stream-core counts were normalized by the simultaneous non-core antihelion population. March, April, and May data were loaded for every year from 2022–2026. Bins with fewer than 40 background meteors were excluded.

This procedure estimates relative activity within the source. Absolute flux and ZHR require direct modeling of station uptime, weather, limiting magnitude, radiant elevation, and collecting area.

### 3.6 Orbit and measurement uncertainty

Southworth–Hawkins D was used for orbital comparisons. The observed median and 90th-percentile distances were compared with source- and time-matched random groups.

To test measurement uncertainty, the trajectory quantities were perturbed within their reported errors and the complete selection and compactness checks were repeated 1,000 times.

### 3.7 Clustered bootstrap

Uncertainty in the mean solution and drifts was estimated with 20,000 bootstrap samples. Years were sampled with replacement, then observing nights were sampled with replacement within each selected year. All meteors from a selected night were retained. A second scheme kept every year exactly once and resampled nights only.

### 3.8 Geographic split

Stations were divided into three groups: Americas, Europe/West Asia, and Oceania/East Asia/Africa. Each trajectory was assigned to one group using the majority of its participating stations. Ties and unclassified prefixes were excluded. The same selection and orbit tests were then run independently in each group.

### 3.9 Sensitivity analysis

The complete candidate test was repeated across 81 combinations of fit-error limit, station count, core radius, and activity-window width. The candidate center and underlying data were unchanged.

### 3.10 External catalogues

The GMN solution was not refitted to CAMS, SonotaCo, or EDMOND. After the bootstrap showed that the geocentric-speed drift was not resolved, the external tests were repeated with that slope set to zero. Orbital elements were again used only after radiant–speed–time selection.

The CAMS and SonotaCo catalogues were first evaluated separately. Their pooled ten-event result was calculated afterward and is described as post-hoc. The EDMOND extension is also described separately because of its compiled provenance.

### 3.11 Catalogue comparison

A direct MDC match required compatible activity timing, drifted radiant separation no greater than 5°, speed difference no greater than 5 km/s, and a complete orbit with D_SH ≤ 0.15. Timing/radiant/speed near matches with incomplete orbits were recorded separately.

## 4. Results

### 4.1 GMN recurrence

The fixed selection found 101 deduplicated meteors from 2019–2026. Five consecutive years passed the individual tests.

| Year | Members | Activity p-value | Orbit-null p-value |
|---:|---:|---:|---:|
| 2022 | 10 | 0.003970 | 0.0001 |
| 2023 | 8 | 0.002168 | 0.0001 |
| 2024 | 14 | 4.888 × 10⁻⁵ | 0.0001 |
| 2025 | 34 | 9.42 × 10⁻⁹ | 0.0001 |
| 2026 | 29 | 4.13 × 10⁻⁶ | 0.0001 |

The other six selected meteors were distributed across 2019–2021, where the yearly activity tests were not significant.

The pooled untouched 2022–2023 sample gave an activity p-value of 1.857 × 10⁻⁵, a shifted-window p-value of 0.01754, and an orbit-null p-value of 0.0001.

### 4.2 Activity profile

The highest observed half-degree bin was centered at solar longitude 38.652° and contained 15 stream-core meteors among 1,021 background meteors. The supported contiguous interval was 35.902°–39.902°. The pooled odds ratio was 4.162, with p = 6.51 × 10⁻¹⁹.

The exact highest bin changed in leave-one-year-out analyses, so the four-degree interval is the stable timing result.

### 4.3 Radiant, speed, and orbit

At solar longitude 36.901963°, the robust matching solution is:

| Quantity | Value |
|---|---:|
| Sun-centered ecliptic longitude | −149.376325° |
| Ecliptic latitude | +7.323038° |
| Geocentric speed | 37.641692 km/s |
| q | 0.079202 AU |
| e | 0.946296 |
| i | 24.709376° |
| ω | 333.493819° |
| Ω | 37.937477° |
| a | 1.474788 AU |

The 95-event GMN sample had median D = 0.04398 and 90th-percentile D = 0.09232. The largest separation between significant-year medoid orbits was 0.05044. All 1,000 measurement-error trials passed.

### 4.4 Bootstrap

The clustered bootstrap gave:

| Drift | Point estimate | 95% interval |
|---|---:|---:|
| dRA/dλ⊙ | +0.887°/° | +0.672 to +1.040 |
| dDec/dλ⊙ | −0.158°/° | −0.248 to −0.037 |
| dVg/dλ⊙ | −0.029 km/s/° | −0.178 to +0.221 |

The angular drifts exclude zero, while the speed interval includes zero and is treated as unresolved.

### 4.5 Geographic split

| Region | Members | Activity p-value | Median D | Orbit-null p-value |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41 × 10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26 × 10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16 × 10⁻¹⁰ | 0.04795 | 0.0001 |

The largest distance between regional medoid orbits was 0.04054.

### 4.6 Sensitivity analysis

All 81 tested settings passed. Membership ranged from 29 to 129, median orbital D ranged from 0.03640 to 0.05548, and the largest activity p-value was 8.55 × 10⁻⁷.

### 4.7 External catalogues

CAMS contributed six matching meteors from 2011–2012. SonotaCo contributed four from 2022, 2023, and 2025. The post-hoc pooled result contained ten meteors and gave:

- activity p = 1.622 × 10⁻⁴;
- shifted-window p = 0.02041;
- median D = 0.04879;
- orbit-null p = 5 × 10⁻⁵; and
- medoid distance from the GMN orbit = 0.01723.

The shower-removed EDMOND subset contributed six additional non-overlapping meteors in 2014, 2016, 2017, and 2022. Their archive-specific activity p-value was 0.01206 and their median D was 0.03669. The sample fell below the project’s standalone N ≥ 8 and p ≤ 0.01 rules.

The currently linked EDMOND files for 2001–2023 recovered exactly those same six events. Their row counts and embedded versions differ from the advertised v6.01 release, so this check is treated as a reproduction of the six events rather than a release-level replication.

### 4.8 Known showers and parent-body screen

The MDC catalogue comparison found no direct match, no timing/radiant/speed near match, and no near match hidden by missing orbital elements. The nearest complete orbit was Northern May Ophiuchids solution 004 at D_SH = 0.23445, with a non-overlapping activity interval and a 9.59° radiant separation at the candidate epoch.

The JPL screen evaluated 729 valid broadly compatible orbits. The nearest object, 2023 HJ7 at D = 0.15939, had a poorly determined orbit based on an 11-day arc. The screen did not identify a credible parent-body association.

## 5. Discussion

The strongest case for a real stream comes from the combination of annual recurrence, untouched-year confirmation, non-orbital activity selection, post-selection orbital compactness, geographic replication, sensitivity to analysis choices, and matching meteors in other catalogues. The case comes from the agreement of these tests rather than any single statistic.

The antihelion background remains the most important scientific concern. The candidate survives inside a deliberately broad source definition, and its orbit is compact after selection without orbital elements. Even so, a specialist may recognize a narrower source component or historical shower solution that is not represented well by the current catalogue comparison.

The geographic split makes a local station artifact unlikely, while the three groups remain part of the same GMN reduction system. The external catalogues help, although their samples are small. CAMS misses the standalone activity cutoff by a small amount, SonotaCo has only four events, and the combined analysis was performed after those separate results were known. EDMOND adds historical breadth but is a compilation rather than a clean third instrument.

The sensitivity analysis shows stability across nearby thresholds. The bootstrap supports the angular drifts and mean orbit while leaving speed drift unresolved. The activity analysis supports a concentrated late-April interval; absolute flux and a precise annual maximum require additional exposure modeling.

The recovered source and exact reruns establish that the event list and numerical results are reproducible from the preserved implementation. The remaining taxonomic question is whether specialists consider the concentration a distinct stream.

## 6. Limitations

1. The analysis uses catalogue trajectories rather than new reductions of raw meteor images.
2. The antihelion source may contain finer structure than the chosen background captures.
3. The activity profile is relative to simultaneous antihelion counts; absolute flux and ZHR require station-level exposure modeling.
4. The geographic groups share GMN’s processing system.
5. The external samples are small, and the pooled CAMS–SonotaCo result is post-hoc.
6. EDMOND is a compiled archive, and its currently linked files differ from the advertised complete release.
7. Specialist comparison with obscure or differently parameterized shower solutions remains the key external check.
8. Dynamical origin modeling is outside the current analysis.
9. The fitted geocentric-speed drift remains unresolved.
10. Raw monthly GMN inputs remain available from their original public source rather than being duplicated as a complete archive here.

## 7. Conclusion

The GMN data contain a recurring, orbitally coherent concentration of late-April meteors that survives the project’s historical, source-matched, geographic, uncertainty, and sensitivity checks. The current official MDC catalogue contains no matching solution, and small historical samples in CAMS and SonotaCo support the same radiant, timing, and orbit.

The evidence supports specialist review and preparation of a formal submission package, with distinctness from known minor-shower and antihelion structure as the central remaining question.

## Data and code availability

The analysis code, 95-event GMN lookup table, draft mean records, saved validation results, and source-provenance record are included in this repository. The GMN trajectories and external catalogues remain available from their original public sources and should be used under the applicable data-use terms.

## References

Campello, R. J. G. B., Moulavi, D., & Sander, J. (2013). Density-based clustering based on hierarchical density estimates. *Advances in Knowledge Discovery and Data Mining*, 160–172. https://doi.org/10.1007/978-3-642-37456-2_14

Jenniskens, P., Jopek, T. J., Janches, D., Hajduková, M., Kokhirova, G. I., & Rudawska, R. (2020). On removing showers from the IAU Working List of Meteor Showers. *Planetary and Space Science, 182*, 104821. https://doi.org/10.1016/j.pss.2019.104821

Jopek, T. J., & Kaňuchová, Z. (2017). IAU Meteor Data Center—the shower database: a status report. *Planetary and Space Science, 143*, 3–6.

Shober, P. M. (2026). *Asteroidal non-shower meteor orbit subsets (CAMS, GMN, EDMOND, SonotaCo) used in Shober (2026, ApJ)* [Data set]. Zenodo record 18664293.

Southworth, R. B., & Hawkins, G. S. (1963). Statistics of meteor streams. *Smithsonian Contributions to Astrophysics, 7*, 261–285.

Vida, D., Šegon, D., Gural, P. S., Brown, P. G., McIntyre, M. J. M., Dijkema, T. J., et al. (2021). The Global Meteor Network—Methodology and first results. *Monthly Notices of the Royal Astronomical Society, 506*(4), 5046–5074. https://doi.org/10.1093/mnras/stab2008
