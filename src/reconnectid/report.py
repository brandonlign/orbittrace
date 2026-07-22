"""Conservative report and predefined GO/CONDITIONAL/NO-GO decision generation."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
from .config import PilotConfig
from .evaluation import event_bootstrap_difference


def _text_table(value: pd.DataFrame | pd.Series, index: bool = True) -> str:
    """Render a dependency-free fixed-width table inside Markdown."""
    if isinstance(value, pd.Series):
        value = value.to_frame("value")
    return "```text\n" + value.to_string(index=index, float_format=lambda x: f"{x:.4g}") + "\n```"


def decide(events: pd.DataFrame, metrics: pd.DataFrame, cfg: PilotConfig, noise: pd.DataFrame | None = None,
           rotation: pd.DataFrame | None = None) -> tuple[str, list[str]]:
    reasons: list[str] = []
    usable = events[events.get("success", False).fillna(False)] if len(events) else events
    if len(usable) < cfg.minimum_events_required:
        return "NO-GO", [f"Only {len(usable)} events passed data-quality requirements; at least {cfg.minimum_events_required} were predefined as necessary."]
    high = usable[usable.get("guide_group", "") == "higher"]
    if len(high) < 3:
        return "NO-GO", [f"Only {len(high)} reliable higher-guide events are available; at least 3 are required."]
    anchor = usable[usable.get("literature_label", "").astype(str).str.contains("guide-field anchor")]
    median = usable.loc[usable.get("reliable", False).fillna(False), "guide_ratio_proxy"].median()
    assessed = anchor.guide_ratio_proxy.notna()
    if assessed.sum() == 2 and not (anchor.loc[assessed, "guide_ratio_proxy"] > median).all():
        below = int((anchor.loc[assessed, "guide_ratio_proxy"] <= median).sum())
        if below == 2: return "NO-GO", ["Both literature anchors fail the predefined above-median guide-proxy validation."]
        return "CONDITIONAL", ["One literature anchor does not rank above the median; the pilot guide stratification is unreliable."]
    if assessed.sum() < 2:
        return "CONDITIONAL", ["The guide-field proxy could not be assessed for both literature anchors."]
    high_metrics = metrics[metrics.event_id.isin(high.event_id)]
    baselines = [m for m in high_metrics.method.unique() if m.startswith("baseline:")]
    if not baselines or not {"sparse_invariant", "nonlinear_invariant"}.issubset(set(high_metrics.method)):
        return "CONDITIONAL", ["Complete baseline, sparse, and nonlinear held-out results are not all available."]
    model_pass = {}
    ci_pass = False
    for model in ("sparse_invariant", "nonlinear_invariant"):
        beats = []
        for baseline in baselines:
            au = event_bootstrap_difference(high_metrics, model, baseline, "auprc", cfg.bootstrap_iterations, cfg.random_seed)
            loc = event_bootstrap_difference(high_metrics, model, baseline, "localization_error_seconds", cfg.bootstrap_iterations, cfg.random_seed, False)
            hit = event_bootstrap_difference(high_metrics, model, baseline, "within_0p30", cfg.bootstrap_iterations, cfg.random_seed)
            rel_loc = loc["estimate"] / max(high_metrics[high_metrics.method==baseline].localization_error_seconds.mean(), 1e-30)
            passed = au["estimate"] >= .10 or rel_loc >= .30 or hit["estimate"] >= .20
            beats.append(passed)
            ci_pass |= (passed and (au["ci_low"] > 0 or loc["ci_low"] > 0 or hit["ci_low"] > 0))
        model_pass[model] = all(beats)
    rotation_pass = rotation is not None and not rotation.empty and rotation.maximum_relative_discrepancy.max() < 1e-8
    noise_pass = noise is not None and not noise.empty and bool(noise.loc[noise.noise_fraction == .02, "improvement_survives"].all())
    if all(model_pass.values()) and ci_pass and rotation_pass and noise_pass:
        return "GO", ["All predefined quantitative, uncertainty, noise, and rotation conditions passed."]
    reasons.extend([f"Sparse/nonlinear beat every baseline: {model_pass}.", f"A qualifying higher-guide bootstrap CI excludes zero: {ci_pass}.", f"Rotation test passed: {rotation_pass}.", f"Improvement survived 2% noise: {noise_pass}."])
    return "CONDITIONAL", reasons


def generate_report(root: Path, cfg: PilotConfig, events: pd.DataFrame, metrics: pd.DataFrame,
                    noise: pd.DataFrame | None = None, rotation: pd.DataFrame | None = None) -> str:
    decision, reasons = decide(events, metrics, cfg, noise, rotation)
    usable = int(events.get("success", pd.Series(False,index=events.index)).fillna(False).sum())
    anchors = events[events.get("literature_label", pd.Series("",index=events.index)).astype(str).str.len()>0]
    anchor_text = "\n".join(f"- {r.event_id}: proxy={getattr(r,'guide_ratio_proxy',np.nan):.4g}, all-event rank={int(r.guide_rank_all_desc) if pd.notna(r.guide_rank_all_desc) else 'NA'}/{len(events)}, reliable rank={int(r.guide_rank_reliable_desc) if pd.notna(r.guide_rank_reliable_desc) else 'NA'}/{int(events.reliable.fillna(False).sum())}, label={r.literature_label}" for _,r in anchors.iterrows()) or "- No anchor had assessable synchronized data."
    def summarize(frame: pd.DataFrame) -> pd.DataFrame:
        return frame.groupby("method").agg(auprc_median=("auprc","median"),
                                            localization_median_seconds=("localization_error_seconds","median"),
                                            within_0p30_fraction=("within_0p30","mean"))
    metric_summary = _text_table(summarize(metrics)) if not metrics.empty else "No held-out metrics were available."
    grouped = metrics.merge(events[["event_id","guide_group"]],on="event_id",how="left") if not metrics.empty else metrics
    guide_summary = _text_table(grouped.groupby(["guide_group","method"]).agg(auprc_median=("auprc","median"),localization_median_seconds=("localization_error_seconds","median"),within_0p30_fraction=("within_0p30","mean"))) if not grouped.empty else "No guide-stratified metrics were available."
    bootstrap_path=root/"results/tables/higher_guide_bootstrap_comparisons.csv"
    bootstrap=pd.read_csv(bootstrap_path) if bootstrap_path.exists() else pd.DataFrame()
    uncertainty_summary=_text_table(bootstrap,index=False) if not bootstrap.empty else "No event-bootstrap comparison table was available."
    noise_summary=(_text_table(noise.groupby(["noise_fraction","method"]).auprc.mean().unstack(0)) if noise is not None and not noise.empty else "Noise results unavailable.")
    timing_path=root/"results/tables/timestamp_uncertainty.csv"; timing=pd.read_csv(timing_path) if timing_path.exists() else pd.DataFrame()
    timing_summary=(_text_table(timing.groupby(["center_shift_seconds","method"]).auprc.median().unstack()) if not timing.empty else "Timestamp results unavailable.")
    reference_path=root/"results/tables/leave_reference_group_out.csv"; reference=pd.read_csv(reference_path) if reference_path.exists() else pd.DataFrame()
    reference_summary=(_text_table(reference.groupby("method").auprc.median()) if not reference.empty else "Reference-group result unavailable.")
    ablation_path=root/"results/tables/feature_ablations.csv"; ablation=pd.read_csv(ablation_path) if ablation_path.exists() else pd.DataFrame()
    ablation_summary=(_text_table(ablation.groupby(["ablation","method"]).auprc.median().unstack()) if not ablation.empty else "Ablation results unavailable.")
    permutation_path=root/"results/tables/permutation_tests.csv"; permutation=pd.read_csv(permutation_path) if permutation_path.exists() else pd.DataFrame()
    permutation_summary=(_text_table(permutation,index=False) if not permutation.empty else "Permutation results unavailable.")
    anchor_metrics=grouped[grouped.event_id.isin(anchors.event_id)] if not grouped.empty else grouped
    anchor_summary=(_text_table(anchor_metrics[["event_id","method","auprc","localization_error_seconds","within_0p30"]],index=False) if not anchor_metrics.empty else "Anchor held-out metrics unavailable.")
    worst=metrics[metrics.method=="sparse_invariant"].nsmallest(3,"auprc") if not metrics.empty else pd.DataFrame()
    worst_summary=(_text_table(worst[["event_id","auprc","localization_error_seconds","within_0p30"]],index=False) if not worst.empty else "Failure-case metrics unavailable.")
    next_step = ("Acquire/repair enough public burst products to reach 12 usable events, then rerun the unchanged protocol." if usable < cfg.minimum_events_required else "Estimate LMN geometry with multi-spacecraft timing/curlometer checks and repeat on a larger preregistered catalog before any PIC or symbolic-discovery investment.")
    text = f"""# ReconnectID Pilot summary

