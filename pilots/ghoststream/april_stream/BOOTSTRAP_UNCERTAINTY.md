# Cluster-bootstrap uncertainty for the GhostStream April solution

## Verdict

**The mean radiant and orbit are stable to year/night resampling. RA and declination drift remain nonzero, but the geocentric-speed drift is not resolved from zero.**

These intervals quantify sampling variability across years and observing nights. They are separate from the 1,000/1,000 measurement-uncertainty clone test, which evaluates perturbations of individual trajectory measurements.

## Primary bootstrap

- Members: **95**
- Years: **2022–2026**
- Unique observing nights: **29**
- Replicates: **20,000**
- Resampling: sample five years with replacement; within every selected year, sample its observing nights with replacement; retain all meteors from each selected night.
- Angular means: circular, mapped near the observed solution.
- Semimajor axis: derived from each bootstrap sample's mean q and e.

| Quantity | Point estimate | 95% year/night cluster-bootstrap interval |
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

| Drift | Point estimate | 95% interval | Interpretation |
|---|---:|---:|---|
| dRA/dλ⊙ | +0.887°/° | +0.672 to +1.040 | resolved positive drift |
| dDec/dλ⊙ | −0.158°/° | −0.248 to −0.037 | resolved negative drift |
| dVg/dλ⊙ | −0.029 km/s/° | −0.178 to +0.221 | **not distinguishable from zero** |

A second bootstrap retained every observed year exactly once and resampled nights only. It produced the same conclusion: RA and declination drift excluded zero; the Vg interval remained wide and crossed zero.

## Leave-one-year-out stability

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

## Interpretation boundary

The paper may report the measured positive RA drift and negative declination drift as resolved. The speed slope should be reported as a fitted value whose clustered confidence interval includes zero, not as a detected physical deceleration.

The arithmetic-mean MDC record remains appropriate and already passed both official MDC consistency programs. The robust medoid orbit remains preferable for membership and similarity tests; the arithmetic mean and clustered intervals should be used for the submission table and manuscript uncertainty statement.
