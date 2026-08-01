# GhostStream recovered method-control audit

**Verdict:** `RECOVERED_METHOD_CONTROL_AUDIT_NEGATIVE_GATE_INFEASIBLE`

The recovered control code was run unchanged from its immutable source commit.
The historical aggregate gate remains a no-go and is not retroactively converted to a pass.

## Preserved results

- Original aggregate known-shower verdict: **`NO_GO_DEGENERATE_PARENT_CLUSTER`**
- Untouched named showers individually recovered: **3/3**
- Lyrids: precision 0.810, recall 1.000, F1 0.895
- Eta Aquariids: precision 0.904, recall 1.000, F1 0.950
- Southern Delta Aquariids: precision 0.856, recall 1.000, F1 0.922
- Injection gate: **`INJECTION_GATE_PASS`**
- 20-member injections: **4/9**, median F1 0.526
- 40-member injections: **7/9**, median F1 0.800
- 80-member injections: **8/9**, median F1 0.870

## Why the aggregate rule was infeasible

Eta Aquariids supplied 6043 of 18230 sampled rows (33.149%). The frozen rule prohibited any cluster larger than 30%. At the observed recall, any ETA-containing target cluster had an unavoidable minimum fraction of 33.149%.

A prospective independent-year holdout with the same 30% threshold applied only to non-target clusters is required. That correction tests the intended failure mode without making a strong real shower mathematically incapable of passing.
