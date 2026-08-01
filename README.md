# GhostStream

GhostStream searches public meteor-trajectory catalogues for weak streams that may have been missed. A blind search of Global Meteor Network (GMN) data found a recurring late-April group with similar radiants, speeds, timing, and orbits in every year from 2022 through 2026. Smaller matching samples also appear in CAMS, SonotaCo, and EDMOND.

The analysis points to an **apparently uncatalogued meteor-stream candidate**. The open question is whether it is a distinct stream or a narrow part of a known shower complex or the antihelion source.

## Start here

- [`candidate/EXPERT_REVIEW_PACKET.md`](candidate/EXPERT_REVIEW_PACKET.md): the quickest route for a reviewer.
- [`candidate/CANDIDATE_DOSSIER.md`](candidate/CANDIDATE_DOSSIER.md): a short explanation of the candidate and the evidence.
- [`RESULTS.md`](RESULTS.md): the main numerical results.
- [`candidate/mdc/MANUSCRIPT_DRAFT.md`](candidate/mdc/MANUSCRIPT_DRAFT.md): the working paper.
- [`candidate/mdc/GhostStream_April_95_GMN_lookup.csv`](candidate/mdc/GhostStream_April_95_GMN_lookup.csv): the 95-event GMN sample used for the draft mean solution.

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

The same group appears in untouched years and remains compact under source-matched null tests, measurement-error simulations, geographic splits, clustered bootstrap resampling, and 81 nearby analysis settings. None of the 2,174 solutions in the checked IAU Meteor Data Center catalogue matched it under the fixed comparison rules.

## Check the repository

The lightweight check covers the file set, result metadata, source hashes, Python syntax, and repository hygiene. The catalogue downloads and full search use the scripts under `pipeline/`.

```bash
python scripts/verify_repository.py
```

The analysis dependencies are listed in `requirements.txt`.

## Use of AI

OpenAI ChatGPT assisted with research planning, code drafting and debugging, source discovery, reproducibility checks, organization, and editing. Brandon Li reviewed the methods, code, sources, numerical results, and interpretations and is responsible for the final work.
