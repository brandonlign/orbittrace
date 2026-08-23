# Paper figures

The three scripts in this directory regenerate the paper figures from the
versioned derived tables.

| Figure | Panels | Inputs |
| --- | --- | --- |
| 1 | exposure-normalized activity, annual recurrence, radiant centroids, orbital coherence | `activity_profile_year_summary.csv`, `activity_profile_metadata.json`, `annual_recurrence_2019_2026.csv`, `gmn_radiant_centroids.csv`, `orbit_coherence.csv`, `orbit_coherence_metadata.json`, external match tables |
| 2 | geographic replication, ACRF core robustness | `geographic_replication.csv`, `results/acrf_core_hyperparameter_robustness.csv` |
| 3 | fixed activity interval, radiant/speed separation, orbital population separation, external timeline | `nop004_comparison.json` (derived from `results/mdc_duplicate_screen.json`), external match tables |

Figure 1D uses the paper's vector-form `D_v` metric throughout. The GMN point
and upper error bar are the internal median and 90th percentile relative to
the GMN medoid, and the CAMS, SonotaCo, and EDMOND `orbit_d` values are `D_v`
from each external matched orbit to the same fixed GMN reference orbit.
Southworth-Hawkins `D_SH` is used separately for the MDC/NOP catalogue
comparisons in Figure 3; the two metrics must not be interchanged.

The manuscript reports the 81-setting validation result in text. Figure 2
shows the complete 153-setting core sweep: a corresponding clustering core is
tracked post-ranking in 153/153 settings, while the plotted overlap points are
the settings materialized within the top-100 reporting budget (83/153). The
target is opened only after each setting's ranked candidate catalogue has been
generated, so target tracking does not affect candidate generation or rank.
The overlap axis is normalized to the 95-member canonical target, so the
dashed reference line is 100% (95/95). Figure 2A reports region-selected
radiant-speed-time members; because orbit is tested afterward, the three
regional counts are not a partition of the 95-member canonical table.

Generate synchronized PNG/PDF/SVG figure exports:

```bash
python figures/figure_1.py
python figures/figure_2.py
python figures/figure_3.py
```

Regenerate the temporary reproduction outputs used by `reproduce.py`:

```bash
python figures/generate_figures.py --out /tmp/orbittrace-figures
```

`figures/generated/` intentionally contains only its generation note in the
source repository. Rendered exports should be regenerated from the release
commit rather than inherited from an older manuscript state.
