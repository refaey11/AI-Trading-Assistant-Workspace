"""Regression test: Similarity must remain evidence-only at the Decision Brain boundary."""
from __future__ import annotations

from copy import deepcopy

import decision_brain
from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance


def _row() -> dict:
    return {
        "mtf_trend_score": 0.0,
        "M5_trend_regime": 0.0,
        "M15_trend_regime": 0.0,
        "M30_trend_regime": 0.0,
        "H1_trend_regime": 0.0,
        "H4_trend_regime": 0.0,
        "D1_trend_regime": 0.0,
        "volume_available": False,
    }


def test_similarity_cannot_change_direction_at_governed_boundary():
    row = _row()

    baseline = assess_with_governance(
        decision_brain,
        row=row,
        query_as_of="2024-12-31T00:00:00Z",
        mode="development",
        historical_evidence={},
    )

    poisoned_similarity = {
        "retrieval_status": "PASS",
        "candidate_count": 20,
        "predicted_return": 0.50,
        "top_k_returned": [0.50] * 20,
    }
    governed = assess_with_governance(
        decision_brain,
        row=deepcopy(row),
        query_as_of="2024-12-31T00:00:00Z",
        mode="development",
        historical_evidence={"similarity": poisoned_similarity},
    )

    assert baseline["status"] == "PASS"
    assert governed["status"] == "PASS"
    assert baseline["assessment"]["directional_bias"] == governed["assessment"]["directional_bias"]
    assert baseline["assessment"]["confidence"] == governed["assessment"]["confidence"]
    assert not any(
        item["module"] == "HistoricalMemory"
        for item in governed["assessment"]["evidence"]
    )
    assert governed["governance"]["similarity_generated_direction"] is False
    assert governed["governance"]["predicted_return_used_as_direction"] is False


def test_2025_and_future_are_locked_at_boundary():
    for timestamp in ("2025-01-01T00:00:00Z", "2026-01-01T00:00:00Z"):
        result = assess_with_governance(
            decision_brain,
            row=_row(),
            query_as_of=timestamp,
            mode="development",
        )
        assert result["status"] == "NOT_EVALUABLE"
        assert result["reason"] == "2025_OOS_LOCKED"
