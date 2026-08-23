# Paper figures

The three scripts in this directory regenerate the paper figures from the
versioned derived tables.

| Figure | Panels | Inputs |
| --- | --- | --- |
| 1 | exposure-normalized activity, annual recurrence, radiant centroids, orbital coherence | `activity_profile_year_summary.csv`, `activity_profile_metadata.json`, `annual_recurrence_2019_2026.csv`, `gmn_radiant_centroids.csv`, `orbit_coherence.csv`, `orbit_coherence_metadata.json`, external match tables |
| 2 | geographic replication, ACRF core robustness | `geographic_replication.csv`, `results/acrf_core_hyperparameter_robustness.csv` |
| 3 | fixed activity interval, radiant/speed separation, orbital population separation, external timeline | `nop004_comparison.json` (derived from `results/mdc_duplicate_screen.json`), external match tables |

The manuscript reports the 81-setting validation result in text. Figure 2
shows the complete 153-setting core sweep: the clustering core is tracked in
153/153 settings, while the plotted overlap points are the settings
materialized within the top-100 reporting budget (83/153). The overlap axis is
normalized to the 95-member canonical target, so the dashed reference line is
100% (95/95).

Regenerate the PNG/PDF/SVG figure set in the repository:

```bash
python figures/figure_1.py
python figures/figure_2.py
python figures/figure_3.py
```

Regenerate the temporary reproduction outputs used by `reproduce.py`:

```bash
python figures/generate_figures.py --out /tmp/orbittrace-figures
```

The committed copies under `figures/generated/` are the release copies used by
the paper.
