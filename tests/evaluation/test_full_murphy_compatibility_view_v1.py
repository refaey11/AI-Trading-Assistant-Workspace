from OOS_2025.full_decision_brain_assembler_v1 import _full_murphy_compatibility


def _evidence(rows):
    return {"evidence_set": {r["source_rule_id"]: r for r in rows}}


def test_full_murphy_pass_overrides_legacy_fail_compatibility_view():
    result = _full_murphy_compatibility(
        _evidence(
            [
                {"source_rule_id": "MURPHY_0003", "status": "NOT_EVALUABLE", "direction": ""},
                {"source_rule_id": "MURPHY_0021", "status": "FAIL", "direction": "NONE"},
                {"source_rule_id": "MURPHY_0022", "status": "PASS", "directional_confirmation": "BULLISH"},
            ]
        )
    )
    assert result["status"] == "PASS"
    assert result["direction"] == "BULLISH"
    assert result["compatibility_source"] == "FULL_34_RULE_EVIDENCE"


def test_full_murphy_conflicting_pass_directions_do_not_choose_a_side():
    result = _full_murphy_compatibility(
        _evidence(
            [
                {"source_rule_id": "MURPHY_0022", "status": "PASS", "direction": "BULLISH"},
                {"source_rule_id": "MURPHY_0023", "status": "PASS", "direction": "BEARISH"},
            ]
        )
    )
    assert result["status"] == "CONFLICT"
    assert result["direction"] == "NONE"


def test_full_murphy_all_fail_remains_fail():
    result = _full_murphy_compatibility(
        _evidence(
            [
                {"source_rule_id": "MURPHY_0021", "status": "FAIL", "direction": "NONE"},
                {"source_rule_id": "MURPHY_0022", "status": "FAIL", "direction": "NONE"},
            ]
        )
    )
    assert result["status"] == "FAIL"
    assert result["direction"] == "NONE"
