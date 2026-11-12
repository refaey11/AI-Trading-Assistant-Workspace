"""Narrow compatibility handoff between Knowledge Alignment and Decision Brain V1.

This module does not create BUY/SELL decisions. It preserves market/book
contradictions and packages upstream evidence for the existing Brain
assessment boundary. TIZ process state is optional metadata only.
"""
from copy import deepcopy

CONTRADICTION_STATES = {"NISON_CONTRADICTION", "NEEDS_REVIEW"}
REVIEW_STATES = {"ABSTAIN", "INSUFFICIENT", "INSUFFICIENT_BOOK_EVIDENCE", "NEEDS_REVIEW"}


def _status(x):
    return str(x or "").strip().upper()


def build_handoff(market_row, alignment_output, similarity=None):
    row = deepcopy(market_row or {})
    a = deepcopy(alignment_output or {})
    alignment_state = _status(a.get("alignment_state"))
    contradiction_gate = _status(a.get("contradiction_gate"))

    # process_gate and PROCESS_BLOCKED are legacy TIZ-derived fields. Preserve
    # their values in the evidence bundle, but never use them for routing.
    contradiction = (
        alignment_state in CONTRADICTION_STATES
        or contradiction_gate in {"FAIL", "CONTRADICTION", "NISON_CONTRADICTION"}
    )
    missing_alignment = alignment_state == ""
    review_required = (
        contradiction
        or missing_alignment
        or alignment_state in REVIEW_STATES
    )

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
            "tiz_decision_authority": False,
            "book_evidence_status": a.get("book_evidence_status"),
            "market_evidence_status": a.get("market_evidence_status"),
            "similarity_record_count": a.get("similarity_record_count"),
            "evidence_bundle": evidence_bundle,
            "final_trade_decision": None,
        },
        "gates": {
            "hard_block": False,
            "contradiction": contradiction,
            "abstain": review_required,
            "tiz_decision_authority": False,
        },
        "routing": "REVIEW" if review_required else "ASSESS",
    }
