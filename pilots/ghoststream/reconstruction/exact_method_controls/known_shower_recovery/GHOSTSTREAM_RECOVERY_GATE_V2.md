# GhostStream known-shower recovery gate v2

**Verdict:** `NO_GO_DEGENERATE_PARENT_CLUSTER`

- Untouched named showers recovered: **3/3**
- Largest untouched cluster fraction: **36.7%**
- Frozen setting: `{'min_cluster_size': 40, 'min_samples': 10, 'scales': [4.0, 4.0, 3.0, 3.0], 'cluster_selection_method': 'eom'}`

## Untouched seasons

- **Lyrids (`LYR`):** n=2703, precision=0.810, recall=1.000, F1=0.895, recovered=True
- **Eta_Aquariids (`ETA`):** n=6043, precision=0.904, recall=1.000, F1=0.950, recovered=True
- **Southern_Delta_Aquariids (`SDA`):** n=8572, precision=0.856, recall=1.000, F1=0.922, recovered=True

The v2 correction was chosen from the v1 fragmentation pattern. None of the three final seasons appeared in v1.
Passing authorizes null-catalog and weak-stream injection tests; it does not claim a discovery.
