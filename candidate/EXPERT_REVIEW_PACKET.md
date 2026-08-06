# Notes for reviewers

I am looking for a critical technical review of a late-April meteor-stream candidate found in public GMN trajectory data. The main things I need checked are the event selection, coordinate conventions, orbit treatment, antihelion background model, and possible historical duplicates.

## Main questions

1. Does the 95-event GMN sample look like a distinct recurring meteor stream, a branch of a known shower complex, or structured antihelion background?
2. Is there a known, working-list, removed, or historically published shower that is a plausible match despite the current catalogue comparison, including the unnamed IMO sequences #181 and #182?
3. Are the radiant, drift, solar-longitude, node, and orbital conventions used consistently?
4. What additional analysis or data would most strengthen the classification?

A brief answer on the main scientific issue is enough for an initial review. A detailed code review is welcome but not necessary.

## What was found

A blind January–July 2026 search selected April as the only full-gate survivor. The fixed candidate definition was then applied to earlier GMN years.

The confirmed sample contains 95 meteors:

| Year | Members |
|---:|---:|
| 2022 | 10 |
| 2023 | 8 |
| 2024 | 14 |
| 2025 | 34 |
| 2026 | 29 |

The 2022–2023 pooled sample was kept untouched until the candidate definition had been fixed. It gave:

- activity p = 1.857 × 10⁻⁵ after the twelve-month familywise rule;
- shifted-window p = 0.01754; and
- source/time-matched orbit-null p = 0.0001.

The final activity selection uses radiant, speed, and solar longitude only. Orbital elements are tested afterward.

## Candidate solution

The robust matching solution at solar longitude 36.901963° is:

| Quantity | Value |
|---|---:|
| Sun-centred ecliptic longitude | −149.376325° |
| Ecliptic latitude | +7.323038° |
| Approximate geocentric RA | 247.06° |
| Approximate geocentric Dec | −14.22° |
| Geocentric speed | 37.641692 km/s |
| q | 0.079202 AU |
| e | 0.946296 |
| i | 24.709376° |
| ω | 333.493819° |
| encounter Ω | 37.937477° |
| a | 1.474788 AU |

The draft MDC record uses the unweighted arithmetic mean of the 95 submitted rows:

| Quantity | Draft mean |
|---|---:|
| Mean solar longitude | 37.149520° |
| RA | 247.169746° |
| Dec | −14.342743° |
| Vg | 37.617513 km/s |
| q | 0.080114 AU |
| e | 0.943593 |
| i | 24.370030° |
| ω | 333.636995° |
| Ω | 37.157321° |
| a | 1.420285 AU |
| N | 95 |

I would also like to know whether using a robust solution for matching and an arithmetic mean for the MDC record is appropriate.

## Complete external-catalogue replication

After the GMN solution and all decision gates were fixed, the unchanged template was applied to the complete usable IAU MDC 2026 CAMS v3, SonotaCo, and EDMOND yearly catalogues. No external-source parameter was refitted.

### SonotaCo

SonotaCo independently passed every preserved replication gate:

- 11 frozen-template members across eight represented years: 2007, 2009, 2010, 2013, 2018, 2020, 2022, and 2023;
- activity p = 5.484 × 10⁻⁵;
- shifted-window p = 0.02041;
- median orbital D = 0.02998;
- 90th-percentile orbital D = 0.05632; and
- orbit-null p = 0.0001.

This is a formal independent external-network replication under the frozen GMN solution.

### CAMS

CAMS supplied nine matching meteors across 2011, 2012, 2014, 2015, and 2016:

- activity p = 0.01526;
- shifted-window p = 0.02041;
- median orbital D = 0.05630;
- 90th-percentile orbital D = 0.11642; and
- orbit-null p = 0.0001.

CAMS passes the member-count, multi-year, shifted-window, and orbital gates. Its activity enhancement is significant under the conventional 5% standard, but it narrowly misses the project’s pre-established 1% activity gate. I therefore describe CAMS as strong independent corroboration rather than a second formal replication pass.

### EDMOND

The complete EDMOND catalogue supplied four supplementary members in 2013, 2014, and 2016. The activity p-value was 0.00939 and the orbit-null p-value was 0.0006, but the sample did not meet the frozen member-count or multi-year gate. EDMOND is also a compiled archive and may share observations with contributing networks.

The complete evidence, member tables, source-file hashes, and machine-readable result are in `../validation/full_external_replication/`.

## Checks already completed

- Exact rerun of the original event-selection code: 101 total selected events and the same 95-event confirmed lookup table.
- Blind January–July 2026 rediscovery: April was the only full-gate survivor.
- Source-preserving antihelion test with orbit evaluated only after selection.
- 1,000 measurement-error trials, all passing the orbital compactness requirements.
- 20,000 year/night bootstrap replicates.
- Three disjoint GMN geographic station groups.
- Eighty-one combinations of nearby analysis choices, all passing.
- Complete frozen-template external replication: SonotaCo passed all gates; CAMS narrowly missed only the conservative 1% activity cutoff; EDMOND remained supplementary.
- Comparison with 2,174 current IAU MDC solutions, with no match under the fixed comparison rules.
- Review of two unnamed single-station IMO sequences (#181 and #182) whose dates overlap the candidate; their public summaries do not provide enough radiant, speed, or orbital detail for a direct match.
- Official MDC radiant/orbit checker run on the draft mean record, with no flagged inconsistencies.

## Main limitations

The discovery and confirmation use catalogue trajectories rather than new raw-image reductions. The antihelion source is structured, and the present source-matched null may miss a narrow component. The three geographic samples share GMN’s processing pipeline. SonotaCo now provides a fully passing independent replication and CAMS provides strong independent corroboration, so external support is no longer the primary limitation. The remaining central question is whether the recurring structure is distinct enough to classify as a separate stream rather than a branch or antihelion substructure.

## Suggested reading order

1. `CANDIDATE_DOSSIER.md` — short scientific explanation.
2. `../validation/full_external_replication/FULL_EXTERNAL_REPLICATION.md` — complete independent-catalogue result.
3. `mdc/OrbitTrace_April_95_GMN_lookup.csv` — the event-level GMN sample.
4. `mdc/MANUSCRIPT_DRAFT.md` — full methods and discussion; its external section predates the complete-catalogue update.
5. `ACTIVITY_PROFILE.md`, `BOOTSTRAP_UNCERTAINTY.md`, `GEOGRAPHIC_SPLIT_VALIDATION.md`, and `SPECIFICATION_CURVE.md` — the main robustness checks.
6. `../validation/` — records from the clean reruns.
7. `../pipeline/` — executable code.
