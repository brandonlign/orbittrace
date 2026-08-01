# GhostStream weak-stream injection gate

**Verdict:** `INJECTION_GATE_PASS`

- n=20: 4/9 recovered (44.4%); median F1=0.526
- n=40: 7/9 recovered (77.8%); median F1=0.800
- n=80: 8/9 recovered (88.9%); median F1=0.870

Each recovery was compared with 99 random label permutations on the same clustered data.
Passing supports moving to full null-catalog calibration; it does not claim an unknown stream.
