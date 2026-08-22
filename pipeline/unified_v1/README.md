# Periodic recurrent hierarchy detector v1

This is an exploratory single-method lane, separate from the frozen paper
evidence. One periodic physical HDBSCAN hierarchy supplies two fixed outputs:

- recurrent-EOM parents for established recurrent structures; and
- compact leaf descendants for novel weak-stream discovery.

The selected representation is periodic in solar longitude and sun-centered
radiant longitude, with scaled latitude and speed. The fixed clustering values
are `min_cluster_size=8` and `min_samples=4`. Novel leaves then face label-free
recurrence, observing-night, station-diversity, source-veto, orbit-compactness,
source-preserving null, catalogue-novelty, untouched-year, and 500-clone gates.

The target table is not imported by clustering, screening, ranking, or
validation. `--target` performs only a final posthoc reveal.

Main entrypoints:

```text
python -m pipeline.unified_v1.recurrent_application --representation periodic_physical6 --min-cluster-size 8 --min-samples 4 --years 2025,2026 --month 4 --out <directory> --target candidate/mdc/GhostStream_April_95_GMN_lookup.csv
python -m pipeline.unified_v1.periodic_controls --out <directory>
python -m pipeline.unified_v1.fair_benchmark --representation periodic_physical6 --min-cluster-size 8 --min-samples 4 --rows-root <rows> --truth-root <truth> --out <directory>
```

See `SELECTED_METHOD.json` for the frozen exploratory configuration and
`EXPERIMENTAL_RESULTS.md` for results and claim boundaries.
