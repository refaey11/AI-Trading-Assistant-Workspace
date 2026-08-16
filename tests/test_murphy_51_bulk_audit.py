from src.rule_factory.murphy_51_bulk_audit import (
    FROZEN_IDS,
    audit_report,
    classify_rule,
)


def test_all_twelve_frozen_rules_are_read_only():
    assert len(FROZEN_IDS) == 12
    for rule_id in FROZEN_IDS:
        assert classify_rule({"rule_id": rule_id, "source_status": "NOT_EVALUABLE"}) == "FROZEN"


def test_ready_for_backtest_is_not_executable_without_all_gates():
    assert classify_rule({"rule_id": "0099", "source_status": "READY_FOR_BACKTEST"}) == "PARTIAL_NEED_SOLUTION"


def test_ready_for_backtest_is_executable_only_when_gates_are_explicitly_passed():
    assert classify_rule({
        "rule_id": "0099",
        "source_status": "READY_FOR_BACKTEST",
        "all_gates_passed": True,
    }) == "EXECUTABLE"


def test_not_evaluable_stays_not_evaluable():
    assert classify_rule({"rule_id": "0099", "source_status": "NOT_EVALUABLE"}) == "NOT_EVALUABLE"


def test_report_excludes_frozen_rules_from_work_queue():
    rules = [
        {"rule_id": "0006", "source_status": "FROZEN"},
        {"rule_id": "0001", "source_status": "PARTIAL", "missing": "operator"},
        {"rule_id": "0002", "source_status": "NOT_EVALUABLE", "missing": "source"},
    ]
    report = audit_report(rules)
    assert report["summary"]["frozen"] == 1
    assert [r["rule_id"] for r in report["work_queue"]] == ["0001", "0002"]


def test_partial_work_queue_names_smallest_missing_piece():
    report = audit_report([
        {"rule_id": "0001", "source_status": "PARTIAL", "missing": "definite_reversal_operator"}
    ])
    row = report["work_queue"][0]
    assert row["classification"] == "PARTIAL_NEED_SOLUTION"
    assert row["missing"] == "definite_reversal_operator"
    assert "smallest missing implementation" in row["next_action"]
