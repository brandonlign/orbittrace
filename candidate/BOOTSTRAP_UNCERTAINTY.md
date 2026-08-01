# Bootstrap uncertainty

The 95 confirmed meteors are spread across five years and 29 observing nights. Meteors from the same night share observing conditions, so the uncertainty analysis resamples years and then nights within each selected year.

Twenty thousand bootstrap samples were generated. Each sample retained all meteors from the nights it selected. Circular means were used for angular quantities, and semimajor axis was recalculated from each sample’s mean q and e.

## Mean solution

| Quantity | Point estimate | 95% interval |
|---|---:|---:|
| Solar longitude | 37.150° | 36.334°–38.043° |
| RA | 247.170° | 246.428°–247.894° |
| Dec | −14.343° | −14.565° to −14.159° |
| Vg | 37.618 km/s | 37.201–37.865 km/s |
| q | 0.080114 AU | 0.078358–0.082575 AU |
| e | 0.943593 | 0.940369–0.945591 |
| i | 24.370° | 23.448°–24.961° |
| ω | 333.637° | 333.262°–333.946° |
| Ω | 37.157° | 36.341°–38.052° |
| a | 1.4203 AU | 1.3725–1.4549 AU |

## Radiant and speed drift

| Drift | Point estimate | 95% interval | Reading |
|---|---:|---:|---|
| dRA/dλ⊙ | +0.887°/° | +0.672 to +1.040 | positive drift is resolved |
| dDec/dλ⊙ | −0.158°/° | −0.248 to −0.037 | negative drift is resolved |
| dVg/dλ⊙ | −0.029 km/s/° | −0.178 to +0.221 | interval includes zero |

A second bootstrap that kept every year exactly once and resampled nights only gave the same qualitative result. The mean radiant and orbit are stable, the angular radiant drifts are supported, and the geocentric-speed drift remains unresolved.

## Leave-one-year-out ranges

| Quantity | Minimum | Maximum |
|---|---:|---:|
| RA | 247.030° | 247.463° |
| Dec | −14.385° | −14.309° |
| Vg | 37.513 km/s | 37.684 km/s |
| q | 0.079649 AU | 0.080748 AU |
| e | 0.942941 | 0.944170 |
| i | 24.089° | 24.507° |
| ω | 333.512° | 333.690° |
| Ω | 37.005° | 37.511° |
| dRA/dλ⊙ | +0.776 | +0.925 |
| dDec/dλ⊙ | −0.182 | −0.114 |
| dVg/dλ⊙ | −0.058 | −0.002 |

The bootstrap was also rerun from the original GMN catalogues rather than from a prepared candidate table. It recovered the required 10, 8, 14, 34, and 29 members for 2022–2026 before resampling.

These intervals describe variation across the observed years and nights. They are separate from the 1,000 event-level measurement perturbations used to test membership and orbital compactness.
