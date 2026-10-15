"""Proposal-only PF-G1 exact-apex convergence operator for Murphy 0013.

This module deliberately does not depend on or replace canonical geometry producers.
It consumes already-resolved line geometry and is NOT production-frozen.
"""

from __future__ import annotations


def evaluate_convergence(upper: dict, lower: dict, evaluation_ts: float) -> dict:
    required = ("slope", "intercept", "availability_ts", "anchor_end_ts")
    if not upper or not lower:
        return {"relationship": "NOT_EVALUABLE"}
    if any(k not in upper for k in required) or any(k not in lower for k in required):
        return {"relationship": "NOT_EVALUABLE"}

    joint_available = max(upper["availability_ts"], lower["availability_ts"])
    latest_anchor = max(upper["anchor_end_ts"], lower["anchor_end_ts"])

    if evaluation_ts < joint_available or evaluation_ts < latest_anchor:
        return {"relationship": "NOT_EVALUABLE"}

    if upper["slope"] >= 0 or lower["slope"] <= 0:
        return {"relationship": "NOT_CONVERGING"}

    denominator = upper["slope"] - lower["slope"]
    if denominator == 0:
        return {"relationship": "NOT_CONVERGING"}

    apex_ts = (lower["intercept"] - upper["intercept"]) / denominator
    apex_price = upper["slope"] * apex_ts + upper["intercept"]

    if apex_ts <= max(joint_available, latest_anchor):
        return {
            "relationship": "NOT_CONVERGING",
            "apex_timestamp": apex_ts,
            "apex_price": apex_price,
        }

    upper_eval = upper["slope"] * evaluation_ts + upper["intercept"]
    lower_eval = lower["slope"] * evaluation_ts + lower["intercept"]
    if upper_eval <= lower_eval:
        return {
            "relationship": "NOT_CONVERGING",
            "apex_timestamp": apex_ts,
            "apex_price": apex_price,
        }

    return {
        "relationship": "CONVERGING",
        "apex_timestamp": apex_ts,
        "apex_price": apex_price,
        "availability_timestamp": joint_available,
    }
