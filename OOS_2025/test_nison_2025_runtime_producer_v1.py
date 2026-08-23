from __future__ import annotations

from nison_2025_runtime_producer_v1 import run_timestamp


def test_all_44_rules_emit_one_result_for_timestamp():
    rows = run_timestamp(
        "2025-01-02T12:00:00Z",
        {
            "NISON_0001": {
                "candles": [
                    {"open": 1.10, "high": 1.11, "low": 1.09, "close": 1.095},
                    {"open": 1.094, "high": 1.12, "low": 1.093, "close": 1.115},
                ],
                "context": {
                    "trend": "Downtrend",
                    "location": "NEAR_SUPPORT",
                },
                "confirmation": {"strong_bullish_candle": True},
            }
        },
    )
    assert len(rows) == 44
    assert {r["rule_id"] for r in rows} == {f"NISON_{i:04d}" for i in range(1, 45)}
    assert rows[0]["status"] == "PASS"
    assert rows[0]["direction"] == "BULLISH"
    assert rows[0]["conflict"] == "supports"
    assert rows[1]["status"] in {"FAIL", "NOT_EVALUABLE"}


def test_missing_source_facts_are_not_evaluable_not_fabricated():
    rows = run_timestamp("2025-01-02T12:00:00Z", {})
    assert len(rows) == 44
    assert all(r["status"] == "NOT_EVALUABLE" for r in rows)
    assert all(r["available"] is False for r in rows)


def test_candidate_direction_is_confirmation_label_only():
    rows = run_timestamp(
        "2025-01-02T12:00:00Z",
        {
            "NISON_0002": {
                "candles": [
                    {"open": 1.10, "high": 1.11, "low": 1.09, "close": 1.105},
                    {"open": 1.106, "high": 1.107, "low": 1.08, "close": 1.085},
                ],
                "context": {"trend": "Uptrend"},
                "confirmation": {"strong_bearish_candle": True},
            }
        },
    )
    out = next(r for r in rows if r["rule_id"] == "NISON_0002")
    assert out["status"] == "PASS"
    assert out["direction"] == "BEARISH"
