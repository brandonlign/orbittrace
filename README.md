# GhostStream

GhostStream searches public meteor-trajectory catalogues for weak streams that may have been missed. A blind search of Global Meteor Network (GMN) data found a recurring late-April group with similar radiants, speeds, timing, and orbits in every year from 2022 through 2026.

The fixed GMN solution was subsequently tested without refitting against the complete IAU MDC 2026 external catalogues. SonotaCo independently passed every preserved replication gate with 11 matching meteors across eight years. CAMS supplied nine additional coherent meteors across five years and passed every preserved gate except the project’s conservative 1% activity threshold. EDMOND supplied four supplementary matches.

The analysis points to an **apparently uncatalogued meteor-stream candidate**. The open question is whether it is a distinct stream, a narrow branch of a known shower complex, or structure within the antihelion source.

## Start here

- [`candidate/EXPERT_REVIEW_PACKET.md`](candidate/EXPERT_REVIEW_PACKET.md): the quickest route for a reviewer.
- [`candidate/CANDIDATE_DOSSIER.md`](candidate/CANDIDATE_DOSSIER.md): a short explanation of the candidate and the evidence.
- [`RESULTS.md`](RESULTS.md): the main numerical results.
- [`validation/full_external_replication/FULL_EXTERNAL_REPLICATION.md`](validation/full_external_replication/FULL_EXTERNAL_REPLICATION.md): complete CAMS, SonotaCo, and EDMOND replication report.
- [`validation/methodology_novelty/METHODOLOGY_NOVELTY_AUDIT.md`](validation/methodology_novelty/METHODOLOGY_NOVELTY_AUDIT.md): literature-backed boundary on what is and is not methodologically novel.
- [`validation/methodology_novelty/BENCHMARK_PROTOCOL.md`](validation/methodology_novelty/BENCHMARK_PROTOCOL.md): preregistered comparison needed before any methods-performance claim.
- [`candidate/mdc/MANUSCRIPT_DRAFT.md`](candidate/mdc/MANUSCRIPT_DRAFT.md): the working paper; its external-catalogue section predates the complete-catalogue replication and should be read together with the report above until the manuscript is revised.
- [`candidate/mdc/GhostStream_April_95_GMN_lookup.csv`](candidate/mdc/GhostStream_April_95_GMN_lookup.csv): the 95-event GMN sample used for the draft mean solution.

## Repository guide

- `pipeline/` contains the discovery, validation, control, and external-catalogue code.
- `candidate/` contains the scientific summary, supporting reports, event tables, and draft submission material.
- `validation/` records the independent reruns, method checks, complete external-catalogue replication, and methodology-novelty audit.
- `results/ghoststream_final_summary.json` records the original recovered package state; the complete external replication is preserved separately under `validation/full_external_replication/`.

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

The strongest external result is now a fully passing frozen-template replication in SonotaCo. CAMS independently gives conventionally significant activity enrichment and highly significant orbital coherence, but its activity p-value of 0.0153 does not cross the pre-established 0.01 gate.

## Methodology claim boundary

GhostStream uses a prospectively frozen, multi-stage validation design. Density clustering, temporal holdout verification, false-positive modeling, and independent-network confirmation all have prior meteor-science precedents, so the project does **not** currently claim a new meteor-stream discovery method. A controlled benchmark is required before claiming that the integrated protocol reduces false discoveries better than existing workflows.

## Check the repository

The lightweight check covers the expected files, result metadata, Python syntax, and repository hygiene. The catalogue downloads and full search use the scripts under `pipeline/`.

```bash
python scripts/verify_repository.py
```

The analysis dependencies are listed in `requirements.txt`.

## Use of AI

ChatGPT assisted with portions of the coding, troubleshooting, and writing. Brandon Li directed the project, evaluated the results, and made the final methodological and scientific decisions.
