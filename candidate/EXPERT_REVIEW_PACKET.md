# GhostStream April candidate — external expert review packet

Last updated: 2026-08-01

## Purpose

This packet requests a critical meteor-science review of an uncatalogued annual late-April meteor-stream candidate identified blindly in public Global Meteor Network (GMN) trajectories.

The requested decision is not whether the analysis is impressive. It is whether the evidence, coordinate conventions, orbit conventions, null models, and duplicate-shower audit support:

1. a provisional submission to the IAU Meteor Data Center (MDC);
2. preparation of a peer-reviewed discovery paper; and
3. the claim boundary stated below.

Please identify any fatal error, likely known-shower duplicate, hidden circularity, or analysis that must be completed before external submission.

## Requested reviewer verdict

Please select one:

- **A — Suitable for MDC submission after minor corrections**
- **B — Scientifically promising, but requires a new analysis or additional data before MDC submission**
- **C — Likely a duplicate of a known, working-list, removed, or historically published shower**
- **D — Likely structured sporadic-source contamination rather than a distinct stream**
- **E — A methodological, coordinate, or orbit-convention error invalidates the candidate**

Please state the specific evidence supporting the verdict.

## Claim being reviewed

> A blind, uncertainty-aware analysis of public GMN trajectories identified a high-confidence uncatalogued annual meteor-stream candidate active in late April. It recurs in five GMN years, survives source-preserving and post-selection orbital null tests, reproduces across three disjoint GMN geographic station groups, passes a frozen 81-cell specification grid, and receives historical support from CAMS and SonotaCo. It is not yet an official IAU discovery or an established shower.

No official name, IAU code, established status, absolute flux, parent body, or detected physical geocentric-speed drift is claimed.

## Recovered implementation and clean reruns

The original executable analysis was initially absent from the main project branch, but it had survived in two immutable temporary runner commits. Those exact source trees are now preserved in the review bundle with file-level SHA-256 provenance:

