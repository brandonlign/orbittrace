# Periodic recurrent hierarchy v1 — exploratory results

## Outcome

The selected hierarchy meets the exploratory combined goal:

- it beats the frozen literature result on all four equal-information SonotaCo
  panels; and
- it recovers an OrbitTrace-like structure without target access during the
  January–July search, with support in every year from 2022 through 2026.

This does not replace the frozen paper evidence. The representation and 8/4
configuration were selected after comparing six inherited parameter pairs on
the already exposed SonotaCo benchmark. OrbitTrace had also been examined in
earlier exploratory development. These results are therefore exploratory and
posthoc, not a newly preregistered confirmatory claim.

## Selected method

One HDBSCAN hierarchy uses the six-dimensional periodic physical embedding

`cos/sin(solar longitude), cos/sin(sun-centered radiant longitude), latitude, speed`

with physical scales `(3.5°, 3.0°, 2.5 km/s, 2.5°)`,
`min_cluster_size=8`, and `min_samples=4`. Recurrent-EOM parents form the
established-stream branch. Same-hierarchy compact leaves form the novel-stream
branch and face fixed label-free physical, recurrence, source, catalogue,
untouched-year, and uncertainty gates.

## Fair literature benchmark

All methods receive the same pooled 2013+2014 label-free rows. Candidate lists
are produced before truth is loaded, evaluated at the comparator's candidate
budget, and matched one-to-one to truth by Hungarian macro-F1.

| Comparator panel | Method F1 | Literature F1 | Method recovered | Literature recovered |
|---|---:|---:|---:|---:|
| Sugar 2013 | 0.3953 | 0.2727 | 24 | 17 |
| Sugar 2014 | 0.4160 | 0.2938 | 23 | 16 |
| HDBSCAN 2013 | 0.2214 | 0.2021 | 13 | 12 |
| HDBSCAN 2014 | 0.2408 | 0.2096 | 13 | 11 |

Verdict: `PASS_PERIODIC_PHYSICAL6_RECURRENT_HIERARCHY_LITERATURE_4_OF_4`.
This benchmark evaluates the hierarchy's recurrent-EOM parent branch, which is
the appropriate fixed output for established showers. It does not substitute
the novel-leaf branch into the comparator after seeing truth.

## Generalization controls

With labels hidden during clustering, the same periodic hierarchy recovered:

| Control | F1 | Recall |
|---|---:|---:|
| Lyrids | 0.893 | 0.999 |
| Eta Aquariids | 0.950 | 1.000 |
| Southern Delta Aquariids | 0.933 | 1.000 |

All 3/3 controls pass. The largest non-target cluster fraction is 0.103.

## Target-free OrbitTrace search

The pooled 2025+2026 April hierarchy produced 1,435 raw leaves. Two passed the
fixed label-free screen; only one passed every 2022–2024 validation and the
500-clone test. That candidate was screened rank 1 in April and has center
`(-149.483852°, 7.399080°, 37.621380 km/s, solar longitude 37.409847°)`.

Before target reveal it had:

- 51 rows / 45 unique event times in 2025+2026;
- support of 10, 8, and 14 members in 2022, 2023, and 2024;
- recurrence-null `p=0.002` in each held-out year; and
- 500/500 uncertainty clones passing.

The January–July scan yielded four final survivors: one in January, OrbitTrace
in April, and two in July. OrbitTrace ranks 2nd globally by the fixed score and
1st within April. It is therefore a clean high-ranked discovery, but not the
only survivor or global rank 1.

Posthoc target reveal gives 76/95 canonical events across 2022–2026, with 77
unique candidate times: precision 0.987, recall 0.800, and F1 0.884. Annual
overlap is 10/10 (2022), 7/8 (2023), 14/14 (2024), 27/34 (2025), and 18/29
(2026). This is full five-year discovery of the structure, not complete 95/95
membership recovery.

## Claim boundary

The evidence supports: “the exploratory periodic recurrent hierarchy recovered
OrbitTrace as a target-free, five-year, uncertainty-stable candidate and beat
the frozen literature values on 4/4 equal-information panels.”

It does not yet support calling this a fresh held-out or preregistered
superiority result. A new main-paper method claim needs this exact configuration
frozen before one untouched comparator dataset or independently held-out
benchmark is opened. The historical blind OrbitTrace discovery and frozen
recurrent-EOM literature result remain the binding confirmatory evidence until
then.
