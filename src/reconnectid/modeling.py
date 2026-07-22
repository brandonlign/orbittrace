"""Leakage-safe event-level model fitting and leave-one-event-out prediction."""
from __future__ import annotations

from dataclasses import dataclass
import logging
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
import sklearn

from .features import BASELINE_SCORES, INVARIANT_FEATURES

LOGGER = logging.getLogger(__name__)


def _sparse_pipeline(C: float, seed: int) -> Pipeline:
    major_minor = tuple(int(x) for x in sklearn.__version__.split(".")[:2])
    # sklearn 1.8 deprecated ``penalty`` in favor of l1_ratio. Keep the same
    # L1 objective without flooding long nested runs with version warnings.
    l1_kwargs = {"l1_ratio": 1.0} if major_minor >= (1, 8) else {"penalty": "l1"}
    return Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
        ("scale", RobustScaler()),
        ("model", LogisticRegression(solver="liblinear", C=C, max_iter=3000, random_state=seed, **l1_kwargs)),
    ])


def _nonlinear_pipeline(seed: int, l2: float = 1.0) -> Pipeline:
    return Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
        ("model", HistGradientBoostingClassifier(max_iter=150, learning_rate=0.05, max_leaf_nodes=7,
                                                  min_samples_leaf=20, l2_regularization=l2,
                                                  early_stopping=False, random_state=seed)),
    ])


def fitting_rows(frame: pd.DataFrame) -> np.ndarray:
    return frame["valid"].astype(bool).to_numpy() & ~frame["ambiguous"].astype(bool).to_numpy()


def assert_event_disjoint(train: pd.DataFrame, test: pd.DataFrame) -> None:
    overlap = set(train.event_id.unique()) & set(test.event_id.unique())
    if overlap:
        raise AssertionError(f"Event leakage: {sorted(overlap)}")


def _inner_score(train: pd.DataFrame, features: list[str], factory) -> float:
    scores = []
    groups = train.event_id.to_numpy()
    unique = np.unique(groups)
    splitter = GroupKFold(n_splits=min(5, len(unique)))
    for train_idx, test_idx in splitter.split(train, groups=groups):
        inner_train = train.iloc[train_idx]
        inner_test = train.iloc[test_idx]
        a = fitting_rows(inner_train)
        if len(np.unique(inner_train.loc[a, "target"])) < 2:
            continue
        model = factory()
        model.fit(inner_train.loc[a, features], inner_train.loc[a, "target"], model__sample_weight=inner_train.loc[a, "sample_weight"])
        for held in inner_test.event_id.unique():
            event_test = inner_test[inner_test.event_id == held]
            b = fitting_rows(event_test)
            if len(np.unique(event_test.loc[b, "target"])) < 2:
                continue
            score = model.predict_proba(event_test.loc[b, features])[:, 1]
            scores.append(average_precision_score(event_test.loc[b, "target"], score))
    return float(np.mean(scores)) if scores else -np.inf


def choose_sparse_c(train: pd.DataFrame, features: list[str], seed: int, grid=(0.01, 0.03, 0.1, 0.3, 1.0, 3.0)) -> float:
    values = [(float(_inner_score(train, features, lambda c=c: _sparse_pipeline(c, seed))), c) for c in grid]
    return float(max(values, key=lambda x: (x[0], -x[1]))[1])


def choose_nonlinear_l2(train: pd.DataFrame, features: list[str], seed: int, grid=(0.3, 1.0, 3.0, 10.0)) -> float:
    values = [(float(_inner_score(train, features, lambda l2=l2: _nonlinear_pipeline(seed, l2))), l2) for l2 in grid]
    return float(max(values, key=lambda x: (x[0], x[1]))[1])


def _baseline_direction(train: pd.DataFrame, feature: str) -> int:
    use = fitting_rows(train) & np.isfinite(train[feature].to_numpy(float))
    y, s = train.loc[use, "target"], train.loc[use, feature]
    if len(np.unique(y)) < 2:
        return 1
    positive = average_precision_score(y, s, sample_weight=train.loc[use, "sample_weight"])
    negative = average_precision_score(y, -s, sample_weight=train.loc[use, "sample_weight"])
    return 1 if positive >= negative else -1


@dataclass
class LOOResult:
    predictions: pd.DataFrame
    coefficients: pd.DataFrame


