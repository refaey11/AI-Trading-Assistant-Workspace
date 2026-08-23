from __future__ import annotations

import pandas as pd

from nison_2025_source_adapter_v1 import build_payload_rows


def test_context_and_confirmation_are_nested_at_runtime_boundary():
    bars = pd.DataFrame([
        {"timestamp": "2025-01-02T00:00:00Z", "open": 1.10, "high": 1.11, "low": 1.09, "close": 1.105},
        {"timestamp": "2025-01-02T01:00:00Z", "open": 1.105, "high": 1.115, "low": 1.10, "close": 1.112},
    ])
    context = pd.DataFrame([
        {
            "timestamp": "2025-01-02T01:00:00Z",
            "trend": "Downtrend",
            "location": "NEAR_SUPPORT",
            "volume_high": True,
            "confirmation": {"strong_bullish_candle": True},
        }
    ])

    rows = build_payload_rows(bars, context)
    payload = next(r["payload"] for r in rows if r["rule_id"] == "NISON_0001" and r["timestamp"].startswith("2025-01-02T01:00:00"))

    assert payload["context"]["trend"] == "Downtrend"
    assert payload["context"]["location"] == "NEAR_SUPPORT"
    assert payload["context"]["volume_high"] is True
    assert payload["confirmation"]["strong_bullish_candle"] is True
    assert "trend" not in payload
    assert "location" not in payload


def test_context_is_not_invented_when_absent():
    bars = pd.DataFrame([
        {"timestamp": "2025-01-02T00:00:00Z", "open": 1.10, "high": 1.11, "low": 1.09, "close": 1.105},
    ])
    payload = build_payload_rows(bars)[0]["payload"]
    assert "context" not in payload
    assert "confirmation" not in payload
