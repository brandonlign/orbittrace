# ReconnectID Pilot summary

## 1. Research question

Does a compact set of coordinate-rotation-invariant plasma quantities localize already-published MMS electron diffusion region (EDR) centers more reliably than individual established diagnostics, especially at higher approximate guide field? This is a feasibility test, not a discovery claim.

## 2. Data and event selection

The source catalog is Zenodo record 8319481 (`EDR_list_MMS.txt`). Selection uses required anchors plus seeded farthest-point stratification across time, spacecraft, and reference identity. 24 events passed the complete acquisition, synchronization, and ≥70% validity requirement. Failures remain in the manifests.

## 3. Diagnostic definitions

The analysis uses electron-frame field `E'=E+v_e×B`, approximate moment current `J=e n_e(v_i-v_e)`, `D_e=J·E'`, parallel/perpendicular projections, pressure invariants, and Swisdak Q. The moment current is not a four-spacecraft curlometer current.

## 4. Unit conversions

Magnetic field nT→T; electric field mV/m→V/m; velocity km/s→m/s; density cm⁻³→m⁻³; pressure nPa→Pa; `e=1.602176634×10⁻¹⁹ C`.

## 5. Guide-field-proxy limitations

The MVA-derived `|B_M|/(0.5|B_L,before−B_L,after|)` is an event-level proxy, not ground truth. Reliability requires magnetic reversal quality and MVA eigenvalue separation. Anchor results:

- EDR001: proxy=2.821, all-event rank=2/24, reliable rank=1/17, label=large-guide-field anchor
- EDR023: proxy=0.3634, all-event rank=15/24, reliable rank=10/17, label=intermediate-guide-field anchor

## 6. Validation strategy

Preprocessing and regularization are fitted inside nested event-level cross-validation. No time samples from a held-out event enter training. Confidence intervals resample events, and structured permutations retain within-event time-series structure.

## 7. Results with uncertainty

```text
                                  auprc_median  localization_median_seconds  within_0p30_fraction
method                                                                                           
baseline:D_e_abs                        0.4149                        0.585                0.4167
baseline:D_e_normalized                0.03609                         3.03               0.04167
baseline:D_e_positive                   0.2838                        0.345                   0.5
baseline:E_parallel_abs                 0.1749                        0.585                0.4167
baseline:E_prime_magnitude              0.1537                        1.125                0.3333
baseline:J_magnitude                    0.7971                         0.03                  0.75
baseline:Q                              0.3994                        0.405                0.4583
baseline:pressure_anisotropy_abs       0.03599                        1.575                  0.25
nonlinear_invariant                     0.6089                        0.045                0.7083
sparse_invariant                        0.5627                        0.045                0.7083
```

Guide-stratified event medians:

```text
                                              auprc_median  localization_median_seconds  within_0p30_fraction
guide_group method                                                                                           
higher      baseline:D_e_abs                        0.2593                        0.795                0.3333
            baseline:D_e_normalized                0.03654                         4.29                     0
            baseline:D_e_positive                   0.1818                        0.405                   0.5
            baseline:E_parallel_abs                 0.1228                         0.45                   0.5
            baseline:E_prime_magnitude              0.1788                        1.875                0.1667
            baseline:J_magnitude                    0.2797                         0.84                0.3333
            baseline:Q                              0.3799                         2.94                0.1667
            baseline:pressure_anisotropy_abs        0.3005                          0.3                   0.5
            nonlinear_invariant                     0.5625                         0.03                0.6667
            sparse_invariant                        0.4547                         0.03                0.6667
lower       baseline:D_e_abs                        0.2242                         0.72                0.1667
            baseline:D_e_normalized                 0.0214                         4.23                     0
            baseline:D_e_positive                  0.09384                        0.675                0.3333
            baseline:E_parallel_abs                0.08751                         2.19                0.1667
            baseline:E_prime_magnitude              0.0471                        1.335                0.1667
            baseline:J_magnitude                     0.974                         0.03                0.8333
            baseline:Q                              0.2379                          0.6                0.3333
            baseline:pressure_anisotropy_abs       0.01557                         2.67                     0
            nonlinear_invariant                     0.6151                        0.105                0.6667
            sparse_invariant                        0.6617                         0.21                0.6667
middle      baseline:D_e_abs                        0.5623                         0.27                   0.6
            baseline:D_e_normalized                0.07039                         2.04                   0.2
            baseline:D_e_positive                   0.3615                          0.3                   0.6
            baseline:E_parallel_abs                 0.2119                         0.03                   0.6
            baseline:E_prime_magnitude              0.2614                            0                   0.6
            baseline:J_magnitude                    0.9435                         0.03                   0.8
            baseline:Q                              0.5802                         0.27                   0.6
            baseline:pressure_anisotropy_abs       0.02222                         1.92                   0.2
            nonlinear_invariant                     0.9164                         0.12                   0.8
            sparse_invariant                        0.8797                         0.15                   0.6
unreliable  baseline:D_e_abs                        0.4041                         0.06                0.5714
            baseline:D_e_normalized                0.04214                         1.77                     0
            baseline:D_e_positive                   0.3729                         0.03                0.5714
            baseline:E_parallel_abs                 0.3463                         0.54                0.4286
            baseline:E_prime_magnitude              0.1655                         2.61                0.4286
            baseline:J_magnitude                    0.7327                            0                     1
            baseline:Q                              0.4845                         0.15                0.7143
            baseline:pressure_anisotropy_abs       0.04863                         0.48                0.2857
            nonlinear_invariant                     0.5614                         0.06                0.7143
            sparse_invariant                        0.7907                         0.03                0.8571
```

