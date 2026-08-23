import pandas as pd

from OOS_2025.nison_2025_source_adapter_v1 import build_payload_rows


def test_adapter_normalizes_trend_and_preserves_exact_candle_facts():
    bars = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "open": 10.0, "high": 11.0, "low": 9.5, "close": 10.5},
            {"timestamp": "2025-01-01T01:00:00Z", "open": 10.4, "high": 11.2, "low": 10.4, "close": 11.0},
        ]
    )
    context = pd.DataFrame(
        [
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
        ]
    )

    rows = build_payload_rows(bars, context)
    second = next(r for r in rows if r["timestamp"].startswith("2025-01-01T01:00:00") and r["rule_id"] == "NISON_0038")
    assert second["payload"]["context"]["trend"] == "Downtrend"
    assert second["payload"]["context"]["formation_confirmed"] is True
    assert second["payload"]["context"]["previous_session"]["high"] == 11.3
    assert second["payload"]["candles"][-1]["color"] == "bullish"
    assert second["payload"]["candles"][-1]["open_inside_previous_body"] is True


def test_transition_is_not_mapped_to_direction():
    bars = pd.DataFrame(
        [{"timestamp": "2025-01-01T00:00:00Z", "open": 10.0, "high": 10.5, "low": 9.5, "close": 10.0}]
    )
    context = pd.DataFrame([{"timestamp": "2025-01-01T00:00:00Z", "trend": "TRANSITION"}])
    row = build_payload_rows(bars, context)[0]
    assert row["payload"]["context"]["trend"] == "TRANSITION"
