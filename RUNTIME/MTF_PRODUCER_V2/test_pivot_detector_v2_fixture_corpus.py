"""Structural validation for the V2 synthetic pivot fixture corpus.

These tests validate fixture integrity and coverage only. They do not implement
or certify a pivot detector and do not select production L/R parameters.
"""
import json
import unittest
from pathlib import Path

FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "pivot_detector_v2_synthetic_golden_fixtures_v1.json"
)


class PivotFixtureCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = cls.payload["fixtures"]

    def test_expected_six_timeframes_and_candidate_windows(self):
        self.assertEqual(
            self.payload["timeframes"], ["M5", "M15", "M30", "H1", "H4", "D1"]
        )
        self.assertEqual(
            [(x["left"], x["right"]) for x in self.payload["candidate_windows"]],
            [(2, 2), (3, 3), (5, 5)],
        )

    def test_complete_timeframe_window_scenario_matrix(self):
        expected_scenarios = {
            "ISOLATED_HIGH",
            "ISOLATED_LOW",
            "EQUAL_HIGH",
            "EQUAL_LOW",
            "GAP_IN_RIGHT_WINDOW",
            "RIGHT_WINDOW_INCOMPLETE",
            "SAME_BAR_DUAL_HIGH_LOW",
            "FUTURE_PERTURBATION",
            "DETERMINISTIC_REPLAY",
            "LEFT_WINDOW_INCOMPLETE",
            "INVALID_OHLC",
            "UNFINISHED_CONFIRMING_BAR",
            "MISSING_PRECISION_METADATA",
            "MISSING_CLOCK_PROVENANCE",
            "WARMUP_WITH_ORIGINAL_PROVENANCE",
            "WARMUP_WITHOUT_ORIGINAL_PROVENANCE",
        }
        ids = [fixture["id"] for fixture in self.fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(self.fixtures), 288)
        for timeframe in self.payload["timeframes"]:
            for window in (2, 3, 5):
                prefix = f"{timeframe}_W{window}_"
                actual = {
                    fixture["id"][len(prefix):]
                    for fixture in self.fixtures
                    if fixture["id"].startswith(prefix)
                }
                self.assertEqual(actual, expected_scenarios)

    def test_bar_indices_are_contiguous_and_closed(self):
        for fixture in self.fixtures:
            bars = fixture["bars"]
            self.assertEqual([bar["index"] for bar in bars], list(range(len(bars))))
            if fixture["id"].endswith("UNFINISHED_CONFIRMING_BAR"):
                self.assertTrue(all(bar["closed"] for bar in bars[:-1]))
                self.assertFalse(bars[-1]["closed"])
            else:
                self.assertTrue(all(bar["closed"] for bar in bars))

    def test_confirmation_boundary_is_explicit(self):
        for fixture in self.fixtures:
            expected = fixture["expected"]
            if expected["status"] == "CONFIRMED_AFTER_RIGHT_WINDOW":
                self.assertEqual(
                    expected["available_bar_index"],
                    expected["candidate_index"] + fixture["window"]["right"],
                )
                self.assertEqual(
                    len(fixture["bars"]) - 1, expected["available_bar_index"]
                )
            elif expected["status"] == "PENDING":
                if expected.get("reason") == "CONFIRMING_BAR_NOT_COMPLETED":
                    self.assertEqual(
                        len(fixture["bars"]) - 1,
                        expected["candidate_index"] + fixture["window"]["right"],
                    )
                    self.assertFalse(fixture["bars"][-1]["closed"])
                else:
                    self.assertLess(
                        len(fixture["bars"]) - 1,
                        expected["candidate_index"] + fixture["window"]["right"],
                    )

    def test_candidate_windows_are_test_only(self):
        self.assertTrue(
            all(x["status"] == "SYNTHETIC_TEST_ONLY"
                for x in self.payload["candidate_windows"])
        )
        self.assertIn("not a pivot detector implementation",
                      self.payload["purpose"])


    def test_same_bar_dual_candidate_order_is_not_inferred(self):
        for fixture in self.fixtures:
            if fixture["id"].endswith("SAME_BAR_DUAL_HIGH_LOW"):
                self.assertEqual(
                    fixture["expected"]["status"],
                    "BOTH_CANDIDATES_ORDER_UNRESOLVED",
                )
                self.assertTrue(fixture["expected"]["high_candidate"])
                self.assertTrue(fixture["expected"]["low_candidate"])

    def test_future_perturbation_is_after_decision_snapshot(self):
        for fixture in self.fixtures:
            if fixture["id"].endswith("FUTURE_PERTURBATION"):
                expected = fixture["expected"]
                self.assertGreater(
                    fixture["future_perturbation"][0]["index"],
                    expected["decision_snapshot_bar_index"],
                )
                self.assertEqual(
                    fixture["future_perturbation"][0]["index"],
                    len(fixture["bars"]),
                )

    def test_replay_fixture_does_not_freeze_identity_encoding(self):
        for fixture in self.fixtures:
            if fixture["id"].endswith("DETERMINISTIC_REPLAY"):
                self.assertEqual(fixture["expected"]["replay_count"], 2)
                self.assertEqual(
                    fixture["expected"]["identity_encoding"], "NOT_YET_FROZEN"
                )


    def test_invalid_input_and_untrusted_metadata_are_explicit(self):
        for fixture in self.fixtures:
            suffix = fixture["id"].split("_W", 1)[-1].split("_", 1)[1]
            expected = fixture["expected"]
            if suffix == "INVALID_OHLC":
                self.assertEqual(expected["reason"], "INVALID_OHLC")
            elif suffix == "UNFINISHED_CONFIRMING_BAR":
                self.assertFalse(fixture["bars"][-1]["closed"])
                self.assertEqual(expected["status"], "PENDING")
            elif suffix == "MISSING_PRECISION_METADATA":
                self.assertIsNone(fixture["metadata"]["instrument_precision"])
                self.assertEqual(expected["status"], "NOT_EVALUABLE")
            elif suffix == "MISSING_CLOCK_PROVENANCE":
                self.assertIsNone(fixture["metadata"]["clock_evidence"])
                self.assertEqual(expected["status"], "UNAVAILABLE")

    def test_warmup_requires_original_identity_and_provenance(self):
        for fixture in self.fixtures:
            if fixture["id"].endswith("WARMUP_WITH_ORIGINAL_PROVENANCE"):
                warmup = fixture["metadata"]["warmup"]
                self.assertTrue(warmup["source_bar_id"])
                self.assertTrue(warmup["available_at"])
                self.assertTrue(warmup["provenance_ref"])
            elif fixture["id"].endswith("WARMUP_WITHOUT_ORIGINAL_PROVENANCE"):
                warmup = fixture["metadata"]["warmup"]
                self.assertIsNone(warmup["source_bar_id"])
                self.assertEqual(
                    fixture["expected"]["reason"],
                    "WARMUP_SOURCE_IDENTITY_OR_PROVENANCE_MISSING",
                )


if __name__ == "__main__":
    unittest.main()
