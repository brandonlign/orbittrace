from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

import numpy as np
import pandas as pd

from acrf.application import load_panel
from acrf.calibration import recurrence_statistic
from acrf.crossfit_membership import _bh_qvalues
from acrf.features import circular_difference_deg
from acrf.reveal import _certify_target_free
from benchmarks.independent_d_criterion import southworth_hawkins_pairs


class FeatureTests(unittest.TestCase):
    def test_circular_difference_wraps_at_zero(self) -> None:
        result = circular_difference_deg(np.array([359.0, 1.0]), np.array([1.0, 359.0]))
        np.testing.assert_allclose(result, np.array([-2.0, 2.0]))

    def test_recurrence_statistic_balanced_years(self) -> None:
        self.assertAlmostEqual(recurrence_statistic([5, 5], [100, 100]), 1.0)

    def test_bh_qvalues(self) -> None:
        result = _bh_qvalues(np.array([0.01, 0.02, 0.5]))
        np.testing.assert_allclose(result, np.array([0.03, 0.03, 0.5]))

    def test_southworth_hawkins_is_zero_for_same_orbit(self) -> None:
        orbit = np.array([[0.94, 0.08, 24.0, 333.0, 37.0]])
        result = southworth_hawkins_pairs(orbit, np.array([[0, 0]]))
        np.testing.assert_allclose(result, np.array([0.0]), atol=1e-12)

    def test_southworth_hawkins_is_symmetric(self) -> None:
        orbits = np.array(
            [
                [0.94, 0.08, 24.0, 333.0, 37.0],
                [0.95, 0.09, 25.0, 334.0, 38.0],
            ]
        )
        forward = southworth_hawkins_pairs(orbits, np.array([[0, 1]]))[0]
        reverse = southworth_hawkins_pairs(orbits, np.array([[1, 0]]))[0]
        self.assertAlmostEqual(float(forward), float(reverse), places=12)


class InputValidationTests(unittest.TestCase):
    @staticmethod
    def _panel() -> pd.DataFrame:
        return pd.DataFrame(
            {
                "event_id": ["a", "b"],
                "year": [2025, 2026],
                "sol_lon_deg": [36.0, 37.0],
                "lamgeo_deg": [246.0, 247.0],
                "betgeo_deg": [7.0, 7.2],
                "vgeo_km_s": [37.0, 38.0],
                "e": [0.94, 0.95],
                "q": [0.08, 0.09],
                "inc": [24.0, 25.0],
                "peri": [333.0, 334.0],
                "node": [37.0, 38.0],
            }
        )

    def _write(self, frame: pd.DataFrame) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "panel.csv"
        frame.to_csv(path, index=False)
        return path

    def test_load_panel_accepts_valid_input(self) -> None:
        result = load_panel(self._write(self._panel()))
        self.assertEqual(len(result), 2)
        self.assertTrue(np.issubdtype(result["year"].dtype, np.integer))

    def test_load_panel_rejects_duplicate_event_ids(self) -> None:
        frame = self._panel()
        frame.loc[1, "event_id"] = "a"
        with self.assertRaisesRegex(ValueError, "event_id must be unique"):
            load_panel(self._write(frame))

    def test_load_panel_rejects_missing_event_id(self) -> None:
        frame = self._panel()
        frame.loc[0, "event_id"] = None
        with self.assertRaisesRegex(ValueError, "event_id cannot be missing"):
            load_panel(self._write(frame))

    def test_load_panel_rejects_nonfinite_values(self) -> None:
        frame = self._panel()
        frame.loc[0, "vgeo_km_s"] = np.nan
        with self.assertRaisesRegex(ValueError, "non-finite"):
            load_panel(self._write(frame))


class RevealGuardTests(unittest.TestCase):
    def test_explicit_false_flag_is_accepted(self) -> None:
        _certify_target_free({"target_accessed_during_generation_or_ranking": False})

    def test_missing_flag_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "certification"):
            _certify_target_free({})

    def test_contradictory_flags_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not certify"):
            _certify_target_free(
                {
                    "target_accessed_during_generation_or_ranking": False,
                    "target_accessed_during_generation_ranking_or_membership": True,
                }
            )

    def test_ambiguous_flag_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not certify"):
            _certify_target_free({"target_accessed_during_generation_or_ranking": None})


if __name__ == "__main__":
    unittest.main()
