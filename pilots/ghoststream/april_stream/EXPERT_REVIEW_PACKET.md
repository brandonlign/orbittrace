# GhostStream April candidate — external expert review packet

Last updated: 2026-08-01

## Purpose

This packet requests a critical meteor-science review of an uncatalogued annual late-April meteor-stream candidate identified blindly in Global Meteor Network (GMN) trajectories.

The requested decision is not whether the analysis is impressive. It is whether the evidence and coordinate/orbit conventions support:

1. a provisional submission to the IAU Meteor Data Center (MDC);
2. preparation of a peer-reviewed discovery paper; and
3. the present claim boundary.

Please identify any fatal error, likely duplicate shower, or analysis that must be completed before external submission.

## Requested reviewer verdict

Please select one:

- **A — Suitable for MDC submission after minor corrections**
- **B — Scientifically promising, but requires a new analysis or additional data before MDC submission**
- **C — Likely a duplicate of a known, working-list, removed, or historically published shower**
- **D — Likely structured sporadic-source contamination rather than a distinct stream**
- **E — A methodological, coordinate, or orbit-convention error invalidates the candidate**

Please state the specific evidence supporting the verdict.

## Claim being reviewed

> A blind, uncertainty-aware analysis of public GMN trajectories identified a high-confidence uncatalogued annual meteor-stream candidate active in late April. It recurs in five GMN years, survives source-preserving and post-selection orbital null tests, reproduces across three disjoint GMN geographic station groups, and receives historical support from CAMS and SonotaCo. It is not yet an official IAU discovery or an established shower.

No official name, IAU code, established status, absolute flux, parent body, or detected physical geocentric-speed drift is claimed.

## Two orbit representations used for different purposes

The project deliberately distinguishes the **frozen robust candidate solution** used for membership/similarity testing from the **arithmetic-mean MDC submission record** calculated from the 95 confirmed GMN members.

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

The separate full-precision means imply `a = 1.420295780... AU` and remain preserved in the calculation audit. Please advise whether this submitted-precision convention is the correct MDC practice.

## Main evidence

### Blind discovery and recurrence

- Candidate generated in an untouched January–July 2026 scan.
- Frozen template selected 101 deduplicated GMN events from 2019–2026.
- Five consecutive years passed the individual confirmation gate:
  - 2022: 10
  - 2023: 8
  - 2024: 14
  - 2025: 34
  - 2026: 29
- The 95 events in those five significant years form the MDC lookup table.
- Untouched 2022–2023 pooled activity p = **1.857×10⁻⁵** after the twelve-month familywise rule.
- Untouched source/time-matched orbit-null p = **0.0001**.

### Source-preserving and non-circular selection

The final activity selection uses only:

- Sun-centered radiant longitude;
- ecliptic latitude;
- geocentric speed; and
- solar longitude.

No eccentricity, perihelion distance, inclination, argument of perihelion, or node is used to select the activity enhancement. Orbital coherence is evaluated afterward inside a deliberately expanded antihelion-source background.

### Orbit and measurement uncertainty

- GMN median orbital distance = **0.04398**.
- GMN q90 orbital distance = **0.09232**.
- Maximum significant-year medoid separation = **0.05044**.
- Measurement-error clone trials: **1,000/1,000 passed**.

### Sampling and analytical robustness

- Hierarchical year/night bootstrap: **20,000 replicates**.
- RA drift 95% interval: **+0.672 to +1.040° per degree of solar longitude**.
- Dec drift 95% interval: **−0.248 to −0.037° per degree**.
- Vg drift 95% interval: **−0.178 to +0.221 km/s per degree**; unresolved.
- Frozen specification curve: **81/81 cells passed**.
- The grid varies trajectory-fit error, minimum station count, radiant-core radius, and activity-window width.

### Geographic replication within GMN

| Region | Members | Activity p | Median D | Orbit-null p |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41×10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26×10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16×10⁻¹⁰ | 0.04795 | 0.0001 |

Maximum regional-medoid separation: **D = 0.04054**.

These groups are trajectory-disjoint but share the GMN reduction system; they are not represented as independent reductions.

