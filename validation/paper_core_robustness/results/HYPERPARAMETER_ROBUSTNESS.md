# ACRF-v3.5 core-hyperparameter robustness

This is a frozen post-hoc sensitivity analysis. It does not select or retune the paper method.

- Raw design cells: **154**
- Unique parameter settings executed: **153**
- Baseline reproduced exactly: **True**
- Tracked family within rank 100: **83/153 (54.2%)**
- Exact 95/95 recovery: **37/153 (24.2%)**
- At least 90/95 recovery: **49/153 (32.0%)**
- At least 80/95 recovery: **60/153 (39.2%)**

## Min/median/max metrics

Final metrics are reported for cells whose selected family was within the preregistered top-100 materialization budget; all-cell values are also retained in the JSON summary.

- Rank (tracked), min / median / max: **3 / 34.0 / 7860**
- Final recall (top-100), min / median / max: **0.3368421052631579 / 0.9894736842105264 / 1.0**
- Final precision (top-100), min / median / max: **0.352059925093633 / 0.7480314960629921 / 1.0**
- Final F1 (top-100), min / median / max: **0.4961240310077519 / 0.8 / 0.924731182795699**
- Final member count (top-100), min / median / max: **34 / 123.0 / 267**

## Grid-specific results

### scale_factorial

- Cells: 81
- Rank <= 100: 51.9%
- Exact 95/95: 32.1%
- >=90/95: 37.0%
- >=80/95: 40.7%
- Final overlap median/range: 55.0 / 0-95

### hdbscan_factorial

- Cells: 9
- Rank <= 100: 77.8%
- Exact 95/95: 33.3%
- >=90/95: 33.3%
- >=80/95: 33.3%
- Final overlap median/range: 78.0 / 0-95

### joint_extreme_interactions

- Cells: 64
- Rank <= 100: 54.7%
- Exact 95/95: 14.1%
- >=90/95: 26.6%
- >=80/95: 39.1%
- Final overlap median/range: 57.0 / 0-95

