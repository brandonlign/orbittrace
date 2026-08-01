# An Uncatalogued Annual April Meteor-Stream Candidate in Global Meteor Network Data

**Working manuscript — not submitted**

**Author:** Brandon Li  
**Affiliation:** John L. Miller Great Neck North High School, Great Neck, New York, USA  
**Corresponding author:** [to be added]

## Abstract

I searched public Global Meteor Network (GMN) trajectory catalogues for weak meteor streams not represented in the IAU Meteor Data Center (MDC) shower catalogue. Candidate groups were found in Sun-centered radiant, geocentric-speed, and encounter-time space, then tested for orbital coherence, recurrence in other years, separation from the antihelion background, measurement uncertainty, geographic consistency, sensitivity to nearby analysis choices, and support in other meteor-orbit catalogues.

One late-April group survived the complete analysis. The confirmed GMN sample contains 95 meteors from 2022 through 2026. A pooled test using 2022–2023, which was not used to choose the candidate, gave an activity p-value of 1.86 × 10⁻⁵ after a twelve-month familywise rule and a source/time-matched orbit-null p-value of 1.0 × 10⁻⁴. Orbital elements were not used to select the activity enhancement. The signal appears in three non-overlapping GMN station groups, passes all 81 tested combinations of nearby quality cuts and window widths, and remains stable in 20,000 year/night bootstrap samples. Six CAMS meteors and four SonotaCo meteors provide the main external support. Six additional meteors occur in a shower-removed EDMOND subset, although EDMOND’s compiled provenance limits how independently that sample can be interpreted.

A checksum-locked comparison with 2,174 official MDC solutions found no matching shower under the fixed timing, radiant, speed, and orbital criteria. The evidence supports a recurring, apparently uncatalogued late-April meteor-stream candidate. Independent specialist review is still needed before an MDC or journal submission.

## 1. Introduction

Weak meteor streams are difficult to distinguish from the structured sporadic background. A compact cluster alone is not enough, especially near the broad helion and antihelion sources, where radiant, speed, and time are already correlated.

A credible weak-stream candidate should recur in multiple years, survive reasonable changes in analysis choices, remain visible across different parts of the observing network, have an orbit more compact than an appropriate local background, and not be an alternate solution for a known shower.

The Global Meteor Network provides public multi-station trajectory catalogues with broad geographic coverage and repeated annual observations. I used those catalogues for a blind search, then tested the surviving candidate in years and external catalogues that were not used to choose it.

## 2. Data

### 2.1 Global Meteor Network

Monthly GMN trajectory catalogues from 2019 through July 2026 were downloaded from the public GMN service. The discovery search used trajectories labelled as sporadic by GMN and required at least two participating stations, median trajectory-fit error no greater than 180 arcsec, finite radiant and orbital quantities, and geocentric speed between 5 and 75 km/s.

When multiple solutions shared the same event time, the solution with the lowest fit error was retained, with station count used as a secondary criterion. The January–July 2026 data were used for the blind rediscovery. Earlier years were examined only after the April candidate definition had been fixed.

### 2.2 External catalogues

The fixed candidate was later applied to the legacy CAMS orbit catalogue, permanent SonotaCo annual catalogues, and a shower-removed EDMOND subset published with Shober (2026). Because EDMOND combines observations from contributing networks, it is treated as supplementary evidence rather than as a wholly independent third instrument.

### 2.3 Known-shower and parent-body data

The candidate was compared with every parsable solution in the official IAU MDC full shower-data catalogue, including working-list entries. A NASA/JPL Small-Body Database search was used for a broad parent-body screen after the meteor-stream solution had been established.

## 3. Methods

### 3.1 Method controls

The Lyrids, Eta Aquariids, and Southern Delta Aquariids were used as positive controls. A flawed early control rule rejected any cluster larger than 30% of a sample; Eta Aquariids themselves exceeded that fraction, making the rule incompatible with high recall. The failure was retained in the record. Before the independent 2024 holdouts were examined, the rule was corrected so that the 30% limit applied to the largest non-target cluster. The three 2024 holdout F1 scores were 0.902, 0.957, and 0.927.

Synthetic weak streams were also inserted into real sporadic backgrounds. Four of nine 20-member injections, seven of nine 40-member injections, and eight of nine 80-member injections were recovered.

### 3.2 Blind search

Each meteor was represented by Sun-centered geocentric ecliptic radiant longitude, geocentric ecliptic radiant latitude, geocentric speed, and solar longitude. The feature scales were 3.5°, 3.0°, 2.5 km/s, and 2.5°. HDBSCAN was run with `min_cluster_size = 12`, `min_samples = 4`, and leaf cluster selection.

