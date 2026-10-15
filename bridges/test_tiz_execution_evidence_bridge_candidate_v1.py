import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridges.tiz_execution_evidence_bridge_candidate_v1 import enrich_execution_record


def test_bridge_preserves_record_and_attaches_matching_evidence():
    record = {
        "trade_id": "T-001",
        "loss_exit_plan": "invalidation",
        "actual_exit_reason": "invalidation",
        "profit_taking_plan": "planned_target",
        "actual_profit_action": "planned_target",
        "loss_event_occurred": True,
        "profit_taking_event_occurred": False,
    }
    enriched = enrich_execution_record(record, timestamp="2026-08-19T00:00:00Z")
    assert enriched["trade_id"] == "T-001"
    assert enriched["tiz_execution_evidence"]["exit_reason_matches_plan"]["value"] is True
    assert enriched["tiz_execution_evidence"]["profit_action_matches_plan"]["value"] is True
    assert enriched["tiz_execution_evidence"]["direction"] == "NEUTRAL"


def test_bridge_does_not_backfill_missing_plan():
    record = {"trade_id": "T-002", "actual_exit_reason": "manual"}
    enriched = enrich_execution_record(record)
    match = enriched["tiz_execution_evidence"]["exit_reason_matches_plan"]
    assert match["value"] is None
    assert match["availability"] is False
