"""Deterministic structural evaluators with mandatory provenance gating.

Only exact geometry is evaluated. Breakout confirmation remains outside this
module. A structural evaluator cannot return CONFIRMED unless every upstream
pivot used by its boundaries was available at the decision timestamp.
"""
from typing import Any, Dict

from .murphy_boundary_provenance_adapter_v1 import validate_boundary_provenance


def _num(d: Dict[str, Any], key: str):
    value = d.get(key)
    return value if isinstance(value, (int, float)) else None


def _converging(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    m1, b1 = _num(a, "slope"), _num(a, "intercept")
    m2, b2 = _num(b, "slope"), _num(b, "intercept")
    if None in (m1, b1, m2, b2) or m1 == m2:
        return False
    return True


def _horizontal(d: Dict[str, Any]) -> bool:
    return _num(d, "slope") == 0


def _provenance_ok(upper: Dict[str, Any], lower: Dict[str, Any], decision_time: Any):
    for boundary in (upper, lower):
        result = validate_boundary_provenance(boundary, decision_time)
        if result["status"] != "PASS":
            return result
    return {"status": "PASS"}


def evaluate_0013(upper, lower, decision_time):
    provenance = _provenance_ok(upper, lower, decision_time)
    if provenance["status"] != "PASS": return provenance
    if not _converging(upper, lower): return {"status":"NOT_EVALUABLE"}
    if _num(upper,"slope") < 0 and _num(lower,"slope") > 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0014(upper, lower, decision_time):
    provenance = _provenance_ok(upper, lower, decision_time)
    if provenance["status"] != "PASS": return provenance
    if _num(upper,"slope") is None or _num(lower,"slope") is None:
        return {"status":"NOT_EVALUABLE"}
    if _horizontal(upper) and _num(lower,"slope") > 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0018(upper, lower, decision_time):
    provenance = _provenance_ok(upper, lower, decision_time)
    if provenance["status"] != "PASS": return provenance
    if not _converging(upper, lower): return {"status":"NOT_EVALUABLE"}
    if _num(upper,"slope") < 0 and _num(lower,"slope") < 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0019(upper, lower, decision_time):
    provenance = _provenance_ok(upper, lower, decision_time)
    if provenance["status"] != "PASS": return provenance
    if not _converging(upper, lower): return {"status":"NOT_EVALUABLE"}
    if _num(upper,"slope") > 0 and _num(lower,"slope") > 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0020(upper, lower, decision_time):
    provenance = _provenance_ok(upper, lower, decision_time)
    if provenance["status"] != "PASS": return provenance
    if _num(upper,"slope") is None or _num(lower,"slope") is None:
        return {"status":"NOT_EVALUABLE"}
    if _horizontal(upper) and _horizontal(lower) and _num(upper,"intercept") != _num(lower,"intercept"):
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}