### Primary external historical support

CAMS + SonotaCo under the uniform zero-speed-drift rule:

- 10 events across 2011, 2012, 2022, 2023, and 2025;
- activity p = **1.622×10⁻⁴**;
- shifted-window p = **0.02041**;
- median orbital distance = **0.04879**;
- q90 orbital distance = **0.07708**;
- orbit-null p = **5×10⁻⁵**;
- external medoid distance from the GMN orbit = **0.01723**.

The pooled synthesis is explicitly post-hoc because it was motivated by sparse archive-specific outcomes.

### EDMOND evidence and release limitation

A shower-removed Shober EDMOND subset contributes six non-overlapping orbitally compact events in 2014, 2016, 2017, and 2022. Its standalone activity p = **0.01206** and N = **6**, so it is supporting rather than independently decisive.

The unchanged frozen template was also applied to all annual files currently linked by the public EDMOND page. It recovered exactly the same six events and no additional events. However, a release-integrity audit shows that the linked files are incomplete or stale relative to the advertised v6.01 release:

- 23 readable annual ZIPs for 2001–2023;
- 2024 linked ZIP returns HTTP 404;
- 481,252 linked rows versus 614,758 advertised for 2001–2023 (**78.283%**);
- annual row-count matches: **0/23**;
- embedded versions are predominantly **513/516**, not 601.

For the currently linked files:

- activity p = **3.3785×10⁻⁴**;
- odds ratio = **7.455**;
- shifted-window p = **0.06122**;
- median Southworth–Hawkins D = **0.03601**;
- q90 D = **0.07344**;
- 20,000-trial orbit-null p = **4.99975×10⁻⁵**.

This is not described as a complete v6.01 replication or as a fully independent third instrument.

## What has already been mechanically verified

### Live official IAU MDC catalogue refresh

The official full shower-data JSON was downloaded and checksum-locked on 2026-08-01:

- catalogue version: **2026-06-25**;
- shower records: **1,072**;
- submitted solutions: **2,174**;
- SHA-256: `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`;
- hard duplicate matches: **0**;
- activity-compatible radiant–speed near matches: **0**;
- orbit-incomplete near matches: **0**.

The nearest complete orbit is Northern May Ophiuchids solution 004 at `D_SH = 0.23445`. Its published activity interval is solar longitude 45°–75°, its mean epoch is 21.70° after the candidate, and its drifted radiant is separated by 9.59°.

This automated result does not replace expert review of historical literature or alternate coordinate conventions.

### Exact official MDC consistency checker

The current official checker archive was downloaded and CRC-verified. The exact committed 95-member mean record was run through:

1. the distributed official Linux binaries; and
2. a fresh GNU Fortran build of the distributed `elements.f` and `radiants.f` source.

Both produced byte-identical comparison files and **zero orbital/geocentric error records**. This validates internal radiant/orbit consistency only, not novelty or membership.

### Package-wide consistency audit

A fail-closed audit recomputed the lookup-table quantities and cross-checked the mean JSON, legacy record, calculation audit, checker inputs, catalogue provenance, EDMOND claim boundary, manuscript, and final summary.

- Checks: **111**
- Passed: **111**
- Failed: **0**

The audit caught and corrected the submitted semimajor-axis rounding inconsistency described above.

## Novelty and parent-body audit

- Current official IAU MDC solutions parsed: **2,174**.
- Hard matches: **0**.
- Radiant–speed–activity near matches: **0**.
- Orbit-incomplete near matches: **0**.
- Nearest official complete orbit: Northern May Ophiuchids, `D_SH = 0.23445`, with mismatched activity and radiant.
- JPL small bodies screened: **6,284**.
- Credible parent candidates at D ≤ 0.15: **0**.

No official name, established status, or parent body is claimed.

## Questions requiring expert judgment

### 1. Coordinate and orbit conventions

