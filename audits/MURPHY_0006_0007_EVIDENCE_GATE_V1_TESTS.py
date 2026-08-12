from datetime import datetime, timezone

from MURPHY_0006_0007_EVIDENCE_GATE_V1 import evaluate_0006_0007_evidence_gate


def _base(rule_id):
    ts = datetime(2024, 1, 2, tzinfo=timezone.utc)
    return dict(
        rule_id=rule_id,
        line_type="LOW" if rule_id == "MURPHY_0006" else "HIGH",
        direction="UP" if rule_id == "MURPHY_0006" else "DOWN",
        line_availability_timestamp=ts,
        third_touch_timestamp=ts,
        third_touch_price=1.25,
        third_touch_detected=True,
        reaction_detected=True,
        no_break_valid=True,
        confirmation_timestamp=ts,
    )


def test_0006_pass():
    out = evaluate_0006_0007_evidence_gate(**_base("MURPHY_0006"))
    assert out["status"] == "PASS"
    assert out["direction"] == "BULLISH"


def test_0007_pass():
    out = evaluate_0006_0007_evidence_gate(**_base("MURPHY_0007"))
    assert out["status"] == "PASS"
    assert out["direction"] == "BEARISH"


def test_missing_reaction_is_not_evaluable():
    args = _base("MURPHY_0006")
    args["reaction_detected"] = None
    out = evaluate_0006_0007_evidence_gate(**args)
    assert out["status"] == "NOT_EVALUABLE"


def test_missing_no_break_is_not_evaluable():
    args = _base("MURPHY_0007")
    args["no_break_valid"] = None
    out = evaluate_0006_0007_evidence_gate(**args)
    assert out["status"] == "NOT_EVALUABLE"


def test_wrong_geometry_is_not_evaluable():
    args = _base("MURPHY_0006")
    args["line_type"] = "HIGH"
    out = evaluate_0006_0007_evidence_gate(**args)
    assert out["status"] == "NOT_EVALUABLE"


def test_touch_before_line_availability_is_not_evaluable():
    args = _base("MURPHY_0006")
    args["third_touch_timestamp"] = datetime(2024, 1, 1, tzinfo=timezone.utc)
    out = evaluate_0006_0007_evidence_gate(**args)
    assert out["status"] == "NOT_EVALUABLE"
