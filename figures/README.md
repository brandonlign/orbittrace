# Paper figures

The three scripts in this directory regenerate the final paper figures from
frozen derived tables. They contain no alternative detectors or exploratory
plots.

| Figure | Panels | Frozen inputs |
| --- | --- | --- |
| 1 | exposure-normalized activity, annual recurrence, radiant centroids, orbital coherence | `activity_profile_year_summary.csv`, `activity_profile_metadata.json`, `annual_recurrence_2019_2026.csv`, `gmn_radiant_centroids.csv`, `orbit_coherence.csv`, `orbit_coherence_metadata.json`, external match tables |
| 2 | geographic replication, ACRF core robustness | `geographic_replication.csv`, `results/acrf_core_hyperparameter_robustness.csv` |
| 3 | supported and observed activity intervals, radiant/speed separation, orbital population separation, external timeline | `nop004_comparison.json`, `mdc_duplicate_screen.json`, external match tables |

The 81-setting validation result is retained in the frozen paper outputs and
reported in the manuscript text rather than given a redundant all-green panel.
Figure 2 reports the complete 153-setting core sweep: the clustering core is
tracked in 153/153 settings, while the plotted overlap points are only settings
materialized within the fixed top-100 reporting budget (83/153). The overlap
axis is normalized to the 95-member canonical target, so the dashed reference
line is 100% (95/95), not a raw count of 95.

Regenerate the paper-facing PNG/PDF/SVG set in the repository:

```bash
python figures/figure_1.py
python figures/figure_2.py
python figures/figure_3.py
```

Regenerate the temporary reproduction outputs used by `reproduce.py`:

```bash
python figures/generate_figures.py --out /tmp/orbittrace-figures
```

The committed copies under `figures/generated/` are synchronized with the
paper-facing copies in `orbittrace-raw/candidate/mdc/figures/`.
