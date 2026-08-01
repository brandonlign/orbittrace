# How the two method-control results fit together

The repository keeps both control results because the first exposed a flaw in the gate and the second tested the corrected rule.

The first control recovered the Lyrids, Eta Aquariids, and Southern Delta Aquariids with strong F1 scores, but the overall gate returned a negative result. Its largest-cluster rule counted the true shower itself. Eta Aquariids occupied more than 30% of the sampled data, so a successful high-recall cluster could not satisfy the 30% ceiling.

The correction changed only what the ceiling measured: the largest unrelated cluster instead of the target shower. That change was fixed before the independent 2024 holdouts were examined.

The 2024 results were:

| Shower | F1 | Largest non-target cluster |
|---|---:|---:|
| Lyrids | 0.902 | 0.130 |
| Eta Aquariids | 0.957 | 0.156 |
| Southern Delta Aquariids | 0.927 | 0.140 |

All three named showers were recovered, and no unrelated cluster approached the 0.30 limit.

The original gate failed because its 30% rule was incompatible with the true prevalence of Eta Aquariids, even though all three target showers were recovered. After the rule was corrected, the same clustering and recovery thresholds passed on independent 2024 data.
