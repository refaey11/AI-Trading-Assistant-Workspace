from __future__ import annotations

from RUNTIME.DECISION_RUNTIME_V1.decision_runtime import MarketSnapshot, build_decision_event


def _snapshot() -> MarketSnapshot:
    return MarketSnapshot(timestamp="2025-01-02T10:00:00Z", symbol="GBPUSD", values={"close": 1.25})


def _base_brain(direction="bullish"):
    return {"directional_bias": direction, "confidence": 0.8}


def _base_murphy():
    return {"status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0001"}


def _base_nison():
    return {"confirmation": "CONFIRMED", "contradiction": False, "source_rule_id": "NISON_0001"}


def _base_tiz():
    return {"process_gate": "PASS"}


def _base_risk():
    return {"risk_pass": True}


def test_buy_event_is_approved():
    event = build_decision_event(
        snapshot=_snapshot(),
        mode="BACKTEST",
        brain_assessment=_base_brain(),
        murphy_evidence=_base_murphy(),
        nison_evidence=_base_nison(),
        tiz_evidence=_base_tiz(),
        risk_evidence=_base_risk(),
        execution_plan={"status": "EXECUTABLE", "entry_price": 1.25, "stop_loss": 1.24, "take_profit": 1.27},
    )
    assert event.direction == "BUY"
    assert event.status == "APPROVED"
    assert event.mode == "BACKTEST"
    assert event.provenance["oos_tuning"] is False


def test_risk_failure_is_fail_closed():
    event = build_decision_event(
        snapshot=_snapshot(),
        mode="BACKTEST",
        brain_assessment=_base_brain(),
        murphy_evidence=_base_murphy(),
        nison_evidence=_base_nison(),
        tiz_evidence=_base_tiz(),
        risk_evidence={"risk_pass": False},
    )
    assert event.direction == "NO_TRADE"
    assert event.status == "NO_TRADE"
    assert "RISK_GATE_FAIL" in event.reason


def test_nison_contradiction_blocks_trade():
    nison = _base_nison() | {"contradiction": True}
    event = build_decision_event(
        snapshot=_snapshot(),
        mode="PAPER",
        brain_assessment=_base_brain(),
        murphy_evidence=_base_murphy(),
        nison_evidence=nison,
        tiz_evidence=_base_tiz(),
        risk_evidence=_base_risk(),
    )
    assert event.direction == "NO_TRADE"
    assert "NISON_CONTRADICTION" in event.reason


def test_invalid_mode_rejected():
    try:
        build_decision_event(
            snapshot=_snapshot(),
            mode="SOMETHING_ELSE",
            brain_assessment=_base_brain(),
            murphy_evidence=_base_murphy(),
            nison_evidence=_base_nison(),
            tiz_evidence=_base_tiz(),
            risk_evidence=_base_risk(),
        )
    except ValueError:
        return
    raise AssertionError("invalid mode must be rejected")
