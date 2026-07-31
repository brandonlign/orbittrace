# GhostStream pilot results

## Verdict

**GO — GhostStream produced a real, repeatable result.**

The pilot did not discover a brand-new meteor shower. Instead, a blind search independently recovered two showers that are still only on the IAU Meteor Data Center working list. One of them, the **Northern March gamma-Virginids (NMV)**, then passed a frozen multi-year confirmation test across previously untouched GMN data.

This is materially different from the earlier failed pilots: the method passed positive controls, passed weak-signal sensitivity tests, generated blind residuals, survived orbital and independent-year validation, and produced a defensible scientific finding.

## Final scientific result

### Northern March gamma-Virginids (NMV)

The 2025 blind search found a 31-member stream-like cluster without using the IAU working-list identity as a positive label. It had:

- Median orbital distance: **0.0705**
- Time-matched null p-value: **0.005**
- Independent 2024 replication: **25 members**, p = **0.005**
- Measurement-uncertainty clone stability: **500/500 trials passed**

The official IAU catalog match identified it as the working-list shower **NMV, Northern March gamma-Virginids**.

A frozen template was then applied to GMN meteors labeled sporadic in every February catalog from 2019 through 2025. A year counted only with at least eight members, a source-preserving permutation p-value at most 0.01, and median orbital distance at most 0.12.

| Year | Members | p-value | Median orbital distance | Pass |
|---|---:|---:|---:|---:|
| 2019 | 0 | 1.000 | — | No |
| 2020 | 5 | 0.450 | 0.0936 | No |
| 2021 | 11 | 0.005 | 0.0581 | Yes |
| 2022 | 8 | 0.005 | 0.0962 | Yes |
| 2023 | 17 | 0.005 | 0.0939 | Yes |
| 2024 | 19 | 0.005 | 0.0634 | Yes |
| 2025 | 52 | 0.005 | 0.0795 | Yes |

**NMV passed in five consecutive years from 2021–2025, including three untouched years (2021–2023), with 107 significant members and 112 selected members overall.** This passes the frozen multi-year confirmation gate.

### eta1-Coronae Australids (EOC)

A second blind residual matched the IAU working-list shower **EOC, eta1-Coronae Australids** and also passed 500/500 uncertainty-clone trials. It was significant in 2023, 2024, and 2025, but only one of the five untouched years passed, below the frozen requirement of three. EOC is therefore **supporting evidence, not a confirmed primary result**.

## Method validation

### Known-shower recovery

After correcting a clearly diagnosed fragmentation problem, the frozen stable-cluster representation recovered all three untouched major-shower controls:

| Shower | Precision | Recall | F1 |
|---|---:|---:|---:|
| Lyrids | 0.810 | 1.000 | 0.895 |
| Eta Aquariids | 0.904 | 1.000 | 0.950 |
| Southern Delta Aquariids | 0.856 | 1.000 | 0.922 |

### Weak-stream sensitivity

Diffuse streams were inserted into real GMN sporadic backgrounds and compared with 99 label permutations per run:

| Injected members | Recovered | Recovery rate | Median F1 |
|---|---:|---:|---:|
| 20 | 4/9 | 44.4% | 0.526 |
| 40 | 7/9 | 77.8% | 0.800 |
| 80 | 8/9 | 88.9% | 0.870 |

The frozen injection gate passed.

## Blind-search audit trail

The first blind null produced 264 apparent residuals because it destroyed real sporadic-source correlations. None were treated as discoveries. The corrected scan preserved radiant-speed structure, permuted only solar longitude, required replication across independent nights, excluded broad helion/antihelion/apex/toroidal regions, and deduplicated cluster fragments. It retained four residuals.

Orbital and 2024 validation reduced those four to two strong survivors. The official IAU catalog then showed that both corresponded to working-list showers rather than unknown showers. That negative novelty check is preserved transparently; it redirected the project from claiming a new shower to independently confirming a poorly established one.

## Current project direction

The strongest defensible project is now:

> **Independent multi-year confirmation and refinement of the Northern March gamma-Virginids using uncertainty-aware clustering of Global Meteor Network trajectories.**

The next research stage should estimate NMV's activity profile, radiant drift, velocity dispersion, orbital evolution, observational-selection robustness, and possible parent-body associations. The result should be framed as an independent confirmation and improved characterization of an IAU working-list shower—not as discovery of a brand-new shower.

## Status

- Known-positive recovery: **PASS**
- Weak-stream injection sensitivity: **PASS**
- Blind residual detection: **PASS after corrected source-preserving null**
- Orbital coherence: **PASS for NMV**
- Independent 2024 replication: **PASS for NMV**
- Official IAU check: **NMV working-list match**
- Uncertainty cloning: **500/500 PASS**
- Untouched 2019–2023 multi-year confirmation: **PASS, 3/5 years**
- Overall: **GO**

No claim of official shower establishment is made. Formal establishment would require fuller characterization, literature comparison, independent expert review, and potentially an IAU Meteor Data Center submission.
