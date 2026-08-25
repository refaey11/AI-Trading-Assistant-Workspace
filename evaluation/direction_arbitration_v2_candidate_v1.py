"""Isolated Direction Arbitration V2 development candidate.

This module does not modify the recovered Decision Brain, Murphy, Nison, TIZ,
or risk implementations. It only classifies directional evidence so the
project can measure an alternative arbitration topology before any contract
freeze.
"""
from __future__ import annotations

from typing import Any, Mapping

DIRECTIONAL = {"BULLISH", "BEARISH"}


def _norm(value: Any) -> str:
    return str(value or "").strip().upper()


def arbitrate(
    *,
    brain_direction: str,
    brain_confidence: float,
    murphy_direction: str,
    murphy_has_valid_setup: bool,
    nison_confirmation: str = "ABSENT",
    nison_contradiction: bool = False,
    tiz_ready: bool = True,
    risk_pass: bool = True,
) -> dict[str, Any]:
    """Classify evidence without changing the live/frozen decision contract.

    Candidate development policy:
    - Murphy owns technical direction when a valid directional setup exists.
    - Brain is contextual agreement/disagreement, not an automatic veto.
    - Nison confirms or blocks only.
    - TIZ and risk are hard execution gates.
    - Ambiguous direction remains NO_TRADE.
    """
    brain = _norm(brain_direction)
    murphy = _norm(murphy_direction)
    nison = _norm(nison_confirmation)

    if not murphy_has_valid_setup and brain not in DIRECTIONAL:
        cls = "NO_DIRECTION"
        direction = "NO_TRADE"
    elif murphy in DIRECTIONAL and brain in DIRECTIONAL:
        cls = "AGREE" if murphy == brain else "CONFLICT"
        direction = murphy
    elif murphy in DIRECTIONAL:
        cls = "MURPHY_ONLY"
        direction = murphy
    elif brain in DIRECTIONAL:
        cls = "BRAIN_ONLY"
        direction = brain
    else:
        cls = "NO_DIRECTION"
        direction = "NO_TRADE"

    blocked_reasons: list[str] = []
    if cls in {"CONFLICT", "NO_DIRECTION"}:
        blocked_reasons.append("DIRECTION_UNRESOLVED")
    if nison_contradiction or nison in {"CONTRADICTED", "CONTRADICTION"}:
        blocked_reasons.append("NISON_CONTRADICTION")
    if not tiz_ready:
        blocked_reasons.append("TIZ_PROCESS_GATE_NOT_READY")
    if not risk_pass:
        blocked_reasons.append("RISK_GATE_FAIL_OR_NOT_EVALUABLE")

    final = direction if direction in DIRECTIONAL and not blocked_reasons else "NO_TRADE"

    return {
        "status": "PASS",
        "mode": "DEVELOPMENT_CANDIDATE",
        "arbitration_classification": cls,
        "direction": direction,
        "final": final,
        "brain_direction": brain,
        "brain_confidence": float(brain_confidence or 0.0),
        "murphy_direction": murphy,
        "nison_confirmation": nison,
        "blocked_reasons": blocked_reasons,
        "semantics_changed": True,
        "2025_oos_allowed": False,
    }
