"""PF-F1 flagpole sharpness governance primitive V1.

This layer makes the missing `sharp` concept explicit without pretending that
Murphy supplies a numeric threshold. A project-approved engineering policy
must provide the minimum normalized move. No default threshold is selected.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class FlagpoleSharpnessPolicy:
    min_normalized_move: float
    normalization: str
    approved_by: Optional[str] = None


def evaluate_pf_f1(
    move: float,
    policy: Optional[FlagpoleSharpnessPolicy],
    evidence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    evidence = evidence or {}
    if policy is None:
        return {"status": "NOT_EVALUABLE", "reason": "sharpness_policy_missing"}
    if policy.min_normalized_move <= 0 or not policy.normalization:
        return {"status": "NOT_EVALUABLE", "reason": "invalid_sharpness_policy"}
    if move >= policy.min_normalized_move:
        return {
            "status": "CONFIRMED",
            "reason": "approved_sharpness_policy_satisfied",
            "normalization": policy.normalization,
            "availability_timestamp": evidence.get("availability_timestamp"),
        }
    return {
        "status": "NOT_CONFIRMED",
        "reason": "approved_sharpness_policy_not_satisfied",
        "normalization": policy.normalization,
        "availability_timestamp": evidence.get("availability_timestamp"),
    }
