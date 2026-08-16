"""Deterministic structural evaluators with mandatory provenance gating.

Only canonical geometry classifications are evaluated. Breakout confirmation
remains outside this module. A structural evaluator cannot return a structural
match when an upstream geometry relationship is missing or unapproved.
"""
from typing import Any, Dict

from .murphy_boundary_provenance_adapter_v1 import validate_boundary_provenance


def _num(d: Dict[str, Any], key: str):
    value = d.get(key)
    return value if isinstance(value, (int, float)) else None


def _converging(a: Dict[str, Any], b: Dict[str, Any]) -> bool | None:
    """Use an explicit canonical relationship; never infer convergence from slopes alone."""
    relationship_a = a.get("relationship")
    relationship_b = b.get("relationship")
    relationships = {relationship_a, relationship_b}
    if "CONVERGING" in relationships and relationships.issubset({"CONVERGING", None}):
        return True
    if relationship_a is None and relationship_b is None:
        return None
    return False


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
    convergence = _converging(upper, lower)
    if convergence is None: return {"status":"NOT_EVALUABLE", "reason":"missing_convergence_relationship"}
    if not convergence: return {"status":"NOT_CONFIRMED"}
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
    convergence = _converging(upper, lower)
    if convergence is None: return {"status":"NOT_EVALUABLE", "reason":"missing_convergence_relationship"}
    if not convergence: return {"status":"NOT_CONFIRMED"}
    if _num(upper,"slope") < 0 and _num(lower,"slope") < 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0019(upper, lower, decision_time):
    provenance = _provenance_ok(upper, lower, decision_time)
    if provenance["status"] != "PASS": return provenance
    convergence = _converging(upper, lower)
    if convergence is None: return {"status":"NOT_EVALUABLE", "reason":"missing_convergence_relationship"}
    if not convergence: return {"status":"NOT_CONFIRMED"}
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
