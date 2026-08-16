import unittest
from nison_0003_0007_source_bounded_gate import (
    Candle, evaluate_0003_dark_cloud, evaluate_0004_piercing,
    evaluate_0005_on_neck, evaluate_0006_in_neck, evaluate_0007_thrusting,
)


class Nison0003To0007Tests(unittest.TestCase):
    def test_0003_missing_context_is_not_evaluable(self):
        r = evaluate_0003_dark_cloud(Candle(1, 2, 0.9, 1.8), Candle(1.9, 2.2, 1.5, 1.6), None)
        self.assertEqual(r["status"], "NOT_EVALUABLE")

    def test_0003_wrong_open_rejects(self):
        r = evaluate_0003_dark_cloud(Candle(1, 2, 0.9, 1.8), Candle(1.9, 2.2, 1.5, 1.6), "uptrend")
        self.assertEqual(r["status"], "FAIL")

    def test_0004_midpoint_boundary_rejects(self):
        r = evaluate_0004_piercing(Candle(2, 2.1, 0.9, 1), Candle(0.8, 1.7, 0.7, 1.4), "downtrend")
        self.assertEqual(r["status"], "NOT_EVALUABLE")

    def test_0004_wrong_context_rejects(self):
        r = evaluate_0004_piercing(Candle(2, 2.1, 0.9, 1), Candle(0.8, 1.7, 0.7, 1.4), "uptrend")
        self.assertEqual(r["status"], "FAIL")

    def test_0005_qualitative_neck_remains_unresolved(self):
        r = evaluate_0005_on_neck(Candle(2, 2.1, 0.9, 1), Candle(0.8, 1.1, 0.7, 1.0), "downtrend")
        self.assertEqual(r["status"], "NOT_EVALUABLE")

    def test_0006_qualitative_neck_remains_unresolved(self):
        r = evaluate_0006_in_neck(Candle(2, 2.1, 0.9, 1), Candle(0.8, 1.3, 0.7, 1.1), "downtrend")
        self.assertEqual(r["status"], "NOT_EVALUABLE")

    def test_0007_above_midpoint_rejects(self):
        r = evaluate_0007_thrusting(Candle(2, 2.1, 0.9, 1), Candle(0.8, 1.7, 0.7, 1.6), "downtrend")
        self.assertEqual(r["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
