"""Deterministic structural evaluators for Murphy 0013/0014/0018/0019/0020.

Only exact geometry is evaluated. Missing inputs are NOT_EVALUABLE.
Breakout confirmation is deliberately outside this module.
"""
from typing import Any, Dict


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


def evaluate_0013(upper, lower):
    if not _converging(upper, lower): return {"status":"NOT_EVALUABLE"}
    if _num(upper,"slope") < 0 and _num(lower,"slope") > 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0014(upper, lower):
    if _num(upper,"slope") is None or _num(lower,"slope") is None:
        return {"status":"NOT_EVALUABLE"}
    if _horizontal(upper) and _num(lower,"slope") > 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0018(upper, lower):
    if not _converging(upper, lower): return {"status":"NOT_EVALUABLE"}
    if _num(upper,"slope") < 0 and _num(lower,"slope") < 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0019(upper, lower):
    if not _converging(upper, lower): return {"status":"NOT_EVALUABLE"}
    if _num(upper,"slope") > 0 and _num(lower,"slope") > 0:
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}


def evaluate_0020(upper, lower):
    if _num(upper,"slope") is None or _num(lower,"slope") is None:
        return {"status":"NOT_EVALUABLE"}
    if _horizontal(upper) and _horizontal(lower) and _num(upper,"intercept") != _num(lower,"intercept"):
        return {"status":"CONFIRMED"}
    return {"status":"NOT_CONFIRMED"}
