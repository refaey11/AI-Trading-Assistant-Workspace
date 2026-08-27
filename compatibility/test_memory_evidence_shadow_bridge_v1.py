"""Boundary tests for Memory Evidence Shadow Bridge V1.

These tests are development-only: 2016-2024 are accepted, 2025+ is rejected,
and memory evidence cannot generate direction or a final trade decision.
"""
from compatibility.memory_evidence_shadow_bridge_v1 import build_shadow_memory_packet


def test_pre2025_passes_and_is_evidence_only():
    result = build_shadow_memory_packet(
        query_as_of="2024-12-31T00:00:00Z",
        historical_context={"status": "PASS", "record": {"timestamp": "2024-12-31T00:00:00Z"}},
        historical_outcome={"status": "PASS", "evidence": {"timestamp": "2024-12-30T00:00:00Z"}},
        similarity={"status": "PASS", "result": {"current_context": {"timestamp": "2024-12-31T00:00:00Z"}}},
        retrieval={"status": "PASS", "candidate_count": 3, "top_k_returned": 3},
        downstream_consumed=False,
    )
    assert result["status"] == "PASS"
    assert result["memory_role"] == "EVIDENCE_ONLY"
    assert result["direction_generated"] is False
    assert result["final_trade_decision_generated"] is False
    assert result["2025_used_for_tuning"] is False


def test_2025_is_locked():
    result = build_shadow_memory_packet(
        query_as_of="2025-01-01T00:00:00Z",
        historical_context={},
        historical_outcome={},
        similarity={},
        retrieval={},
        downstream_consumed=False,
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"


def test_future_data_is_forbidden():
    result = build_shadow_memory_packet(
        query_as_of="2026-01-01T00:00:00Z",
        historical_context={},
        historical_outcome={},
        similarity={},
        retrieval={},
        downstream_consumed=False,
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "FUTURE_DATA_FORBIDDEN"
