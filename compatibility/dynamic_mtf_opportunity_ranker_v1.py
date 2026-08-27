"""Governed MTF opportunity selector.

Evaluates all six native project timeframes independently and selects the best
currently executable opportunity using the existing evidence contract.

No performance-derived weights, thresholds, or BUY/SELL logic are introduced.
The selector only orders candidates by explicit evidence gates and uses timeframe
size as a deterministic tie-break after equal evidence quality.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

TIMEFRAMES = ("D1", "H4", "H1", "M30", "M15", "M5")
EXECUTION_TIMEFRAMES = ("M30", "M15", "M5")

@dataclass(frozen=True)
class TimeframeVerdict:
    timeframe: str
    status: str
    direction: str | None
    context_complete: bool
    structure_complete: bool
    setup_complete: bool
    confirmation_complete: bool
    contradicted: bool
    risk_feasible: bool
    opportunity_state: str
    rejection_reasons: tuple[str, ...]

@dataclass(frozen=True)
class OpportunitySelection:
    status: str
    selected_timeframe: str | None
    selected_direction: str | None
    all_verdicts: tuple[TimeframeVerdict, ...]
    selection_reasons: tuple[str, ...]


def _b(item: Mapping[str, Any], key: str) -> bool:
    return item.get(key) is True


def _direction(item: Mapping[str, Any]) -> str | None:
    value = str(item.get("direction", "")).upper().strip()
    return value if value in {"BUY", "SELL", "BULLISH", "BEARISH"} else None


def _reasons(item: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    for key, label in (
        ("context_complete", "context_incomplete"),
        ("structure_complete", "structure_incomplete"),
        ("setup_complete", "setup_incomplete"),
        ("confirmation_complete", "confirmation_incomplete"),
        ("risk_feasible", "risk_not_feasible"),
    ):
        if not _b(item, key):
            reasons.append(label)
    if _b(item, "contradicted"):
        reasons.append("contradicted")
    if _direction(item) is None:
        reasons.append("direction_missing")
    return reasons


def evaluate_timeframe(timeframe: str, item: Mapping[str, Any]) -> TimeframeVerdict:
    tf = timeframe.upper()
    if tf not in TIMEFRAMES:
        return TimeframeVerdict(tf, "NOT_EVALUABLE", None, False, False, False, False, False, False, "NOT_EVALUABLE", ("unsupported_timeframe",))
    reasons = _reasons(item)
    direction = _direction(item)
    complete = not reasons
    if complete:
        state = "EXECUTABLE_OPPORTUNITY" if tf in EXECUTION_TIMEFRAMES else "COMPLETE_NON_EXECUTION_CONTEXT"
        status = "PASS"
    else:
        state = "BLOCKED"
        status = "NOT_EVALUABLE"
    return TimeframeVerdict(tf, status, direction, _b(item,"context_complete"), _b(item,"structure_complete"), _b(item,"setup_complete"), _b(item,"confirmation_complete"), _b(item,"contradicted"), _b(item,"risk_feasible"), state, tuple(reasons))


def select_best_opportunity(timeframe_evidence: Mapping[str, Mapping[str, Any]]) -> OpportunitySelection:
    verdicts = tuple(evaluate_timeframe(tf, timeframe_evidence.get(tf, {})) for tf in TIMEFRAMES)
    candidates = [v for v in verdicts if v.opportunity_state == "EXECUTABLE_OPPORTUNITY"]
    if not candidates:
        return OpportunitySelection("NO_TRADE", None, None, verdicts, ("No timeframe has a complete non-contradicted setup/confirmation/risk chain.",))

    order = {tf: i for i, tf in enumerate(EXECUTION_TIMEFRAMES)}
    chosen = sorted(candidates, key=lambda v: order[v.timeframe])[0]
    reasons = (
        f"{chosen.timeframe}: complete context + structure + setup + confirmation + risk",
        "No performance history, 2025 data, or synthetic score used for selection.",
        "Equal-quality executable candidates are resolved deterministically by existing execution-timeframe order.",
    )
    return OpportunitySelection("PASS", chosen.timeframe, chosen.direction, verdicts, reasons)
