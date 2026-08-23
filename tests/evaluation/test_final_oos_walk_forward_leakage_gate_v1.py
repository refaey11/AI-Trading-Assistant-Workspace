from __future__ import annotations

import pandas as pd

from OOS_2025.final_oos_walk_forward_leakage_gate_v1 import run

META = {
    "signal_contract_id": "FROZEN_CANDIDATE_V2_4H",
    "execution_protocol_id": "ENTRY_CLOSE_SL_0.75ATR20_TP_2R",
    "cost_model_id": "GOVERNED_EXECUTION_COSTS_V1",
    "ambiguity_policy_id": "AMBIGUOUS_EXCLUDED_V1",
}


def _write(path, year, values):
    rows = []
    for i, net in enumerate(values):
        row = {
            "event_id": f"{year}-{i}",
            "timestamp": f"{year}-01-01T0{i}:00:00Z",
            "direction": "BUY",
            "gross_r": net + 0.01,
            "cost_r": 0.01,
            "net_r": net,
            "outcome": "TP" if net > 0 else "SL",
            "ambiguous": False,
            "feature_available_at": f"{year}-01-01T0{i}:00:00Z",
            "memory_built_through": f"{year}-01-01T0{i}:00:00Z",
            "decision_available_at": f"{year}-01-01T0{i}:00:00Z",
            **META,
        }
        rows.append(row)
    pd.DataFrame(rows).to_csv(path, index=False)


def test_uniform_two_fold_metrics_and_costs(tmp_path):
    a = tmp_path / "2024.csv"
    b = tmp_path / "2025.csv"
    _write(a, 2024, [2.0, -1.0])
    _write(b, 2025, [2.0, -1.0, 2.0])
    result = run(a, b)
    assert result["status"] == "PASS"
    assert result["uniform_protocol"]["cost_model_id"] == "GOVERNED_EXECUTION_COSTS_V1"
    assert result["metrics"]["2024_oos"]["profit_factor"] == 2.0
    assert result["metrics"]["2025_oos"]["trades"] == 3
    assert result["metrics"]["combined"]["costs_r"] == 0.05


def test_future_feature_availability_is_rejected(tmp_path):
    a = tmp_path / "2024.csv"
    b = tmp_path / "2025.csv"
    _write(a, 2024, [1.0])
    _write(b, 2025, [1.0])
    df = pd.read_csv(b)
    df.loc[0, "feature_available_at"] = "2025-01-01T01:00:00Z"
    df.to_csv(b, index=False)
    try:
        run(a, b)
    except ValueError as exc:
        assert "future feature availability" in str(exc)
    else:
        raise AssertionError("expected future feature availability failure")


def test_protocol_mismatch_is_rejected(tmp_path):
    a = tmp_path / "2024.csv"
    b = tmp_path / "2025.csv"
    _write(a, 2024, [1.0])
    _write(b, 2025, [1.0])
    df = pd.read_csv(b)
    df.loc[0, "execution_protocol_id"] = "OTHER_PROTOCOL"
    df.to_csv(b, index=False)
    try:
        run(a, b)
    except ValueError as exc:
        assert "protocol mismatch" in str(exc)
    else:
        raise AssertionError("expected protocol mismatch failure")
