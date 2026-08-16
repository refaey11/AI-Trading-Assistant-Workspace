from src.rule_factory.murphy_0013_0020_evaluator_shell_v1 import (
    evaluate_ready_batch,
    evaluate_rule_shell,
)


def _ready():
    return {
        "PF-H1": {"status": "CONFIRMED"},
        "PF-G1": {"status": "CONVERGING_EXACT"},
        "PF-B1": {"status": "CONFIRMED"},
        "PF-F1": {"status": "CONFIRMED"},
    }


def test_ready_rules_are_ready_for_semantics_not_production():
    result = evaluate_ready_batch(_ready())
    assert set(result) == {"0013", "0014", "0018", "0019", "0020"}
    assert all(item["status"] == "READY_FOR_RULE_SEMANTICS" for item in result.values())


def test_missing_breakout_policy_blocks_rule_shell():
    primitives = _ready()
    primitives["PF-B1"] = {"status": "NOT_EVALUABLE"}
    result = evaluate_rule_shell("0013", primitives)
    assert result["status"] == "PARTIAL"
    assert result["blocked_primitives"] == ["PF-B1"]
