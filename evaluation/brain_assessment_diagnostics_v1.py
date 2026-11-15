"""Read-only diagnostics for Decision Brain V1 evidence aggregation.

This module does not change the recovered Brain, generate direction, recalibrate
confidence, or authorize/block a trade. It makes aggregation blind spots visible
for audit and regression testing.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any, Mapping


REGIME_FIELDS = (
    "M5_trend_regime", "M15_trend_regime", "M30_trend_regime",
    "H1_trend_regime", "H4_trend_regime", "D1_trend_regime",
)


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, str) and not value.strip():
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _direction(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text if text in {"bullish", "bearish", "neutral", "conflicted"} else "unknown"


def diagnose_brain_assessment(
    row: Mapping[str, Any],
    assessment: Mapping[str, Any],
    decision: Mapping[str, Any] | None = None,
    governance_execution: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an audit-only breakdown of MTF votes, confidence inputs and NO_TRADE handoff."""
    regimes = {field: _number(row.get(field)) for field in REGIME_FIELDS}
    available = {field: value for field, value in regimes.items() if value is not None}
    votes = Counter(
        "bullish" if value > 0 else "bearish" if value < 0 else "neutral"
        for value in available.values()
    )
    regime_mean = sum(available.values()) / len(available) if available else None
    vote_direction = (
        "bullish" if votes["bullish"] > votes["bearish"]
        else "bearish" if votes["bearish"] > votes["bullish"]
        else "mixed"
    )
    structure_direction = (
        "bullish" if regime_mean is not None and regime_mean > 0.20
        else "bearish" if regime_mean is not None and regime_mean < -0.20
        else "neutral"
    )
    mtf_score = _number(row.get("mtf_trend_score"))
    score_direction = (
        "bullish" if mtf_score is not None and mtf_score > 0
        else "bearish" if mtf_score is not None and mtf_score < 0
        else "neutral" if mtf_score == 0
        else "unavailable"
    )

    evidence = [item for item in (assessment.get("evidence") or []) if isinstance(item, Mapping)]
    evidence_directions = Counter(_direction(item.get("direction")) for item in evidence)
    directional_strength = {
        side: sum(_number(item.get("strength")) or 0.0 for item in evidence if _direction(item.get("direction")) == side)
        for side in ("bullish", "bearish")
    }
    neutral_strength = sum(
        _number(item.get("strength")) or 0.0
        for item in evidence if _direction(item.get("direction")) == "neutral"
    )
    directional_total = directional_strength["bullish"] + directional_strength["bearish"]
    reproduced_directional_confidence = (
        abs(directional_strength["bullish"] - directional_strength["bearish"]) / directional_total
        if directional_total > 0 else 0.0
    )

    no_trade_reasons = [str(reason) for reason in (assessment.get("no_trade_reasons") or [])]
    final_decision = str((decision or {}).get("final") or "").strip().upper()
    execution = dict(governance_execution or {})
    handoff_gap = bool(no_trade_reasons) and final_decision in {"BUY", "SELL"}
    eligible_with_reasons = bool(execution.get("eligible")) and bool(no_trade_reasons)

    return {
        "diagnostic_only": True,
        "direction_generation": False,
        "decision_authority": False,
        "mtf": {
            "available_regime_count": len(available),
            "missing_regime_fields": [field for field, value in regimes.items() if value is None],
            "vote_counts": dict(votes),
            "regime_mean": regime_mean,
            "vote_direction": vote_direction,
            "structure_direction_using_brain_v1_threshold": structure_direction,
            "mtf_trend_score": mtf_score,
            "score_direction": score_direction,
            "score_vs_regime_vote_disagreement": (
                score_direction in {"bullish", "bearish"}
                and vote_direction in {"bullish", "bearish", "mixed"}
                and score_direction != vote_direction
            ),
            "both_bullish_and_bearish_regimes_present": votes["bullish"] > 0 and votes["bearish"] > 0,
        },
        "confidence_audit": {
            "reported_confidence": _number(assessment.get("confidence")),
            "reproduced_directional_confidence": reproduced_directional_confidence,
            "directional_strength": directional_strength,
            "neutral_evidence_count": evidence_directions["neutral"],
            "neutral_strength_excluded_from_directional_denominator": neutral_strength,
            "directional_evidence_count": evidence_directions["bullish"] + evidence_directions["bearish"],
            "note": "Diagnostic decomposition only; not a calibrated probability or replacement confidence.",
        },
        "no_trade_handoff_audit": {
            "brain_no_trade_reasons": no_trade_reasons,
            "downstream_final_decision": final_decision or "NOT_SUPPLIED",
            "governance_execution_eligible": execution.get("eligible"),
            "governance_hard_blocks": list(execution.get("hard_blocks") or []),
            "governance_needs_review": list(execution.get("needs_review") or []),
            "eligible_while_brain_reports_no_trade_reasons": eligible_with_reasons,
            "reasons_present_but_directional_decision_returned": handoff_gap,
            "note": "Review flag only; V1 reason semantics are not reinterpreted as new hard gates.",
        },
    }


__all__ = ["diagnose_brain_assessment"]
