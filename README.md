# OrbitTrace reproducibility package

This repository reproduces the OrbitTrace analyses from versioned, machine-readable outputs and the final ACRF implementation. It contains the code, configurations, derived tables, results, and figure-generation source used in the paper.

## Quick start

```bash
python -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python reproduce.py --all
```

`--all` checks the versioned derived and result files, emits the analysis reports, summarizes the benchmark and control outputs, and regenerates Figures 1–3 into a temporary output directory. It uses the derived tables in the repository rather than downloading third-party catalogues or rerunning their upstream preparation. The command prints the output directory; pass `--out /path/to/output` to choose it explicitly.

To apply ACRF to a newly prepared, label-free panel:

```bash
./.venv/bin/python -m acrf.application \
  --panel /path/to/prepared_panel.csv \
  --out /tmp/orbittrace_acrf_application.json
./.venv/bin/python -m acrf.reveal \
  --artifact /tmp/orbittrace_acrf_application.json \
  --target data/derived/canonical_95.csv \
  --out /tmp/orbittrace_acrf_reveal.json
```

The prepared-panel schema is documented in [`data/README.md`](data/README.md). For discovery work, generate and rank candidates before comparing them with `canonical_95.csv`.

## What the package reproduces

The headline results are:

| Result | Expected output |
|---|---:|
| ACRF tracked-family rank | 7 |
| ACRF discovery family | 123 unique observation timestamps |
| Canonical overlap | 95/95 |
| Precision / recall / F1 | 0.7724 / 1.0000 / 0.8716 |
| Canonical annual counts | 2022: 10; 2023: 8; 2024: 14; 2025: 34; 2026: 29 |
| CAMS / SonotaCo / EDMOND matches | 9 / 11 / 4 |
| Formal independent archive pass | SonotaCo |
| Core robustness exact 95/95 | 37/153 settings |
| Core robustness ≥90/95 | 49/153 settings |
| Core robustness ≥80/95 | 60/153 settings |
| Core robustness rank ≤100 | 83/153 settings |
| MDC hard duplicates | 0 |
| Nearest complete-orbit alternative | NOP-004, D_SH = 0.2344515 |

The 123-member table represents unique observation timestamps. It retains all source trajectory identifiers in `trajectory_ids`; 129 trajectory rows collapse to 123 timestamps because six timestamps have multiple trajectories.

The 153-setting ACRF robustness analysis tracks the corresponding OrbitTrace core only after each setting's ranked candidate catalogue has been produced. Target information therefore does not affect candidate generation or rank; the fixed baseline remains the reported method.

## Paper-to-code map

| Manuscript analysis | Public entry point | Output |
|---|---|---|
| OrbitTrace discovery | `analysis/discovery.py`, `acrf/application.py` | `data/derived/acrf_discovery_family_123.csv` |
| Earlier-year confirmation | `analysis/earlier_year_confirmation.py` | `data/derived/annual_membership.csv` |
| Activity null | `analysis/activity_null.py` | `results/paper_headline_results.json` |
| Orbital null | `analysis/orbital_null.py` | `results/paper_headline_results.json` |
| Uncertainty clones | `analysis/uncertainty_clones.py` | `results/paper_headline_results.json` |
| Hierarchical bootstrap | `analysis/hierarchical_bootstrap.py` | `results/paper_headline_results.json` |
| Geographic replication | `analysis/geographic_replication.py` | `results/paper_headline_results.json` |
| 81-setting validation sensitivity | `analysis/validation_sensitivity.py` | `results/paper_headline_results.json` |
| External archive replication | `analysis/external_archive_replication.py` | `results/external_replication.json` |
| Exhaustive MDC duplicate screen | `analysis/mdc_duplicate_screen.py` | `results/mdc_duplicate_screen.json` |
| NOP-004 population comparison | `analysis/nop004_population_comparison.py` | `data/derived/nop004_comparison.json` |
| JPL parent-body screen | `analysis/jpl_parent_body_screen.py` | `results/paper_headline_results.json` |
| 153-setting ACRF core robustness | `analysis/core_hyperparameter_robustness.py` | `results/acrf_core_hyperparameter_robustness.csv` |

The fair comparisons are separated from ACRF under `benchmarks/`: Sugar, catalogue-HDBSCAN, an independent D-criterion implementation, and the three known-shower controls.

## Repository layout

- `acrf/` — the final ACRF implementation only.
- `configs/` — method, threshold, seed, external-replication, and robustness-grid settings.
- `data/derived/` — canonical, discovery-family, annual, external-match, template, and audit tables.
- `data/README.md` — source URLs, versions, acquisition dates, hashes, and raw-download instructions.
- `analysis/` — only the analyses reported in the paper.
- `benchmarks/` — comparator registry, independent D-criterion implementation, and benchmark/control outputs.
- `results/` — machine-readable paper outputs.
- `figures/` — final Figure 1–3 regeneration scripts and the panel-to-input map in `figures/README.md`; `figures/generated/` documents the generated-output contract but does not retain stale rendered binaries.
- `reproduce.py` — one entry point for the major paper stages.

## Data policy

The package uses derived tables from the public GMN, CAMS, SonotaCo, EDMOND, and MDC sources. Follow `data/README.md` to download the cited source versions and record a local SHA-256 manifest; the source archives themselves are not redistributed here.

Figure 1D uses vector-form `D_v` for both the internal GMN compactness summary and external matched-orbit distances to the fixed GMN reference orbit. Southworth–Hawkins `D_SH` is a separate metric used for the MDC/NOP catalogue comparisons; the two are not interchangeable.

OpenAI ChatGPT assisted with code development and language editing; the author independently reviewed and verified the repository and results.

## Scope

ACRF is the OrbitTrace discovery method, and the analysis identifies a recurring candidate that is not present in the catalogues tested here. The paper does not assign an official shower designation or parent body; performance comparisons cover the comparator panels listed in `benchmarks/`.
