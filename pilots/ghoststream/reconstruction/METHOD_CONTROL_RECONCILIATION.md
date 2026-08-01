# GhostStream method-control reconciliation

Updated: 2026-08-01

## Historical recovered result

The original recovered v2 method-control code was run unchanged from immutable commit `4175e5187fcc6faf3d1befb099a9e35be96850f2`.

It produced:

- Lyrids recovered: precision 0.810, recall 1.000, F1 0.895;
- Eta Aquariids recovered: precision 0.904, recall 1.000, F1 0.950;
- Southern Delta Aquariids recovered: precision 0.856, recall 1.000, F1 0.922;
- weak-stream injection gate: `INJECTION_GATE_PASS`;
- aggregate known-shower verdict: `NO_GO_DEGENERATE_PARENT_CLUSTER`.

The aggregate no-go is preserved. It is not rewritten as a pass merely because all three named targets were recovered.

## Why the v2 aggregate rule was contradictory

The v2 pass rule prohibited any cluster larger than 30% of the sampled holdout, including the cluster selected as the real target shower.

For the Eta Aquariids holdout:

- sampled rows: 18,230;
- true ETA members: 6,043;
- target prevalence: 33.149%;
- observed recall: 100%;
- frozen largest-cluster ceiling: 30%.

Therefore any full-recall ETA cluster necessarily exceeded the ceiling before a single contaminant was added. The target cluster had 90.4% precision and F1 0.950, but the aggregate rule was mathematically incapable of accepting it.

The contradiction concerns the degeneracy rule, not the individual recovery metrics. It does not justify silently deleting or overriding the original no-go.

## Prospective correction

Before examining independent 2024 holdouts, the following correction was frozen:

- keep the exact recovered HDBSCAN setting;
- keep the exact precision, recall, F1, and minimum-member thresholds;
- keep labels hidden during clustering;
- keep the 30% ceiling;
- apply the ceiling to the largest **non-target** cluster rather than the real target-shower cluster.

This directly tests the intended failure mode: a giant unrelated parent cluster dominating the partition.

## Independent 2024 result

| Control | Precision | Recall | F1 | Target-cluster fraction | Largest non-target fraction | Result |
|---|---:|---:|---:|---:|---:|:---:|
| Lyrids | 0.821 | 1.000 | 0.902 | 0.298 | 0.130 | Pass |
| Eta Aquariids | 0.917 | 1.000 | 0.957 | 0.365 | 0.156 | Pass |
| Southern Delta Aquariids | 0.864 | 1.000 | 0.927 | 0.280 | 0.140 | Pass |

All three targets were recovered, and all three largest non-target cluster fractions remained below the unchanged 0.30 ceiling.

## Authoritative evidence

Historical no-go and injection evidence:

- `exact_method_controls/method_controls.json`

Prospective corrected holdout:

- `exact_method_controls_v3/method_controls_v3.json`
- `exact_method_controls_v3/METHOD_CONTROLS_V3.md`

## Claim boundary

The correct statement is:

> The original recovered v2 aggregate gate returned a no-go because its global cluster-size rule was infeasible for a target-dominated Eta Aquariid holdout. That result remains preserved. A prospective correction, frozen before independent 2024 data were inspected and changing only the object to which the existing 30% ceiling was applied, passed all three named-shower controls.

This does not establish GhostStream as an official shower or replace independent meteor-science review.
