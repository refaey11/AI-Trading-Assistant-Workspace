import unittest
from nison_0008_0015_source_contract_gate import evaluate


class Nison0008To0015Tests(unittest.TestCase):
    def test_0008_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0008", 3, "downtrend")["status"], "NOT_EVALUABLE")

    def test_0009_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0009", 3, "uptrend")["status"], "NOT_EVALUABLE")

    def test_0010_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0010", 3, "downtrend")["status"], "NOT_EVALUABLE")

    def test_0011_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0011", 3, "uptrend")["status"], "NOT_EVALUABLE")

    def test_0012_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0012", 3, "uptrend")["status"], "NOT_EVALUABLE")

    def test_0013_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0013", 2, "downtrend")["status"], "NOT_EVALUABLE")

    def test_0014_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0014", 2, "uptrend")["status"], "NOT_EVALUABLE")

    def test_0015_missing_operator_fails_closed(self):
        self.assertEqual(evaluate("NISON_0015", 2, "uptrend")["status"], "NOT_EVALUABLE")

    def test_wrong_source_context_rejects(self):
        self.assertEqual(evaluate("NISON_0008", 3, "uptrend")["status"], "FAIL")
        self.assertEqual(evaluate("NISON_0009", 3, "downtrend")["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
