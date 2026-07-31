# An Uncatalogued Annual April Meteor Stream Identified in Global Meteor Network Trajectories

**Draft manuscript — not submitted**

**Author:** Brandon Li  
**Affiliation:** John L. Miller Great Neck North High School, Great Neck, New York, USA  
**Corresponding author:** [email to be added]

## Abstract

A blind search for weak meteor streams was conducted using public Global Meteor Network (GMN) trajectory catalogues. Candidate structures were detected in a joint radiant–speed–time representation and then evaluated with orbital coherence, independent-year replication, measurement-uncertainty cloning, source-preserving null tests, and comparison against the International Astronomical Union Meteor Data Center (IAU MDC) shower catalogue. One compact structure discovered in April 2026 survived the complete audit. A frozen template identified 95 members in five significant GMN years from 2022 through 2026. In the two untouched confirmation years, 2022 and 2023, the pooled activity enhancement remained significant after a twelve-month familywise correction (p = 1.86 × 10⁻⁵), while a source- and time-matched orbital null gave p = 1.0 × 10⁻⁴. No orbital element was used to select the final activity enhancement. The refined GMN orbit is q = 0.0792 AU, e = 0.9463, i = 24.71°, ω = 333.49°, and Ω = 37.94°. Ten additional meteors in the independently reduced CAMS and SonotaCo archives span 2011, 2012, 2022, 2023, and 2025; their pooled medoid is separated from the GMN orbit by D = 0.0172. No matching solution was found among 2,174 parsed IAU MDC shower solutions. These results support an uncatalogued annual meteor-stream candidate active in late April. The stream is not claimed as established pending expert duplicate review, publication, and IAU MDC evaluation.

## 1. Introduction

Meteor streams are commonly identified as concentrations in radiant, velocity, encounter time, and orbital-element space. Weak streams are difficult to distinguish from the structured sporadic background, especially near the broad helion and antihelion sources. A clustering method can therefore generate convincing false positives if its null model destroys real source correlations or if orbital node is used both to select and to test an activity enhancement.

The Global Meteor Network provides a large, public, multi-station trajectory catalogue with sufficient precision for meteor-shower studies. Its wide geographic coverage and repeated annual observations make it suitable for blind discovery followed by independent-year validation. The present study developed an uncertainty-aware search in which candidate generation was separated from confirmatory testing.

The goals were to:

1. recover established showers and injected weak streams before beginning a novelty search;
2. identify residual structures without using known-shower labels as positive training targets;
3. reject known and working-list showers using activity-aware catalogue matching;
4. require replication in data not used to choose the candidate;
5. test activity inside a source-preserving background without using orbital elements; and
6. seek support in independently reduced meteor-orbit archives.

## 2. Data

### 2.1 Global Meteor Network

Monthly GMN trajectory catalogues from 2019 through July 2026 were accessed through the public GMN data service. Only multi-station trajectories were retained. The principal quality requirements were:

- at least two participating stations;
- median trajectory-fit error no greater than 180 arcsec;
- finite geocentric radiant, speed, and orbital elements;
- geocentric speed between 5 and 75 km s⁻¹; and
- a GMN shower label corresponding to sporadic activity.

Multiple trajectory solutions with the same event time were deduplicated. The solution with the lowest fit error was retained, with station count used as a secondary criterion.

### 2.2 Independent archives

The frozen candidate was later tested in:

- the official legacy CAMS orbit catalogue covering 2010–2013; and
- permanent SonotaCo annual catalogues for 2022–2025.

The independent-catalogue tests used the GMN-derived center, drift, widths, and activity interval without refitting.

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

These tests established that the search had useful, though incomplete, sensitivity to diffuse low-member streams.

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

### 3.5 Orbital coherence and uncertainty

Orbital compactness was measured with a five-element orbital dissimilarity statistic based on eccentricity, perihelion distance, orbital-plane angle, and perihelion-direction angle. Null groups were drawn from meteors observed in the same time and broad antihelion source but outside the narrow radiant–speed core.

Measurement uncertainties were propagated through 1,000 clone trials. A clone trial passed only if the median and 90th-percentile orbital dispersions remained below frozen thresholds.

### 3.6 Independent-catalogue test

CAMS and SonotaCo meteors were selected using only the frozen GMN radiant, speed, drift, and activity interval. Orbit was tested afterward. Archive-specific thresholds were set before examining each result. Because both archives were sparse, a pooled cross-archive test was later performed and is labeled exploratory rather than preregistered.

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

The result therefore remains localized in time and orbit even when the broad antihelion source is preserved and orbital elements are excluded from activity selection.

### 4.3 Radiant and speed

At solar longitude 36.902°, the drift-corrected solution is:

- Sun-centered ecliptic longitude = −149.376°;
- ecliptic latitude = +7.323°;
- geocentric right ascension ≈ 246.96°;
- geocentric declination ≈ −14.34°; and
- geocentric speed = 37.642 km s⁻¹.

The measured drift per degree of solar longitude is:

- −0.10295° in Sun-centered ecliptic longitude;
- −0.02305° in ecliptic latitude; and
- −0.02935 km s⁻¹ in geocentric speed.

The IAU MDC arithmetic-mean record calculated directly from the 95 lookup-table meteors has solar longitude 37.150°, RA 247.170°, Dec −14.343°, and Vg 37.618 km s⁻¹.

