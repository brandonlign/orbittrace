# OrbitTrace

Code and derived data for a recurrent late-April meteor-stream candidate found in Global Meteor Network (GMN) trajectories.

The repository includes the ACRF search code, the tables and result files used in the paper, benchmark summaries, and the scripts for Figures 1–3. I do not redistribute the original third-party catalogues here. Their sources, coverage, preparation notes, and checksums are in [`data/README.md`](data/README.md).

## Run the release check

Use Python 3.12 or newer.

```bash
python -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python reproduce.py --all
```

That command runs the core tests, checks the archived headline results and table invariants, summarizes the benchmark/control files, and regenerates the three paper figures. It uses a temporary output directory unless `--out` is supplied.

This is a **derived-data reproduction**. It verifies the released analysis products, but it does not automatically redownload and rebuild every source catalogue from scratch. The raw-data sources and the GMN filtering/deduplication rules are documented in [`data/README.md`](data/README.md).

## Main result

ACRF ranked OrbitTrace-April-36.9 seventh in the April search. The discovery family contains 123 unique observation times and includes all 95 meteors in the canonical 2022–2026 sample. The annual canonical counts are 10, 8, 14, 34, and 29. SonotaCo independently passes the fixed external-replication criteria with 11 matches across eight observing years; CAMS and EDMOND contain 9 and 4 compatible matches. The full 2,179-row IAU MDC screen finds no hard duplicate.

The broader ACRF sensitivity sweep contains 153 unique settings. A corresponding OrbitTrace core can be tracked after ranking in every setting, but only 83 place it within the fixed top-100 candidate budget. The target is not used to generate or rank candidates.

The main machine-readable summary is [`results/paper_headline_results.json`](results/paper_headline_results.json). The full robustness table is [`results/acrf_core_hyperparameter_robustness.csv`](results/acrf_core_hyperparameter_robustness.csv).

## Apply ACRF to a prepared panel

The prepared-panel schema is listed in [`data/README.md`](data/README.md).

```bash
./.venv/bin/python -m acrf.application \
  --panel /path/to/prepared_panel.csv \
  --out /tmp/acrf_candidates.json

./.venv/bin/python -m acrf.reveal \
  --artifact /tmp/acrf_candidates.json \
  --target data/derived/canonical_95.csv \
  --out /tmp/orbittrace_reveal.json
```

`acrf.application` generates and ranks the candidate catalogue without opening the target table. `acrf.reveal` is the separate post-hoc comparison step.

## Files

- `acrf/` — ACRF implementation
- `analysis/` — checks/reporters for the analyses used in the paper
- `benchmarks/` — comparator code and archived benchmark/control results
- `configs/` — released method, threshold, seed, and robustness settings
- `data/derived/` — versioned analysis tables
- `results/` — machine-readable results
- `figures/` — figure scripts and input map
- `tests/` — small regression tests for the public code path
- `reproduce.py` — release check and figure regeneration

One terminology note: the internal compactness analyses use the paper's vector-form `D_v`. The IAU MDC/NOP catalogue comparison uses Southworth–Hawkins `D_SH`. They are different metrics.

## Citation and license

Citation metadata are in [`CITATION.cff`](CITATION.cff). Once this version is archived, cite the Zenodo DOI for the software/data release and add the paper citation when it is available.

The source code is MIT licensed. The repository is a mixed-license archive because some derived tables come from external catalogues; [`NOTICE.md`](NOTICE.md) gives the short rights summary and [`data/README.md`](data/README.md) records the source-specific attribution. When archiving the full repository on Zenodo, use its mixed-license support rather than applying MIT to every file.

OrbitTrace is a meteor-stream candidate, not an official IAU shower designation, and no parent body is assigned here.

OpenAI ChatGPT was used during code development and language editing. The released code, data products, and reported results were reviewed by the author.
