# Notes for reviewers

Thank you for taking the time to look at this project. I am seeking a critical technical review of a late-April meteor-stream candidate found in public GMN trajectory data.

I would especially value a check of the event selection, coordinate conventions, orbit treatment, background model, and possible historical duplicates.

## The questions I most need answered

1. Does the 95-event GMN sample look like a real recurring meteor stream rather than structured antihelion background?
2. Is there a known, working-list, removed, or historically published shower that is a plausible match despite the current catalogue comparison?
3. Are the radiant, drift, solar-longitude, node, and orbital conventions used consistently?
4. What additional analysis or data would most strengthen the interpretation?

A brief answer focused on the main scientific issue would be very useful; a detailed code review is optional.

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

The pooled 2022–2023 confirmation was reserved until after the candidate definition had been fixed and gave:

- activity p = 1.857 × 10⁻⁵ after the twelve-month familywise rule;
- shifted-window p = 0.01754; and
- source/time-matched orbit-null p = 0.0001.

The final activity selection uses radiant, speed, and solar longitude only. Orbital elements are tested afterward.

## Candidate solution

The robust matching solution at solar longitude 36.901963° is:

| Quantity | Value |
|---|---:|
| Sun-centered ecliptic longitude | −149.376325° |
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

I would especially appreciate advice on whether this distinction between a robust matching solution and an arithmetic-mean submission record is appropriate for MDC practice.

## Checks already completed

- Exact rerun of the original event-selection code: 101 total selected events and the same 95-event confirmed lookup table.
- Blind January–July 2026 rediscovery: April was the only full-gate survivor.
- Source-preserving antihelion test with orbit evaluated only after selection.
- 1,000 measurement-error trials, all passing the orbital compactness requirements.
- 20,000 year/night bootstrap replicates.
- Three disjoint GMN geographic station groups.
- Eighty-one combinations of nearby analysis choices, all passing.
- Six CAMS and four SonotaCo matches; the pooled ten-event result is explicitly post-hoc.
- Six additional events in a shower-removed EDMOND subset, treated as supplementary because EDMOND is a compilation.
- Comparison with 2,174 current IAU MDC solutions, with no match under the fixed comparison rules.
- Official MDC radiant/orbit checker run on the draft mean record, with no flagged inconsistencies.

## Most important limitations

The discovery and confirmation use catalogue trajectories rather than new raw-image reductions. The antihelion source is structured, and the present source-matched null may miss a narrow component. The three geographic samples share GMN’s processing pipeline. The external catalogues are sparse, and their pooled result was decided after the separate outcomes were known.

## Suggested reading order

1. `CANDIDATE_DOSSIER.md` — short scientific explanation.
2. `mdc/GhostStream_April_95_GMN_lookup.csv` — the event-level GMN sample.
3. `mdc/MANUSCRIPT_DRAFT.md` — full methods and discussion.
4. `ACTIVITY_PROFILE.md`, `BOOTSTRAP_UNCERTAINTY.md`, `GEOGRAPHIC_SPLIT_VALIDATION.md`, and `SPECIFICATION_CURVE.md` — the main robustness checks.
5. `../validation/` — records from the clean reruns.
6. `../pipeline/` — executable code.

The repository’s top-level README explains the code history and assistance used in preparing the project.