## 1. Research question

Does a compact set of coordinate-rotation-invariant plasma quantities localize already-published MMS electron diffusion region (EDR) centers more reliably than individual established diagnostics, especially at higher approximate guide field? This is a feasibility test, not a discovery claim.

## 2. Data and event selection

The source catalog is Zenodo record 8319481 (`EDR_list_MMS.txt`). Selection uses required anchors plus seeded farthest-point stratification across time, spacecraft, and reference identity. {usable} events passed the complete acquisition, synchronization, and ≥{cfg.minimum_valid_fraction:.0%} validity requirement. Failures remain in the manifests.

## 3. Diagnostic definitions

The analysis uses electron-frame field `E'=E+v_e×B`, approximate moment current `J=e n_e(v_i-v_e)`, `D_e=J·E'`, parallel/perpendicular projections, pressure invariants, and Swisdak Q. The moment current is not a four-spacecraft curlometer current.

## 4. Unit conversions

Magnetic field nT→T; electric field mV/m→V/m; velocity km/s→m/s; density cm⁻³→m⁻³; pressure nPa→Pa; `e=1.602176634×10⁻¹⁹ C`.

## 5. Guide-field-proxy limitations

The MVA-derived `|B_M|/(0.5|B_L,before−B_L,after|)` is an event-level proxy, not ground truth. Reliability requires magnetic reversal quality and MVA eigenvalue separation. Anchor results:

