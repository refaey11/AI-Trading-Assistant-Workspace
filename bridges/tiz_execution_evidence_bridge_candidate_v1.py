"""Bridge an execution record into the TIZ evidence envelope.

Candidate integration boundary. It only consumes fields explicitly present in
the execution record and never derives missing psychology from mechanics.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "03_TIZ"))
from tiz_execution_evidence_producer_candidate_v1 import build_evidence


def enrich_execution_record(record, *, timestamp=None,
                            provenance="execution_record_producer_v1"):
    """Return a copy with explicit TIZ execution evidence attached."""
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
