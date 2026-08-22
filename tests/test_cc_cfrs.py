from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from pipeline.cc_cfrs_v1 import (
    SourceSpec,
    CCFConfig,
    CCFScanner,
    CanonicalCell,
    PhasePermutationNull,
    Stage0Config,
    Stage0PipelineSummary,
    clopper_pearson_upper,
    combine_recurrence_p,
    derive_seed,
    evaluate_stage0_gate,
    normalize_frame,
    run_stage0,
    adapt_frame,
    adapt_raw_frame,
    project_annual_catalogue,
    ranked_catalogue,
    run_frozen_temporal_holdout,
)


def make_frame() -> pd.DataFrame:
    rows = []
    event_number = 0
    rng = np.random.default_rng(7)
    for year, center in ((2021, 35.0), (2022, 35.4), (2023, 35.8)):
        for index in range(18):
            rows.append(
                {
                    "event_id": f"stream-{year}-{index}",
                    "year": year,
                    "sol_lon_deg": center + rng.normal(0, 0.5),
                    "radiant_lon_deg": 120.0 + 0.7 * (center - 35.0) + rng.normal(0, 0.25),
                    "radiant_lat_deg": -14.0 + rng.normal(0, 0.25),
                    "speed_km_s": 37.5 + rng.normal(0, 0.15),
                }
            )
            event_number += 1
        for index in range(20):
            rows.append(
                {
                    "event_id": f"noise-{year}-{index}",
                    "year": year,
                    "sol_lon_deg": 100.0 + rng.uniform(0, 200),
                    "radiant_lon_deg": rng.uniform(0, 360),
                    "radiant_lat_deg": rng.uniform(-60, 60),
                    "speed_km_s": rng.uniform(20, 65),
                }
            )
    return pd.DataFrame(rows)


