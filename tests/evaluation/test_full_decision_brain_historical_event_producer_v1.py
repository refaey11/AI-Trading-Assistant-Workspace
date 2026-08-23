from __future__ import annotations

import pandas as pd

from OOS_2025.full_decision_brain_historical_event_producer_v1 import build_events


TS = pd.Timestamp("2024-12-31T23:00:00Z")


def _frame(row):
    return pd.DataFrame([row])


def test_event_producer_executes_full_path_with_optional_tiz():
    context = _frame({
        "timestamp": TS,
        "mtf_trend_score": 0.7,
        "M5_trend_regime": 0.4,
        "M15_trend_regime": 0.5,
        "M30_trend_regime": 0.3,
        "H1_trend_regime": 0.4,
        "H4_trend_regime": 0.2,
        "D1_trend_regime": 0.1,
        "volume_available": True,
        "M5_volume_regime": 0.2,
        "M15_volume_regime": 0.1,
    })
    murphy = _frame({"timestamp": TS, "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"})
    nison = _frame({"timestamp": TS, "confirmation": "CONFIRMED", "contradiction": False, "source_rule_id": "NISON_0001"})
    risk = _frame({"timestamp": TS, "risk_status": "PASS"})
    execution = _frame({"timestamp": TS, "entry_price": 1.275, "atr": 0.002})

    out = build_events(
        market_context=context, murphy=murphy, nison=nison, risk=risk,
        execution=execution, tiz=None, year=2024, optional_tiz=True,
    )
    assert len(out) == 1
    assert out.loc[0, "status"] == "EXECUTABLE"
    assert out.loc[0, "direction"] == "BUY"
    assert bool(out.loc[0, "tiz_verified"]) is False


def test_event_producer_rejects_nison_contradiction():
    context = _frame({"timestamp": TS, "mtf_trend_score": 0.7, "M5_trend_regime": 0.4, "volume_available": True})
    murphy = _frame({"timestamp": TS, "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"})
    nison = _frame({"timestamp": TS, "confirmation": "CONTRADICTION", "contradiction": True, "source_rule_id": "NISON_0001"})
    risk = _frame({"timestamp": TS, "risk_status": "PASS"})
    execution = _frame({"timestamp": TS, "entry_price": 1.275, "atr": 0.002})

    out = build_events(
        market_context=context, murphy=murphy, nison=nison, risk=risk,
        execution=execution, tiz=None, year=2024, optional_tiz=True,
    )
    assert out.loc[0, "status"] == "NO_TRADE"
    assert out.loc[0, "direction"] == "NO_TRADE"


def test_event_producer_uses_only_requested_year():
    context = _frame({"timestamp": TS, "mtf_trend_score": 0.7, "M5_trend_regime": 0.4, "volume_available": True})
    murphy = _frame({"timestamp": TS, "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"})
    nison = _frame({"timestamp": TS, "confirmation": "CONFIRMED", "contradiction": False, "source_rule_id": "NISON_0001"})
    risk = _frame({"timestamp": TS, "risk_status": "PASS"})
    execution = _frame({"timestamp": TS, "entry_price": 1.275, "atr": 0.002})

    out = build_events(
        market_context=context, murphy=murphy, nison=nison, risk=risk,
        execution=execution, tiz=None, year=2025, optional_tiz=True,
    )
    assert out.empty
