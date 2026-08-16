"""PF-B1 governance gate V1.

Policy-parametric only: this module does not choose a breakout threshold.
It accepts an explicitly approved policy and refuses decisive confirmation
when no policy is supplied. This keeps Murphy source semantics separate from
project operationalization.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class PFB1Status(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"
    NOT_EVALUABLE = "NOT_EVALUABLE"


@dataclass(frozen=True)
class BreakoutPolicy:
    family: str  # PRICE_FILTER or TIME_FILTER
    condition: Dict[str, Any]
    context: Optional[str] = None
    approved_by: Optional[str] = None


def evaluate_pf_b1(boundary_id: str, direction: str, policy: Optional[BreakoutPolicy], evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate only when an explicit policy is supplied.

    No default percentage, ATR, pip distance, lookback, or two-day rule is
    selected here. Missing policy is deterministically NOT_EVALUABLE.
    """
    if policy is None or not policy.family or not policy.condition:
        return {
            "boundary_id": boundary_id,
            "direction": direction,
            "status": PFB1Status.NOT_EVALUABLE.value,
            "reason": "approved_breakout_policy_missing",
        }

    if policy.family not in {"PRICE_FILTER", "TIME_FILTER"}:
        return {
            "boundary_id": boundary_id,
            "direction": direction,
            "status": PFB1Status.NOT_EVALUABLE.value,
            "reason": "unsupported_policy_family",
        }

    # The policy evaluator itself must be supplied by the approved project
    # implementation. This governance layer deliberately does not invent the
    # condition or optimize it.
    if evidence.get("policy_satisfied") is True:
        return {
            "boundary_id": boundary_id,
            "direction": direction,
            "status": PFB1Status.CONFIRMED.value,
            "raw_break_timestamp": evidence.get("raw_break_timestamp"),
            "confirmation_timestamp": evidence.get("confirmation_timestamp"),
            "availability_timestamp": evidence.get("availability_timestamp"),
        }

    return {
        "boundary_id": boundary_id,
        "direction": direction,
        "status": PFB1Status.NOT_CONFIRMED.value,
        "reason": "approved_policy_not_satisfied",
        "availability_timestamp": evidence.get("availability_timestamp"),
    }
