# GhostStream

GhostStream is a reproducible search for weak meteor streams hidden in public meteor-trajectory archives. The current result is a high-confidence, apparently uncatalogued late-April stream candidate recovered in a blind Global Meteor Network search and supported by recurrence across multiple years and by smaller CAMS and SonotaCo samples.

The candidate is not an officially recognized IAU meteor shower. Independent meteor-science review, duplicate-shower review, and final data-use and submission checks are still required.

## Repository structure

- `pilots/ghoststream/RESULTS.md` — current scientific result and claim boundary
- `pilots/ghoststream/april_stream/` — candidate solution, external checks, and expert-review materials
- `pilots/ghoststream/reconstruction/` — exact recovery, blind rediscovery, null tests, robustness checks, and method controls
- `pilots/ghoststream/recovered_pipeline/` — recovered executable source and source manifest
- `pilots/ghoststream/results/ghoststream_final_summary.json` — canonical machine-readable summary
- `.github/workflows/ghoststream-*` — reproducibility and audit workflows

## Current status

The supported claim is: **a computationally reproduced, high-confidence late-April meteor-stream discovery candidate that appears uncatalogued in the automated IAU comparison.**

This repository does not claim official IAU recognition, established-shower status, a confirmed parent body, absolute flux or ZHR, or publication readiness before independent review.

The canonical evidence source is commit `af9a21e10d8c365cf4ca75f945b9c04bdde137e0`. The checksum-locked canonical package and expert-review bundle are also preserved outside GitHub.
