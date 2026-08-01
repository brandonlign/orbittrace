# Original method controls

The early control run recovered all three named showers, but the combined gate still failed. The failure exposed a problem in the gate itself.

## Named-shower recovery

| Shower | Precision | Recall | F1 |
|---|---:|---:|---:|
| Lyrids | 0.810 | 1.000 | 0.895 |
| Eta Aquariids | 0.904 | 1.000 | 0.950 |
| Southern Delta Aquariids | 0.856 | 1.000 | 0.922 |

## Injection sensitivity

| Injected members | Recovered runs | Median F1 |
|---:|---:|---:|
| 20 | 4 / 9 | 0.526 |
| 40 | 7 / 9 | 0.800 |
| 80 | 8 / 9 | 0.870 |

## Why the combined rule failed

The rule rejected any result whose largest cluster contained more than 30% of the sampled rows. Eta Aquariids made up 33.149% of their sample, so a correct full-recall cluster had to exceed the limit. The contradiction was in the gate, even though the clustering recovered the shower. The corrected 2024 holdout is documented in `../exact_method_controls_v3/`.