class CCFRSTest(unittest.TestCase):
    def test_canonical_cell_identity_is_stable_and_orderable(self) -> None:
        cell = CanonicalCell(1, 4, 5, 6, 7, 8, 9, 10)
        self.assertEqual(cell.as_tuple(), (1, 4, 5, 6, 7, 8, 9, 10))
        self.assertEqual(cell.hash_hex(), CanonicalCell(*cell.as_tuple()).hash_hex())
        self.assertNotEqual(cell.hash_hex(), CanonicalCell(1, 4, 5, 6, 7, 8, 9, 11).hash_hex())

    def test_partial_conjunction_requires_same_cell_and_three_years(self) -> None:
        self.assertEqual(combine_recurrence_p([0.01, 0.02, 1.0]), 0.04)
        self.assertEqual(combine_recurrence_p({2021: 0.2, 2022: 0.3, 2023: 0.4}), 0.6)
        with self.assertRaises(ValueError):
            combine_recurrence_p([0.01, 0.02])

    def test_normalization_drops_invalid_rows_and_orders_year_then_id(self) -> None:
        frame = make_frame()
        frame.loc[len(frame)] = {
            "event_id": "invalid",
            "year": 2023,
            "sol_lon_deg": 35,
            "radiant_lon_deg": 10,
            "radiant_lat_deg": 100,
            "speed_km_s": 30,
        }
        normalized = normalize_frame(frame)
        self.assertNotIn("invalid", set(normalized["event_id"]))
        self.assertEqual(list(normalized["year"].unique()), [2021, 2022, 2023])
        self.assertTrue(normalized["event_id"].is_unique)

    def test_null_preserves_rows_years_and_solar_multiset(self) -> None:
        frame = make_frame()
        frame = frame.loc[~frame["sol_lon_deg"].between(20, 55)].reset_index(drop=True)
        config = CCFConfig(heldout_randomizations=7)
        null = PhasePermutationNull(frame, config)
        normalized = normalize_frame(frame)
        first = null(0)
        second = null(0)
        self.assertTrue(first["event_id"].equals(normalized["event_id"]))
        self.assertTrue(first["year"].equals(normalized["year"]))
        self.assertTrue(np.allclose(np.sort(first["sol_lon_deg"]), np.sort(normalized["sol_lon_deg"])))
        self.assertTrue(first.equals(second))
        self.assertNotEqual(derive_seed("cc-cfrs-v1", 0), derive_seed("cc-cfrs-v1", 1))
        self.assertEqual(null.endpoint_hash, PhasePermutationNull(frame, config).endpoint_hash)
        shifted = normalized.copy()
        shifted.loc[0, "sol_lon_deg"] += 0.001
        shifted_null = PhasePermutationNull(shifted, config)
        self.assertNotEqual(null.endpoint_hash, shifted_null.endpoint_hash)
        with self.assertRaises(ValueError):
            PhasePermutationNull(make_frame(), config, require_target_interval_excluded=True)

    def test_discovery_adapter_retains_target_domain_by_default(self) -> None:
        raw = pd.DataFrame(
            {
                "IID": ["late-april"],
                "Yr": [2024],
                "LS": [35.0],
                "lamgeo_deg": [120.0],
                "betgeo_deg": [-14.0],
                "Vg": [37.5],
            }
        )
        result = adapt_raw_frame(raw, SourceSpec("GMN"))
        self.assertEqual(len(result.frame), 1)
        self.assertEqual(float(result.frame.iloc[0]["sol_lon_deg"]), 35.0)

        raw = raw.rename(columns={"IID": "CurNum"})
        result = adapt_raw_frame(raw, SourceSpec("GMN"))
        self.assertEqual(len(result.frame), 1)

    def test_scanner_requires_three_years_and_runs_on_label_free_frame(self) -> None:
        frame = make_frame()
        frame = frame.loc[~frame["sol_lon_deg"].between(20, 55)].reset_index(drop=True)
        config = CCFConfig(scales=(1.0,), minimum_training_members=4, heldout_randomizations=5)
        scanner = CCFScanner(config)
        null = PhasePermutationNull(frame, config)
        result = scanner.scan(frame, null, randomizations=5)
        self.assertGreaterEqual(len(result.candidates), len(result.selected))
        self.assertTrue(all(0.0 <= candidate.recurrence_p <= 1.0 for candidate in result.candidates))
        two_years = frame.loc[frame["year"] != 2023].copy()
        with self.assertRaises(ValueError):
            scanner.scan(two_years, null, randomizations=5)

    def test_stage0_gate_uses_exact_panel_denominators(self) -> None:
        contract = Stage0Config()
        rejections = [False] * contract.validation_panels
        strata = [index // contract.panels_per_stratum for index in range(contract.validation_panels)]
        result = evaluate_stage0_gate(rejections, strata, contract)
        self.assertTrue(result.passed)
        self.assertEqual(result.overall_panels, 2000)
        self.assertEqual(result.stratum_panels, (500, 500, 500, 500))
        self.assertLessEqual(clopper_pearson_upper(0, 2000), 0.003)

    def test_stage0_runner_uses_fixed_calibration_and_validation_counts(self) -> None:
        calls = {"calibration": 0, "validation": 0}
        frame = make_frame().loc[lambda value: ~value["sol_lon_deg"].between(20, 55)].reset_index(drop=True)

        def panel_factory(bank: str, index: int):
            calls[bank] += 1
            return frame, index // 500 if bank == "validation" else index % 4

        def pipeline(panel: pd.DataFrame, seed: int) -> Stage0PipelineSummary:
            self.assertGreater(len(panel), 0)
            return Stage0PipelineSummary(max_statistic=0.0, selected_statistics=())

        result = run_stage0(panel_factory, pipeline)
        self.assertTrue(result.gate.passed)
        self.assertEqual(calls, {"calibration": 999, "validation": 2000})
        self.assertEqual(len(result.calibration_maxima), 999)
        self.assertEqual(len(result.validation_rejections), 2000)

    def test_source_adapter_converts_ecliptic_radiant_and_applies_firewall(self) -> None:
        raw = pd.DataFrame(
            {
                "IID": ["a", "b", "c"],
                "Yr": [2021, 2022, 2023],
                "LS": [10.0, 60.0, 100.0],
                "lamgeo_deg": [20.0, 70.0, 130.0],
                "betgeo_deg": [5.0, 6.0, 7.0],
                "Vg": [30.0, 31.0, 32.0],
            }
        )
        result = adapt_frame(raw, SourceSpec("GMN", radiant_lon_mode="ecliptic"))
        self.assertEqual(result.manifest["rows_before_target_exclusion"], 3)
        self.assertEqual(result.manifest["rows_after_target_exclusion"], 3)
        self.assertEqual(list(result.frame["radiant_lon_deg"]), [10.0, 10.0, 30.0])
        self.assertTrue(all(str(value).startswith("GMN:") for value in result.frame["event_id"]))
        self.assertTrue(all(":202" in str(value) for value in result.frame["event_id"]))

    def test_source_adapter_rejects_truth_bearing_columns(self) -> None:
        raw = pd.DataFrame(
            {
                "id": ["a"],
                "year": [2021],
                "sol": [100.0],
                "radiant_lon_deg": [10.0],
                "radiant_lat_deg": [5.0],
                "speed_km_s": [30.0],
                "shower_label": ["hidden"],
            }
        )
        with self.assertRaises(ValueError):
            adapt_frame(raw, SourceSpec("GMN"))

    def test_raw_firewall_drops_source_truth_columns_before_normalization(self) -> None:
        raw = pd.DataFrame(
            {
                "IID": ["a"],
                "Yr": [2012],
                "LS": [100.0],
                "RA": [120.0],
                "DECL": [-10.0],
                "Vg": [35.0],
                "sh": [17],
                "DB": ["source-metadata"],
            }
        )
        result = adapt_raw_frame(raw, SourceSpec("SonotaCo", year=2012))
        self.assertIn("sh", result.manifest["pre_firewall_dropped_columns"])
        self.assertIn("DB", result.manifest["pre_firewall_dropped_columns"])
        self.assertEqual(len(result.frame), 1)

    def test_annual_projection_preserves_global_order_and_capacity(self) -> None:
        frame = make_frame()
        # Keep the synthetic recurring stream outside the preregistered
        # target-exclusion interval while retaining the noise fixture.
        stream = frame.loc[frame["event_id"].str.startswith("stream-")].copy()
        frame.loc[frame["event_id"].str.startswith("stream-"), "sol_lon_deg"] += 80.0
        second_stream = stream.copy()
        second_stream["event_id"] = second_stream["event_id"].str.replace("stream-", "stream2-", regex=False)
        second_stream["sol_lon_deg"] += 180.0
        second_stream["radiant_lon_deg"] += 150.0
        second_stream["radiant_lat_deg"] += 35.0
        second_stream["speed_km_s"] += 12.0
        frame = pd.concat([frame, second_stream], ignore_index=True)
        frame = frame.loc[~frame["sol_lon_deg"].between(20, 55)].reset_index(drop=True)
        config = CCFConfig(scales=(1.0,), minimum_training_members=4, heldout_randomizations=2)
        scanner = CCFScanner(config)
        null = PhasePermutationNull(frame, config)
        result = scanner.scan(frame, null, randomizations=2)
        self.assertGreaterEqual(len(result.selected), 2)
        projection = project_annual_catalogue(frame, ranked_catalogue(result), 2022, 2, config)
        self.assertEqual(projection.capacity, 2)
        self.assertEqual(projection.returned_count, 2)
        self.assertEqual(len(projection.member_ids), 2)
        with self.assertRaises(ValueError):
            project_annual_catalogue(frame, ranked_catalogue(result), 2022, 10000, config)

    def test_frozen_holdout_ranks_once_and_records_underfilled_years(self) -> None:
        frame = make_frame()
        frame.loc[frame["event_id"].str.startswith("stream-"), "sol_lon_deg"] += 80.0
        holdout = frame.loc[frame["year"] == 2023].copy()
        holdout["year"] = 2024
        holdout["event_id"] = holdout["event_id"].str.replace("2023", "2024", regex=False)
        frame = pd.concat([frame, holdout], ignore_index=True)
        frame = frame.loc[~frame["sol_lon_deg"].between(20, 55)].reset_index(drop=True)
        config = CCFConfig(scales=(1.0,), minimum_training_members=4, heldout_randomizations=2)
        run = run_frozen_temporal_holdout(
            frame,
            discovery_years=(2021, 2022, 2023),
            holdout_years=(2024,),
            capacity=2,
            randomizations=2,
            config=config,
        )
        self.assertEqual(run.discovery_years, (2021, 2022, 2023))
        self.assertEqual(run.holdout_years, (2024,))
        self.assertEqual(len(run.projections), 1)
        self.assertEqual(run.projections[0].capacity, 2)
        self.assertLessEqual(run.projections[0].returned_count, 2)
        self.assertEqual(run.capacity_satisfied, run.projections[0].capacity_satisfied)
        self.assertEqual(run.underfilled_years, () if run.capacity_satisfied else (2024,))
        self.assertTrue(run.ranking_fingerprint)
        with self.assertRaises(ValueError):
            run_frozen_temporal_holdout(
                frame,
                discovery_years=(2021, 2022),
                holdout_years=(2024,),
                capacity=1,
                randomizations=2,
                config=config,
            )


if __name__ == "__main__":
    unittest.main()
