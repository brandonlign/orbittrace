# GhostStream corrected independent-year method controls

**Verdict:** `CORRECTED_INDEPENDENT_YEAR_CONTROL_PASS`

The historical v2 gate remains recorded as `NO_GO_DEGENERATE_PARENT_CLUSTER`. That verdict is not retroactively changed. Its global 30% largest-cluster ceiling included the real target-shower cluster and was mathematically infeasible for Eta Aquariids because ETA itself occupied more than 30% of the sample.

A prospective correction was frozen before inspecting the 2024 holdouts. It retained the exact recovered HDBSCAN setting, recovery thresholds, label hiding, and 30% ceiling. The only correction was to apply the ceiling to the largest **non-target** cluster, which directly measures the intended unrelated-parent-cluster failure mode.

## Independent 2024 results

| Control | True members | Precision | Recall | F1 | Target cluster | Largest non-target cluster | Passed |
|---|---:|---:|---:|---:|---:|---:|:---:|
| Lyrids | 1,230 | 0.821 | 1.000 | 0.902 | 0.298 | 0.130 | Yes |
| Eta Aquariids | 4,875 | 0.917 | 1.000 | 0.957 | 0.365 | 0.156 | Yes |
| Southern Delta Aquariids | 5,270 | 0.864 | 1.000 | 0.927 | 0.280 | 0.140 | Yes |

- Eligible controls: **3/3**
- Recovered controls: **3/3**
- Largest non-target cluster checks below 0.30: **3/3**
- Seed: `20260801`
- Recovered source commit: `4175e5187fcc6faf3d1befb099a9e35be96850f2`
- Worker run: `30684874661`
- Evidence artifact: `8813559905`
- Artifact ZIP SHA-256: `920aa797a4228b02c89649fa871af7be85f6bc0c716b7b6380cc52ceb1209dd1`

The Lyrid and Southern Delta Aquariid windows each contained one unavailable GMN day. The gate passed on the available public trajectories without imputing the missing days.

## Interpretation

This resolves the specific v2 gate-design contradiction while preserving its historical no-go result. It demonstrates that the unchanged recovered clustering and recovery thresholds recover all three named showers in an independent year without producing an unrelated cluster above the frozen 30% ceiling.

It does not make GhostStream an official meteor shower, eliminate the need for expert duplicate review, or substitute for the recovered 2026 blind-discovery rerun.
