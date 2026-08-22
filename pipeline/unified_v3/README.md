# ACRF-v3.5 selected internal method

ACRF-v3.5 is the selected target-exposed method-development result. It combines
a global recurrent backbone with fixed overlapping local recurrent
refinements, prioritizes families repeated across windows, and fuses nested
parent/leaf cores before cross-year recovery.

The final refinement membership is a leave-one-year-out robust q99 envelope
with a frozen 1.02 finite-sample tolerance, followed by the D<=0.15 orbital
coherence gate. Solar-pair permutation q-values are retained as diagnostics.
Ranking is frozen before membership expansion and target reveal.

The method passes all eight frozen fair-comparison panels and recovers
OrbitTrace at rank 7 with 95/95 recall, 0.772 precision, and 0.872 F1. Because
OrbitTrace and the fair benchmark were exposed during version development,
this supports a recovery/rediscovery claim, not prospective discovery or
pristine cross-survey generalization. AMOS was not run because no rows are
present and repository governance closes that acquisition/execution lane.

Run the fair benchmark with:

```bash
python -m pipeline.unified_v3.fair_benchmark \
  --rows-root <rows> --truth-root <truth> --out <directory>
```
