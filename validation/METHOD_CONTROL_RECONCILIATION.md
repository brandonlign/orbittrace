# How the two method-control results fit together

Two control results are kept because they answer different questions.

The first control recovered the Lyrids, Eta Aquariids, and Southern Delta Aquariids with strong F1 scores, but the overall gate returned a negative result. Its largest-cluster rule counted the true shower itself. Eta Aquariids occupied more than 30% of the sampled data, so a successful high-recall cluster could not satisfy the 30% ceiling.

The corrected control changed only the object to which that ceiling applied. Instead of limiting the target shower, it limited the largest unrelated cluster. This was specified before the independent 2024 holdouts were examined.

The 2024 results were:

| Shower | F1 | Largest non-target cluster |
|---|---:|---:|
| Lyrids | 0.902 | 0.130 |
| Eta Aquariids | 0.957 | 0.156 |
| Southern Delta Aquariids | 0.927 | 0.140 |

All three named showers were recovered, and no unrelated cluster approached the 0.30 limit.

The original gate remains recorded as a specification error. The prospective correction passed in an independent year with the same clustering and recovery thresholds.
