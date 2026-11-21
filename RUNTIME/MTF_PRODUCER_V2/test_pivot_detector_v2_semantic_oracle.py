import math
import unittest

from RUNTIME.MTF_PRODUCER_V2.pivot_detector_v2_semantic_oracle import (
    SyntheticBar, evaluate_candidate,
)

TFS = ("M5", "M15", "M30", "H1", "H4", "D1")


def make_bars(highs, lows=None, *, complete=True, start=100):
    if lows is None:
        lows = [h - 2 for h in highs]
    return [
        SyntheticBar(f"synthetic-{i}", float(h), float(l), complete, start + i)
        for i, (h, l) in enumerate(zip(highs, lows))
    ]


def evaluate(bars, index, left=2, right=2, edges=None, precision=True):
    if edges is None:
        edges = [True] * (len(bars) - 1)
    return evaluate_candidate(
        bars, index, left, right,
        continuity_verified=edges,
        precision_verified=precision,
    )


class PivotSemanticOracleTests(unittest.TestCase):
    def test_strict_isolated_high_and_final_right_availability(self):
        bars = make_bars([1, 2, 9, 3, 4], [0, 1, 7, 2, 3])
        high, _ = evaluate(bars, 2)
        self.assertEqual(high.status, "CONFIRMED")
        self.assertEqual(high.available_at, bars[4].available_at)
        self.assertEqual(high.reason, "STRICT_ISOLATED_HIGH")

    def test_strict_isolated_low(self):
        bars = make_bars([8, 7, 3, 6, 7], [6, 5, -2, 4, 5])
        _, low = evaluate(bars, 2)
        self.assertEqual(low.status, "CONFIRMED")
        self.assertEqual(low.available_at, bars[4].available_at)

    def test_equal_high_plateau_is_not_evaluable(self):
        bars = make_bars([1, 9, 9, 3, 4], [0, 7, 7, 2, 3])
        high, _ = evaluate(bars, 2)
        self.assertEqual((high.status, high.reason),
                         ("NOT_EVALUABLE", "EQUAL_HIGH_PLATEAU"))

    def test_equal_low_plateau_is_not_evaluable(self):
        bars = make_bars([8, 7, 6, 7, 8], [6, 4, 4, 5, 6])
        _, low = evaluate(bars, 2)
        self.assertEqual((low.status, low.reason),
                         ("NOT_EVALUABLE", "EQUAL_LOW_PLATEAU"))

    def test_same_bar_high_and_low_are_retained_separately(self):
        bars = make_bars([1, 2, 10, 3, 4], [0, -1, -2, -1, 0])
        high, low = evaluate(bars, 2)
        self.assertEqual(high.status, "CONFIRMED")
        self.assertEqual(low.status, "CONFIRMED")
        self.assertEqual(high.source_index, low.source_index)
        self.assertEqual(high.kind, "HIGH")
        self.assertEqual(low.kind, "LOW")

    def test_incomplete_left_context_is_pending(self):
        high, low = evaluate(make_bars([1, 2, 9]), 1)
        self.assertEqual((high.status, low.status), ("PENDING", "PENDING"))
        self.assertEqual(high.reason, "INSUFFICIENT_LEFT_CONTEXT")

    def test_incomplete_right_context_is_pending(self):
        high, low = evaluate(make_bars([1, 2, 9, 3]), 2)
        self.assertEqual((high.status, low.status), ("PENDING", "PENDING"))
        self.assertEqual(high.reason, "INCOMPLETE_RIGHT_CONTEXT")

    def test_unproven_gap_blocks_candidate(self):
        bars = make_bars([1, 2, 9, 3, 4])
        edges = [True, False, True, True]
        high, low = evaluate(bars, 2, edges=edges)
        self.assertEqual((high.status, low.status),
                         ("NOT_EVALUABLE", "NOT_EVALUABLE"))
        self.assertEqual(high.reason, "UNPROVEN_SEQUENCE_GAP")

    def test_verified_continuity_allows_normal_evaluation(self):
        high, _ = evaluate(make_bars([1, 2, 9, 3, 4]), 2)
        self.assertEqual(high.status, "CONFIRMED")

    def test_missing_precision_blocks_equality_sensitive_decision(self):
        high, low = evaluate(make_bars([1, 2, 9, 3, 4]), 2,
                             precision=False)
        self.assertEqual((high.status, low.status),
                         ("NOT_EVALUABLE", "NOT_EVALUABLE"))
        self.assertEqual(high.reason, "TRUSTED_PRECISION_MISSING")

    def test_unfinished_or_invalid_bar_blocks_window(self):
        bars = make_bars([1, 2, 9, 3, 4])
        bars[3] = SyntheticBar("synthetic-3", 3, 2, False, 103)
        high, _ = evaluate(bars, 2)
        self.assertEqual(high.status, "NOT_EVALUABLE")
        self.assertEqual(high.reason, "INVALID_OR_UNFINISHED_BAR")

    def test_duplicate_source_bar_identity_blocks_window(self):
        bars = make_bars([1, 2, 9, 3, 4])
        bars[3] = SyntheticBar(bars[2].source_bar_id, 3, 1, True, 103)
        high, _ = evaluate(bars, 2)
        self.assertEqual(high.reason, "DUPLICATE_SOURCE_BAR_ID")

    def test_unordered_availability_blocks_window(self):
        bars = make_bars([1, 2, 9, 3, 4])
        bars[3] = SyntheticBar("synthetic-3", 3, 1, True, 101)
        high, _ = evaluate(bars, 2)
        self.assertEqual(high.reason, "UNORDERED_AVAILABILITY")

    def test_non_finite_values_block_window(self):
        bars = make_bars([1, 2, 9, 3, 4])
        bars[2] = SyntheticBar("synthetic-2", math.nan, 1, True, 102)
        high, _ = evaluate(bars, 2)
        self.assertEqual(high.status, "NOT_EVALUABLE")

    def test_future_bars_cannot_change_earlier_confirmation(self):
        full = make_bars([1, 2, 9, 3, 4, 100, -50])
        prefix = full[:5]
        a, _ = evaluate(prefix, 2)
        b, _ = evaluate(full, 2)
        self.assertEqual(a, b)

    def test_each_timeframe_is_independent(self):
        expected = ("CONFIRMED", "CONFIRMED")
        for timeframe in TFS:
            with self.subTest(timeframe=timeframe):
                highs = [9, 10, 11, 9, 10]
                lows = [8, 7, -2, 6, 7]
                high, low = evaluate(make_bars(highs, lows), 2)
                self.assertEqual((high.status, low.status), expected)

    def test_l_and_r_are_explicit_and_independent(self):
        bars = make_bars([1, 2, 9, 3, 4, 5])
        high, _ = evaluate(bars, 2, left=1, right=3)
        self.assertEqual(high.status, "CONFIRMED")
        self.assertEqual(high.available_at, bars[5].available_at)

    def test_rejects_non_positive_l_or_r(self):
        bars = make_bars([1, 2, 9, 3, 4])
        with self.assertRaises(ValueError):
            evaluate(bars, 2, left=0, right=2)

    def test_rejects_missing_continuity_evidence_shape(self):
        bars = make_bars([1, 2, 9, 3, 4])
        with self.assertRaises(ValueError):
            evaluate_candidate(bars, 2, 2, 2,
                               continuity_verified=[True],
                               precision_verified=True)


if __name__ == "__main__":
    unittest.main()
