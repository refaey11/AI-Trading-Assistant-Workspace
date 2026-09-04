from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "BACKTEST" / "DEV_BACKTEST_RUNNER_GOVERNED_V2.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("governed_runner", RUNNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_uses_separate_governed_gate_and_fail_closes_missing_tiz_risk():
    r = load_runner()
    assert r.GATE_PATH.name == "murphy_governed_decision_gate_v1.py"
    assert r.BRAIN_PATH.name == "decision_brain.py"


def test_murphy_aggregation_does_not_infer_direction():
    r = load_runner()
    import pandas as pd
    df = pd.DataFrame([
        {"timestamp": "2024-01-01T00:00:00Z", "status": "PASS", "direction": None, "source_rule_id": "MURPHY_0003"},
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    out = r.aggregate_murphy(df)
    assert out.iloc[0]["direction"] is None
    assert out.iloc[0]["status"] == "NOT_EVALUABLE"


def test_murphy_conflicting_explicit_directions_fail_closed():
    r = load_runner()
    import pandas as pd
    df = pd.DataFrame([
        {"timestamp": "2024-01-01T00:00:00Z", "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"},
        {"timestamp": "2024-01-01T00:00:00Z", "status": "PASS", "direction": "BEARISH", "source_rule_id": "MURPHY_0025"},
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    out = r.aggregate_murphy(df)
    assert out.iloc[0]["direction"] is None
    assert out.iloc[0]["status"] == "PASS"
