from compatibility.rule_adapter_contract_v1 import normalize_rule_result


def test_valid_rule_output_is_normalized_without_strategy_logic():
    out = normalize_rule_result({
        "module": "Nison",
        "statement": "Pattern confirms existing context.",
        "direction": "bullish",
        "strength": 0.8,
        "available": True,
        "source_rule_id": "NISON_0031",
        "gate": "pass",
        "conflict": "supports",
        "decision_hint": "bullish",
        "confidence_delta": 0.1,
    })
    assert out.direction == "bullish"
    assert out.gate == "pass"
    assert out.source_rule_id == "NISON_0031"
    assert out.strength == 0.8


def test_invalid_enums_fail_closed_to_safe_values():
    out = normalize_rule_result({
        "direction": "BUY",
        "gate": "execute",
        "conflict": "override",
        "decision_hint": "BUY",
        "strength": 99,
        "confidence_delta": 99,
    })
    assert out.direction == "neutral"
    assert out.gate == "needs_review"
    assert out.conflict == "insufficient"
    assert out.decision_hint == "neutral"
    assert out.strength == 1.0
    assert out.confidence_delta == 1.0


def test_missing_rule_metadata_does_not_invent_source_rule():
    out = normalize_rule_result({})
    assert out.source_rule_id is None
    assert out.available is False
    assert out.gate == "needs_review"