- recovery/discovery controls: 13 files from commit `4175e5187fcc6faf3d1befb099a9e35be96850f2`;
- novel-search/downstream analysis: 35 files from commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`.

The recovered implementation was rerun without retuning.

### Exact primary reproduction

- selected GMN events from 2019–2026: **101**;
- exact annual counts: **1, 4, 1, 10, 8, 14, 34, 29**;
- significant-year events from 2022–2026: **95**;
- committed lookup timestamps recovered: **95/95**;
- missing preserved timestamps: **0**;
- additional timestamps: **0**;
- validator verdict: `APRIL_STREAM_DISCOVERY_CANDIDATE_SURVIVES_AUDIT`.

### Exact internal downstream reproduction

The recovered source regenerated and passed:

- untouched 2022–2023 source-preserving activity p = **1.857134 × 10⁻⁵**;
- shifted-window p = **0.0175439**;
- source/time-matched orbit-null p = **0.0001**;
- year/night bootstrap: **95 members, 29 nights, 20,000 replicates per scheme**;
- resolved RA and Dec drift, unresolved speed drift;
- corrected activity core: solar longitude **35.902°–39.902°**;
- geographic member counts: **30 / 22 / 44**;
- maximum cross-region medoid distance: **D = 0.0405368**;
- frozen specification grid: **81/81 eligible cells passed**.

### Exact external reproduction

The recovered archive scripts regenerated the preserved member sets:

- CAMS: **6** events in 2011–2012;
- SonotaCo: **4** events in 2022, 2023, and 2025;
- pooled CAMS + SonotaCo synthesis: exact preserved **10-event ID set**;
- pooled activity p = **1.6218438847 × 10⁻⁴**;
- pooled shifted-window p = **0.0204082**;
- pooled median orbital distance = **0.0487914**;
- pooled orbit-null p = **5 × 10⁻⁵**;
- pooled medoid distance from the refined GMN orbit = **0.0172305**.

CAMS narrowly misses its standalone activity threshold, and SonotaCo is below the frozen minimum member count. Their pooled result is explicitly post-hoc and is supporting evidence, not a preregistered independent discovery.

## Two orbit representations used for different purposes

The project distinguishes the **frozen robust candidate solution** used for membership and similarity testing from the **arithmetic-mean MDC draft record** calculated from the 95 confirmed GMN members.

### Frozen robust solution at solar longitude 36.901963°

| Quantity | Value |
|---|---:|
| Sun-centered ecliptic longitude | −149.376325° |
| Geocentric ecliptic latitude | +7.323038° |
| Approximate geocentric RA | 247.06° |
| Approximate geocentric Dec | −14.22° |
| Geocentric speed | 37.641692 km/s |
| q | 0.079202 AU |
| e | 0.946296 |
| i | 24.709376° |
| ω | 333.493819° |
| encounter Ω | 37.937477° |
| a | 1.474788 AU |
| period | 1.790995 yr |
| Tisserand parameter relative to Jupiter | 3.8416 |

Activity core: solar longitude **35.902°–39.902°**.

The fitted geocentric-speed drift is not statistically resolved and is not claimed as physical. Final external-archive tests fix `dVg/dλ⊙ = 0`.

### Arithmetic-mean MDC draft record from 95 members

| Quantity | Submitted value |
|---|---:|
| Mean solar longitude | 37.149520° |
| Geocentric RA | 247.169746° |
| Geocentric Dec | −14.342743° |
| Geocentric speed | 37.617513 km/s |
| q | 0.080114 AU |
| e | 0.943593 |
| i | 24.370030° |
| ω | 333.636995° |
| Ω | 37.157321° |
| a | 1.420285 AU |
| N | 95 |

The submitted semimajor axis is calculated from the submitted six-decimal q and e:

`0.080114 / (1 − 0.943593) = 1.420284716... AU`, rounded to `1.420285 AU`.

The separate full-precision means imply `a = 1.420295780... AU` and remain preserved in the calculation audit. Please advise whether this submitted-precision convention is appropriate for the MDC.

## Main evidence

### Blind discovery and recurrence

- The candidate arose from an all-season discovery search rather than a targeted April query.
- The frozen template selected 101 deduplicated GMN events from 2019–2026.
- Five consecutive years passed the individual confirmation gate:
  - 2022: 10
  - 2023: 8
  - 2024: 14
  - 2025: 34
  - 2026: 29
- The 95 events in those five significant years form the MDC lookup table.
- Untouched 2022–2023 pooled activity p = **1.857 × 10⁻⁵** after the twelve-month familywise rule.
- Untouched source/time-matched orbit-null p = **0.0001**.

A clean blind-rediscovery rerun is included separately when available. Its gate requires the recovered all-season search to find the April survivor and validate it in 2024 and 2023 without being supplied the final month or 95-event lookup.

### Non-circular source-preserving selection

The final activity selection uses only:

- Sun-centered radiant longitude;
- ecliptic latitude;
- geocentric speed; and
- solar longitude.

No eccentricity, perihelion distance, inclination, argument of perihelion, or node is used to select the activity enhancement. Orbital coherence is evaluated afterward inside an expanded antihelion-source background.

### Orbit and uncertainty

- GMN median orbital distance = **0.04398**.
- GMN q90 orbital distance = **0.09232**.
- Maximum significant-year medoid separation = **0.05044**.
- Measurement-error clone trials: **1,000/1,000 passed**.
- Frozen specification curve: **81/81 cells passed**.

### Geographic replication within GMN

| Region | Members | Activity p | Median D | Orbit-null p |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41×10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26×10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16×10⁻¹⁰ | 0.04795 | 0.0001 |

These trajectory sets are disjoint but share the GMN reduction system; they are not represented as independent reductions.

## EDMOND evidence and release limitation

A shower-removed EDMOND subset contributes six non-overlapping orbitally compact events in 2014, 2016, 2017, and 2022. Its standalone activity p = **0.01206** and N = **6**, so it is supporting rather than independently decisive.

The unchanged template was also applied to every annual file currently linked by the public EDMOND page. It recovered exactly the same six events and no additional events. However:

- 23 readable annual ZIPs cover 2001–2023;
- the advertised 2024 ZIP returns HTTP 404;
- linked rows for 2001–2023: **481,252**;
- advertised rows for those years: **614,758**;
- coverage: **78.283%**;
- annual row-count matches: **0/23**;
- embedded versions are predominantly **513/516**, not 601.

This is not described as a complete v6.01 replication or as a fully independent third instrument.

## Novelty and current parent screen

The checksum-locked official IAU MDC refresh used catalogue version **2026-06-25**:

- shower records: **1,072**;
- submitted solutions: **2,174**;
- hard duplicate matches: **0**;
- activity-compatible radiant–speed near matches: **0**;
- orbit-incomplete near matches: **0**;
- catalogue SHA-256: `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`.

The nearest complete catalogue orbit is Northern May Ophiuchids solution 004 at `D_SH = 0.23445`, with a non-overlapping activity interval and a 9.59° drifted-radiant separation.

The freshly rerun JPL screen returned:

- broad-compatible objects fetched and evaluated: **729/729**;
- objects at D ≤ 0.15: **0**;
- objects at D ≤ 0.25: **2**;
- nearest: **2023 HJ7**, D = **0.1593946**;
- nearest condition code: **8**;
- nearest observational arc: **11 days**.

No parent body is claimed.

## Official checker and package audit

The exact committed 95-member mean record was run through both the distributed official MDC Linux binaries and a fresh GNU Fortran build of the distributed source. Both produced byte-identical comparison files and zero orbital/geocentric error records. This validates internal radiant/orbit consistency only, not novelty or membership.

The recovered package audit recomputes lookup-table quantities, checks the mean JSON, legacy record, calculation audit, official checker inputs, live catalogue provenance, EDMOND boundary, manuscript and final summary, and verifies the recovered source plus primary, downstream, and external clean-rerun evidence. Its machine-readable report and complete file-hash manifest are included in the bundle.

## Questions requiring expert judgment

### Coordinate and orbit conventions

- Are the geocentric J2000 radiant, Sun-centered ecliptic radiant, encounter-node, and argument-of-perihelion conventions internally correct?
- Is the 180° node/perihelion normalization used for historical video archives appropriate in every source?
- Is the frozen robust/medoid solution appropriate for membership and similarity testing?
- Is the arithmetic-mean 95-member solution appropriate for MDC submission?
- Should q, e, and a be supplied with more precision or with a different semimajor-axis convention?

### Duplicate-shower risk

- Does any established, working-list, removed, or literature-only shower plausibly match this epoch, drifted radiant, speed, and orbit despite failing the current automated veto?
- Is Northern May Ophiuchids or another Ophiuchid/Virginid/antihelion-complex solution credible under another convention?
- Which historical catalogues or papers should be checked manually?

### Antihelion-source interpretation

- Is the expanded antihelion null sufficiently conservative?
- Does the four-degree activity enhancement plus post-selection orbital compactness justify treating the structure as a stream rather than antihelion-source substructure?
- What alternative source-preserving null would be strongest?

### External evidence

- Is pooling CAMS and SonotaCo defensible when explicitly labeled post-hoc?
- Should EDMOND remain in the paper, move to supplementary material, or be omitted because the linked release is incomplete/stale and its upstream provenance may overlap?
- Is a fresh independent reduction mandatory before MDC submission?

### Submission strategy

- Is the current evidence sufficient for a provisional MDC submission after revisions?
- Which files and precision should be supplied to the MDC?
- Which journal, collaborators, network acknowledgments, and data-use statements are appropriate?

## Known limitations

- Public catalogue-level trajectories were used; no raw-image re-reduction was performed.
- Raw monthly GMN source bytes were not vendored as a complete immutable archive, although source code, environments, selected tables, and clean-rerun evidence are preserved.
- Absolute flux, ZHR, and mass index are unavailable from public Level 3 trajectories.
- Geographic splits share the GMN reduction system.
- CAMS–SonotaCo pooling is post-hoc.
- EDMOND is a compilation with possible upstream-network overlap, and the linked files are incomplete/stale relative to advertised v6.01.
- No credible parent shortlist exists for dynamical integration.
- The fitted speed drift is unresolved.
- Automated catalogue matching cannot exclude an obscure literature-only duplicate under an alternate convention.
- Substantive generative-AI assistance is disclosed in `mdc/AI_AND_SOFTWARE_PROVENANCE.md`; AI tools are not treated as authors or independent reviewers.

## Highest-priority files

1. `april_stream/mdc/MANUSCRIPT_DRAFT.md`
2. `april_stream/mdc/GhostStream_April_95_GMN_lookup.csv`
3. `april_stream/mdc/GhostStream_April_mean_submission.json`
4. `reconstruction/exact_recovered/EXACT_REPRODUCTION.md`
5. `reconstruction/exact_downstream/DOWNSTREAM_REPRODUCTION.md`
6. `reconstruction/exact_external/EXTERNAL_REPRODUCTION.md`
7. `recovered_pipeline/SOURCE_MANIFEST.json`
8. `april_stream/mdc/MDC_PACKAGE_CONSISTENCY_AUDIT.md`
9. `april_stream/mdc/MDC_OFFICIAL_CHECKER_REPORT.md`
10. `april_stream/mdc/LIVE_MDC_NOVELTY_REFRESH.md`
11. `april_stream/mdc/AI_AND_SOFTWARE_PROVENANCE.md`

## Requested response format

Please return:

1. overall verdict A–E;
2. any fatal error;
3. most likely known-shower duplicate, if any;
4. any coordinate or orbit-convention correction;
5. required revisions before MDC submission;
6. whether a fresh independent reduction is mandatory first;
7. whether the EDMOND evidence should remain in the paper;
8. recommended collaborators or journal; and
9. permission to quote or acknowledge the review, if appropriate.
