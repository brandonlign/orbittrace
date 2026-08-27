# OrbitTrace

Code and derived data for the OrbitTrace late-April meteor-stream candidate.

This repository contains the ACRF implementation used for the search, the versioned tables and result files used in the paper, the benchmark summaries, and the scripts that regenerate Figures 1–3. The original third-party catalogues are not redistributed here; their sources and acquisition details are listed in [`data/README.md`](data/README.md).

## Reproduce the archived results

Use Python 3.12 or newer. The release environment is pinned in `requirements.txt`.

```bash
python -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python reproduce.py --all
```

The command checks the archived headline results and key table invariants, writes a small report for each analysis, summarizes the benchmark/control files, and regenerates Figures 1–3 from the plotted data tables. By default it writes to a temporary directory; use `--out /path/to/output` to keep the generated files.

This is a derived-data reproduction, not a raw-data download pipeline. Repeating the analysis from the original GMN, CAMS, SonotaCo, EDMOND, or MDC archives first requires downloading and preparing those catalogues as described in [`data/README.md`](data/README.md).

## Apply ACRF to a prepared panel

A prepared panel must follow the schema documented in [`data/README.md`](data/README.md). Candidate generation is run before any comparison with the OrbitTrace target table.

```bash
./.venv/bin/python -m acrf.application \
  --panel /path/to/prepared_panel.csv \
  --out /tmp/acrf_candidates.json

./.venv/bin/python -m acrf.reveal \
  --artifact /tmp/acrf_candidates.json \
  --target data/derived/canonical_95.csv \
  --out /tmp/orbittrace_reveal.json
```

## Main results in the archive

| Result | Archived value |
|---|---:|
| ACRF candidate rank | 7 |
| Discovery family | 123 unique observation times |
| Canonical overlap | 95/95 |
| Precision / recall / F1 | 0.7724 / 1.0000 / 0.8716 |
| Annual counts, 2022–2026 | 10 / 8 / 14 / 34 / 29 |
| CAMS / SonotaCo / EDMOND matches | 9 / 11 / 4 |
| Independent archive passing the fixed replication criteria | SonotaCo |
| 153-setting sweep: exact 95/95 recovery | 37/153 |
| 153-setting sweep: rank ≤100 | 83/153 |
| MDC hard duplicates | 0 |
| Nearest complete-orbit MDC alternative | NOP-004, `D_SH = 0.2344515` |

The discovery table has 123 unique observation timestamps. Six timestamps have more than one source trajectory, so the 129 source trajectory rows collapse to 123 observations while the source IDs are retained in `trajectory_ids`.

The 153-setting ACRF sweep tracks the corresponding OrbitTrace core only after each setting has already produced its ranked candidate catalogue. The target therefore does not affect candidate generation or rank.

## Where each paper result lives

| Analysis | Entry point | Archived output |
|---|---|---|
| Discovery | `analysis/discovery.py`, `acrf/application.py` | `data/derived/acrf_discovery_family_123.csv` |
| Earlier-year confirmation | `analysis/earlier_year_confirmation.py` | `data/derived/annual_membership.csv` |
| Activity and orbital nulls | `analysis/activity_null.py`, `analysis/orbital_null.py` | `results/paper_headline_results.json` |
| Uncertainty clones | `analysis/uncertainty_clones.py` | `results/paper_headline_results.json` |
| Hierarchical bootstrap | `analysis/hierarchical_bootstrap.py` | `results/paper_headline_results.json` |
| Geographic replication | `analysis/geographic_replication.py` | `data/derived/geographic_replication.csv` |
| 81-setting validation grid | `analysis/validation_sensitivity.py` | `results/paper_headline_results.json` |
| External archives | `analysis/external_archive_replication.py` | `results/external_replication.json` |
| MDC duplicate screen | `analysis/mdc_duplicate_screen.py` | `results/mdc_duplicate_screen.json` |
| NOP-004 comparison | `analysis/nop004_population_comparison.py` | `data/derived/nop004_comparison.json` |
| Parent-body screen | `analysis/jpl_parent_body_screen.py` | `results/paper_headline_results.json` |
| 153-setting ACRF sweep | `analysis/core_hyperparameter_robustness.py` | `results/acrf_core_hyperparameter_robustness.csv` |

The benchmark files under `benchmarks/` contain the matched comparisons with Sugar, catalogue-HDBSCAN, an independent D-criterion implementation, and the three known-shower controls.

## Repository layout

- `acrf/` — ACRF search and membership code
- `analysis/` — reporters/checks for the analyses used in the paper
- `benchmarks/` — comparator code and archived benchmark/control results
- `configs/` — fixed method, threshold, seed, and robustness settings
- `data/derived/` — versioned tables used by the analyses and figures
- `results/` — machine-readable headline and robustness results
- `figures/` — Figure 1–3 scripts and plotted-data map
- `reproduce.py` — release-level verification and figure regeneration

## Data and metrics

The package uses derived tables from public GMN, CAMS, SonotaCo, EDMOND, JPL, and IAU MDC sources. Source URLs, coverage, acquisition notes, and archived-file checksums are in [`data/README.md`](data/README.md).

`D_v` is used for the OrbitTrace internal compactness and matched-orbit analyses. Southworth–Hawkins `D_SH` is used separately for the MDC/NOP catalogue comparison; the two distances should not be interchanged.

## Citation and license

Citation metadata are in [`CITATION.cff`](CITATION.cff). After a Zenodo release is created, the DOI should be cited for the archived software/data release and the paper citation added when available.

The code is released under the MIT License. Third-party source catalogues remain subject to their original providers' terms.

## Scope

OrbitTrace is reported as a recurrent meteor-stream candidate, not an official IAU shower designation. No parent body is assigned. The performance claims in the paper are limited to the benchmark panels included in this repository.

OpenAI ChatGPT was used during code development and language editing; all released code, data products, and reported results were reviewed by the author.
