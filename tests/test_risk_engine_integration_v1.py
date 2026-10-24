import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "RUNTIME"
    / "RISK_ENGINE_INTEGRATION_V1"
    / "risk_engine_integration_v1.py"
)
SPEC = importlib.util.spec_from_file_location("risk_engine_integration_v1", MODULE_PATH)
assert SPEC and SPEC.loader
risk = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(risk)


class RiskEngineHardGateTests(unittest.TestCase):
    def evaluate(self, **overrides):
        args = {
            "equity": 10_000.0,
            "entry": 100.0,
            "stop_loss": 99.25,
            "take_profit": 101.5,
            "atr": 1.0,
            "prior_loss_streak": 0,
            "peak_equity": 10_000.0,
        }
        args.update(overrides)
        return risk.evaluate_risk(**args)

    def test_valid_2r_trade_passes_and_position_size_is_positive(self):
        result = self.evaluate()
        self.assertTrue(result.risk_pass)
        self.assertEqual(result.reason, "RISK_GATE_PASS")
        self.assertGreater(result.position_size, 0)

    def test_missing_stop_or_target_fails_closed(self):
        result = self.evaluate(stop_loss=None)
        self.assertFalse(result.risk_pass)
        self.assertEqual(result.reason, "MISSING_EXECUTION_INPUT")

    def test_subminimum_rr_fails_closed(self):
        result = self.evaluate(take_profit=100.5)
        self.assertFalse(result.risk_pass)
        self.assertEqual(result.reason, "RR_BELOW_CURRENT_CANONICAL_MINIMUM")

    def test_drawdown_circuit_breaker_fails_closed(self):
        result = self.evaluate(equity=9_400.0, peak_equity=10_000.0)
        self.assertFalse(result.risk_pass)
        self.assertEqual(result.reason, "DRAWDOWN_CIRCUIT_BREAKER")

    def test_risk_budget_above_maximum_fails_closed(self):
        result = self.evaluate(risk_budget_pct=0.02)
        self.assertFalse(result.risk_pass)
        self.assertEqual(result.reason, "RISK_BUDGET_INVALID")


if __name__ == "__main__":
    unittest.main()
