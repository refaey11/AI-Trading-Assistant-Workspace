"""PF-H1 horizontal-level governance primitive V1.

A horizontal level is evaluable only when its boundary representation is
explicitly horizontal. This module does not invent a tolerance, clustering
window, ATR multiple, or price-distance threshold.
"""
from typing import Any, Dict


def evaluate_pf_h1(boundary: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(boundary, dict):
        return {"status": "NOT_EVALUABLE", "reason": "boundary_missing"}

    slope = boundary.get("slope")
    if slope is None:
        return {"status": "NOT_EVALUABLE", "reason": "horizontal_tolerance_not_defined"}

    if slope == 0:
        return {"status": "CONFIRMED", "reason": "exact_horizontal_boundary"}

    return {"status": "NOT_CONFIRMED", "reason": "boundary_not_exactly_horizontal"}
