"""PF-G1 convergence/parallelism governance primitive V1.

Uses only explicit line geometry. No tolerance or similarity threshold is
invented here. Near-parallel/near-convergent cases remain NOT_EVALUABLE until
an approved engineering tolerance is supplied.
"""
from typing import Any, Dict, Tuple


def _line(boundary: Dict[str, Any]) -> Tuple[float, float]:
    return float(boundary["slope"]), float(boundary["intercept"])


def evaluate_pf_g1(upper: Dict[str, Any], lower: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(upper, dict) or not isinstance(lower, dict):
        return {"status": "NOT_EVALUABLE", "reason": "boundary_missing"}
    if "slope" not in upper or "intercept" not in upper or "slope" not in lower or "intercept" not in lower:
        return {"status": "NOT_EVALUABLE", "reason": "line_geometry_missing"}

    m1, b1 = _line(upper)
    m2, b2 = _line(lower)

    if m1 == m2:
        if b1 == b2:
            return {"status": "NOT_EVALUABLE", "reason": "coincident_boundaries"}
        return {"status": "PARALLEL_EXACT", "status_class": "PARALLEL"}

    x_apex = (b2 - b1) / (m1 - m2)
    return {
        "status": "CONVERGING_EXACT",
        "status_class": "CONVERGING",
        "intersection_x": x_apex,
    }
