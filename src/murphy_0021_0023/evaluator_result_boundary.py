"""Lossless boundary for Murphy 0021-0023 evaluator results.

This module transports evaluator output without mapping it into the narrower
canonical NormalizedEvidence schema. It does not recompute rule outcomes,
infer direction, strength, conflict, or gate status.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, Literal

EvaluatorStatus = Literal["PASS", "FAIL", "NOT_EVALUABLE"]


@dataclass(frozen=True)
class EvaluatorResultBoundary:
    rule_id: str
    status: EvaluatorStatus
    directional_confirmation: Optional[str]
    reason: Optional[str]
    confirmation_available_timestamp: Optional[str] = None


def preserve_evaluator_result(result: Dict[str, Any]) -> EvaluatorResultBoundary:
    """Preserve source evaluator fields exactly; perform no semantic mapping."""
    rule_id = result.get("rule_id")
    status = result.get("status")

    if rule_id not in {"MURPHY_0021", "MURPHY_0022", "MURPHY_0023"}:
        raise ValueError("unsupported Murphy 0021-0023 rule_id")
    if status not in {"PASS", "FAIL", "NOT_EVALUABLE"}:
        raise ValueError("unsupported evaluator status")

    return EvaluatorResultBoundary(
        rule_id=rule_id,
        status=status,
        directional_confirmation=result.get("directional_confirmation"),
        reason=result.get("reason"),
        confirmation_available_timestamp=result.get("confirmation_available_timestamp"),
    )


def to_dict(result: EvaluatorResultBoundary) -> Dict[str, Any]:
    return asdict(result)
