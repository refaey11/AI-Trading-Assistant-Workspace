from datetime import datetime, timezone

from src.murphy_0006_0007.decision_brain_adapter import confirmation_to_decision_evidence
from src.murphy_0006_0007.murphy_event_operator import Confirmation, PivotEvent


def _confirmation(rule_id: str) -> Confirmation:
    t1 = datetime(2020, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2020, 2, 1, tzinfo=timezone.utc)
    return Confirmation(
        rule_id=rule_id,
        third_touch=PivotEvent(t1, t1, "LOW" if rule_id == "MURPHY_0006" else "HIGH", 1.2),
        reaction=PivotEvent(t2, t2, "HIGH" if rule_id == "MURPHY_0006" else "LOW", 1.3 if rule_id == "MURPHY_0006" else 1.1),
        confirmation_available_at=t2,
    )


def test_0006_maps_to_bullish_murphy_context_without_creating_trade():
    out = confirmation_to_decision_evidence(_confirmation("MURPHY_0006"))
    assert out["module"] == "murphy_context"
    assert out["source_rule_id"] == "MURPHY_0006"
    assert out["direction"] == "bullish"
    assert out["available"] is True
    assert out["gate"] == "pass"
    assert 0.0 <= out["strength"] <= 1.0
    assert out["confidence_delta"] == 0.0


def test_0007_maps_to_bearish_murphy_context_without_creating_trade():
    out = confirmation_to_decision_evidence(_confirmation("MURPHY_0007"))
    assert out["module"] == "murphy_context"
    assert out["source_rule_id"] == "MURPHY_0007"
    assert out["direction"] == "bearish"
    assert out["available"] is True
    assert out["gate"] == "pass"
    assert 0.0 <= out["strength"] <= 1.0
    assert out["confidence_delta"] == 0.0


def test_unavailable_evidence_is_neutral_and_insufficient():
    out = confirmation_to_decision_evidence(None)
    assert out["direction"] == "neutral"
    assert out["available"] is False
    assert out["gate"] == "needs_review"
    assert out["conflict"] == "insufficient"
    assert out["decision_hint"] == "neutral"
