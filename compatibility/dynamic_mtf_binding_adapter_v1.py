"""Contract-bound Dynamic MTF binding adapter.

Validates an explicitly supplied role assignment against DYNAMIC_MTF_BINDING_V1.
It does not invent scoring, thresholds, or directional logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Tuple

ALLOWED = {"M5", "M15", "M30", "H1", "H4", "D1"}
ROLE_CANDIDATES = {
    "macro_context": ALLOWED,
    "context": ALLOWED,
    "setup": {"H4", "H1", "M30", "M15", "M5"},
    "confirmation": {"H1", "M30", "M15", "M5"},
    "execution": {"M30", "M15", "M5"},
}
ROLE_ORDER = ["macro_context", "context", "setup", "confirmation", "execution"]

@dataclass(frozen=True)
class DynamicMTFResult:
    status: str
    alignment_state: str
    role_timeframes: Mapping[str, str]
    evidence_trace: Tuple[str, ...]
    final_trade_decision: Optional[str] = None


def _minutes(tf: str) -> int:
    return {"M5": 5, "M15": 15, "M30": 30, "H1": 60, "H4": 240, "D1": 1440}[tf]


def bind_dynamic_mtf(*, available_timeframes: Iterable[str], role_assignments: Mapping[str, str], evidence_trace: Iterable[str] = (), required_roles: Iterable[str] = ROLE_ORDER) -> DynamicMTFResult:
    """Validate source-backed role assignments; otherwise fail closed."""
    available = set(available_timeframes)
    required = list(required_roles)
    if not available or not available.issubset(ALLOWED):
        return DynamicMTFResult("NOT_EVALUABLE", "NOT_EVALUABLE", {}, tuple(evidence_trace))
    if any(role not in ROLE_CANDIDATES for role in required):
        return DynamicMTFResult("NOT_EVALUABLE", "NOT_EVALUABLE", {}, tuple(evidence_trace))
    if any(role not in role_assignments for role in required):
        return DynamicMTFResult("NOT_EVALUABLE", "NOT_EVALUABLE", {}, tuple(evidence_trace))
    selected = {}
    for role in required:
        tf = role_assignments[role]
        if tf not in available or tf not in ROLE_CANDIDATES[role]:
            return DynamicMTFResult("NOT_EVALUABLE", "NOT_EVALUABLE", {}, tuple(evidence_trace))
        selected[role] = tf
    for higher, lower in zip(required, required[1:]):
        if _minutes(selected[higher]) < _minutes(selected[lower]):
            return DynamicMTFResult("NOT_EVALUABLE", "CONFLICTED", selected, tuple(evidence_trace))
    alignment = "MIXED" if len(set(selected.values())) < len(selected) else "ALIGNED"
    return DynamicMTFResult("PASS", alignment, selected, tuple(evidence_trace))