Candidates had to contain 12–300 members, appear on at least four nights and six stations, avoid domination by one night or station set, and have at least 80% valid orbits. Median and 90th-percentile orbital distances had to remain below fixed limits. Alternating-night split tests, local time permutations, broad sporadic-source vetoes, and known-shower comparisons were applied before a candidate could proceed.

The January–July 2026 rerun produced one full-gate survivor, in April. No other month produced a full-gate candidate.

### 3.3 Historical confirmation and background test

The April center, drift, widths, and activity interval were fixed before earlier years were tested. A year counted as significant only when both the activity test and the post-selection orbital test passed.

The pooled 2022–2023 sample was reserved as an untouched confirmation. The final background placed the candidate inside a deliberately broad antihelion region. Candidate selection used radiant, speed, and solar longitude only. No orbital element, including node, entered the activity selection. Orbital compactness was evaluated afterward against source- and time-matched comparison groups.

### 3.4 Uncertainty and robustness

Reported trajectory uncertainties were used to perturb the events and repeat the complete selection and compactness checks 1,000 times.

A separate clustered bootstrap generated 20,000 samples by resampling years and then observing nights within years. All meteors from a selected night were retained. This accounts for the dependence among meteors observed on the same night.

The GMN sample was also split into three non-overlapping geographic station groups. Finally, the candidate was re-evaluated under all 81 combinations of three fit-error limits, three minimum station counts, three radiant/speed core widths, and three activity windows.

### 3.5 External catalogues and catalogue comparison

The GMN solution was not refitted to CAMS, SonotaCo, or EDMOND. After the bootstrap showed that geocentric-speed drift was not resolved, external tests were repeated with that slope set to zero while retaining the same radiant center, angular drift, widths, activity interval, and orbital rules.

A direct MDC match required compatible activity timing, a drifted-radiant separation no greater than 5°, a speed difference no greater than 5 km/s, and a complete orbit with D_SH ≤ 0.15. Timing/radiant/speed near matches with incomplete orbits were recorded separately.

## 4. Results

### 4.1 Recurrence

The fixed selection found 101 deduplicated meteors from 2019–2026. Five consecutive years passed the individual tests.

| Year | Members | Activity p-value | Orbit-null p-value |
|---:|---:|---:|---:|
| 2022 | 10 | 0.003970 | 0.0001 |
| 2023 | 8 | 0.002168 | 0.0001 |
| 2024 | 14 | 4.888 × 10⁻⁵ | 0.0001 |
| 2025 | 34 | 9.42 × 10⁻⁹ | 0.0001 |
| 2026 | 29 | 4.13 × 10⁻⁶ | 0.0001 |

The pooled untouched 2022–2023 sample gave an activity p-value of 1.857 × 10⁻⁵, a shifted-window p-value of 0.01754, and an orbit-null p-value of 0.0001.

### 4.2 Mean solution and timing

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

A March–May activity profile supports a contiguous interval from solar longitude 35.902° to 39.902°. The highest half-degree bin was centered at 38.652°, but that exact peak shifted when individual years were removed, so the broader four-degree interval is the more stable result.

The 95-event sample had median orbital D = 0.04398 and 90th-percentile D = 0.09232. All 1,000 measurement-error trials passed the fixed compactness requirements.

### 4.3 Bootstrap and geographic split

The clustered bootstrap gave:

| Drift | Point estimate | 95% interval |
|---|---:|---:|
| dRA/dλ⊙ | +0.887°/° | +0.672 to +1.040 |
| dDec/dλ⊙ | −0.158°/° | −0.248 to −0.037 |
| dVg/dλ⊙ | −0.029 km/s/° | −0.178 to +0.221 |

The angular drifts exclude zero. The speed interval does not, so no physical speed drift is claimed.

| Region | Members | Activity p-value | Median D | Orbit-null p-value |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41 × 10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26 × 10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16 × 10⁻¹⁰ | 0.04795 | 0.0001 |

The largest distance between regional medoid orbits was 0.04054.

### 4.4 Sensitivity analysis

All 81 tested settings passed. Membership ranged from 29 to 129, median orbital D ranged from 0.03640 to 0.05548, and the largest activity p-value was 8.55 × 10⁻⁷. These settings overlap heavily and are interpreted as a sensitivity analysis, not as independent replications.

### 4.5 External catalogues

CAMS contributed six matching meteors from 2011–2012. SonotaCo contributed four from 2022, 2023, and 2025. Their post-hoc pooled result contained ten meteors and gave an activity p-value of 1.622 × 10⁻⁴, shifted-window p-value of 0.02041, median D of 0.04879, orbit-null p-value of 5 × 10⁻⁵, and medoid distance from the GMN orbit of 0.01723.

