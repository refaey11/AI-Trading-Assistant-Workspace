import unittest
from mtf_structure_producer_v2 import (
    Bar, ConfirmedPivot, produce_structure_v2, aggregate_mtf_context
)


def bars(n, close=10.0):
    return [Bar(i, close, close + 1, close - 1, close) for i in range(n)]


def pivot(pid, kind, price, source, available):
    return ConfirmedPivot(pid, kind, price, source, available)


class ProducerV2Tests(unittest.TestCase):
    def bullish_pivots(self):
        return [
            pivot("h1", "HIGH", 10, 0, 2), pivot("h2", "HIGH", 12, 3, 5),
            pivot("l1", "LOW", 5, 1, 3), pivot("l2", "LOW", 7, 4, 6),
        ]

    def test_pivot_not_visible_before_availability(self):
        out = produce_structure_v2(bars(8), self.bullish_pivots(),
                                   symbol="GBPUSD", timeframe="M5")
        self.assertNotIn("h2", out["rows"][4]["available_pivot_ids"])
        self.assertIn("h2", out["rows"][5]["available_pivot_ids"])

    def test_bullish_state_from_hh_hl(self):
        out = produce_structure_v2(bars(8), self.bullish_pivots(),
                                   symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][6]["structure_state"], "BULLISH_STRUCTURE")

    def test_bearish_state_from_lh_ll(self):
        ps = [pivot("h1","HIGH",12,0,2), pivot("h2","HIGH",10,3,5),
              pivot("l1","LOW",7,1,3), pivot("l2","LOW",5,4,6)]
        out = produce_structure_v2(bars(8), ps, symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][6]["structure_state"], "BEARISH_STRUCTURE")

    def test_mixed_and_equal_are_not_directional(self):
        ps = [pivot("h1","HIGH",10,0,2), pivot("h2","HIGH",10,3,5),
              pivot("l1","LOW",5,1,3), pivot("l2","LOW",7,4,6)]
        out = produce_structure_v2(bars(8), ps, symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][6]["structure_state"], "RANGE_OR_MIXED")

    def test_insufficient_history(self):
        out = produce_structure_v2(bars(5), [pivot("h1","HIGH",10,0,2)],
                                   symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][-1]["structure_state"], "INSUFFICIENT_PIVOT_HISTORY")

    def test_future_bar_perturbation_does_not_change_past(self):
        ps = self.bullish_pivots()
        a = produce_structure_v2(bars(8), ps, symbol="GBPUSD", timeframe="M5")
        b = produce_structure_v2(bars(10), ps, symbol="GBPUSD", timeframe="M5")
        self.assertEqual(a["rows"], b["rows"][:8])

    def test_mtf_conflict_is_not_averaged(self):
        out = aggregate_mtf_context({"H4":"BULLISH_STRUCTURE","M15":"BEARISH_STRUCTURE"})
        self.assertEqual(out["status"], "CONFLICTED")
        self.assertIsNone(out["directional_score"])
        self.assertFalse(out["majority_vote_used"])

    def test_unverified_clock_is_not_claimed_available(self):
        out = produce_structure_v2(bars(3), [], symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][0]["availability_status"], "CLOCK_UNVERIFIED")

    def test_rejects_unclosed_bars(self):
        data = bars(3)
        data[1] = Bar(1, 10, 11, 9, 10, completed=False)
        with self.assertRaises(ValueError):
            produce_structure_v2(data, [], symbol="GBPUSD", timeframe="M5")

    def test_rejects_early_pivot_confirmation(self):
        with self.assertRaises(ValueError):
            produce_structure_v2(bars(4), [pivot("bad","HIGH",10,1,2)],
                                 symbol="GBPUSD", timeframe="M5")


    def test_bos_up_is_continuation_of_bullish_structure(self):
        data = bars(8) + [Bar(8, 12, 14, 11, 13)]
        out = produce_structure_v2(data, self.bullish_pivots(),
                                   symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][8]["event"]["event_type"], "BOS_UP")

    def test_choch_down_is_break_against_bullish_structure(self):
        data = bars(8) + [Bar(8, 8, 9, 5, 6)]
        out = produce_structure_v2(data, self.bullish_pivots(),
                                   symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][8]["event"]["event_type"], "CHOCH_DOWN")

    def test_wick_only_break_does_not_emit_close_confirmed_event(self):
        data = bars(8) + [Bar(8, 10, 13, 9, 11)]
        out = produce_structure_v2(data, self.bullish_pivots(),
                                   symbol="GBPUSD", timeframe="M5")
        self.assertIsNone(out["rows"][8]["event"])

    def test_choch_up_is_break_against_bearish_structure(self):
        ps = [pivot("h1","HIGH",12,0,2), pivot("h2","HIGH",10,3,5),
              pivot("l1","LOW",7,1,3), pivot("l2","LOW",5,4,6)]
        data = bars(8) + [Bar(8, 9, 12, 8, 11)]
        out = produce_structure_v2(data, ps, symbol="GBPUSD", timeframe="M5")
        self.assertEqual(out["rows"][8]["event"]["event_type"], "CHOCH_UP")


if __name__ == "__main__":
    unittest.main()
