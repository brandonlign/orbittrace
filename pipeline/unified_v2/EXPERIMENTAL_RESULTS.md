# Unified v2 exploratory results

This file records the new method lane separately from the frozen v1 evidence.
The run below is a fresh target-label-sealed v2 execution, but it is not a
prospective historical discovery because OrbitTrace was already known while
v2 was being developed.

## Method

The method has three components:

1. fixed overlapping 10-degree solar-longitude windows, each containing an
   exposure-normalized recurrent HDBSCAN condensed-tree score over the seed
   years, followed by 0.80-Jaccard duplicate removal;
2. leave-one-year-out robust conformal halo propagation, repeated in two
   simultaneous passes; and
3. a fixed orbital-distance coherence gate applied after propagation when
   orbital rows are available.

Candidates must have positive lower-tail support in both 2025 and 2026 and no
more than the pre-existing 300-member discovery ceiling. The full 163,737-row
five-year April panel remains available for halo propagation. Seed generation,
ranking, expansion, and the orbit gate all run without the OrbitTrace table.

## Equal-information literature benchmark

The archived pooled 2013+2014 rows, budgets, truth projection, and Hungarian
macro-F1 rule were retained. Truth was loaded only after v2 candidates were
generated.

| Panel | v2 F1 | Literature F1 | v2 recovered | Literature recovered |
|---|---:|---:|---:|---:|
| Sugar 2013 | 0.3996 | 0.2727 | 24 | 17 |
| Sugar 2014 | 0.4172 | 0.2938 | 23 | 16 |
| HDBSCAN 2013 | 0.2273 | 0.2021 | 13 | 12 |
| HDBSCAN 2014 | 0.2461 | 0.2096 | 13 | 11 |

Verdict: `PASS_V2_LITERATURE_4_OF_4`.

### Added D-criterion comparator

A clean-room adapter of the published EDMOND procedure was run on the exact
same rows, truth projections, candidate budgets, and Hungarian evaluator. It
uses Southworth-Hawkins `D_SH=0.05` seed grouping, geocentric `D_x=0.15`
centroid merging, and a five-member minimum. It is not the authors' original
code.

| Panel | v2 F1 | D-criterion F1 | v2 recovered | D-criterion recovered |
|---|---:|---:|---:|---:|
| Sugar 2013 | 0.3996 | 0.2168 | 24 | 13 |
| Sugar 2014 | 0.4172 | 0.2333 | 23 | 12 |
| HDBSCAN 2013 | 0.2273 | 0.1476 | 13 | 8 |
| HDBSCAN 2014 | 0.2461 | 0.1647 | 13 | 9 |

Expanded verdict: `PASS_V2_LITERATURE_AND_DCRITERION_8_OF_8`.

The wavelet family remains out of the direct claim because its native output
is a radiant-time density grid rather than a ranked family catalogue under the
frozen benchmark budget.

## Known-shower controls

Two-year 2024/2025 panels were clustered without passing labels to the method;
labels were joined only for scoring.

| Control | F1 | Recall | Precision |
|---|---:|---:|---:|
| Lyrids | 0.903 | 1.000 | 0.823 |
| Eta Aquariids | 0.956 | 1.000 | 0.916 |
| Southern Delta Aquariids | 0.962 | 0.963 | 0.961 |

All 3/3 controls pass the inherited 0.35 precision/recall/F1 rule. The largest
non-target cluster fraction is 0.196.

## Fresh target-label-sealed OrbitTrace run

The partitioned v2 hierarchy fit directly from raw GMN monthly rows; it did not
reuse the v1 seed catalogue. The target-free seed artifact contains 3,560
eligible recurrent families and has SHA-256
`f2b5f43ed15467ef38cc852d881c0aa48df16d28a42bb83459483db04d0bd621`.
Before expansion, posthoc exact-ID reveal found a pure 46-event OrbitTrace core
at rank 232.

All 3,560 families were then expanded without target access. The expanded
artifact has SHA-256
`21749aafd4ffd94721bc30b188a082309796cd3a836f0f687559c1fbcd951209`
and records the seed artifact hash. Posthoc reveal gives two important frozen
families:

| Rank | Branch | Overlap | Reported | Precision | Recall | F1 |
|---:|---|---:|---:|---:|---:|---:|
| 81 | leaf | 94/95 | 121 | 0.777 | 0.989 | 0.870 |
| 232 | recurrent EOM | **95/95** | 142 | 0.669 | **1.000** | 0.802 |

The rank-232 family therefore gives complete OrbitTrace event coverage in a
fresh target-sealed v2 run. The precision is moderate: 47 of the 142 reported
events are not in the frozen 95-event table. The rank-81 leaf is cleaner but
misses one event. This distinction must be stated rather than reporting only
the full-recall family.

An all-five-year global v2 hierarchy was also tested and discarded: its best
posthoc family recovered only 12/95. This supports the anchor-seed plus
cross-year propagation revision, rather than a claim that any recurrent score
is sufficient.

## Claim boundary

The evidence supports: “A fresh target-label-sealed partitioned-v2 catalogue
recovered all 95 OrbitTrace events in a rank-232 recurrent family with 66.9%
precision, while a rank-81 leaf recovered 94/95 with 77.7% precision. On the
equal-information SonotaCo benchmark, v2 beat the archived Sugar and HDBSCAN
comparators and a clean-room EDMOND D-criterion adapter on all evaluated
panels.”

It does not support universal state-of-the-art, an exact reproduction of the
EDMOND authors' code, a direct wavelet win, or formal FDR control. Because the
target was already known during method development, the correct phrase is
“fresh target-label-sealed recovery” or “label-blind rediscovery,” not
“prospective independent discovery of an unknown stream.” The original
historical OrbitTrace discovery claim must continue to rest on its separately
frozen discovery evidence.
