from OOS_2025.full_decision_brain_historical_event_producer_v1 import _decision_ready_tiz


def test_optional_tiz_missing_evidence_does_not_hard_block_gate():
    result = _decision_ready_tiz({"process_gate": "NOT_EVALUABLE"}, optional_tiz=True)
    assert result["process_gate"] == "READY"
    assert result["tiz_verified"] is False


def test_non_optional_tiz_missing_evidence_remains_not_evaluable():
    result = _decision_ready_tiz({"process_gate": "NOT_EVALUABLE"}, optional_tiz=False)
    assert result["process_gate"] == "NOT_EVALUABLE"
