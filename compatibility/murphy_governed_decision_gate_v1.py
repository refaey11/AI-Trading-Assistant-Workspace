"""Governed Murphy -> Decision Brain V1 integration gate.

The recovered Decision Brain V1 remains untouched. Murphy evidence is applied
as a separate governance layer after V1 assessment. No direction is inferred
from rule ids, status, timeframe, predicted returns, Nison, TIZ, or risk.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Mapping

LOCKED_OOS_YEAR = 2025
VALID_DIRECTIONS = {"BULLISH", "BEARISH"}
VALID_TIZ_MODES = {"optional", "strict"}


def _year(value: Any) -> int | None:
    if isinstance(value, datetime):
        return value.year
    if isinstance(value, str):
        text = value.strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(text).year
        except ValueError:
            try:
                return datetime.strptime(text[:10], "%Y-%m-%d").year
            except ValueError:
                return None
    return None


def _gate(value: Any) -> str:
    text = str(value or "").strip().upper()
    return text if text in {"PASS", "FAIL", "NOT_EVALUABLE"} else "NOT_EVALUABLE"


def _brain_direction(assessment: Mapping[str, Any]) -> str | None:
    value = str(assessment.get("directional_bias") or "").strip().upper()
    return value if value in VALID_DIRECTIONS else None


def _explicit_murphy_direction(murphy: Mapping[str, Any]) -> tuple[str | None, str]:
    """Accept only explicit source-preserved direction; never infer it."""
    candidates: list[str] = []
    for key in ("direction", "source_direction", "explicit_direction"):
        value = str(murphy.get(key) or "").strip().upper()
        if value in VALID_DIRECTIONS:
            candidates.append(value)
    if not candidates:
        return None, "MISSING_EXPLICIT_DIRECTION"
    unique = sorted(set(candidates))
    if len(unique) != 1:
        return None, "CONFLICTING_EXPLICIT_DIRECTIONS"
    return unique[0], "EXPLICIT_SOURCE_DIRECTION"


def _sanitize_historical(historical: Mapping[str, Any] | None) -> dict[str, Any]:
    payload = dict(historical or {})
    out = deepcopy(payload)
    out["predicted_return_used_as_direction"] = False
    return out


def _decision(
    *,
    brain_direction: str | None,
    murphy_direction: str | None,
    murphy_status: str,
    tiz_gate: str,
    tiz_mode: str,
    tiz_unverified: bool,
    risk_gate: str,
    nison_contradiction: bool,
) -> dict[str, Any]:
    hard_blocks: list[str] = []
    needs_review: list[str] = []

    if murphy_status != "PASS":
        hard_blocks.append("MURPHY_NOT_PASS")
    if murphy_direction is None:
        hard_blocks.append("MURPHY_DIRECTION_NOT_EVALUABLE")

    if tiz_gate == "FAIL":
        hard_blocks.append("TIZ_FAIL")
    elif tiz_mode == "strict" and tiz_gate != "PASS":
        hard_blocks.append("TIZ_NOT_EVALUABLE")
    elif tiz_mode == "optional" and tiz_unverified:
        # Explicitly recorded, but not a block in optional mode.
        pass
    elif tiz_mode == "optional" and tiz_gate != "PASS":
        needs_review.append("TIZ_NOT_EVALUABLE")

    if risk_gate != "PASS":
        hard_blocks.append(f"RISK_{risk_gate}")

    if nison_contradiction:
        needs_review.append("NISON_CONTRADICTION")

    alignment = "NOT_EVALUABLE"
    if brain_direction and murphy_direction:
        alignment = "ALIGNED" if brain_direction == murphy_direction else "CONTRADICTED"
        if alignment == "CONTRADICTED":
            needs_review.append("MURPHY_BRAIN_CONTRADICTION")

    eligible = not hard_blocks and not needs_review and alignment == "ALIGNED"
    if eligible:
        final = "EXECUTE_TIZ_UNVERIFIED" if tiz_mode == "optional" and tiz_unverified else "EXECUTE"
    elif needs_review and not hard_blocks:
        final = "NEEDS_REVIEW"
    else:
        final = "BLOCKED"

    return {
        "alignment": alignment,
        "execution_eligible": eligible,
        "hard_blocks": hard_blocks,
        "needs_review": needs_review,
        "tiz_unverified": tiz_unverified,
        "final_trade_decision": final,
    }


def assess_with_murphy_gate(
    decision_brain_module,
    *,
    row: Mapping[str, Any],
    query_as_of: Any,
    mode: str = "development",
    murphy_evidence: Mapping[str, Any] | None = None,
    nison_evidence: Mapping[str, Any] | None = None,
    tiz_evidence: Mapping[str, Any] | None = None,
    risk_evidence: Mapping[str, Any] | None = None,
    historical_evidence: Mapping[str, Any] | None = None,
    provenance: Mapping[str, Any] | None = None,
    tiz_mode: str = "optional",
) -> dict[str, Any]:
    if mode not in {"development", "oos_evaluation"}:
        return {"status": "NOT_EVALUABLE", "reason": "INVALID_MODE"}
    if tiz_mode not in VALID_TIZ_MODES:
        return {"status": "NOT_EVALUABLE", "reason": "INVALID_TIZ_MODE"}

    year = _year(query_as_of)
    if year is None:
        return {"status": "NOT_EVALUABLE", "reason": "INVALID_QUERY_TIMESTAMP"}
    if mode == "development" and year >= LOCKED_OOS_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "2025_OOS_LOCKED"}
    if year > LOCKED_OOS_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "FUTURE_DATA_FORBIDDEN"}

    row_copy = deepcopy(dict(row))
    assessment = decision_brain_module.assess(row_copy, similarity=None)
    assessment_dict = {
        "market_state": assessment.market_state,
        "directional_bias": assessment.directional_bias,
        "confidence": assessment.confidence,
        "evidence": deepcopy(assessment.evidence),
        "contradictions": deepcopy(assessment.contradictions),
        "no_trade_reasons": deepcopy(assessment.no_trade_reasons),
    }

    murphy = dict(murphy_evidence or {})
    nison = dict(nison_evidence or {})
    tiz = dict(tiz_evidence or {})
    risk = dict(risk_evidence or {})

    murphy_status = _gate(murphy.get("status") or murphy.get("gate"))
    murphy_direction, murphy_direction_source = _explicit_murphy_direction(murphy)
    tiz_gate = _gate(tiz.get("process_gate") or tiz.get("status"))
    tiz_unverified = bool(tiz.get("unverified", False)) or tiz_gate == "NOT_EVALUABLE"
    risk_gate = _gate(risk.get("risk_status") or risk.get("status"))
    nison_contradiction = bool(nison.get("contradiction", False)) or str(
        nison.get("confirmation") or ""
    ).strip().upper() in {"CONTRADICTED", "CONTRADICTION"}

    result = _decision(
        brain_direction=_brain_direction(assessment_dict),
        murphy_direction=murphy_direction,
        murphy_status=murphy_status,
        tiz_gate=tiz_gate,
        tiz_mode=tiz_mode,
        tiz_unverified=tiz_unverified,
        risk_gate=risk_gate,
        nison_contradiction=nison_contradiction,
    )

    return {
        "status": "PASS",
        "mode": mode,
        "query_as_of": query_as_of,
        "assessment": assessment_dict,
        "murphy_evidence": deepcopy(murphy),
        "murphy_direction": murphy_direction,
        "murphy_direction_source": murphy_direction_source,
        "nison_evidence": nison,
        "tiz_evidence": tiz,
        "risk_evidence": risk,
        "historical_evidence": _sanitize_historical(historical_evidence),
        "execution": result,
        "governance": {
            "recovered_v1_unchanged": True,
            "murphy_generates_direction": False,
            "direction_requires_explicit_source": True,
            "predicted_return_used_as_direction": False,
            "nison_generates_direction": False,
            "tiz_generates_direction": False,
            "risk_gate_overridable": False,
            "future_data_allowed": False,
            "2025_used_for_tuning": False,
            "synthetic_direction": False,
            "tiz_mode": tiz_mode,
            "tiz_optional": tiz_mode == "optional",
        },
        "provenance": deepcopy(provenance or {}),
    }
