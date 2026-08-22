# ACRF/HDBSCAN clustering-core hyperparameter robustness

This is the frozen post-hoc clustering-core diagnostic preregistered before execution. It does **not** select replacement hyperparameters and does **not** claim that every parameter setting reproduces the full ACRF-v3.5 123-member catalogue. For each setting, HDBSCAN clustering was completed without access to OrbitTrace target membership; the 63 canonical 2025-2026 timestamps were opened only afterward to track the corresponding recurrent family.

## Frozen design

- 154 raw design cells collapse to **153 unique parameter settings** because the baseline occurs in both the feature-scale and HDBSCAN factorials.
- Full 3^4 factorial over the four physical scales: **81 settings**.
- Full 3x3 factorial over `min_cluster_size` and `min_samples` at the paper scales: **9 settings**.
- Low/high scale corners crossed with four HDBSCAN corners: **64 settings**.
- No setting was added, deleted, narrowed, substituted, or selected after results were observed.

## Result

The corresponding recurrent family was found in **153/153 settings**. The tracked cluster remained high-purity: median precision was **1.000** (range 0.667-1.000). Fragmentation varied with the clustering geometry: median overlap was **43/63**, ranging from **11/63** to **56/63**, and median F1 was **0.800** (range 0.297-0.908). Seven settings recovered at least 50/63 canonical seed events; no single raw HDBSCAN cluster recovered all 63.

At the manuscript baseline [3.5, 3.0, 2.5, 2.5], `min_cluster_size=8`, `min_samples=4`, the tracked leaf contained **43** events and all 43 were canonical (precision 1.000; recall 0.683; F1 0.811). This is a clustering-core diagnostic, so its membership is intentionally not the full ACRF fused/recovered 123-member output.

### Breakdown

| Grid | Settings | Tracked | Median overlap | Overlap range | Median precision | Median F1 |
|---|---:|---:|---:|---:|---:|---:|
| Feature-scale factorial | 81 | 81 | 43/63 | 25-54 | 1.000 | 0.811 |
| HDBSCAN factorial | 9 | 9 | 48/63 | 32-51 | 1.000 | 0.865 |
| Joint extreme interactions | 64 | 64 | 39.5/63 | 11-56 | 1.000 | 0.757 |

## Interpretation

The criticism that the clustering hyperparameters were never stress-tested is no longer correct: all four physical distance scales and both HDBSCAN core parameters were varied over a frozen, broad grid. The result is not uniform invariance. Instead, it shows a persistent high-purity OrbitTrace density component across every tested setting, with substantial parameter-dependent fragmentation in the raw HDBSCAN core. That sensitivity must be reported rather than hidden; ACRF's cross-window fusion and cross-year recovery are the parts of the method intended to recover a fuller family from such fragmented cores.

## Execution provenance

- Public execution repository: `brandonlign/runner`
- Frozen branch head: `97d355abdad34f209f3c5d33912b937ec06a4293`
- Workflow run: `32585805245`
- Shard artifact digests:
  - shard 0: `sha256:abd9e4f862b1acdebd69da2eeaae9a66eb06bbdb8cd0458f9303ad5643f4c8a4`
  - shard 1: `sha256:ca9afd8081af2ff42f18931dfcd62bffe9895cfe936686a87d7d63a28aa32544`
  - shard 2: `sha256:ab6fe753d63f1ba903bcd2d0a48cb1d5fa6f290499f44cc3d4b85647439bd8a9`
  - shard 3: `sha256:028b081c334be17fc961caad69e3d2f86f70aec6f3c989f9da0336de3ef848b3`

The four shard jobs completed successfully. The workflow's separate aggregation job failed because its aggregation environment omitted `hdbscan`; the raw shard CSVs were complete and were combined without recomputation. The consolidated table contains exactly one row for each of the 153 preregistered unique settings.
