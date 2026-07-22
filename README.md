# ReconnectID Pilot

ReconnectID Pilot is a reproducible feasibility study of whether compact coordinate-rotation-invariant plasma quantities help localize **already published** MMS electron diffusion region (EDR) events, particularly at larger approximate guide field. It does not search for new events and must not be interpreted as discovery, causality, or a new physical law.

## Reproduce

```bash
conda env create -f environment.yml
conda activate reconnectid-pilot

python scripts/00_environment_check.py
python scripts/01_fetch_event_list.py
python scripts/02_download_events.py
python scripts/03_build_dataset.py
python scripts/04_run_baselines.py
python scripts/05_run_models.py
python scripts/06_run_robustness.py
python scripts/07_generate_report.py

pytest -q
```

The complete sequence can also be launched with:

```bash
python -m reconnectid.run_all --config configs/pilot.yaml
```

Run the required three-event acquisition smoke test before scaling:

```bash
python scripts/01_fetch_event_list.py
python scripts/02_download_events.py --smoke
pytest -q
```

All downloads are cached under `data/raw/`; event array checkpoints are under `data/cache/events/`. Existing nonempty catalog and completed event checkpoints are reused. Raw CDFs are never modified. Failures are retained in `data/event_metadata/download_manifest.csv` and per-event JSON manifests; no event is silently removed and no values are fabricated.

## Event protocol and leakage controls

The source catalog is the published `EDR_list_MMS.txt` in [Zenodo record 8319481](https://doi.org/10.5281/zenodo.8319481). The two literature guide-field anchors and the 2015-10-16 canonical event are forced into a deterministic, seed-controlled farthest-point selection that balances time, spacecraft, and reference source. It does not take the first rows.

Every outer fold holds out one complete event. Imputation, missingness indicators, robust scaling, score direction, and regularization selection are fit from training events only. Inner model selection also holds out complete events. Samples from ±0.15 s are positive, samples from 0.15–0.60 s are excluded from binary fitting, and samples beyond ±0.60 s are negative. Event weights sum to one so dense events cannot dominate. Timestamp, sample index, time from center, event/spacecraft/reference identity, labels, and soft targets are excluded from model features.

## Physical definitions and units

All joint vectors and tensors are resolved in GSE. Values are converted before calculation: nT→T, mV/m→V/m, km/s→m/s, cm⁻³→m⁻³, and nPa→Pa. The exact elementary charge is `1.602176634e-19 C`.

The electron-frame nonideal field is

`E' = E + v_e × B`,

and electron-frame energy conversion is `D_e = J · E'`. The current used here is the quasi-neutral, single-spacecraft moment estimate

`J = e n_e (v_i − v_e)`.

It is an approximation and is **not equivalent** to a four-spacecraft curlometer current.

For a symmetric electron pressure tensor `P`, magnetic unit vector `b`, first invariant `I1 = tr(P)`, and second invariant `I2 = 1/2[(tr P)^2 − tr(P^2)]`, the code uses

`P_parallel = bᵀ P b`

and

`Q = 1 − 4 I2 / [(I1 − P_parallel)(I1 + 3 P_parallel)]`.

This is Eq. 5 of Swisdak, “Quantifying gyrotropy in magnetic reconnection,” *Geophysical Research Letters* 43, 43–49 (2016), [doi:10.1002/2015GL066980](https://doi.org/10.1002/2015GL066980). It is an invariant formulation, not a formula copied from an unverified secondary source. Non-positive-semidefinite tensors are flagged and their pressure features become missing; they are never silently repaired. MMS tensors returned as 3×3 are symmetrized only at floating-point precision; a six-component fallback documents its component convention in code.

## Synchronization and guide proxy

Each product is linearly synchronized to a 30 ms grid centered on the catalog time. Interpolation is supported only by two finite neighbors separated by no more than 0.15 s. A joint validity mask and per-product interpolation decisions are stored. Events below 70% final joint validity fail explicitly.

The event-level guide-field proxy uses magnetic minimum variance analysis: maximum variance approximates L, minimum variance approximates N, and M completes a right-handed system. Upstream medians estimate the L reversal; central median `|B_M|` estimates guide amplitude:

`guide_ratio_proxy = |B_M,center| / [0.5 |B_L,before − B_L,after| + epsilon]`.

This proxy is not ground truth. MVA eigenvalue ratios and reversal quality determine reliability. Both literature anchors must rank above the reliable-event median for a GO unless a documented data failure prevents assessment; otherwise the guide stratification is reported as unreliable.

## Outputs and interpretation

Intermediate scientific tables are Parquet; user-facing summaries are CSV/Markdown. Figures are always saved as PNG and PDF. `results/GO_NO_GO.md` applies the thresholds in `configs/pilot.yaml` and the predefined decision criteria without relaxing them after looking at results. Missing robustness evidence cannot count as a pass.

The nonlinear model is only a feasibility upper bound. Even a GO would justify a preregistered larger validation followed by stronger multi-spacecraft geometry and particle-in-cell simulation—not naming the composite a new diagnostic or physical law.
