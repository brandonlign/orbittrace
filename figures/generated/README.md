# Generated figure exports

This directory is intentionally source-generated. The release source of truth is the plotting code in `figures/`, the versioned derived tables in `data/derived/`, and the frozen robustness table in `results/`.

Generate synchronized PDF, PNG, and SVG exports with:

```bash
python figures/figure_1.py
python figures/figure_2.py
python figures/figure_3.py
```

or regenerate the complete temporary reproduction bundle with:

```bash
python reproduce.py --all
```

Do not treat older rendered copies as scientific inputs. Figure 1D uses the paper's vector-form `D_v` for GMN and external archive coherence; standard Southworth-Hawkins `D_SH` is used separately for the MDC/NOP catalogue comparison. Figure 2A contains region-selected members, not a partition of the 95-member canonical sample.
