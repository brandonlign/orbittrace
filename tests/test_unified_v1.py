from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from pipeline.unified_v1.method import (
    UnifiedConfig,
    best_known_cluster,
    cluster_hierarchy,
    largest_non_target_fraction,
    reveal_full_history_overlap,
)
from pipeline.unified_v1.recurrent_application import (
    geo6,
    periodic_physical6,
    periodic_physical6_from_raw,
    recurrent_candidates,
)


class UnifiedHierarchyTests(unittest.TestCase):
    def test_config_is_single_frozen_hierarchy(self) -> None:
        config = UnifiedConfig()
        self.assertEqual(config.hierarchy_methods, ("eom", "leaf"))
        self.assertEqual(config.feature_scales, (3.5, 3.0, 2.5, 2.5))

    def test_hierarchy_returns_both_parent_and_leaf_levels_without_labels(self) -> None:
        rng = np.random.default_rng(41)
        left = rng.normal(loc=(-5.0, 0.0, 35.0, -1.0), scale=(0.25, 0.25, 0.3, 0.2), size=(30, 4))
        right = rng.normal(loc=(5.0, 0.0, 45.0, 1.0), scale=(0.25, 0.25, 0.3, 0.2), size=(30, 4))
        clusters = cluster_hierarchy(np.vstack([left, right]), UnifiedConfig())
        self.assertTrue({item["method"] for item in clusters} == {"eom", "leaf"})
        self.assertTrue(all("members" in item and "label" not in item for item in clusters))

    def test_known_scoring_uses_labels_only_after_clustering(self) -> None:
        labels = np.asarray(["A"] * 12 + ["B"] * 12 + ["SPORADIC"] * 6)
        clusters = [
            {"method": "eom", "global_cluster": 0, "members": np.arange(12)},
            {"method": "leaf", "global_cluster": 1, "members": np.arange(12, 24)},
        ]
        score = best_known_cluster(labels, clusters, "A")
        self.assertEqual(score["method"], "eom")
        self.assertEqual(score["recall"], 1.0)
        self.assertEqual(largest_non_target_fraction(labels, clusters, "A"), 12 / 30)

    def test_full_history_reveal_uses_discovery_and_validation_members(self) -> None:
        candidate = {
            "month": 4,
            "hierarchy_method": "leaf",
            "member_ids_2025": ["20260102030405_A"],
            "validation": {"2025": {"member_ids": ["20250102030405_B"]}},
        }
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target.csv"
            pd.DataFrame({"Tobs": ["2026-01-02-03:04:05", "2025-01-02-03:04:05"]}).to_csv(target, index=False)
            result = reveal_full_history_overlap([candidate], target, 2026)[0]
        self.assertEqual(result["target_overlap"], 2)
        self.assertEqual(result["target_recall"], 1.0)

    def test_geo6_shape_and_recurrent_candidates_are_label_free(self) -> None:
        frame = pd.DataFrame(
            {
                "sol_lon_deg": [10.0, 20.0],
                "lamgeo_deg": [40.0, 50.0],
                "betgeo_deg": [5.0, -5.0],
                "vgeo_km_s": [30.0, 40.0],
            }
        )
        self.assertEqual(geo6(frame).shape, (2, 6))

        rng = np.random.default_rng(7)
        left_2025 = rng.normal(0.0, 0.01, size=(15, 6))
        left_2026 = rng.normal(0.0, 0.01, size=(15, 6))
        right_2025 = rng.normal(1.0, 0.01, size=(15, 6))
        right_2026 = rng.normal(1.0, 0.01, size=(15, 6))
        matrix = np.vstack([left_2025, left_2026, right_2025, right_2026])
        years = np.asarray([2025] * 15 + [2026] * 15 + [2025] * 15 + [2026] * 15)
        ids = np.asarray([f"event-{index}" for index in range(len(matrix))])
        candidates, diagnostics = recurrent_candidates(matrix, years, ids)
        self.assertTrue(candidates)
        self.assertTrue(diagnostics["recurrent_candidates"] >= 1)
        self.assertTrue(all("label" not in candidate for candidate in candidates))

    def test_periodic_transform_matches_raw_gate_order(self) -> None:
        frame = pd.DataFrame(
            {
                "sol_lon_deg": [359.0, 1.0],
                "lamgeo_deg": [358.0, 2.0],
                "betgeo_deg": [5.0, -5.0],
                "vgeo_km_s": [30.0, 40.0],
            }
        )
        raw = np.column_stack(
            (
                frame["lamgeo_deg"] - frame["sol_lon_deg"],
                frame["betgeo_deg"],
                frame["vgeo_km_s"],
                np.asarray([-1.0, 1.0]),
            )
        )
        direct = periodic_physical6(frame)
        from_gate = periodic_physical6_from_raw(raw)
        direct_distances = np.linalg.norm(direct[:, None, :] - direct[None, :, :], axis=2)
        gate_distances = np.linalg.norm(from_gate[:, None, :] - from_gate[None, :, :], axis=2)
        np.testing.assert_allclose(direct_distances, gate_distances)


if __name__ == "__main__":
    unittest.main()
