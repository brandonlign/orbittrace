from __future__ import annotations

import unittest

import numpy as np

from pipeline.unified_v2 import V2Config, expand_candidate, fit_recurrent_hierarchy
from pipeline.unified_v2.common_evaluator import evaluate_candidate_catalogue
from pipeline.unified_v2.comparators import literature_comparator_registry
from pipeline.unified_v2.d_criterion import (
    edmond_d_criterion_candidates,
    southworth_hawkins_pairs,
)
from pipeline.unified_v2.features import periodic_physical6_from_raw
from pipeline.unified_v2.partitioned_hierarchy import fit_partitioned_recurrent_hierarchy


class UnifiedV2Tests(unittest.TestCase):
    def test_comparator_registry_and_hungarian_evaluator_are_explicit(self) -> None:
        names = {item.name for item in literature_comparator_registry()}
        self.assertIn("sugar_dbscan_uncertainty", names)
        self.assertIn("d_criterion_edmond", names)
        truth = {f"a{index}": "A" for index in range(4)}
        truth.update({f"b{index}": "B" for index in range(4)})
        result = evaluate_candidate_catalogue(
            [{"event_ids": [f"a{index}" for index in range(4)]}, {"event_ids": [f"b{index}" for index in range(4)]}],
            truth,
            2,
        )
        self.assertEqual(result["eligible_showers"], 2)
        self.assertEqual(result["recovered_f1_gt_0_5"], 2)

    def test_periodic_transform_keeps_longitude_seam_continuous(self) -> None:
        raw = np.asarray(
            [
                [179.0, 0.0, 35.0, -179.0],
                [-179.0, 0.0, 35.0, 179.0],
            ],
            dtype=float,
        )
        transformed = periodic_physical6_from_raw(raw)
        self.assertLess(float(np.linalg.norm(transformed[0] - transformed[1])), 1.0)

    def test_southworth_hawkins_adapter_is_symmetric_and_groups_streams(self) -> None:
        orbit = np.asarray([[0.8, 0.5, 12.0, 220.0, 35.0]], dtype=float)
        doubled = np.vstack((orbit, orbit))
        self.assertEqual(float(southworth_hawkins_pairs(doubled, np.asarray([[0, 1]]))[0]), 0.0)
        rows = []
        for family, offset in (("a", 0.0), ("b", 80.0)):
            for index in range(6):
                delta = (index - 2.5) * 0.001
                rows.append(
                    {
                        "id": f"{family}{index}",
                        "e": 0.80 + delta,
                        "q": 0.50 + delta,
                        "inc": 12.0 + delta,
                        "peri": 220.0 + offset + delta,
                        "node": 35.0 + offset + delta,
                        "sol": 35.0 + offset + delta,
                        "ra": 120.0 + offset + delta,
                        "dec": 20.0 + delta,
                        "vg": 32.0 + delta,
                    }
                )
        candidates, diagnostics = edmond_d_criterion_candidates(rows)
        self.assertEqual(diagnostics["truth_accessed"], False)
        self.assertEqual(len(candidates), 2)
        self.assertTrue(all(candidate["member_count"] == 6 for candidate in candidates))

    def test_partitioned_hierarchy_is_label_free_and_deduplicates_windows(self) -> None:
        rng = np.random.default_rng(31)
        matrices = []
        years = []
        solar = []
        for year in (2025, 2026):
            matrices.append(rng.normal(0.0, 0.03, size=(14, 6)))
            matrices.append(rng.normal(4.0, 0.08, size=(20, 6)))
            years.extend([year] * 34)
            solar.extend(rng.normal(22.0, 0.5, size=34))
        matrix = np.vstack(matrices)
        year_array = np.asarray(years, dtype=np.int64)
        event_ids = np.asarray([f"blind-{index}" for index in range(len(matrix))])
        parents, leaves, diagnostics = fit_partitioned_recurrent_hierarchy(
            matrix,
            year_array,
            event_ids,
            np.asarray(solar, dtype=float),
            V2Config(
                min_cluster_size=6,
                min_samples=3,
                hierarchy_window_width_deg=10.0,
                hierarchy_window_stride_deg=5.0,
            ),
        )
        self.assertGreaterEqual(diagnostics["windows_fit"], 1)
        self.assertTrue(parents or leaves)
        self.assertTrue(all("label" not in item for item in parents + leaves))
        self.assertTrue(all("seed_score" in item for item in parents + leaves))

    def test_recurrent_hierarchy_supports_more_than_two_years(self) -> None:
        rng = np.random.default_rng(17)
        rows = []
        years = []
        for year in (2022, 2023, 2024):
            rows.append(rng.normal(0.0, 0.02, size=(18, 6)))
            rows.append(rng.normal(4.0, 0.02, size=(18, 6)))
            years.extend([year] * 36)
        matrix = np.vstack(rows)
        year_array = np.asarray(years, dtype=np.int64)
        event_ids = np.asarray([f"event-{index}" for index in range(len(matrix))])
        parents, leaves, diagnostics = fit_recurrent_hierarchy(
            matrix,
            year_array,
            event_ids,
            V2Config(min_cluster_size=5, min_samples=3),
        )
        self.assertEqual(diagnostics["years"], [2022, 2023, 2024])
        self.assertTrue(parents)
        self.assertTrue(leaves)
        self.assertTrue(all("label" not in item for item in parents + leaves))
        self.assertTrue(all(len(item["annual_counts"]) == 3 for item in parents))

    def test_crossfit_halo_uses_other_years_and_rejects_far_background(self) -> None:
        rng = np.random.default_rng(23)
        matrix = []
        years = []
        members = []
        for year in (2022, 2023, 2024):
            start = len(matrix)
            core = rng.normal(0.0, 0.03, size=(10, 2))
            halo = rng.normal(0.06, 0.03, size=(2, 2))
            unrelated = rng.normal(3.0, 0.05, size=(8, 2))
            matrix.extend(np.vstack((core, halo, unrelated)))
            years.extend([year] * 20)
            members.extend(range(start, start + 10))
        values = np.asarray(matrix, dtype=float)
        year_array = np.asarray(years, dtype=np.int64)
        event_ids = np.asarray([f"event-{index}" for index in range(len(values))])
        candidate = {"family_id": "synthetic", "members": members}
        result = expand_candidate(
            candidate,
            values,
            year_array,
            event_ids,
            V2Config(min_cluster_size=5, min_samples=3, halo_min_training_members=6),
        )
        expanded = set(result["expanded_members"])
        self.assertTrue(set(members).issubset(expanded))
        self.assertGreater(result["halo_added_count"], 0)
        self.assertFalse(any(index in expanded for index in range(12, 20)))
        self.assertTrue(all(not fold.get("skipped", False) for fold in result["crossfit_halo"]["folds"].values()))


if __name__ == "__main__":
    unittest.main()
