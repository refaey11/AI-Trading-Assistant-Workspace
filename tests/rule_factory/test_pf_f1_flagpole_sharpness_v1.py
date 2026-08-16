from src.rule_factory.pf_f1_flagpole_sharpness_v1 import (
    FlagpoleSharpnessPolicy,
    evaluate_pf_f1,
)


def test_missing_policy_is_not_evaluable():
    assert evaluate_pf_f1(2.0, None)["status"] == "NOT_EVALUABLE"


def test_approved_policy_can_confirm():
    policy = FlagpoleSharpnessPolicy(2.0, "NORMALIZED_MOVE")
    assert evaluate_pf_f1(2.5, policy)["status"] == "CONFIRMED"


def test_approved_policy_can_reject():
    policy = FlagpoleSharpnessPolicy(2.0, "NORMALIZED_MOVE")
    assert evaluate_pf_f1(1.5, policy)["status"] == "NOT_CONFIRMED"


def test_no_default_threshold_is_invented():
    policy = FlagpoleSharpnessPolicy(0, "NORMALIZED_MOVE")
    result = evaluate_pf_f1(100, policy)
    assert result["status"] == "NOT_EVALUABLE"
