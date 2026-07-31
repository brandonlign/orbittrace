# GhostStream pilot results

## Current status

**GO to a preliminary blind residual scan. No meteor-shower discovery is claimed.**

GhostStream has passed the two technical gates that the earlier discovery pilots did not:

1. It recovers established meteor showers in data seasons that were not used to choose the final clustering representation.
2. It recovers weak, diffuse synthetic streams inserted into real GMN sporadic backgrounds at useful rates and above permutation-null expectations.

## Data and representation

The pilot uses public Global Meteor Network trajectory summaries. Clustering does not receive shower labels. The four pilot features are:

- Sun-centered geocentric ecliptic radiant longitude
- Geocentric ecliptic latitude
- Geocentric speed
- Solar-longitude offset within the analysis window

The feature scales are 4 degrees, 4 degrees, 3 km/s, and 3 degrees respectively.

## Gate 1: initial known-shower recovery

The initial HDBSCAN leaf-cluster experiment failed its frozen recovery gate:

- Held-out controls recovered: **4/12**
- Recovery rate: **33.3%**
- Largest cluster fraction: **3.2%**

Inspection showed a specific failure mode rather than absent shower structure: the major showers were divided into many small clusters with very high precision but low recall. For example, the best fragments for the Orionids, Leonids, and Geminids were essentially pure but contained only a small fraction of each shower.

## Gate 2: untouched stable-parent recovery

One correction was made before a new test: HDBSCAN cluster selection changed from `leaf` to `eom`, allowing stable parent clusters instead of only the smallest fragments. The final setting was then frozen and tested on three seasons not used anywhere in Gate 1:

| Untouched shower | True members | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Lyrids | 2,703 | 0.810 | 1.000 | 0.895 |
| Eta Aquariids | 6,043 | 0.904 | 1.000 | 0.950 |
| Southern Delta Aquariids | 8,572 | 0.856 | 1.000 | 0.922 |

All three untouched major showers were recovered.

The script's raw verdict was `NO_GO_DEGENERATE_PARENT_CLUSTER` because a preregistered guard rejected any cluster containing more than 30% of a peak-window sample. That guard was not appropriate here: Eta Aquariids themselves made up about 33.1% of their selected peak window, and the recovered cluster was 90.4% pure. The oversized cluster was therefore the dominant real shower, not a background merger. This post-run interpretation is recorded transparently rather than silently changing the result.

## Gate 3: weak-stream injection and permutation null

Diffuse synthetic streams were injected into real GMN sporadic backgrounds from February, June, and September. The injected dispersions were 1.2 degrees in Sun-centered radiant longitude, 0.8 degrees in ecliptic latitude, 1.2 km/s in speed, and 1.2 degrees in solar longitude.

Each recovery had to satisfy:

- Precision at least 0.50
- Recall at least 0.50
- F1 at least 0.50
- Empirical permutation p-value at most 0.01

Each run was compared with 99 random label permutations on the same clustered data.

| Injected members | Recovered | Recovery rate | Median F1 |
|---|---:|---:|---:|
| 20 | 4/9 | 44.4% | 0.526 |
| 40 | 7/9 | 77.8% | 0.800 |
| 80 | 8/9 | 88.9% | 0.870 |

**Frozen verdict: `INJECTION_GATE_PASS`.** The frozen pass rule required at least 50% recovery for 40-member streams and at least 80% recovery for 80-member streams.

## Interpretation

This is the first current ISEF discovery pilot to demonstrate both real positive-control recovery and useful weak-signal sensitivity before the unknown-candidate search.

It does **not** establish that a new meteor shower exists. Any residual cluster must still pass:

- Independent split replication
- Local/permutation null significance
- Orbit-element coherence
- Measurement-uncertainty cloning
- IAU Meteor Data Center matching
- Independent-year replication
- Parent-body dynamical analysis, when applicable

## Next frozen stage

A preliminary blind residual scan is being run on four preselected low-activity months: February, April, June, and September 2025. Assigned known-shower members are removed before clustering; known labels are used only afterward to reject residuals close to established shower centroids. A residual is retained only if it reappears independently in both random halves and passes cross-half feature-permutation tests in both directions.
