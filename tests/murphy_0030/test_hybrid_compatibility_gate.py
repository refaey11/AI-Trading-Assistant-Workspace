from src.murphy_0030.hybrid_compatibility_gate import evaluate_0030_compatibility_gate


def base_kwargs():
    return {
        "source_contract": True,
        "engine_compatibility": True,
        "box_size_policy_approved": True,
        "availability_no_lookahead": True,
        "deterministic_replay": True,
    }


def test_0030_gate_passes_only_when_all_required_gates_pass():
    assert evaluate_0030_compatibility_gate(**base_kwargs()) == "PASS"


def test_0030_gate_blocks_without_source_contract():
    args = base_kwargs()
    args["source_contract"] = False
    assert evaluate_0030_compatibility_gate(**args) == "BLOCKED"


def test_0030_gate_is_not_evaluable_without_approved_box_size_policy():
    args = base_kwargs()
    args["box_size_policy_approved"] = False
    assert evaluate_0030_compatibility_gate(**args) == "NOT_EVALUABLE"


def test_0030_gate_is_not_evaluable_without_engine_compatibility():
    args = base_kwargs()
    args["engine_compatibility"] = False
    assert evaluate_0030_compatibility_gate(**args) == "NOT_EVALUABLE"


def test_0030_gate_is_not_evaluable_without_availability_no_lookahead():
    args = base_kwargs()
    args["availability_no_lookahead"] = False
    assert evaluate_0030_compatibility_gate(**args) == "NOT_EVALUABLE"


def test_0030_gate_is_not_evaluable_without_deterministic_replay():
    args = base_kwargs()
    args["deterministic_replay"] = False
    assert evaluate_0030_compatibility_gate(**args) == "NOT_EVALUABLE"
