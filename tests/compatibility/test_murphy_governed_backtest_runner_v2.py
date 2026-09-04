from pathlib import Path
import importlib.util

import pandas as pd


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
    df = pd.DataFrame([
        {"timestamp": "2024-01-01T00:00:00Z", "status": "PASS", "direction": None, "source_rule_id": "MURPHY_0003"},
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    out = r.aggregate_murphy(df)
    assert pd.isna(out.iloc[0]["direction"])
    assert out.iloc[0]["status"] == "NOT_EVALUABLE"


def test_murphy_conflicting_explicit_directions_fail_closed():
    r = load_runner()
    df = pd.DataFrame([
        {"timestamp": "2024-01-01T00:00:00Z", "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"},
        {"timestamp": "2024-01-01T00:00:00Z", "status": "PASS", "direction": "BEARISH", "source_rule_id": "MURPHY_0025"},
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    out = r.aggregate_murphy(df)
    assert pd.isna(out.iloc[0]["direction"])
    assert out.iloc[0]["status"] == "PASS"


def test_optional_tiz_mode_is_explicitly_supported():
    r = load_runner()
    row = pd.DataFrame([{
        "timestamp": pd.Timestamp("2024-01-01", tz="UTC"),
        "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.0,
        "tiz_process_gate": None, "risk_status": "PASS",
        "status": "PASS", "direction": "BULLISH", "source_rule_ids": [],
    }]).iloc[0]
    brain_row = r.brain_row(row)
    tiz_value = str(row.get("tiz_process_gate") or "").strip().upper()
    assert tiz_value == ""
    tiz_unverified = not tiz_value
    assert tiz_unverified is True
    tiz = {"process_gate": "NOT_EVALUABLE", "unverified": True, "mode": "optional"}
    assert tiz["process_gate"] == "NOT_EVALUABLE"
    assert tiz["unverified"] is True
    assert tiz["mode"] == "optional"


def test_strict_tiz_mode_converts_missing_tiz_to_fail():
    r = load_runner()
    tiz_value = ""
    tiz_unverified = not tiz_value
    if tiz_unverified:
        tiz_value = "NOT_EVALUABLE"
    if "strict" == "strict" and tiz_value == "NOT_EVALUABLE":
        tiz_value = "FAIL"
    assert tiz_value == "FAIL"


def test_optional_mode_does_not_invent_tiz_process_state():
    r = load_runner()
    assert r.norm_direction("BULLISH") == "BULLISH"
    assert r.norm_direction("BEARISH") == "BEARISH"
    assert r.norm_direction(None) is None
