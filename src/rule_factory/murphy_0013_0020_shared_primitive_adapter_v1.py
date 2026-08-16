"""Shared primitive adapter for Murphy rules 0013-0020.

This is a wiring layer only. It does not add pattern semantics or thresholds.
It reports which shared primitives are available and preserves their
NOT_EVALUABLE state when an approved policy/contract is missing.
"""
from typing import Any, Dict


def evaluate_shared_primitives(
    *,
    horizontal: Dict[str, Any],
    geometry: Dict[str, Any],
    breakout: Dict[str, Any],
    flagpole: Dict[str, Any],
) -> Dict[str, Any]:
    results = {
        "PF-H1": horizontal,
        "PF-G1": geometry,
        "PF-B1": breakout,
        "PF-F1": flagpole,
    }
    blocked = [name for name, result in results.items() if result.get("status") in {"NOT_EVALUABLE", "NOT_CONFIRMED"}]
    return {
        "status": "READY_FOR_RULE_EVALUATION" if not blocked else "PARTIAL",
        "primitives": results,
        "blocked_primitives": blocked,
    }


RULE_PRIMITIVE_MAP = {
    "0013": ["PF-H1", "PF-G1", "PF-B1"],
    "0014": ["PF-H1", "PF-G1", "PF-B1"],
    "0015": ["PF-G1", "PF-B1", "PF-F1"],
    "0016": ["PF-G1", "PF-B1", "PF-F1"],
    "0017": ["PF-G1", "PF-B1", "PF-F1"],
    "0018": ["PF-G1", "PF-B1"],
    "0019": ["PF-G1", "PF-B1"],
    "0020": ["PF-G1", "PF-B1"],
}