def leave_one_event_out(samples: pd.DataFrame, features: list[str] | None = None, seed: int = 2026,
                        include_baselines: bool = True, include_sparse: bool = True,
                        include_nonlinear: bool = True) -> LOOResult:
    """Strict nested leave-one-event-out evaluation with equal event fitting weight."""
    features = list(features or INVARIANT_FEATURES)
    predictions, coefficients = [], []
    events = list(samples.event_id.unique())
    if len(events) < 3:
        raise ValueError("At least three events are required for nested event-level evaluation")
    for held in events:
        train, test = samples[samples.event_id != held].copy(), samples[samples.event_id == held].copy()
        assert_event_disjoint(train, test)
        train_use, test_valid = fitting_rows(train), test["valid"].astype(bool).to_numpy()
        common = test.loc[test_valid, ["event_id", "delta_t", "target", "ambiguous", "soft_target"]].reset_index(drop=True)
        if include_baselines:
            for feature in BASELINE_SCORES:
                direction = _baseline_direction(train, feature)
                out = common.copy()
                out["method"] = f"baseline:{feature}"
                out["score"] = direction * test.loc[test_valid, feature].to_numpy(float)
                out["score_direction"] = direction
                predictions.append(out)
        if include_sparse:
            C = choose_sparse_c(train.loc[train_use | ~train_use], features, seed)
            model = _sparse_pipeline(C, seed)
            model.fit(train.loc[train_use, features], train.loc[train_use, "target"], model__sample_weight=train.loc[train_use, "sample_weight"])
            out = common.copy(); out["method"] = "sparse_invariant"; out["score"] = model.predict_proba(test.loc[test_valid, features])[:, 1]
            out["score_direction"] = 1; predictions.append(out)
            names = model.named_steps["impute"].get_feature_names_out(features)
            coef = model.named_steps["model"].coef_[0]
            coefficients.extend({"held_out_event": held, "feature": n, "coefficient": c, "C": C} for n, c in zip(names, coef))
        if include_nonlinear:
            l2 = choose_nonlinear_l2(train, features, seed)
            model = _nonlinear_pipeline(seed, l2)
            model.fit(train.loc[train_use, features], train.loc[train_use, "target"], model__sample_weight=train.loc[train_use, "sample_weight"])
            out = common.copy(); out["method"] = "nonlinear_invariant"; out["score"] = model.predict_proba(test.loc[test_valid, features])[:, 1]
            out["score_direction"] = 1; predictions.append(out)
    return LOOResult(pd.concat(predictions, ignore_index=True), pd.DataFrame(coefficients))


def grouped_holdout_fixed(samples: pd.DataFrame, features: list[str] | None = None, group_column: str = "event_id",
                          seed: int = 2026, C: float = 0.3, l2: float = 1.0,
                          include_baselines: bool = False, holdout_groups: list[str] | None = None) -> pd.DataFrame:
    """Event-safe grouped holdout with hyperparameters fixed before the robustness fit.

    This is used for robustness/ablation analyses after nested clean-data model
    selection. It never re-selects a hyperparameter from a held-out group.
    """
    features = list(features or INVARIANT_FEATURES)
    predictions = []
    groups = holdout_groups if holdout_groups is not None else list(samples[group_column].dropna().unique())
    for group in groups:
        train, test = samples[samples[group_column] != group], samples[samples[group_column] == group]
        assert_event_disjoint(train, test)
        train_use = fitting_rows(train); test_valid = test.valid.astype(bool).to_numpy()
        common = test.loc[test_valid, ["event_id", "delta_t", "target", "ambiguous", "soft_target"]].reset_index(drop=True)
        if include_baselines:
            for feature in BASELINE_SCORES:
                out=common.copy(); out["method"]=f"baseline:{feature}"; out["score"]=_baseline_direction(train,feature)*test.loc[test_valid,feature].to_numpy(float); out["score_direction"]=1; predictions.append(out)
        sparse=_sparse_pipeline(C,seed); sparse.fit(train.loc[train_use,features],train.loc[train_use,"target"],model__sample_weight=train.loc[train_use,"sample_weight"])
        out=common.copy(); out["method"]="sparse_invariant"; out["score"]=sparse.predict_proba(test.loc[test_valid,features])[:,1]; out["score_direction"]=1; predictions.append(out)
        nonlinear=_nonlinear_pipeline(seed,l2); nonlinear.fit(train.loc[train_use,features],train.loc[train_use,"target"],model__sample_weight=train.loc[train_use,"sample_weight"])
        out=common.copy(); out["method"]="nonlinear_invariant"; out["score"]=nonlinear.predict_proba(test.loc[test_valid,features])[:,1]; out["score_direction"]=1; predictions.append(out)
    return pd.concat(predictions,ignore_index=True)
