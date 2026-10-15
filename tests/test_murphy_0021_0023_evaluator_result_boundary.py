"""Deterministic tests for the lossless Murphy 0021-0023 evaluator boundary."""

from src.murphy_0021_0023.evaluator_result_boundary import (
    preserve_evaluator_result,
    to_dict,
)


def test_pass_preserves_source_fields():
    src = {
        "rule_id": "MURPHY_0021",
        "status": "PASS",
        "directional_confirmation": "BULLISH",
        "reason": "Requires price UP + volume UP; no extra threshold added.",
    }
    assert to_dict(preserve_evaluator_result(src)) == {
        **src,
        "confirmation_available_timestamp": None,
    }


def test_fail_preserves_source_fields():
    src = {
        "rule_id": "MURPHY_0022",
        "status": "FAIL",
        "directional_confirmation": "NONE",
        "reason": "Requires price UP + volume UP + futures OI UP; no extra threshold added.",
    }
    assert to_dict(preserve_evaluator_result(src)) == {
        **src,
        "confirmation_available_timestamp": None,
    }


def test_not_evaluable_preserves_unknown_direction():
    src = {
        "rule_id": "MURPHY_0023",
        "status": "NOT_EVALUABLE",
        "directional_confirmation": "UNKNOWN",
        "reason": "Missing completed-bar price, volume, or available futures-OI evidence.",
    }
    out = to_dict(preserve_evaluator_result(src))
    assert out["status"] == "NOT_EVALUABLE"
    assert out["directional_confirmation"] == "UNKNOWN"


def test_timestamp_is_preserved_when_present():
    src = {
        "rule_id": "MURPHY_0021",
        "status": "PASS",
        "directional_confirmation": "BULLISH",
        "reason": "test",
        "confirmation_available_timestamp": "2024-01-02T00:00:00Z",
    }
    assert to_dict(preserve_evaluator_result(src))["confirmation_available_timestamp"] == src[
        "confirmation_available_timestamp"
    ]


def test_no_strength_or_conflict_is_synthesized():
    src = {
        "rule_id": "MURPHY_0021",
        "status": "PASS",
        "directional_confirmation": "BULLISH",
        "reason": "test",
    }
    out = to_dict(preserve_evaluator_result(src))
    assert "strength" not in out
    assert "conflict" not in out
    assert "gate" not in out


def test_unsupported_status_is_rejected():
    src = {
        "rule_id": "MURPHY_0021",
        "status": "needs_review",
        "directional_confirmation": "UNKNOWN",
        "reason": "test",
    }
    try:
        preserve_evaluator_result(src)
    except ValueError:
        return
    raise AssertionError("unsupported evaluator status must be rejected")
