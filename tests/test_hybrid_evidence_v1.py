from src.engineering_evidence.hybrid_evidence_v1 import evaluate_hybrid


def test_hard_gate_dominates_high_soft_score():
    result = evaluate_hybrid(False, 0.99, 0.99)
    assert result["status"] == "NOT_EVALUABLE"
    assert result["evidence_only"] is True
    assert result["engineering"].grade == "HIGH"


def test_canonical_pass_preserves_evidence_only_boundary():
    result = evaluate_hybrid(True, 0.90, 0.80)
    assert result["status"] == "CANONICAL_PASS"
    assert result["evidence_only"] is True


def test_low_engineering_evidence_does_not_create_failure():
    result = evaluate_hybrid(True, 0.10, 0.20)
    assert result["status"] == "CANONICAL_PASS"
    assert result["engineering"].grade == "LOW"
