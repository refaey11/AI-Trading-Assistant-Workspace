import unittest

from bridges.murphy_0028_evaluator_to_evidence import adapt_evaluator_result


class Murphy0028BridgeTests(unittest.TestCase):
    def test_pass_bearish_warning_maps_to_bearish(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "status": "PASS",
            "directional_confirmation": "BEARISH_WARNING",
            "reason": "Confirmed bearish price/RSI divergence on a high-pivot sequence.",
        })
        self.assertEqual(result["direction"], "bearish")
        self.assertEqual(result["decision_hint"], "bearish")
        self.assertEqual(result["gate"], "pass")
        self.assertEqual(result["conflict"], "neutral")
        self.assertTrue(result["available"])

    def test_pass_plain_bearish_is_accepted(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "status": "PASS",
            "directional_confirmation": "BEARISH",
        })
        self.assertEqual(result["direction"], "bearish")
        self.assertEqual(result["decision_hint"], "bearish")

    def test_fail_never_infers_bullish(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "status": "FAIL",
            "directional_confirmation": "NONE",
        })
        self.assertEqual(result["direction"], "neutral")
        self.assertEqual(result["decision_hint"], "neutral")
        self.assertEqual(result["gate"], "fail")
        self.assertEqual(result["conflict"], "contradicts")
        self.assertTrue(result["available"])

    def test_not_evaluable_is_needs_review(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "status": "NOT_EVALUABLE",
            "reason": "Missing divergence evidence.",
        })
        self.assertEqual(result["direction"], "neutral")
        self.assertEqual(result["decision_hint"], "neutral")
        self.assertEqual(result["gate"], "needs_review")
        self.assertEqual(result["conflict"], "insufficient")
        self.assertFalse(result["available"])

    def test_unknown_status_is_neutral_and_needs_review(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "status": "UNKNOWN",
            "directional_confirmation": "BEARISH_WARNING",
        })
        self.assertEqual(result["direction"], "neutral")
        self.assertEqual(result["decision_hint"], "neutral")
        self.assertEqual(result["gate"], "needs_review")
        self.assertEqual(result["conflict"], "insufficient")

    def test_missing_status_does_not_create_evidence(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "directional_confirmation": "BEARISH_WARNING",
        })
        self.assertFalse(result["available"])
        self.assertEqual(result["decision_hint"], "neutral")

    def test_confidence_delta_is_zero(self):
        result = adapt_evaluator_result({
            "rule_id": "MURPHY_0028",
            "status": "PASS",
            "directional_confirmation": "BEARISH_WARNING",
        })
        self.assertEqual(result["confidence_delta"], 0)

    def test_raw_result_is_preserved(self):
        raw = {
            "rule_id": "MURPHY_0028",
            "status": "PASS",
            "directional_confirmation": "BEARISH_WARNING",
            "reason": "Confirmed bearish price/RSI divergence on a high-pivot sequence.",
            "availability_timestamp": "2024-01-01T00:00:00Z",
        }
        result = adapt_evaluator_result(raw)
        self.assertEqual(result["raw_evaluator_result"], raw)
        self.assertIsNot(result["raw_evaluator_result"], raw)


if __name__ == "__main__":
    unittest.main()
