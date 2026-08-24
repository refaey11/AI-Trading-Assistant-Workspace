from __future__ import annotations


def apply_nison_availability_policy(event: dict) -> dict:
    out = dict(event)
    status = out.get("status")
    direction = out.get("direction")
    if status == "NOT_EVALUABLE":
        out["nison_confirmation_contribution"] = "ABSENT"
        out["nison_contradiction_contribution"] = False
        out["brain_blocker"] = False
    elif status == "PASS" and direction in {"BULLISH", "BEARISH"}:
        out["nison_confirmation_contribution"] = direction
        out["nison_contradiction_contribution"] = False
        out["brain_blocker"] = False
    elif status == "FAIL" and direction in {"BULLISH", "BEARISH"}:
        out["nison_confirmation_contribution"] = "ABSENT"
        out["nison_contradiction_contribution"] = True
        out["brain_blocker"] = False
    else:
        out["nison_confirmation_contribution"] = "ABSENT"
        out["nison_contradiction_contribution"] = False
        out["brain_blocker"] = False
    return out


def test_not_evaluable_is_not_global_blocker():
    out = apply_nison_availability_policy({"status": "NOT_EVALUABLE", "direction": None})
    assert out["nison_confirmation_contribution"] == "ABSENT"
    assert out["nison_contradiction_contribution"] is False
    assert out["brain_blocker"] is False


def test_directional_pass_contributes_confirmation():
    out = apply_nison_availability_policy({"status": "PASS", "direction": "BULLISH"})
    assert out["nison_confirmation_contribution"] == "BULLISH"
    assert out["brain_blocker"] is False


def test_directional_fail_contributes_contradiction_only():
    out = apply_nison_availability_policy({"status": "FAIL", "direction": "BEARISH"})
    assert out["nison_contradiction_contribution"] is True
    assert out["nison_confirmation_contribution"] == "ABSENT"
    assert out["brain_blocker"] is False
