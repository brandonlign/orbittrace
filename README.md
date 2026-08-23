# OrbitTrace reproducibility package

This repository reproduces the paper-facing OrbitTrace analyses from frozen, machine-readable outputs and one clean implementation of the final ACRF detector. It is intentionally a release package: development branches, abandoned detectors, exploratory notebooks, manuscript drafts, automation infrastructure, and historical implementation variants are not included.

## Quick start

```bash
python -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python reproduce.py --all
```

`--all` validates the frozen derived and results files, emits the paper-stage reports, summarizes the frozen benchmark and control outputs, and regenerates Figures 1–3 into a temporary output directory. It does not recompute every upstream analysis from raw data or download third-party raw catalogues. The command prints the output directory; pass `--out /path/to/output` to choose it explicitly.

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

The prepared-panel schema is documented in [`data/README.md`](data/README.md). The target table must only be opened after target-free generation and ranking when making a discovery claim.

## What the package reproduces

The frozen headline results are:

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

## Paper-to-code map

| Manuscript analysis | Public entry point | Frozen output |
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
| NOP-004 population comparison | `analysis/nop004_population_comparison.py` | `results/mdc_duplicate_screen.json` |
| JPL parent-body screen | `analysis/jpl_parent_body_screen.py` | `results/paper_headline_results.json` |
| 153-setting ACRF core robustness | `analysis/core_hyperparameter_robustness.py` | `results/acrf_core_hyperparameter_robustness.csv` |

The fair comparisons are separated from ACRF under `benchmarks/`: Sugar, catalogue-HDBSCAN, a clean-room D-criterion implementation, and the three known-shower controls.

## Repository layout

- `acrf/` — the final ACRF implementation only.
- `configs/` — frozen method, threshold, seed, external-replication, and robustness-grid settings.
- `data/derived/` — canonical, discovery-family, annual, external-match, template, and audit tables.
- `data/README.md` — exact source URLs, versions, freeze dates, hashes, and raw-download instructions.
- `analysis/` — only the analyses reported in the paper.
- `benchmarks/` — comparator registry, clean-room D-criterion code, and frozen benchmark/control outputs.
- `results/` — frozen machine-readable paper outputs.
- `figures/` — final Figure 1–3 regeneration scripts, synchronized PDF/PNG/SVG exports, and the panel-to-input map in `figures/README.md`.
- `reproduce.py` — one entry point for the major paper stages.

## Data policy

Raw third-party files are deliberately excluded. Follow `data/README.md`, download the cited versions yourself, and preserve a local SHA-256 manifest. The derived tables in this repository are sufficient to reproduce the manuscript headline numbers and figures without redistributing source archives.

## Claim boundary

The package documents ACRF as the OrbitTrace discovery method and the recurring, apparently uncatalogued candidate it identifies. It does not claim an official shower designation or an identified parent body, and performance claims are limited to the explicitly tested comparator panels.
