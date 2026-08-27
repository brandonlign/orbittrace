# ACRF hyperparameter sensitivity

The released sweep contains 154 design cells and 153 unique parameter settings; the baseline appears twice in the raw design. The baseline reproduces the paper result exactly.

A corresponding OrbitTrace core can be tracked after ranking in all 153 settings. Rank is much less stable than the existence of the core itself: 83 settings place it within the fixed top-100 candidate budget.

- rank ≤ 100: **83/153 (54.2%)**
- exact 95/95 canonical recovery: **37/153 (24.2%)**
- at least 90/95 recovery: **49/153 (32.0%)**
- at least 80/95 recovery: **60/153 (39.2%)**

For settings inside the top-100 budget, final recall ranges from 0.337 to 1.000 (median 0.989), precision from 0.352 to 1.000 (median 0.748), F1 from 0.496 to 0.925 (median 0.800), and reported membership from 34 to 267 (median 123). Across all settings, the tracked rank ranges from 3 to 7,860 with a median of 34.

## By part of the sweep

| Grid | Cells | Rank ≤ 100 | Exact 95/95 | ≥90/95 | ≥80/95 | Median final overlap |
|---|---:|---:|---:|---:|---:|---:|
| Physical-scale factorial | 81 | 51.9% | 32.1% | 37.0% | 40.7% | 55 |
| HDBSCAN factorial | 9 | 77.8% | 33.3% | 33.3% | 33.3% | 78 |
| Joint extreme interactions | 64 | 54.7% | 14.1% | 26.6% | 39.1% | 57 |

The target is opened only after each setting has produced its ranked candidate catalogue, so target tracking does not affect candidate generation or rank. The full cell-level results are in `acrf_core_hyperparameter_robustness.csv`; the JSON file contains the same sweep summarized for machine use.
