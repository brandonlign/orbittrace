# GhostStream

GhostStream is a search for weak meteor streams in public meteor-trajectory catalogues. The project began as a blind search of Global Meteor Network (GMN) data and found one recurring concentration of meteors in late April. The same radiant, timing, speed, and orbital pattern appears in GMN data from 2022 through 2026, with smaller supporting samples in CAMS, SonotaCo, and EDMOND.

The result is best described as an **apparently uncatalogued meteor-stream candidate**. The main scientific question is whether it is a distinct stream or a narrow component of a known shower complex or the antihelion source.

## Start here

- [`candidate/EXPERT_REVIEW_PACKET.md`](candidate/EXPERT_REVIEW_PACKET.md) gives a reviewer the shortest useful route through the project.
- [`candidate/CANDIDATE_DOSSIER.md`](candidate/CANDIDATE_DOSSIER.md) explains the candidate and the evidence in plain scientific language.
- [`RESULTS.md`](RESULTS.md) collects the main numerical results.
- [`candidate/mdc/MANUSCRIPT_DRAFT.md`](candidate/mdc/MANUSCRIPT_DRAFT.md) is the working paper draft.
- [`candidate/mdc/GhostStream_April_95_GMN_lookup.csv`](candidate/mdc/GhostStream_April_95_GMN_lookup.csv) contains the 95 GMN meteors used for the draft mean solution.

## Repository guide

- `pipeline/` preserves the executable discovery, validation, control, and external-catalogue code.
- `candidate/` contains the scientific summary, supporting reports, event tables, and draft submission material.
- `validation/` records the independent reruns and method checks.
- `results/ghoststream_final_summary.json` is the compact machine-readable summary.
- `pipeline/SOURCE_MANIFEST.json` records the immutable source commits and file hashes.

The repository was reorganized after the analysis was complete. One-time download probes, inspection scripts, superseded versions, and runtime patch wrappers were removed from the active code tree. The original source hashes and immutable commits remain listed in `pipeline/SOURCE_MANIFEST.json`.

## Main result

The final GMN sample contains 95 meteors from five consecutive significant years:

| Year | Members |
|---:|---:|
| 2022 | 10 |
| 2023 | 8 |
| 2024 | 14 |
| 2025 | 34 |
| 2026 | 29 |

The candidate also survived an untouched-year test, a source-matched background test, orbital null tests, measurement-error simulations, geographic splits, clustered bootstrap resampling, and an 81-setting sensitivity analysis. The current IAU Meteor Data Center catalogue contains no matching shower solution under the project’s comparison rules.

## Check the repository

The lightweight check verifies the expected files, fixed result metadata, source provenance, Python syntax, and repository hygiene. The full search uses the public catalogues and the analysis scripts in `pipeline/`.

```bash
python scripts/verify_repository.py
```

The analysis dependencies are listed in `requirements.txt`.

## Use of AI

OpenAI ChatGPT assisted with research planning, code drafting and debugging, source discovery, reproducibility checks, organization, and editing. Brandon Li reviewed the final methods, code, sources, numerical results, and interpretations and takes responsibility for the work.
