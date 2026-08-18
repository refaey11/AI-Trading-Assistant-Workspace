"""Bridge an execution record into the TIZ evidence envelope.

This is deliberately a candidate integration boundary. It only consumes fields
explicitly present in the execution record; it never derives missing psychology
from mechanical outcomes.
"""

from 03_TIZ.tiz_execution_evidence_producer_candidate_v1 import build_evidence


def enrich_execution_record(record, *, timestamp=None,
                            provenance="execution_record_producer_v1"):
    """Return a copy of an execution record with explicit TIZ evidence.

    The caller must supply the pre-entry plan fields and post-exit actual fields.
    Missing values remain unavailable and therefore cannot become a TIZ PASS.
    """
    evidence = build_evidence(
        loss_exit_plan=record.get("loss_exit_plan"),
        actual_exit_reason=record.get("actual_exit_reason"),
        profit_taking_plan=record.get("profit_taking_plan"),
        actual_profit_action=record.get("actual_profit_action"),
        loss_event_occurred=record.get("loss_event_occurred", False),
        profit_taking_event_occurred=record.get("profit_taking_event_occurred", False),
        timestamp=timestamp,
        provenance=provenance,
    )
    enriched = dict(record)
    enriched["tiz_execution_evidence"] = evidence
    return enriched
