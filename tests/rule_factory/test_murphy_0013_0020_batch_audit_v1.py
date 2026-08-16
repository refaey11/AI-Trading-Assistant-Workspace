from src.rule_factory.murphy_0013_0020_batch_audit_v1 import audit_rules_0013_0020


def test_batch_audit_returns_all_eight_rules():
    results = audit_rules_0013_0020({
        "PF-H1": {"status": "CONFIRMED"},
        "PF-G1": {"status": "CONVERGING_EXACT"},
        "PF-B1": {"status": "CONFIRMED"},
        "PF-F1": {"status": "NOT_EVALUABLE"},
    })
    assert set(results) == {"0013", "0014", "0015", "0016", "0017", "0018", "0019", "0020"}


def test_batch_audit_marks_flagpole_dependents_partial():
    results = audit_rules_0013_0020({
        "PF-H1": {"status": "CONFIRMED"},
        "PF-G1": {"status": "CONVERGING_EXACT"},
        "PF-B1": {"status": "CONFIRMED"},
        "PF-F1": {"status": "NOT_EVALUABLE"},
    })
    assert results["0015"]["status"] == "PARTIAL"
    assert results["0016"]["status"] == "PARTIAL"
    assert results["0017"]["status"] == "PARTIAL"
    assert results["0018"]["status"] == "READY_FOR_RULE_EVALUATION"
    assert results["0019"]["status"] == "READY_FOR_RULE_EVALUATION"
    assert results["0020"]["status"] == "READY_FOR_RULE_EVALUATION"
