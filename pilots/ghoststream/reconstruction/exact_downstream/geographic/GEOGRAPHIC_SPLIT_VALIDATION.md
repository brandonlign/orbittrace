# Disjoint geographic GMN replication

**Verdict:** `APRIL_STREAM_REPLICATES_ACROSS_THREE_DISJOINT_GMN_GEOGRAPHIC_GROUPS`

Trajectories were assigned to exactly one geographic station group by majority station-country prefix. Ties and unknown prefixes were excluded. Thus no trajectory contributes to more than one regional test.

| Region | Members | Years | Activity p | Median D | Orbit-null p | Pass |
|---|---:|---|---:|---:|---:|:---:|
| Americas | 30 | 2022,2023,2024,2025,2026 | 6.41424e-07 | 0.04503 | 0.0001 | True |
| Europe_WestAsia | 22 | 2022,2023,2024,2025,2026 | 0.000225581 | 0.03375 | 0.0001 | True |
| Oceania_EastAsia_Africa | 44 | 2023,2024,2025,2026 | 2.1645e-10 | 0.04795 | 0.0001 | True |

Maximum cross-region medoid distance: **0.04054**

This is a geographically disjoint robustness test within the GMN processing system, not a fully independent reduction pipeline.
