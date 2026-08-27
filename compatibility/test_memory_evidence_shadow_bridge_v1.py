"""Boundary tests for Memory Evidence Shadow Bridge V1.

These tests are development-only: 2016-2024 are accepted, 2025+ is rejected,
and memory evidence cannot generate direction or a final trade decision.
"""
import pytest

from compatibility.memory_evidence_shadow_bridge_v1 import build_shadow_memory_envelope
from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance


class _StubBrain:
    def assess(self, row, similarity=None):
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Assessment:
            directional_bias: str = "neutral"
            confidence: float = 0.0
        assert similarity is None
        return Assessment()


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


def test_downstream_handoff_consumes_memory_as_evidence_only():
    memory = build_shadow_memory_envelope(
        query_as_of="2024-12-31T00:00:00Z",
        murphy_direction="LONG",
        memory_evidence={
            "historical_context": {"status": "PASS", "candidate_count": 12},
            "historical_outcome": {"status": "PASS", "candidate_count": 8},
            "similarity": {"status": "PASS", "candidate_count": 0},
            "context_aware_retrieval": {"status": "PASS", "candidate_count": 0},
        },
    )
    result = assess_with_governance(
        _StubBrain(),
        row={"timestamp": "2024-12-31T00:00:00Z"},
        query_as_of="2024-12-31T00:00:00Z",
        mode="development",
        historical_evidence=memory,
        provenance={"test": "memory_downstream_consumption"},
    )
    assert result["status"] == "PASS"
    assert result["historical_evidence"]["candidate_count"] is None
    assert result["historical_evidence"]["predicted_return_used_as_direction"] is False
    assert result["governance"]["predicted_return_used_as_direction"] is False


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
