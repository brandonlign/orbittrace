"""Deterministic publication-style pilot figures, saved as PNG and PDF."""
from __future__ import annotations

from pathlib import Path
from typing import Callable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _save(fig: plt.Figure, directory: Path, name: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "pdf"):
        fig.savefig(directory / f"{name}.{suffix}", dpi=300 if suffix == "png" else None, bbox_inches="tight")
    plt.close(fig)


def _empty(title: str, message: str = "Not available: required upstream data did not pass validation") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 4)); ax.axis("off"); ax.set_title(title); ax.text(.5, .5, message, ha="center", va="center", wrap=True)
    return fig


def generate_figures(root: Path, events: pd.DataFrame, metrics: pd.DataFrame | None = None,
                     predictions: pd.DataFrame | None = None, coefficients: pd.DataFrame | None = None,
                     rotation: pd.DataFrame | None = None, noise: pd.DataFrame | None = None) -> None:
    out = root / "results/figures"; metrics = metrics if metrics is not None else pd.DataFrame()
    # 1. Availability (all catalog-selected events, including failures).
    fig, ax = plt.subplots(figsize=(9, 3)); total = len(events); usable = int(events.get("success", pd.Series(False, index=events.index)).fillna(False).sum()); ax.axis("off")
    boxes=[(.08,"Catalog-selected",total,"#4c78a8"),(.40,"All products resolved",total,"#76b7b2"),(.72,"Quality-pass dataset",usable,"#59a14f")]
    for x,label,value,color in boxes:
        ax.text(x,.58,f"{label}\n{value} events",ha="center",va="center",color="white",fontsize=11,bbox=dict(boxstyle="round,pad=.8",fc=color,ec="none"),transform=ax.transAxes)
    for x0,x1 in ((.17,.31),(.49,.63)): ax.annotate("",xy=(x1,.58),xytext=(x0,.58),xycoords="axes fraction",arrowprops=dict(arrowstyle="->",lw=1.8))
    ax.text(.72,.15,f"Explicit failures: {total-usable}",ha="center",transform=ax.transAxes,color="#e15759"); ax.set_title("Data availability flow")
    _save(fig, out, "01_data_availability_flowchart")
    # 2. Guide distribution.
    if "guide_ratio_proxy" in events and events.guide_ratio_proxy.notna().any():
        fig, ax = plt.subplots(figsize=(8, 4)); valid = events.guide_ratio_proxy.dropna(); ax.hist(valid, bins=min(10, len(valid)), color="#4c78a8", alpha=.7)
        for _, row in events[events.get("literature_label", "").astype(str).str.len() > 0].iterrows():
            if pd.notna(row.guide_ratio_proxy): ax.axvline(row.guide_ratio_proxy, ls="--", label=row.literature_label)
        ax.set(xlabel="Approximate guide-ratio proxy", ylabel="Events", title="Guide-field proxy (not ground truth)"); ax.legend(fontsize=8)
    else: fig = _empty("Guide-field proxy distribution")
    _save(fig, out, "02_guide_proxy_distribution")
    # 3. Required examples selected by metadata rule, never visual appearance.
    sample_path=root/"data/processed/samples.parquet"
    samples=pd.read_parquet(sample_path) if sample_path.exists() else pd.DataFrame()
    anchors=events[events.literature_label.astype(str).str.contains("guide-field anchor")]
    lower=events[events.get("guide_group","")=="lower"]
    if not samples.empty and len(anchors)==2 and not lower.empty:
        lower_median=lower.guide_ratio_proxy.median(); lower_pick=lower.iloc[(lower.guide_ratio_proxy-lower_median).abs().argmin()]
        ordered=[lower_pick, anchors[anchors.literature_label.str.startswith("intermediate")].iloc[0], anchors[anchors.literature_label.str.startswith("large")].iloc[0]]
        fig,axes=plt.subplots(3,1,figsize=(9,8),sharex=True)
        for ax,row in zip(axes,ordered):
            g=samples[samples.event_id==row.event_id]
            ax.plot(g.delta_t,g.Q,label="Q")
            ax.plot(g.delta_t,g.D_e_normalized_abs,label="|normalized Dₑ|")
            ax.plot(g.delta_t,g.E_prime_normalized,label="normalized |E′|")
            ax.axvspan(-.15,.15,color="tab:red",alpha=.12); ax.axvspan(-.60,.60,color="tab:orange",alpha=.06)
            ax.set_title(f"{row.event_id}: {row.literature_label or 'lower-guide event closest to group median'}"); ax.set_ylabel("Dimensionless value"); ax.legend(fontsize=7,ncol=3)
        axes[-1].set_xlabel("Time from published EDR center (s)")
    else: fig = _empty("Rule-selected event time series", "Required synchronized event examples unavailable")
    _save(fig, out, "03_example_time_series")
    # 4-6 evaluation figures.
    if not metrics.empty:
        pivot = metrics.pivot(index="event_id", columns="method", values="auprc")
        best_baseline = pivot[[c for c in pivot if c.startswith("baseline:")]].max(axis=1)
        fig, ax = plt.subplots(figsize=(5, 5)); ax.scatter(best_baseline, pivot.get("sparse_invariant"), alpha=.8); lim=[0,1]; ax.plot(lim,lim,"k--",lw=1); ax.set(xlabel="Best individual baseline AUPRC", ylabel="Sparse invariant AUPRC", title="Held-out event performance")
        _save(fig, out, "04_baseline_vs_composite_auprc")
        fig, ax = plt.subplots(figsize=(9, 4)); order=metrics.groupby("method").localization_error_seconds.median().sort_values(); ax.barh(order.index, order.values); ax.set(xlabel="Median |peak time − catalog time| (s)", title="Temporal localization error")
        _save(fig, out, "05_localization_error_by_method")
        merged=metrics.merge(events[["event_id","guide_ratio_proxy"]],on="event_id",how="left"); fig,ax=plt.subplots(figsize=(7,4))
        for method,g in merged.groupby("method"): ax.scatter(g.guide_ratio_proxy,g.auprc,label=method,s=20)
        ax.set(xlabel="Guide-ratio proxy",ylabel="Event AUPRC",title="Performance versus approximate guide field"); ax.legend(fontsize=6,ncol=2)
        _save(fig,out,"06_performance_vs_guide_proxy")
    else:
        for name,title in (("04_baseline_vs_composite_auprc","Baseline versus composite AUPRC"),("05_localization_error_by_method","Temporal localization error"),("06_performance_vs_guide_proxy","Performance versus guide proxy")): _save(_empty(title),out,name)
    # 7 rotation.
    if rotation is not None and not rotation.empty:
        fig,ax=plt.subplots(figsize=(9,4)); values=rotation.groupby("feature").maximum_relative_discrepancy.max().sort_values(); ax.barh(values.index,values.values); ax.axvline(1e-8,color="red",ls="--",label="required maximum"); ax.set_xscale("log"); ax.set(xlabel="Maximum relative discrepancy",title="Numerical coordinate-rotation invariance"); ax.legend()
    else: fig=_empty("Numerical coordinate-rotation invariance")
    _save(fig,out,"07_rotation_invariance_error")
    # 8 noise.
    if noise is not None and not noise.empty:
        fig,ax=plt.subplots(figsize=(7,4));
        summary=noise.groupby(["method","noise_fraction"]).auprc.agg(["mean","std"]).reset_index()
        shown={"baseline:J_magnitude","sparse_invariant","nonlinear_invariant"}; summary=summary[summary.method.isin(shown)]
        for method,g in summary.groupby("method"):
            ax.plot(g.noise_fraction,g["mean"],marker="o",label=method)
            ax.fill_between(g.noise_fraction,g["mean"]-g["std"],g["mean"]+g["std"],alpha=.10)
        ax.set(xlabel="Relative Gaussian noise",ylabel="Mean event AUPRC",title="Noise robustness"); ax.legend()
    else: fig=_empty("Noise robustness")
    _save(fig,out,"08_noise_robustness")
    # 9 coefficients.
    if coefficients is not None and not coefficients.empty:
        fig,ax=plt.subplots(figsize=(9,5)); top=coefficients.groupby("feature").coefficient.apply(lambda x: np.median(np.abs(x))).nlargest(15).index
        data=[coefficients.loc[coefficients.feature==f,"coefficient"] for f in top]
        try: ax.boxplot(data,tick_labels=top,vert=False)
        except TypeError: ax.boxplot(data,labels=top,vert=False)  # matplotlib <3.9
        ax.axvline(0,color="k",lw=.5); ax.set(title="L1 coefficient stability across held-out folds",xlabel="Scaled coefficient")
    else: fig=_empty("L1 coefficient stability")
    _save(fig,out,"09_l1_coefficient_stability")
    # 10 calibration.
    if predictions is not None and not predictions.empty:
        fig,ax=plt.subplots(figsize=(5,5));
        for method in ("sparse_invariant","nonlinear_invariant"):
            g=predictions[(predictions.method==method)&(~predictions.ambiguous.astype(bool))]; bins=pd.cut(g.score,np.linspace(0,1,11),include_lowest=True); cal=g.groupby(bins,observed=False).agg(pred=("score","mean"),obs=("target","mean")).dropna(); ax.plot(cal.pred,cal.obs,marker="o",label=method)
        ax.plot([0,1],[0,1],"k--"); ax.set(xlabel="Predicted probability",ylabel="Observed fraction",title="Out-of-event calibration"); ax.legend()
    else: fig=_empty("Out-of-event calibration")
    _save(fig,out,"10_calibration_curve")
    # 11 heatmap.
    if not metrics.empty:
        table=metrics.pivot(index="event_id",columns="method",values="auprc"); fig,ax=plt.subplots(figsize=(max(8,.45*len(table.columns)),max(5,.3*len(table)))); image=ax.imshow(table,cmap="viridis",aspect="auto",vmin=0,vmax=1); ax.set_xticks(range(len(table.columns)),table.columns,rotation=70,ha="right",fontsize=7); ax.set_yticks(range(len(table.index)),table.index,fontsize=7); fig.colorbar(image,ax=ax,label="AUPRC"); ax.set_title("Per-event held-out results")
    else: fig=_empty("Per-event results heatmap")
    _save(fig,out,"11_per_event_results_heatmap")
    # 12 exactly the three worst composite held-outs when available.
    if predictions is not None and not predictions.empty and not metrics.empty:
        worst=metrics[metrics.method=="sparse_invariant"].nsmallest(3,"auprc").event_id; fig,axes=plt.subplots(len(worst),1,figsize=(9,2.6*max(len(worst),1)),squeeze=False)
        for ax,event in zip(axes[:,0],worst):
            g=predictions[(predictions.event_id==event)&(predictions.method=="sparse_invariant")]; ax.plot(g.delta_t,g.score); ax.axvspan(-.15,.15,color="tab:red",alpha=.15); ax.set_title(f"{event} (rule: three lowest held-out AUPRC)"); ax.set_ylabel("Score")
        axes[-1,0].set_xlabel("Time from published center (s)")
    else: fig=_empty("Three worst held-out events")
    _save(fig,out,"12_failure_cases")