- Are the geocentric J2000 radiant, Sun-centered ecliptic radiant, encounter-node, and argument-of-perihelion conventions internally correct?
- Is the 180° node/perihelion normalization used for historical video archives appropriate in every source?
- Is the frozen robust/medoid solution appropriate for membership and similarity testing?
- Is the arithmetic-mean 95-member solution the correct representation for MDC submission?
- Is calculating submitted `a` from the submitted rounded q and e the preferred MDC convention, or should more precision be supplied for all three fields?

### 2. Duplicate-shower risk

- Does any established, working-list, removed, or historically published shower plausibly match this epoch, drifted radiant, speed, and orbit despite failing the current automated veto?
- Is Northern May Ophiuchids or another Ophiuchid/Virginid/antihelion-complex solution credible under a different element or node convention?
- Are there important historical catalogues or papers absent from the current MDC JSON that should be checked manually?

### 3. Antihelion-source interpretation

- Is the expanded antihelion null sufficiently conservative?
- Does the four-degree activity enhancement plus post-selection orbital compactness justify treating the structure as a stream rather than a transient substructure of the antihelion source?
- Is the Fisher inside/outside-window formulation appropriate for this source geometry?
- What alternative source-preserving null would be strongest?

### 4. External evidence

- Is pooling CAMS and SonotaCo scientifically defensible when explicitly labeled post-hoc?
- Should the EDMOND evidence remain in the paper, be relegated to supplementary material, or be omitted because the currently linked release is incomplete/stale and upstream provenance may overlap?
- Is the exact six-event reproduction across the currently linked EDMOND files meaningful provenance support despite adding no new events?
- Is a fresh independent reduction mandatory before MDC submission, or can it follow provisional submission?

### 5. MDC package and publication strategy

- Is the current evidence sufficient for a provisional MDC submission?
- Should the MDC receive the current-structure JSON record, legacy text record, or both?
- Which journal is appropriate for the methods-and-discovery paper?
- What GMN acknowledgment, data-use statement, and collaborator invitation are expected?
- Should GMN or other network representatives be invited as collaborators before submission?

## Known limitations disclosed to the reviewer

- Public catalogue-level trajectories were used; no raw-image re-reduction was performed.
- Absolute flux, ZHR, and mass index are unavailable from public Level 3 trajectories.
- Geographic splits share the GMN reduction system.
- CAMS–SonotaCo pooling is post-hoc.
- EDMOND is a compilation with possible upstream network overlap.
- The currently linked EDMOND files are incomplete/stale relative to the advertised v6.01 release.
- The advertised EDMOND 2024 attachment is unavailable; no inference is drawn from its absence.
- No parent-body dynamics were performed because no credible parent shortlist exists.
- The fitted geocentric-speed drift is unresolved.
- Automated catalogue matching cannot exclude an obscure literature-only duplicate under an alternate convention.

## Files to review

### Highest priority

1. `mdc/MANUSCRIPT_DRAFT.md`
2. `mdc/GhostStream_April_95_GMN_lookup.csv`
3. `mdc/GhostStream_April_mean_submission.json`
4. `mdc/calculation_audit.json`
5. `mdc/MDC_OFFICIAL_CHECKER_REPORT.md`
6. `mdc/MDC_PACKAGE_CONSISTENCY_AUDIT.md`
7. `mdc/LIVE_MDC_NOVELTY_REFRESH.md`
8. `candidate_solution.json`
9. `CANDIDATE_DOSSIER.md`

### Robustness and external evidence

10. `BOOTSTRAP_UNCERTAINTY.md`
11. `SPECIFICATION_CURVE.md`
12. `ACTIVITY_PROFILE.md`
13. `GEOGRAPHIC_SPLIT_VALIDATION.md`
14. `ALL_EXTERNAL_ZERO_SPEED.md`
15. `all_external_members_zero_speed.csv`
16. `shober_edmond/SHOBER_EDMOND_VALIDATION.md`
17. `edmond_2024/EDMOND_CURRENT_RELEASE_AUDIT.md`

### Machine-readable audit records

18. `mdc/exact_official_checker_summary.json`
19. `mdc/live_mdc_novelty_refresh_summary.json`
20. `mdc/mdc_package_consistency_summary.json`

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
