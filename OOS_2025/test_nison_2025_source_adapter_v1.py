from __future__ import annotations

import pandas as pd
import pytest

from nison_2025_source_adapter_v1 import build_payload_rows, iter_payload_rows


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