The shower-removed EDMOND subset contributed six additional non-overlapping meteors. Their archive-specific activity p-value was 0.01206 and median D was 0.03669. This sample did not meet the project’s standalone N ≥ 8 and p ≤ 0.01 rules.

### 4.6 Known showers and parent-body screen

The MDC comparison found no direct match, no timing/radiant/speed near match, and no near match hidden by missing orbital elements. The nearest complete orbit was Northern May Ophiuchids solution 004 at D_SH = 0.23445, with a non-overlapping activity interval and a 9.59° radiant separation at the candidate epoch.

The JPL screen evaluated 729 valid broadly compatible orbits. None had D ≤ 0.15. The nearest object, 2023 HJ7 at D = 0.15939, had a poorly determined orbit based on an 11-day observational arc. No parent-body association is proposed.

## 5. Discussion

The case for a real stream comes from the combination of annual recurrence, untouched-year confirmation, activity selection without orbital elements, post-selection orbital compactness, geographic consistency, robustness to nearby analysis choices, and matching meteors in other catalogues. No single test carries the result by itself.

The antihelion background remains the most important scientific concern. The candidate survives inside a broad source definition, but a specialist may recognize a narrower source component or historical shower solution not represented well by the current catalogue comparison.

The geographic split makes a local station artifact unlikely, but the three groups are not independent reductions. The external samples help, although they are small. CAMS narrowly misses the standalone activity cutoff, SonotaCo has only four events, and the combined analysis was performed after the separate results were known. EDMOND adds historical breadth but is a compilation rather than a clean third instrument.

The recovered source and clean reruns show that the event list and numerical results are reproducible from the preserved implementation. Computational reproducibility does not answer the remaining taxonomic question: whether this concentration should be recognized as a distinct shower.

## 6. Limitations

1. The analysis uses catalogue trajectories rather than new reductions of raw meteor images.
2. The antihelion source may contain structure not fully represented by the chosen background.
3. The activity profile is relative to simultaneous antihelion counts and is not an absolute flux or ZHR measurement.
4. The geographic groups share GMN’s processing system.
5. The external samples are small, and the pooled CAMS–SonotaCo result is post-hoc.
6. EDMOND is a compiled archive whose currently linked files do not match the advertised complete release.
7. No specialist has completed an independent review of obscure or differently parameterized shower solutions.
8. No parent body or dynamical origin has been established.
9. The fitted geocentric-speed drift is not resolved from zero.

## 7. Conclusion

The GMN data contain a recurring, orbitally coherent concentration of late-April meteors that survives the historical, source-matched, geographic, uncertainty, and sensitivity checks used here. The current official MDC catalogue contains no matching solution, and small historical samples in CAMS and SonotaCo support the same radiant, timing, and orbit.

The evidence is strong enough to justify independent expert review and preparation of a formal submission package. It is not yet enough to describe the object as an officially discovered or established meteor shower.

## Data and code availability

The analysis code, 95-event GMN lookup table, draft mean records, saved validation results, and source-provenance record are included in this repository. The GMN trajectories and external catalogues remain available from their original public sources and should be used under the applicable data-use terms.

## References

Campello, R. J. G. B., Moulavi, D., & Sander, J. (2013). Density-based clustering based on hierarchical density estimates. *Advances in Knowledge Discovery and Data Mining*, 160–172.

Jenniskens, P., Jopek, T. J., Janches, D., Hajduková, M., Kokhirova, G. I., & Rudawska, R. (2020). On removing showers from the IAU Working List of Meteor Showers. *Planetary and Space Science, 182*, 104821.

Jopek, T. J., & Kaňuchová, Z. (2017). IAU Meteor Data Center—the shower database: a status report. *Planetary and Space Science, 143*, 3–6.

Shober, P. M. (2026). *Asteroidal non-shower meteor orbit subsets (CAMS, GMN, EDMOND, SonotaCo) used in Shober (2026, ApJ)* [Data set]. Zenodo record 18664293.

Southworth, R. B., & Hawkins, G. S. (1963). Statistics of meteor streams. *Smithsonian Contributions to Astrophysics, 7*, 261–285.

Vida, D., Šegon, D., Gural, P. S., Brown, P. G., McIntyre, M. J. M., Dijkema, T. J., et al. (2021). The Global Meteor Network—Methodology and first results. *Monthly Notices of the Royal Astronomical Society, 506*(4), 5046–5074.
