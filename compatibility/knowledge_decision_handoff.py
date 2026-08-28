"""Narrow compatibility handoff between Knowledge Alignment and Decision Brain V1.

This module does not create BUY/SELL decisions. It preserves hard blocks and
contradictions while packaging all upstream evidence for the existing
Decision Brain assessment boundary. Evidence remains attributed and cannot
become an automatic trading command here.
"""
from copy import deepcopy

HARD_BLOCK_STATES = {"PROCESS_BLOCKED"}
CONTRADICTION_STATES = {"NISON_CONTRADICTION", "NEEDS_REVIEW"}


def _status(x):
    return str(x or "").strip().upper()


def build_handoff(market_row, alignment_output, similarity=None):
    row = deepcopy(market_row or {})
    a = deepcopy(alignment_output or {})
    alignment_state = _status(a.get("alignment_state"))
    contradiction_gate = _status(a.get("contradiction_gate"))
    process_gate = _status(a.get("process_gate"))

    hard_block = (
        alignment_state in HARD_BLOCK_STATES
        or process_gate in {"FAIL", "BLOCK", "BLOCKED", "PROCESS_BLOCKED"}
    )
    contradiction = (
        alignment_state in CONTRADICTION_STATES
        or contradiction_gate in {"FAIL", "CONTRADICTION", "NISON_CONTRADICTION"}
    )
    missing_alignment = alignment_state == ""

    evidence_bundle = deepcopy(a.get("evidence_bundle", {}))
    evidence_bundle.setdefault("similarity", deepcopy(similarity))
    evidence_bundle["final_trade_decision"] = None
    evidence_bundle["direction_generated_by_memory"] = False
    evidence_bundle["direction_generated_by_retrieval"] = False
    evidence_bundle["2025_used_for_tuning"] = False

    return {
        "decision_brain_row": row,
        "similarity": deepcopy(similarity),
        "knowledge_evidence": {
            "alignment_state": a.get("alignment_state"),
            "candidate_direction": a.get("candidate_direction"),
            "contradiction_gate": a.get("contradiction_gate"),
            "process_gate": a.get("process_gate"),
            "book_evidence_status": a.get("book_evidence_status"),
            "market_evidence_status": a.get("market_evidence_status"),
            "similarity_record_count": a.get("similarity_record_count"),
            "evidence_bundle": evidence_bundle,
            "final_trade_decision": None,
        },
        "gates": {
            "hard_block": hard_block,
            "contradiction": contradiction,
            "abstain": hard_block or contradiction or missing_alignment or alignment_state in {"ABSTAIN", "INSUFFICIENT", "NEEDS_REVIEW"},
        },
        "routing": "BLOCK" if hard_block else ("REVIEW" if contradiction or missing_alignment else "ASSESS"),
    }
