# CC-CFRS exploratory results

This file records exploratory, target-aware method design followed by
target-input-free execution. It is not a new paper claim and does not reopen
the frozen recurrent-EOM or locked-RRF results.

## Outcome

CC-CFRS did not achieve the unified objective of fair literature superiority,
useful transfer, and clean OrbitTrace recovery on the real five-year GMN April
panel. The lane is stopped before any production Stage 0 bank or formal
superiority claim.

## Controlled engineering smoke

The label-free scanner was tested on 765 rows containing a recurring synthetic
stream plus uniform background across three years. With 99 held-out phase
permutations, the best candidate contained all 285 synthetic stream rows with
precision 1.0 and recall 1.0. This is an implementation smoke test only; the
stream was synthetically constructed and does not establish scientific power.

## Full public GMN April panel

The same adapter loaded April 2022–2026 without target labels: 194,666 physical
rows. The preserved 95-row OrbitTrace table was joined only after ranking by
matching public trajectory timestamps for posthoc evaluation.

The production null count was not run. The following are bounded exploratory
runs with 9 randomizations, so their p-values are coarse diagnostics rather
than formal evidence:

| variant | candidates | selected | best posthoc target overlap | recurrence result |
|---|---:|---:|---:|---|
| initial exact-cell scan | 72 | 55 | 0/95 | null-level scan |
| compact-core + 2×2 alias family | 331 | 204 | 1/95 | null-level scan |
| compact-core + 4×4 alias family | 457 | 286 | 26/95 | best family `p_rec=1.0` |
| compact-core + 8×8 alias family | 509 | 369 | 68/95 | family `p_rec=0.8`, not cleanly selected |

The 8×8 result demonstrates why alias widening is not a valid rescue: it
increases target overlap by taking a broad union of nearby cells while losing
held-out significance and increasing runtime to 167 seconds for only 9 nulls.

## Independent density-family probe

A separate per-year HDBSCAN family probe was run on the same physical rows
without labels:

- published-style support (`min_cluster_size=15`, `min_samples=5`): 114
  recurrent families; best target overlap 5/95;
- lower-support exploratory setting (`8`, `4`): 607 families; best target
  overlap 36/95, but at rank 328/607 and not cleanly selected.

This rejects a naive yearly-HDBSCAN-plus-matching replacement as the unified
method.

## Closest binding results already in the repository

The existing evidence remains stronger than this exploratory lane, but it is a
two-method result rather than one unified method:

- recurrent-EOM passed the fair equal-information SonotaCo literature
  comparison on all four frozen panels, with macro-F1 0.3938 vs 0.2727,
  0.4280 vs 0.2938, 0.2205 vs 0.2021, and 0.2348 vs 0.2096;
- the separately frozen locked-RRF scan recovered OrbitTrace at rank 46/766
  with 29/95 exact members across four years;
- pristine cross-survey generalization remains unestablished.

Therefore the current honest answer is: no single new method in this work
beats the literature fairly, generalizes, and cleanly recovers OrbitTrace. The
existing paper-facing claim should retain its split roles and its explicit
generalization limitation.
