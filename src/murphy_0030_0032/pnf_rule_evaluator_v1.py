"""Fail-closed evaluator wrapper for Murphy 0030-0032.

This wrapper reuses the existing PNF3BoxReference core. It does not select
box size, infer trend context, or invent stop offsets. Until the project
approves both the box-size and bootstrap policies, evaluation remains
NOT_EVALUABLE even when structural calculations are available.
"""
from __future__ import annotations

from typing import Literal

from .pnf_3box_reference import PNF3BoxReference, PNFBar, bullish_support_reference, stop_reference

Status = Literal["PASS", "FAIL", "NOT_EVALUABLE"]


def evaluate_0030_0032(
    bars: list[PNFBar],
    *,
    box_size: float | None,
    box_size_policy_approved: bool,
    bootstrap_policy_approved: bool,
    direction_context: Literal["BULLISH", "BEARISH"] | None = None,
) -> dict:
    """Evaluate 0030-0032 without inventing missing policy/context.

    0030 is structural bullish-support evidence.
    0031/0032 are risk references only and require explicit direction context.
    """
    if not bars or box_size is None:
        return {"status": "NOT_EVALUABLE", "reason": "Missing P&F input or box size"}
    if not box_size_policy_approved:
        return {"status": "NOT_EVALUABLE", "reason": "Box-size policy is not governance-approved"}
    if not bootstrap_policy_approved:
        return {"status": "NOT_EVALUABLE", "reason": "Bootstrap policy is not governance-approved"}
    if any(str(bar.timestamp)[:4] == "2025" for bar in bars):
        return {"status": "NOT_EVALUABLE", "reason": "2025 is OOS and cannot enter this evaluator"}

    columns = PNF3BoxReference(box_size).build(bars)
    support = bullish_support_reference(columns)
    out = {
        "status": "PASS",
        "rule_0030": {
            "status": "PASS" if support else "NOT_EVALUABLE",
            "evidence_type": "PNF_BULLISH_SUPPORT_REFERENCE",
            "direction": "BULLISH" if support else None,
            "support": support,
        },
        "rule_0031": {"status": "NOT_EVALUABLE", "evidence": None},
        "rule_0032": {"status": "NOT_EVALUABLE", "evidence": None},
    }

    if direction_context == "BULLISH":
        out["rule_0031"] = {"status": "PASS" if stop_reference(columns, "BULLISH") else "NOT_EVALUABLE", "evidence": stop_reference(columns, "BULLISH")}
    elif direction_context == "BEARISH":
        out["rule_0032"] = {"status": "PASS" if stop_reference(columns, "BEARISH") else "NOT_EVALUABLE", "evidence": stop_reference(columns, "BEARISH")}

    return out
