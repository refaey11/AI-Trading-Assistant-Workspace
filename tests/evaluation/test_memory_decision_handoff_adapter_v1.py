from compatibility.memory_decision_handoff_adapter_v1 import build_memory_handoff


def test_memory_handoff_is_consumable_and_evidence_only():
    result = build_memory_handoff(
        query_as_of="2024-12-31T12:00:00Z",
        murphy_direction="BULLISH",
        historical_context={"status": "WORKING", "candidate_count": 10},
        historical_outcome={"status": "WORKING", "candidate_count": 8},
        similarity={"status": "PRESENT_BUT_NOT_CONSUMED", "candidate_count": 3},
        context_aware_retrieval={"status": "PRESENT_BUT_NOT_CONSUMED", "candidate_count": 0},
        provenance={"test": "memory-handoff"},
    )
    evidence = result["historical_evidence"]
    assert result["status"] == "PASS_SHADOW_ONLY"
    assert evidence["memory_role"] == "EVIDENCE_ONLY"
    assert evidence["consumed_by_decision_boundary"] is True
    assert evidence["final_trade_decision"] is None
    assert evidence["direction"] is None
    assert evidence["governance"]["memory_generated_direction"] is False
    assert evidence["governance"]["2025_used_for_tuning"] is False


def test_memory_handoff_blocks_2025():
    try:
        build_memory_handoff(
            query_as_of="2025-01-01T00:00:00Z",
            murphy_direction="BULLISH",
        )
    except ValueError as exc:
        assert str(exc) == "2025_OOS_LOCKED"
    else:
        raise AssertionError("2025 must remain locked")
