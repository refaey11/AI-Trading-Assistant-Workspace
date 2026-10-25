from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve().parents[1] / "BACKTEST" / "DEV_BACKTEST_RUNNER_V1.py"
SPEC = importlib.util.spec_from_file_location("dev_backtest_runner_v1_test", RUNNER_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


class RunnerRiskGateWiringTests(unittest.TestCase):
    def test_risk_engine_dynamic_loader_executes(self):
        module = runner.load_risk_engine()
        result = module.evaluate_risk(
            equity=10_000.0,
            peak_equity=10_000.0,
            entry=100.0,
            stop_loss=99.25,
            take_profit=101.5,
            atr=1.0,
            prior_loss_streak=0,
        )
        self.assertTrue(result.risk_pass)
        self.assertEqual(result.reason, "RISK_GATE_PASS")

    def test_missing_equity_inputs_are_configured_to_fail_closed(self):
        self.assertIn("equity", runner.run.__kwdefaults__)
        self.assertIsNone(runner.run.__kwdefaults__["equity"])
        self.assertIsNone(runner.run.__kwdefaults__["peak_equity"])

    def test_brain_lowercase_bias_normalizes_to_governed_direction(self):
        self.assertEqual(runner.normalize_direction("bullish"), "BULLISH")
        self.assertEqual(runner.normalize_direction("bearish"), "BEARISH")
        self.assertIsNone(runner.normalize_direction("conflicted"))


if __name__ == "__main__":
    unittest.main()