{anchor_text}

## 6. Validation strategy

Preprocessing and regularization are fitted inside nested event-level cross-validation. No time samples from a held-out event enter training. Confidence intervals resample events, and structured permutations retain within-event time-series structure.

## 7. Results with uncertainty

{metric_summary}

Guide-stratified event medians:

{guide_summary}

Higher-guide event-bootstrap model-minus-baseline comparisons (95% percentile intervals; localization signs are oriented so positive favors the model):

{uncertainty_summary}

Held-out literature-anchor results:

{anchor_summary}

## 8. Robustness results

Rotation required maximum relative discrepancy <1e-8; observed maximum was {rotation.maximum_relative_discrepancy.max():.4g} if the rotation table was available.

Mean event AUPRC over input-noise trials:

{noise_summary}

Median event AUPRC under catalog-time shifts:

{timing_summary}

Median leave-reference-group-out AUPRC:

{reference_summary}

Feature-ablation median event AUPRC:

{ablation_summary}

Event-center permutation results:

{permutation_summary}

## 9. Failure cases

The three worst events are selected mechanically by held-out sparse-model AUPRC:

{worst_summary}

Data and analysis failures are preserved in `data/event_metadata/download_manifest.csv` and `data/processed/events.parquet`.

## 10. Decision: {decision}

""" + "\n".join(f"- {reason}" for reason in reasons) + f"""

## 11. What this pilot does not prove

It does not discover an EDR, establish causality, validate a physical law, prove that the proxy is the true guide field, or establish transfer to simulations or other missions. Statistical discrimination, temporal localization, coordinate invariance, and physical interpretation are distinct claims.

## 12. Exact recommended next step

{next_step}
"""
    (root/"results/pilot_summary.md").write_text(text)
    (root/"results/GO_NO_GO.md").write_text(f"# {decision}\n\n"+"\n".join(f"- {r}" for r in reasons)+f"\n\nNext experiment: {next_step}\n")
    return decision
