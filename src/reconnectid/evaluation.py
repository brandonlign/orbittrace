"""Per-event localization metrics, event bootstrap intervals, and structured permutations."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score


def expected_calibration_error(y: np.ndarray, p: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0, 1, bins + 1)
    result = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        use = (p >= lo) & ((p < hi) if hi < 1 else (p <= hi))
        if use.any():
            result += use.mean() * abs(float(y[use].mean()) - float(p[use].mean()))
    return float(result)


def evaluate_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    """Calculate each metric separately for every held-out event and method."""
    rows = []
    for (event_id, method), group in predictions.groupby(["event_id", "method"], sort=True):
        group = group.sort_values("delta_t")
        fit = ~group.ambiguous.astype(bool) & np.isfinite(group.score)
        y, score = group.loc[fit, "target"].to_numpy(int), group.loc[fit, "score"].to_numpy(float)
        if len(np.unique(y)) < 2:
            auprc = roc = np.nan
        else:
            auprc, roc = average_precision_score(y, score), roc_auc_score(y, score)
        finite = np.isfinite(group.score)
        best_dt = float(group.loc[finite].iloc[np.nanargmax(group.loc[finite, "score"].to_numpy())].delta_t) if finite.any() else np.nan
        n_top = max(1, int(np.ceil(fit.sum() * 0.01)))
        top = group.loc[fit].nlargest(n_top, "score")
        positives = max(int(group.loc[fit, "target"].sum()), 1)
        probability_like = method in {"sparse_invariant", "nonlinear_invariant"}
        outside = finite & (group.delta_t.abs() > 0.60)
        rows.append({
            "event_id": event_id, "method": method, "auprc": auprc, "roc_auc": roc,
            "localization_error_seconds": abs(best_dt), "within_0p15": abs(best_dt) <= .15,
            "within_0p30": abs(best_dt) <= .30, "within_0p60": abs(best_dt) <= .60,
            "top_1pct_recall": float(top.target.sum() / positives),
            "false_positive_burden": float(group.loc[outside, "score"].mean()) if probability_like else np.nan,
            "calibration_error": expected_calibration_error(y, score) if probability_like and len(y) else np.nan,
        })
    return pd.DataFrame(rows)


def assign_guide_groups(events: pd.DataFrame, low_q: float, high_q: float) -> pd.DataFrame:
    result = events.copy()
    result["guide_group"] = "unreliable"
    reliable = result.success.fillna(False) & result.reliable.fillna(False) & result.guide_ratio_proxy.notna()
    if reliable.any():
        low = result.loc[reliable, "guide_ratio_proxy"].quantile(low_q)
        high = result.loc[reliable, "guide_ratio_proxy"].quantile(high_q)
        result.loc[reliable, "guide_group"] = "middle"
        result.loc[reliable & (result.guide_ratio_proxy <= low), "guide_group"] = "lower"
        result.loc[reliable & (result.guide_ratio_proxy >= high), "guide_group"] = "higher"
        result["guide_low_threshold"] = low; result["guide_high_threshold"] = high
        result["guide_rank_all_desc"] = result["guide_ratio_proxy"].rank(method="min",ascending=False)
        result.loc[reliable,"guide_rank_reliable_desc"] = result.loc[reliable,"guide_ratio_proxy"].rank(method="min",ascending=False)
    return result


def event_bootstrap_difference(metrics: pd.DataFrame, candidate: str, baseline: str, metric: str,
                               iterations: int, seed: int, higher_is_better: bool = True) -> dict[str, float]:
    wide = metrics.pivot(index="event_id", columns="method", values=metric).dropna(subset=[candidate, baseline])
    difference = wide[candidate].astype(float) - wide[baseline].astype(float)
    if not higher_is_better:
        difference = -difference
    if difference.empty:
        return {"estimate": np.nan, "ci_low": np.nan, "ci_high": np.nan, "n_events": 0}
    rng = np.random.default_rng(seed)
    values = difference.to_numpy()
    boot = np.array([np.mean(rng.choice(values, len(values), replace=True)) for _ in range(iterations)])
    return {"estimate": float(values.mean()), "ci_low": float(np.quantile(boot, .025)),
            "ci_high": float(np.quantile(boot, .975)), "n_events": len(values)}


def event_center_permutation(predictions: pd.DataFrame, iterations: int, seed: int, half_window: float = 6.0) -> pd.DataFrame:
    """Shift centers within each event, preserving each predicted time series."""
    rng = np.random.default_rng(seed)
    observed = evaluate_predictions(predictions).groupby("method").auprc.mean()
    null: dict[str, list[float]] = {m: [] for m in observed.index}
    grouped = [(event, method, g.delta_t.to_numpy(float), g.score.to_numpy(float))
               for (event, method), g in predictions.groupby(["event_id", "method"], sort=False)]
    events = predictions.event_id.unique()
    for _ in range(iterations):
        shifts = dict(zip(events, rng.uniform(-half_window * .75, half_window * .75, len(events))))
        iteration_scores: dict[str, list[float]] = {m: [] for m in observed.index}
        for event, method, original_dt, score in grouped:
            dt = original_dt - shifts[event]
            use = ((np.abs(dt) <= .15) | (np.abs(dt) > .60)) & np.isfinite(score)
            y = (np.abs(dt[use]) <= .15).astype(int)
            if len(np.unique(y)) == 2:
                iteration_scores[method].append(average_precision_score(y, score[use]))
        for method, values in iteration_scores.items():
            null[method].append(float(np.mean(values)) if values else np.nan)
    return pd.DataFrame({"method": list(observed.index), "observed_mean_auprc": observed.values,
                         "permutation_p": [(1 + np.sum(np.asarray(null[m]) >= observed[m])) / (iterations + 1) for m in observed.index]})
