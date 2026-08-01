# GhostStream April candidate — external expert review packet

## Purpose

This packet asks for a critical meteor-science review of an uncatalogued annual April meteor-stream candidate identified blindly in Global Meteor Network (GMN) trajectories.

The requested decision is not whether the work is impressive. It is whether the evidence supports submission to the IAU Meteor Data Center and a peer-reviewed journal, and what must be corrected first.

## Requested reviewer verdict

Please select one:

- **A — Suitable for MDC submission after minor corrections**
- **B — Scientifically promising, but requires a new analysis or additional data before MDC submission**
- **C — Likely a duplicate of a known/working-list shower**
- **D — Likely structured sporadic-source contamination rather than a distinct stream**
- **E — Methodological or coordinate error invalidates the candidate**

Please identify the specific evidence supporting the verdict.

## Candidate summary

Internal label: `GhostStream-April-36.9`

At solar longitude 36.902°:

| Quantity | Frozen solution |
|---|---:|
| Sun-centered ecliptic longitude | −149.376° |
| Geocentric ecliptic latitude | +7.323° |
| Approximate geocentric RA | 247.0° |
| Approximate geocentric Dec | −14.3° |
| Geocentric speed | 37.642 km/s |
| q | 0.079202 AU |
| e | 0.946296 |
| i | 24.709° |
| ω | 333.494° |
| encounter Ω | 37.937° |
| a | 1.475 AU |

Activity core: solar longitude 35.902°–39.902°.

The fitted geocentric-speed drift is not statistically resolved and is not claimed as physical. Final external-archive tests fix dVg/dλ⊙ = 0.

## Main evidence

### Blind discovery and recurrence

- Candidate generated in an untouched January–July 2026 scan.
- Frozen template recovers 95 confirmed GMN members in five consecutive years:
  - 2022: 10
  - 2023: 8
  - 2024: 14
  - 2025: 34
  - 2026: 29
- Untouched 2022–2023 pooled activity p = 1.857×10⁻⁵ after the twelve-month familywise rule.
- Untouched source-matched orbit-null p = 0.0001.

### Source-preserving and non-circular selection

The final activity selection uses only:

- Sun-centered radiant longitude;
- ecliptic latitude;
- geocentric speed; and
- solar longitude.

No orbital element or node is used to select the activity enhancement. Orbital coherence is evaluated afterward inside an expanded antihelion source.

### Orbit and uncertainty

- GMN median orbital D = 0.04398.
- GMN q90 orbital D = 0.09232.
- Maximum significant-year medoid separation = 0.05044.
- Measurement-error clones: 1,000/1,000 passed.
- Official MDC radiant/orbit checker: zero flagged inconsistencies in both directions.

### Sampling and analytical robustness

- Hierarchical year/night bootstrap: 20,000 replicates.
- RA drift 95% interval: +0.672 to +1.040° per degree of solar longitude.
- Dec drift 95% interval: −0.248 to −0.037° per degree.
- Vg drift 95% interval: −0.178 to +0.221 km/s per degree; unresolved.
- Frozen specification curve: 81/81 cells passed.
- Specification grid varies fit-error maximum, station minimum, radiant-core radius, and activity-window width.

### Geographic replication within GMN

| Region | Members | Activity p | Median D | Orbit-null p |
|---|---:|---:|---:|---:|
| Americas | 30 | 6.41×10⁻⁷ | 0.04503 | 0.0001 |
| Europe / West Asia | 22 | 2.26×10⁻⁴ | 0.03375 | 0.0001 |
| Oceania / East Asia / Africa | 44 | 2.16×10⁻¹⁰ | 0.04795 | 0.0001 |

Maximum regional-medoid separation: D = 0.04054.

### External archive support

Primary CAMS + SonotaCo synthesis under zero speed drift:

- 10 events across 2011, 2012, 2022, 2023, and 2025;
- activity p = 1.622×10⁻⁴;
- shifted-window p = 0.02041;
- median D = 0.04879;
- orbit-null p = 5×10⁻⁵;
- external medoid distance from GMN = 0.01723.

A shower-removed Shober EDMOND subset adds six non-overlapping orbitally compact events. Its standalone activity p = 0.01206 and N = 6, so it is supporting rather than independently decisive. EDMOND is a compilation and is not counted as a clean third independent instrument.

### Novelty audit

- IAU MDC solutions parsed: 2,174.
- Hard matches: 0.
- Nearest official orbit: Northern May Ophiuchids, D ≈ 0.235, with mismatched activity and radiant.
- JPL small bodies screened: 6,284.
- Credible parent candidates at D ≤ 0.15: 0.

No official name, established status, or parent body is claimed.

## Questions requiring expert judgment

### 1. Coordinate and orbit conventions

- Are the geocentric J2000 radiant, Sun-centered ecliptic radiant, encounter node, and argument-of-perihelion conventions internally correct?
- Is the 180° node/perihelion normalization used for historical video archives appropriate?
- Is the reported MDC mean solution the correct representation of the 95-member sample?

### 2. Duplicate-shower risk

- Does any established, working-list, removed, or historically published shower plausibly match this epoch, drifted radiant, speed, and orbit despite failing the automated veto?
- Is Northern May Ophiuchids or another Ophiuchid/Virginid complex a credible duplicate under a different convention?

### 3. Antihelion-source interpretation

- Is the expanded antihelion null sufficiently conservative?
- Does the four-degree activity enhancement plus post-selection orbital compactness justify treating the structure as a stream rather than a substructure of the antihelion source?
- What alternative source-preserving null would be stronger?

### 4. External evidence

- Is pooling CAMS and SonotaCo scientifically defensible when labeled post-hoc?
- How should the Shober EDMOND subset be described given possible network provenance overlap?
- Is a fresh independent reduction mandatory before MDC submission, or can it follow submission?

### 5. Submission and authorship

- Is the current evidence sufficient for a provisional MDC submission?
- Which journal is appropriate for the full methods-and-discovery paper?
- What GMN acknowledgment, data-use statement, and collaborator invitation are expected?

## Known limitations disclosed to the reviewer

- Public catalogue-level trajectories were used; no raw-image re-reduction was performed.
- Absolute flux, ZHR, and mass index are not available from public Level 3 trajectories.
- Geographic splits share the GMN reduction system.
- CAMS–SonotaCo pooling and the three-archive extension are post-hoc.
- The live official EDMOND 2024 annual attachment was unavailable during the audit.
- No parent-body dynamics have been performed because no credible parent shortlist exists.
- The fitted speed drift is unresolved.

## Files to review

Highest priority:

1. `mdc/MANUSCRIPT_DRAFT.md`
2. `mdc/GhostStream_April_95_GMN_lookup.csv`
3. `mdc/GhostStream_April_mean_submission.json`
4. `mdc/MDC_OFFICIAL_CHECKER_REPORT.md`
5. `candidate_solution.json`
6. `CANDIDATE_DOSSIER.md`

Robustness evidence:

7. `BOOTSTRAP_UNCERTAINTY.md`
8. `SPECIFICATION_CURVE.md`
9. `ACTIVITY_PROFILE.md`
10. `GEOGRAPHIC_SPLIT_VALIDATION.md`
11. `ALL_EXTERNAL_ZERO_SPEED.md`
12. `all_external_members_zero_speed.csv`

## Requested response format

Please return:

1. overall verdict A–E;
2. any fatal error;
3. most likely known-shower duplicate, if any;
4. required revisions before MDC submission;
5. whether a fresh independent reduction is mandatory first;
6. recommended collaborators or journal; and
7. permission to quote or acknowledge the review, if appropriate.
