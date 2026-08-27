"""Boundary tests for Memory Evidence Shadow Bridge V1."""
import pytest

from compatibility.memory_evidence_shadow_bridge_v1 import build_shadow_memory_envelope


def test_pre2025_passes_and_is_evidence_only():
    result = build_shadow_memory_envelope(
        query_as_of="2024-12-31T00:00:00Z",
        murphy_direction="LONG",
        memory_evidence={
            "historical_context": {"status": "PASS", "candidate_count": 1},
            "historical_outcome": {"status": "PASS", "candidate_count": 1},
            "similarity": {"status": "PASS", "candidate_count": 2},
            "context_aware_retrieval": {"status": "PASS", "candidate_count": 3},
        },
    )
    assert result["status"] == "PASS_SHADOW_ONLY"
    assert result["governance"]["memory_role"] == "EVIDENCE_ONLY"
    assert result["governance"]["memory_generated_direction"] is False
    assert result["governance"]["2025_used_for_tuning"] is False
    assert result["summary"]["total_candidate_count"] == 7


def test_2025_is_locked():
    with pytest.raises(ValueError, match="2025_OOS_LOCKED"):
        build_shadow_memory_envelope(
            query_as_of="2025-01-01T00:00:00Z",
            murphy_direction=None,
        )


def test_future_data_is_forbidden():
    with pytest.raises(ValueError, match="2025_OOS_LOCKED"):
        build_shadow_memory_envelope(
            query_as_of="2026-01-01T00:00:00Z",
            murphy_direction=None,
        )
