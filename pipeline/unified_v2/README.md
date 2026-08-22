# Unified v2 exploratory detector

This lane is separate from the frozen `unified_v1` results. It implements three
method revisions that are still experimental:

1. fixed overlapping solar-longitude windows that keep each hierarchy
   memory-bounded, followed by deterministic overlap deduplication;
2. HDBSCAN condensed trees scored with exposure-normalized lower-tail annual
   stability and an explicit year-support gate;
3. a leave-one-year-out robust conformal halo expansion, with optional event
   uncertainties and local-background density q-values recorded for audit.

The fresh application ranks latest-two-year recurrent seeds, applies a fixed
300-member seed ceiling, and propagates eligible families through the full
five-year panel. A fixed orbital-distance gate is applied after the halo stage.

The default halo gate is the cross-fitted core-conformity envelope. The local
background q-values are diagnostics unless `halo_enforce_density_fdr=True` is
explicitly selected, because a formal FDR claim requires a separately frozen
null generator.

The application uses GMN's catalogue labels only to exclude already labelled
showers; it does not use OrbitTrace membership. For a rigorous run, do not pass
`--target` to the application. Freeze the generated artifact and use
`pipeline.unified_v2.reveal` in a separate process.

`--seed-only` freezes the complete target-free seed ranking before expansion.
`--seed-candidates` then replays that exact seed catalogue and records its
SHA-256 digest. The expanded application artifact is compacted after the orbit
gate so exhaustive candidate coverage does not retain redundant index lists.

Example:

```text
PYTHONPATH=/private/tmp/orbittrace-py314-deps:/private/tmp/orbittrace-benchmark-deps \
python3 -m pipeline.unified_v2.application \
  --years 2022,2023,2024,2025,2026 --month 4 \
  --seed-years 2025,2026 --seed-only --out <seed-output>
```
