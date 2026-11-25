from __future__ import annotations

import pandas as pd
import pytest

from OOS_2025.nison_2025_source_adapter_v1 import build_payload_rows, iter_payload_rows


def test_maps_2025_ohlc_and_preserves_only_explicit_context():
    bars = pd.DataFrame([
        {"timestamp": "2025-01-02T00:00:00Z", "open": 1.10, "high": 1.11, "low": 1.09, "close": 1.105},
        {"timestamp": "2025-01-02T01:00:00Z", "open": 1.105, "high": 1.115, "low": 1.10, "close": 1.112},
        {"timestamp": "2025-01-02T02:00:00Z", "open": 1.112, "high": 1.12, "low": 1.108, "close": 1.118},
    ])
    context = pd.DataFrame([
        {"timestamp": "2025-01-02T02:00:00Z", "trend": "Downtrend", "location": "NEAR_SUPPORT"}
    ])

    rows = build_payload_rows(bars, context)
    assert len(rows) == 3 * 44
    last = next(r for r in rows if r["timestamp"].startswith("2025-01-02T02:00:00") and r["rule_id"] == "NISON_0001")
    assert last["payload"]["candles"][-1]["close"] == pytest.approx(1.118)
    assert last["payload"]["context"]["trend"] == "Downtrend"
    assert last["payload"]["context"]["location"] == "NEAR_SUPPORT"
    assert "trend" not in last["payload"]
    assert "location" not in last["payload"]
    assert "confirmation" not in last["payload"]


def test_non_2025_rows_are_excluded():
    bars = pd.DataFrame([
        {"timestamp": "2024-12-31T23:00:00Z", "open": 1.1, "high": 1.2, "low": 1.0, "close": 1.1},
        {"timestamp": "2025-01-01T00:00:00Z", "open": 1.1, "high": 1.2, "low": 1.0, "close": 1.1},
    ])
    assert len(build_payload_rows(bars)) == 44


def test_invalid_rule_id_is_rejected_not_normalized():
    with pytest.raises(ValueError):
        list(iter_payload_rows([{"timestamp": "2025-01-02T00:00:00Z", "rule_id": "NISON_9999", "payload": {}}]))


def test_normalizes_trend_and_preserves_exact_context_and_candle_facts():
    bars = pd.DataFrame([
        {"timestamp": "2025-01-01T00:00:00Z", "open": 10.0, "high": 11.0, "low": 9.5, "close": 10.5},
        {"timestamp": "2025-01-01T01:00:00Z", "open": 10.4, "high": 11.2, "low": 10.4, "close": 11.0},
    ])
    context = pd.DataFrame([
        {
            "timestamp": "2025-01-01T00:00:00Z",
            "trend": "BULL_TREND",
            "location": "SUPPORT",
            "volume_high": True,
            "candlestick": {"bull_engulf": True},
        },
        {
            "timestamp": "2025-01-01T01:00:00Z",
            "trend": "BEAR_TREND",
            "location": "RESISTANCE",
            "formation_confirmed": True,
            "previous_session": {"high": 11.3, "low": 10.0},
            "current_session": {"high": 11.1, "low": 10.2},
        },
    ])

    rows = build_payload_rows(bars, context, evaluation_year=2025)
    second = next(
        r for r in rows
        if r["timestamp"].startswith("2025-01-01T01:00:00")
        and r["rule_id"] == "NISON_0038"
    )
    assert second["payload"]["context"]["trend"] == "Downtrend"
    assert second["payload"]["context"]["location"] == "RESISTANCE"
    assert second["payload"]["context"]["formation_confirmed"] is True
    assert second["payload"]["context"]["previous_session"]["high"] == 11.3
    assert second["payload"]["candles"][-1]["color"] == "bullish"
    assert second["payload"]["candles"][-1]["open_inside_previous_body"] is True


def test_transition_trend_is_not_mapped_to_direction():
    bars = pd.DataFrame([
        {"timestamp": "2025-01-01T00:00:00Z", "open": 10.0, "high": 10.5, "low": 9.5, "close": 10.0}
    ])
    context = pd.DataFrame([
        {"timestamp": "2025-01-01T00:00:00Z", "trend": "TRANSITION"}
    ])

    row = build_payload_rows(bars, context, evaluation_year=2025)[0]
    assert row["payload"]["context"]["trend"] == "TRANSITION"


def test_rule_0031_exposes_five_candles_when_history_is_available():
    bars = pd.DataFrame([
        {
            "timestamp": f"2025-01-01T0{i}:00:00Z",
            "open": 10.0 + i,
            "high": 10.5 + i,
            "low": 9.5 + i,
            "close": 10.2 + i,
        }
        for i in range(6)
    ])

    rows = build_payload_rows(bars, evaluation_year=2025)
    latest = next(
        r for r in rows
        if r["timestamp"].startswith("2025-01-01T05:00:00")
        and r["rule_id"] == "NISON_0031"
    )
    assert len(latest["payload"]["candles"]) == 5
    assert latest["payload"]["candles"][0]["open"] == 11.0
    assert latest["payload"]["candles"][-1]["open"] == 15.0