Higher-guide event-bootstrap model-minus-baseline comparisons (95% percentile intervals; localization signs are oriented so positive favors the model):

```text
              model                         baseline                     metric  estimate    ci_low  ci_high  n_events
   sparse_invariant                 baseline:D_e_abs                      auprc    0.1449  -0.09713   0.3676         6
   sparse_invariant                 baseline:D_e_abs localization_error_seconds      0.52    -1.486    2.585         6
   sparse_invariant                 baseline:D_e_abs                within_0p30    0.3333         0   0.6667         6
   sparse_invariant          baseline:D_e_normalized                      auprc    0.4032    0.2467   0.6029         6
   sparse_invariant          baseline:D_e_normalized localization_error_seconds     2.455      0.71    4.375         6
   sparse_invariant          baseline:D_e_normalized                within_0p30    0.6667    0.3333        1         6
   sparse_invariant            baseline:D_e_positive                      auprc    0.1678  -0.09885   0.3861         6
   sparse_invariant            baseline:D_e_positive localization_error_seconds      0.37    -1.645    2.505         6
   sparse_invariant            baseline:D_e_positive                within_0p30    0.1667         0      0.5         6
   sparse_invariant          baseline:E_parallel_abs                      auprc    0.2703   0.05641   0.5245         6
   sparse_invariant          baseline:E_parallel_abs localization_error_seconds       0.6     -0.08     1.64         6
   sparse_invariant          baseline:E_parallel_abs                within_0p30    0.1667   -0.3333   0.6667         6
   sparse_invariant       baseline:E_prime_magnitude                      auprc    0.2403  -0.03228   0.5251         6
   sparse_invariant       baseline:E_prime_magnitude localization_error_seconds     1.635     0.515     3.02         6
   sparse_invariant       baseline:E_prime_magnitude                within_0p30       0.5    0.1667   0.8333         6
   sparse_invariant             baseline:J_magnitude                      auprc   0.03008   -0.1482   0.1896         6
   sparse_invariant             baseline:J_magnitude localization_error_seconds    -0.055     -1.86     1.29         6
   sparse_invariant             baseline:J_magnitude                within_0p30    0.3333         0   0.6667         6
   sparse_invariant                       baseline:Q                      auprc   0.03374   -0.1053   0.1552         6
   sparse_invariant                       baseline:Q localization_error_seconds     1.535     0.445    2.735         6
   sparse_invariant                       baseline:Q                within_0p30       0.5    0.1667   0.8333         6
   sparse_invariant baseline:pressure_anisotropy_abs                      auprc   0.05539    -0.197   0.3078         6
   sparse_invariant baseline:pressure_anisotropy_abs localization_error_seconds     0.315   -0.7451     1.52         6
   sparse_invariant baseline:pressure_anisotropy_abs                within_0p30    0.1667         0      0.5         6
nonlinear_invariant                 baseline:D_e_abs                      auprc     0.211  -0.02397   0.4334         6
nonlinear_invariant                 baseline:D_e_abs localization_error_seconds     1.155     -0.18    2.881         6
nonlinear_invariant                 baseline:D_e_abs                within_0p30    0.3333   -0.3333   0.8333         6
nonlinear_invariant          baseline:D_e_normalized                      auprc    0.4693    0.2916   0.6492         6
nonlinear_invariant          baseline:D_e_normalized localization_error_seconds      3.09      1.59     4.49         6
nonlinear_invariant          baseline:D_e_normalized                within_0p30    0.6667    0.3333        1         6
nonlinear_invariant            baseline:D_e_positive                      auprc    0.2338 -0.004197   0.4419         6
nonlinear_invariant            baseline:D_e_positive localization_error_seconds     1.005    -0.285     2.82         6
nonlinear_invariant            baseline:D_e_positive                within_0p30    0.1667   -0.3333   0.6667         6
nonlinear_invariant          baseline:E_parallel_abs                      auprc    0.3364    0.1393   0.5492         6
nonlinear_invariant          baseline:E_parallel_abs localization_error_seconds     1.235     -0.09    2.815         6
nonlinear_invariant          baseline:E_parallel_abs                within_0p30    0.1667   -0.3333   0.6667         6
nonlinear_invariant       baseline:E_prime_magnitude                      auprc    0.3064  -0.01538   0.5761         6
nonlinear_invariant       baseline:E_prime_magnitude localization_error_seconds      2.27      0.38    4.238         6
nonlinear_invariant       baseline:E_prime_magnitude                within_0p30       0.5   -0.1667        1         6
nonlinear_invariant             baseline:J_magnitude                      auprc   0.09613  -0.06972   0.2736         6
nonlinear_invariant             baseline:J_magnitude localization_error_seconds      0.58     -0.01     1.48         6
nonlinear_invariant             baseline:J_magnitude                within_0p30    0.3333         0   0.6667         6
nonlinear_invariant                       baseline:Q                      auprc   0.09979  -0.07074   0.2497         6
nonlinear_invariant                       baseline:Q localization_error_seconds      2.17    0.9136    3.495         6
nonlinear_invariant                       baseline:Q                within_0p30       0.5    0.1667   0.8333         6
nonlinear_invariant baseline:pressure_anisotropy_abs                      auprc    0.1214   -0.1415   0.3843         6
nonlinear_invariant baseline:pressure_anisotropy_abs localization_error_seconds      0.95    -0.365    2.265         6
nonlinear_invariant baseline:pressure_anisotropy_abs                within_0p30    0.1667   -0.3333   0.6667         6
```

