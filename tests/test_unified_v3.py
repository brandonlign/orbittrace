from __future__ import annotations

import unittest

import numpy as np

from pipeline.unified_v3.calibration import (
    benjamini_yekutieli_qvalues,
    calibrate_candidate,
    recurrence_statistic,
)
from pipeline.unified_v3.config import V3Config
from pipeline.unified_v3.method import generate_multiscale_candidates


class UnifiedV3Tests(unittest.TestCase):
    def test_balanced_recurrence_outranks_year_concentration(self) -> None:
        exposure = [100, 100]
        balanced = calibrate_candidate(
            {"family_id": "balanced", "annual_counts": [10, 10], "member_count": 20},
            exposure,
            permutations=999,
            seed=1,
        )
        concentrated = calibrate_candidate(
            {"family_id": "concentrated", "annual_counts": [19, 1], "member_count": 20},
            exposure,
            permutations=999,
            seed=1,
        )
        self.assertGreater(recurrence_statistic([10, 10], exposure), recurrence_statistic([19, 1], exposure))
        self.assertLess(balanced["calibrated_p_value"], concentrated["calibrated_p_value"])

    def test_by_qvalues_are_valid_and_monotone_in_ranked_order(self) -> None:
        p_values = np.asarray([0.01, 0.20, 0.03, 0.60])
        q_values = benjamini_yekutieli_qvalues(p_values)
        self.assertTrue(np.all((q_values >= p_values) & (q_values <= 1.0)))
        order = np.argsort(p_values, kind="mergesort")
        self.assertTrue(np.all(np.diff(q_values[order]) >= 0.0))

    def test_candidate_generation_is_target_label_free_and_deterministic(self) -> None:
        rng = np.random.default_rng(37)
        matrix_parts = []
        years = []
        solar = []
        for year in (2025, 2026):
            matrix_parts.append(rng.normal(0.0, 0.03, size=(12, 6)))
            matrix_parts.append(rng.normal(4.0, 0.05, size=(12, 6)))
            years.extend([year] * 24)
            solar.extend(rng.normal(25.0, 0.2, size=24))
        matrix = np.vstack(matrix_parts)
        year_array = np.asarray(years, dtype=np.int64)
        event_ids = np.asarray([f"event-{index}" for index in range(len(matrix))])
        config = V3Config(
            min_cluster_size=4,
            min_samples=2,
            hierarchy_window_width_deg=360.0,
            hierarchy_window_stride_deg=360.0,
            hierarchy_max_candidate_members=100,
            global_anchor_count=2,
            calibration_permutations=999,
            halo_min_training_members=4,
        )
        first, diagnostics = generate_multiscale_candidates(
            matrix, year_array, event_ids, np.asarray(solar), config
        )
        second, _ = generate_multiscale_candidates(
            matrix, year_array, event_ids, np.asarray(solar), config
        )
        self.assertTrue(first)
        self.assertTrue(diagnostics["refinement_recurrent_eom_uses_year_labels"])
        self.assertFalse(diagnostics["refinement_leaf_memberships_use_year_labels"])
        self.assertTrue(diagnostics["global_anchor_selection_uses_year_labels_for_recurrence"])
        self.assertTrue(all(item["membership_mode"] == "hierarchy_core" for item in first[:2]))
        self.assertTrue(all("label" not in candidate for candidate in first))
        self.assertEqual(
            [(item["family_id"], item.get("calibrated_p_value")) for item in first],
            [(item["family_id"], item.get("calibrated_p_value")) for item in second],
        )


if __name__ == "__main__":
    unittest.main()
