# Corrected independent-year controls

The corrected control keeps the HDBSCAN settings, recovery thresholds, hidden labels, and 30% ceiling unchanged. It applies the ceiling to the largest **non-target** cluster instead of the true shower cluster.

That correction was set before the independent 2024 holdout data were examined.

| Control | True members | Precision | Recall | F1 | Target-cluster fraction | Largest non-target cluster | Passed |
|---|---:|---:|---:|---:|---:|---:|:---:|
| Lyrids | 1,230 | 0.821 | 1.000 | 0.902 | 0.298 | 0.130 | Yes |
| Eta Aquariids | 4,875 | 0.917 | 1.000 | 0.957 | 0.365 | 0.156 | Yes |
| Southern Delta Aquariids | 5,270 | 0.864 | 1.000 | 0.927 | 0.280 | 0.140 | Yes |

All three showers were recovered, and every non-target cluster remained below 30%.

The independent holdout shows that the unchanged clustering and recovery thresholds work when the degeneracy rule measures the intended failure mode. The earlier failed gate remains in the record because it documents the original flaw.