Held-out literature-anchor results:

```text
event_id                           method   auprc  localization_error_seconds  within_0p30
  EDR001                 baseline:D_e_abs  0.7265                           0         True
  EDR001          baseline:D_e_normalized  0.1193                        0.69        False
  EDR001            baseline:D_e_positive  0.8289                           0         True
  EDR001          baseline:E_parallel_abs  0.5617                           0         True
  EDR001       baseline:E_prime_magnitude  0.2315                        2.25        False
  EDR001             baseline:J_magnitude  0.7568                           0         True
  EDR001                       baseline:Q  0.3162                        3.21        False
  EDR001 baseline:pressure_anisotropy_abs  0.8224                        0.03         True
  EDR001              nonlinear_invariant  0.5799                           0         True
  EDR001                 sparse_invariant  0.4162                           0         True
  EDR023                 baseline:D_e_abs  0.5623                        0.27         True
  EDR023          baseline:D_e_normalized 0.02499                        1.68        False
  EDR023            baseline:D_e_positive 0.06133                         0.3         True
  EDR023          baseline:E_parallel_abs  0.1879                        0.03         True
  EDR023       baseline:E_prime_magnitude 0.06423                        0.75        False
  EDR023             baseline:J_magnitude       1                        0.03         True
  EDR023                       baseline:Q  0.5802                        0.27         True
  EDR023 baseline:pressure_anisotropy_abs 0.02222                        1.38        False
  EDR023              nonlinear_invariant       1                        0.12         True
  EDR023                 sparse_invariant       1                        0.03         True
```

## 8. Robustness results

Rotation required maximum relative discrepancy <1e-8; observed maximum was 1.019e-09 if the rotation table was available.

Mean event AUPRC over input-noise trials:

