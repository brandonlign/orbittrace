# GhostStream methodology-novelty audit

## Verdict

**NO-GO for claiming that GhostStream currently introduces a new meteor-stream discovery method.**

The project combines several strong safeguards in one prospectively frozen chain, but the major ingredients already appear in prior meteor-stream research:

- density-based clustering in geocentric radiant–speed–solar-longitude space;
- measurement-error and false-positive testing;
- temporal verification using later or otherwise separate data;
- confirmation in an independent meteor network; and
- comparison with known-shower catalogues and orbital coherence.

The defensible description is therefore:

> GhostStream uses a prospectively frozen, multi-stage validation protocol assembled from established meteor-stream identification and confirmation practices.

This is rigorous methodology. It is not yet demonstrated methodological novelty.

## What prior work already establishes

### Density-based stream discovery

Sugar et al. (2017) applied DBSCAN to meteor trajectories using solar longitude, geocentric velocity, and Sun-centered ecliptic radiant. They included measurement errors, false-positive/false-negative analysis, and comparison with an established shower-detection method.

Peña-Asensio and Ferrari (2025) applied HDBSCAN to CAMS v3 using geocentric and orbital feature sets, varied the minimum cluster size and cluster-selection method, and compared its classifications with CAMS labels. Therefore neither density-based clustering nor HDBSCAN itself is novel to GhostStream.

### False-positive and background modeling

Moorhead (2016) developed shower-specific orbital-similarity cutoffs corresponding to a chosen false-positive rate.

Shober and Vaubaillon (2024) modeled the sporadic background with kernel-density estimation and generated synthetic samples to estimate false shower associations. Therefore simulation- or null-based false-positive control is established practice.

### Temporal holdout verification

Jenniskens et al. (2016) reported that CAMS detections originally derived from data through March 2013 were checked with the larger data set available through March 2015. The later data were used to verify the earlier detections, explicitly not to identify further showers or improve their median orbital elements. This is already a form of fixed temporal holdout verification.

GhostStream's untouched-year confirmation is stricter and more fully documented, but the general concept is not new.

### Independent-network confirmation

CAMS studies repeatedly used SonotaCo as an independent survey. Jenniskens and Nénon (2016) confirmed previously reported showers with CAMS, while Jenniskens et al. (2016) reported that many newly detected CAMS showers were also present in SonotaCo. A related verification study found that only 20 of 55 proposed high-threshold D-criterion detections produced convincing density enhancements in both CAMS and SonotaCo.

Therefore external-network replication is an established confirmation practice, not a GhostStream invention.

### Independent identification and catalogue comparison

Rudawska et al. (2015) independently identified showers in EDMOND using orbital grouping followed by comparison in geocentric parameters and against the IAU MDC list. Matlovič et al. (2023) later applied a modified version to three populous EDMOND years. Independent catalogue-wide identification and duplicate checking are established.

## What is distinctive about GhostStream

The project combines the following sequence with unusually explicit locking and provenance:

1. blind candidate generation without a supplied target month or radiant;
2. fixed candidate center, widths, timing, drift treatment, and decision gates;
3. untouched-year confirmation without refitting;
4. activity selection using radiant, speed, and time, followed by a separate orbital-coherence test;
5. source- and time-matched nulls;
6. measurement-error trials, clustered bootstrap, geographic splits, and an 81-cell sensitivity grid;
7. unchanged-template tests in complete usable external catalogues; and
8. preserved negative, near-pass, and supplementary outcomes rather than threshold repair.

This exact integrated sequence was not found in the papers reviewed here. However, an unlocated identical sequence is not enough to establish novelty, because its components and the central holdout/replication logic already exist.

## Allowed claims

- "prospectively frozen multi-stage validation protocol"
- "rigorous separation of candidate generation and confirmation"
- "untouched-year and unchanged-template external validation"
- "an integrated validation design assembled from established statistical and meteor-science practices"
- "the protocol is more extensively documented than typical catalogue searches reviewed here"

## Claims not currently supported

- "a new meteor-stream discovery method"
- "the first use of HDBSCAN for meteor streams"
- "the first temporal holdout validation of a meteor shower"
- "the first independent-network replication of a meteor shower"
- "a demonstrated reduction in false discoveries compared with existing methods"

## What would create a methods contribution

A controlled benchmark must compare a pooled or same-data workflow with the prospectively frozen holdout workflow on known showers, injected weak streams, and null controls. The methods claim becomes defensible only if the frozen protocol measurably reduces false candidate survival while retaining useful recovery.

The benchmark is preregistered separately in `BENCHMARK_PROTOCOL.md`. Until it is executed, GhostStream's main contribution remains the astronomical candidate and its unusually strong validation, not a new algorithm.

## Literature reviewed

- Jenniskens, P., Nénon, Q., Gural, P. S., et al. (2016). CAMS newly detected meteor showers and the sporadic background. *Icarus, 266*, 384–409. https://doi.org/10.1016/j.icarus.2015.11.009
- Jenniskens, P., & Nénon, Q. (2016). CAMS confirmation of previously reported meteor showers. *Icarus, 266*, 355–370. https://doi.org/10.1016/j.icarus.2015.08.014
- Jenniskens, P., Nénon, Q., Albers, J., et al. (2016). CAMS verification of single-linked high-threshold D-criterion detected meteor showers. *Icarus, 266*, 371–383. https://doi.org/10.1016/j.icarus.2015.10.004
- Matlovič, P., et al. (2023). Independent identification of meteor showers from the EDMOND and the search for their parent bodies. *Planetary and Space Science, 236*, 105752. https://doi.org/10.1016/j.pss.2023.105752
- Moorhead, A. V. (2016). Performance of D-criteria in isolating meteor showers from the sporadic background in an optical data set. *MNRAS, 455*, 4329–4338. https://doi.org/10.1093/mnras/stv2610
- Peña-Asensio, E., & Ferrari, F. (2025). Meteoroid Stream Identification with HDBSCAN Unsupervised Clustering Algorithm. *The Astronomical Journal, 170*, 140. https://doi.org/10.3847/1538-3881/adec8c
- Rudawska, R., Matlovič, P., Tóth, J., & Kornoš, L. (2015). Independent identification of meteor showers in EDMOND database. *Planetary and Space Science, 118*, 38–47. https://doi.org/10.1016/j.pss.2015.07.011
- Shober, P. M., & Vaubaillon, J. (2024). A generalizable method for estimating meteor shower false positives. *Astronomy & Astrophysics, 686*, A93. https://doi.org/10.1051/0004-6361/202348476
- Sugar, G., Moorhead, A., Brown, P., & Cooke, W. (2017). Meteor shower detection with density-based clustering. *Meteoritics & Planetary Science, 52*, 1048–1059. https://doi.org/10.1111/maps.12856
