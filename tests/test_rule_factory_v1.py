from src.rule_factory.rule_factory_v1 import RuleSpec, RuleStatus, evaluate_rule


def _spec(**overrides):
    base = dict(
        rule_id="TEST",
        canonical_evaluator=lambda ctx: {"status": "PASS"},
        tests=lambda ctx: True,
        historical_qa=lambda ctx: True,
        lookahead_gate=lambda ctx: True,
        oos_gate=lambda ctx: True,
        source_status="",
    )
    base.update(overrides)
    return RuleSpec(**base)


def test_canonical_block_does_not_stop_other_rules():
    result = evaluate_rule(_spec(canonical_evaluator=lambda ctx: {"status": "NOT_EVALUABLE"}), {})
    assert result["status"] == RuleStatus.BLOCKED.value


def test_canonical_failure_is_not_rescued():
    result = evaluate_rule(_spec(canonical_evaluator=lambda ctx: {"status": "FAIL"}), {})
    assert result["status"] == RuleStatus.FAIL.value


def test_all_gates_pass_to_frozen():
    result = evaluate_rule(_spec(), {})
    assert result["status"] == RuleStatus.FROZEN.value


def test_ready_for_backtest_is_candidate_after_gates():
    result = evaluate_rule(_spec(source_status="READY_FOR_BACKTEST"), {})
    assert result["status"] == RuleStatus.CANDIDATE.value


def test_ready_for_backtest_does_not_bypass_failed_tests():
    result = evaluate_rule(_spec(source_status="READY_FOR_BACKTEST", tests=lambda ctx: False), {})
    assert result["status"] == RuleStatus.FAIL.value


def test_ready_for_backtest_does_not_bypass_historical_qa():
    result = evaluate_rule(_spec(source_status="READY_FOR_BACKTEST", historical_qa=lambda ctx: False), {})
    assert result["status"] == RuleStatus.CANDIDATE.value


def test_ready_for_backtest_does_not_bypass_lookahead():
    result = evaluate_rule(_spec(source_status="READY_FOR_BACKTEST", lookahead_gate=lambda ctx: False), {})
    assert result["status"] == RuleStatus.BLOCKED.value


def test_ready_for_backtest_does_not_bypass_oos():
    result = evaluate_rule(_spec(source_status="READY_FOR_BACKTEST", oos_gate=lambda ctx: False), {})
    assert result["status"] == RuleStatus.BLOCKED.value


def test_failed_lookahead_blocks_freeze():
    result = evaluate_rule(_spec(lookahead_gate=lambda ctx: False), {})
    assert result["status"] == RuleStatus.BLOCKED.value


def test_oos_failure_blocks_freeze():
    result = evaluate_rule(_spec(oos_gate=lambda ctx: False), {})
    assert result["status"] == RuleStatus.BLOCKED.value
