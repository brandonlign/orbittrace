# Original method controls

The early control run recovered all three named showers, but its combined pass rule failed. That failure is kept because it exposed a real problem in the way the control gate had been written.

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

The original rule rejected any result whose largest cluster contained more than 30% of the sampled rows. Eta Aquariids themselves made up 33.149% of their sample. At full recall, a correct Eta Aquariid cluster therefore had to exceed the limit.

That is a contradiction in the control definition, not evidence that the clustering failed to recover Eta Aquariids. The original negative result remains recorded. A corrected rule was then specified before a separate 2024 holdout was examined; that run is documented in `../exact_method_controls_v3/`.
