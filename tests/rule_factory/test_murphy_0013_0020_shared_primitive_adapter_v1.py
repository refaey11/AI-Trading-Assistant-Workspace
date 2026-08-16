from src.rule_factory.murphy_0013_0020_shared_primitive_adapter_v1 import (
    RULE_PRIMITIVE_MAP,
    evaluate_shared_primitives,
)


def test_all_eight_rules_have_shared_primitive_mapping():
    assert set(RULE_PRIMITIVE_MAP) == {"0013", "0014", "0015", "0016", "0017", "0018", "0019", "0020"}


def test_adapter_preserves_blocked_primitive_state():
    result = evaluate_shared_primitives(
        horizontal={"status": "CONFIRMED"},
        geometry={"status": "CONVERGING_EXACT"},
        breakout={"status": "NOT_EVALUABLE"},
        flagpole={"status": "NOT_EVALUABLE"},
    )
    assert result["status"] == "PARTIAL"
    assert "PF-B1" in result["blocked_primitives"]
    assert "PF-F1" in result["blocked_primitives"]