```text
noise_fraction                     0.005   0.010   0.020   0.050
method                                                          
baseline:D_e_abs                  0.3863  0.3858   0.386  0.3874
baseline:D_e_normalized          0.05503 0.05519 0.05569 0.05545
baseline:D_e_positive             0.3164  0.3161   0.316  0.3152
baseline:E_parallel_abs           0.2336  0.2346  0.2359  0.2338
baseline:E_prime_magnitude        0.2205  0.2202  0.2197  0.2182
baseline:J_magnitude              0.7209   0.721  0.7192  0.7126
baseline:Q                        0.3929  0.3647  0.2743 0.09465
baseline:pressure_anisotropy_abs  0.1552  0.1547  0.1547  0.1511
nonlinear_invariant               0.5833  0.5801  0.5624  0.5365
sparse_invariant                  0.6183  0.5979  0.5615  0.3331
```

Median event AUPRC under catalog-time shifts:

```text
method                baseline:D_e_abs  baseline:D_e_normalized  baseline:D_e_positive  baseline:E_parallel_abs  baseline:E_prime_magnitude  baseline:J_magnitude  baseline:Q  baseline:pressure_anisotropy_abs  nonlinear_invariant  sparse_invariant
center_shift_seconds                                                                                                                                                                                                                                  
-0.12                           0.2387                   0.0348                 0.1492                   0.1165                       0.108                0.6488      0.3464                           0.03078               0.5495            0.5147
-0.06                           0.3071                  0.03521                 0.2263                   0.1657                       0.147                0.7925      0.4061                            0.0385                0.606            0.5455
-0.03                           0.3435                  0.03439                 0.2361                   0.1664                      0.1462                0.8662      0.4717                           0.02667               0.6326            0.6582
 0.03                           0.4195                   0.0406                 0.2978                   0.1943                      0.1597                0.8363      0.4012                           0.03203                0.624            0.5788
 0.06                           0.4022                   0.0452                 0.3297                   0.1833                      0.1529                0.8085      0.3862                           0.03384               0.5791            0.5513
 0.12                           0.3082                  0.04179                 0.2261                   0.1765                      0.1288                0.6094      0.3491                            0.0312               0.4997             0.457
```

Median leave-reference-group-out AUPRC:

```text
                     value
method                    
nonlinear_invariant 0.4258
sparse_invariant    0.5173
```

Feature-ablation median event AUPRC:

```text
method               nonlinear_invariant  sparse_invariant
ablation                                                  
all_except_D_e                    0.5235            0.5627
all_except_Q                       0.557            0.6401
all_invariant                     0.5235            0.5627
established_only                  0.5808            0.6905
field_velocity_only               0.3767            0.6759
pressure_only                     0.3055            0.3778
```

Event-center permutation results:

```text
                          method  observed_mean_auprc  permutation_p
                baseline:D_e_abs               0.3873       0.001996
         baseline:D_e_normalized              0.05536         0.2236
           baseline:D_e_positive               0.3167       0.001996
         baseline:E_parallel_abs               0.2326       0.001996
      baseline:E_prime_magnitude               0.2205       0.001996
            baseline:J_magnitude               0.7211       0.001996
                      baseline:Q                 0.41       0.001996
baseline:pressure_anisotropy_abs               0.1555        0.05389
             nonlinear_invariant               0.6549       0.001996
                sparse_invariant               0.6221       0.001996
```

## 9. Failure cases

The three worst events are selected mechanically by held-out sparse-model AUPRC:

```text
event_id   auprc  localization_error_seconds  within_0p30
  EDR060 0.04158                        1.89        False
  EDR003   0.188                         5.1        False
  EDR021  0.2223                        0.03         True
```

Data and analysis failures are preserved in `data/event_metadata/download_manifest.csv` and `data/processed/events.parquet`.

## 10. Decision: CONDITIONAL

- One literature anchor does not rank above the median; the pilot guide stratification is unreliable.

## 11. What this pilot does not prove

It does not discover an EDR, establish causality, validate a physical law, prove that the proxy is the true guide field, or establish transfer to simulations or other missions. Statistical discrimination, temporal localization, coordinate invariance, and physical interpretation are distinct claims.

## 12. Exact recommended next step

Estimate LMN geometry with multi-spacecraft timing/curlometer checks and repeat on a larger preregistered catalog before any PIC or symbolic-discovery investment.
