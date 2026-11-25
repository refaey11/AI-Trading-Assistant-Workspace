"""Regression tests for the MT5 display bridge response contract.

These tests cover display-only response fields; they do not enable or test order
execution, profitability, or live trading readiness.
"""
from tools.mt5_decision_brain_bridge import assessment_payload


def test_assessment_echoes_numeric_timeframe_regimes_and_keeps_orders_disabled():
    row = {
        "mtf_trend_score": 0.25,
        "M5_trend_regime": 1,
        "M15_trend_regime": 0.25,
        "M30_trend_regime": 0,
        "H1_trend_regime": -0.25,
        "H4_trend_regime": -1,
        "D1_trend_regime": 1,
        "volume_available": False,
    }

    payload = assessment_payload(row)

    for timeframe in ("M5", "M15", "M30", "H1", "H4", "D1"):
        assert payload[f"{timeframe}_trend_regime"] == float(row[f"{timeframe}_trend_regime"])
    assert payload["order_execution"] == "DISABLED"
    assert payload["official_profitability_claim_allowed"] is False


def test_boolean_is_not_accepted_as_numeric_timeframe_regime():
    payload = assessment_payload({
        "M5_trend_regime": True,
        "volume_available": False,
    })

    assert "M5_trend_regime" not in payload
    assert payload["order_execution"] == "DISABLED"
    assert payload["official_profitability_claim_allowed"] is False


def test_missing_timeframe_fields_remain_missing_not_fabricated():
    payload = assessment_payload({"volume_available": False})

    assert all(
        f"{timeframe}_trend_regime" not in payload
        for timeframe in ("M5", "M15", "M30", "H1", "H4", "D1")
    )
    assert payload["order_execution"] == "DISABLED"
