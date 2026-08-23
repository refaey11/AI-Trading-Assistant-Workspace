from __future__ import annotations

import pandas as pd

from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021
from OOS_2025.run_murphy_0021_2025_fresh_v1 import run


def test_volume_direction_uses_canonical_m1_derived_h1_context(tmp_path):
    src = tmp_path / "h1.csv"
    m1 = tmp_path / "m1.csv"
    pd.DataFrame([
        {"timestamp": "2025-01-01T00:00:00Z", "open": 1, "high": 2, "low": 0.5, "close": 1.5},
        {"timestamp": "2025-01-01T01:00:00Z", "open": 1.5, "high": 2.5, "low": 1.2, "close": 2.0},
        {"timestamp": "2025-01-01T02:00:00Z", "open": 2.0, "high": 2.2, "low": 1.4, "close": 1.8},
    ]).to_csv(src, index=False)
    pd.DataFrame([
        {"timestamp": "2024-12-31T23:59:00Z", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 10},
        {"timestamp": "2025-01-01T00:00:00Z", "open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 20},
        {"timestamp": "2025-01-01T01:00:00Z", "open": 1.5, "high": 2.5, "low": 1.2, "close": 2.0, "volume": 30},
        {"timestamp": "2025-01-01T02:00:00Z", "open": 2.0, "high": 2.2, "low": 1.4, "close": 1.8, "volume": 10},
    ]).to_csv(m1, index=False)

    out, manifest = run(src, m1)
    assert len(out) == 3
    assert out.iloc[0]["status"] == "PASS"
    assert out.iloc[0]["directional_confirmation"] == "BULLISH"
    assert out.iloc[1]["status"] == "PASS"
    assert out.iloc[1]["directional_confirmation"] == "BULLISH"
    assert out.iloc[2]["status"] == "FAIL"
    assert manifest["tuning"] is False
    assert "M1_TitanFX" in manifest["volume_semantics"]


def test_missing_canonical_volume_context_stays_not_evaluable(tmp_path):
    src = tmp_path / "h1.csv"
    m1 = tmp_path / "m1.csv"
    pd.DataFrame([
        {"timestamp": "2025-01-01T00:00:00Z", "open": 1, "high": 2, "low": 0.5, "close": 1.5},
        {"timestamp": "2025-01-01T01:00:00Z", "open": 1.5, "high": 2.5, "low": 1.2, "close": 2.0},
    ]).to_csv(src, index=False)
    pd.DataFrame([
        {"timestamp": "2025-01-01T00:00:00Z", "open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 20},
    ]).to_csv(m1, index=False)

    out, manifest = run(src, m1)
    assert len(out) == 2
    assert out.iloc[1]["status"] == "NOT_EVALUABLE"
    assert out.iloc[1]["directional_confirmation"] == "UNKNOWN"
    assert manifest["missing_canonical_volume_context_rows"] == 2
    assert manifest["tuning"] is False


def test_evaluator_never_promotes_missing_volume_direction():
    result = evaluate_0021({"close": 2.0, "previous_close": 1.0, "volume_direction": None})
    assert result["status"] == "NOT_EVALUABLE"
    assert result["directional_confirmation"] == "UNKNOWN"