### 4.4 Orbit

The robust GMN medoid orbit is:

| Element | Value |
|---|---:|
| a | 1.475 AU |
| q | 0.0792 AU |
| e | 0.9463 |
| i | 24.709° |
| ω | 333.494° |
| Ω | 37.937° |

The full GMN sample has median orbital D = 0.04398 and 90th-percentile D = 0.09232. All 1,000 uncertainty-clone trials passed the frozen compactness requirements.

### 4.5 Independent archives

Legacy CAMS contained six strict matches in 2011–2012. Their median orbital D was 0.05068, and their source-matched orbit-null p-value was 0.0001. The archive-specific activity test gave p = 0.01251, narrowly above the frozen p ≤ 0.01 threshold.

SonotaCo contained four strict matches in 2022, 2023, and 2025. Their activity p-value was 0.00715, median orbital D was 0.03614, and orbit-null p-value was 0.0001, but the sample did not reach the frozen minimum member count.

The explicitly post-hoc pooled synthesis contained ten meteors across five years:

- activity p = 1.622 × 10⁻⁴;
- shifted-window p = 0.02041;
- median orbital D = 0.04879;
- orbit-null p = 5 × 10⁻⁵; and
- medoid distance from the GMN orbit = 0.01723.

### 4.6 Catalogue and parent-body checks

No hard match was found among 2,174 parsed IAU MDC shower solutions. The nearest official orbit was the Northern May Ophiuchids at D ≈ 0.235, but its activity epoch and radiant do not match the candidate.

A NASA/JPL Small-Body Database screen found no credible parent. The nearest listed object had D ≈ 0.159 but an uncertainty-code-8 orbit based on an 11-day observational arc. No parent-body association is proposed.

## 5. Discussion

The strongest evidence for a real stream is the conjunction of five properties: recurrence across five GMN years, confirmation in untouched years, a source-preserving activity excess, orbital coherence after non-orbital selection, and matching historical meteors in two independent archives.

The candidate is not merely defined by an orbital node near the date of observation. The final activity test excludes all orbital elements, and the orbit remains far more compact than source- and time-matched null samples. The candidate also survives when embedded inside a deliberately expanded antihelion background, reducing the risk that it is an artifact of a conventional source boundary.

The independent evidence is supportive but not definitive. CAMS and SonotaCo contain only ten matching meteors in total. Each archive is individually underpowered under at least one frozen rule, and their pooled analysis was motivated after observing the separate sparse results. A fresh independent network analysis using a preregistered pipeline is therefore the most valuable next validation.

The absence of a credible known parent is not evidence against the stream. Weak meteoroid streams may have unrecognized, poorly determined, dormant, or dynamically evolved parents. Dynamical integrations would be premature until a plausible parent-body shortlist exists.

## 6. Limitations

1. The discovery and confirmatory analyses use public catalogue-level trajectories rather than raw image re-reductions.
2. The broad antihelion source has complex internal structure that may not be captured completely by the chosen null.
3. The observed activity bounds are limited by the frozen selection interval and are not exposure-corrected flux bounds.
4. The independent pooled test is post-hoc.
5. The literature and duplicate-shower audit cannot guarantee that no obscure historical solution uses a different convention or incomplete orbit.
6. No dynamical parent-body connection has been demonstrated.

## 7. Conclusion

A blind search of GMN trajectories identified an annual late-April meteor-stream candidate with a compact radiant and orbit. The candidate is significant in five consecutive GMN years, survives a node-independent source-preserving test, and receives historical support from CAMS and SonotaCo. No matching IAU MDC solution or credible parent body was found. The result warrants submission to the IAU MDC and independent expert review, but it should remain described as an uncatalogued discovery candidate until publication and formal evaluation.

## Data and code availability

The GMN trajectory catalogues are publicly available through the Global Meteor Network. The frozen search, validation scripts, lookup table, candidate solution, and audit outputs are preserved in the project repository. The IAU MDC lookup table accompanying this draft contains the 95 GMN meteors used for the arithmetic-mean submission record.

## References

Campello, R. J. G. B., Moulavi, D., & Sander, J. (2013). Density-based clustering based on hierarchical density estimates. *Advances in Knowledge Discovery and Data Mining*, 160–172. https://doi.org/10.1007/978-3-642-37456-2_14

Jenniskens, P., Jopek, T. J., Janches, D., Hajduková, M., Kokhirova, G. I., & Rudawska, R. (2020). On removing showers from the IAU Working List of Meteor Showers. *Planetary and Space Science, 182*, 104821. https://doi.org/10.1016/j.pss.2019.104821

Jopek, T. J., & Kaňuchová, Z. (2017). IAU Meteor Data Center—the shower database: a status report. *Planetary and Space Science, 143*, 3–6.

Southworth, R. B., & Hawkins, G. S. (1963). Statistics of meteor streams. *Smithsonian Contributions to Astrophysics, 7*, 261–285.

Vida, D., Šegon, D., Gural, P. S., Brown, P. G., McIntyre, M. J. M., Dijkema, T. J., et al. (2021). The Global Meteor Network—Methodology and first results. *Monthly Notices of the Royal Astronomical Society, 506*(4), 5046–5074. https://doi.org/10.1093/mnras/stab2008
