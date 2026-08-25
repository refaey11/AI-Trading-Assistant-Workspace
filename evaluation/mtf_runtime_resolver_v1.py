"""Dynamic MTF runtime resolver (V1).

Implements only the existing Dynamic Timeframe Selection Policy.
It does not assign static timeframes to Murphy rules, create BUY/SELL signals,
or introduce numeric thresholds/weights.

Input event schema (dict):
  timeframes: mapping timeframe -> evidence dict
Each evidence dict may contain:
  context_complete: bool
  setup_complete: bool
  confirmation_complete: bool
  risk_feasible: bool
  direction: optional[str]  # bullish/bearish/neutral/None
  higher_timeframe_conflict: bool
  available: bool
  reason: optional[str]

The resolver is fail-closed. If multiple execution candidates are equally valid,
resolution remains unresolved instead of inventing a priority rule.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping, Optional


TIMEFRAMES = ("M5", "M15", "M30", "H1", "H4", "D1")
EXECUTION_CANDIDATES = ("M5", "M15", "M30", "H1", "H4")


@dataclass(frozen=True)
class MTFResolution:
    status: str
    selected_execution_timeframe: Optional[str]
    context_timeframes_used: tuple[str, ...]
    confirmation_timeframes_used: tuple[str, ...]
    holding_horizon: Optional[str]
    selection_reasons: tuple[str, ...]
    rejected_candidate_reasons: Mapping[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _bool(evidence: Mapping[str, Any], key: str) -> bool:
    return evidence.get(key) is True


def resolve_mtf(event: Mapping[str, Any]) -> MTFResolution:
    """Resolve an execution timeframe from already-produced evidence.

    Policy behavior:
    - all available timeframes are read first;
    - execution candidates are limited to M5/M15/M30/H1/H4;
    - a candidate must be available, setup-complete, confirmation-complete,
      risk-feasible, and free of an explicit higher-timeframe conflict;
    - if exactly one candidate is valid, select it;
    - if zero or >1 candidates are valid, fail closed.

    No scoring, weighting, or static rule->timeframe mapping is introduced.
    """
    raw = event.get("timeframes")
    if not isinstance(raw, Mapping):
        return MTFResolution(
            status="NO_TRADE_MTF_INPUT_MISSING",
            selected_execution_timeframe=None,
            context_timeframes_used=(),
            confirmation_timeframes_used=(),
            holding_horizon=None,
            selection_reasons=("timeframes mapping missing",),
            rejected_candidate_reasons={},
        )

    evidence = {tf: (raw.get(tf) if isinstance(raw.get(tf), Mapping) else {}) for tf in TIMEFRAMES}
    available = tuple(tf for tf in TIMEFRAMES if evidence[tf].get("available", True) is True)

    context_used = tuple(tf for tf in ("D1", "H4", "H1") if tf in available and _bool(evidence[tf], "context_complete"))
    confirmation_used = tuple(tf for tf in ("H1", "M30", "M15", "M5") if tf in available and _bool(evidence[tf], "confirmation_complete"))

    rejected: dict[str, str] = {}
    candidates: list[str] = []
    for tf in EXECUTION_CANDIDATES:
        ev = evidence[tf]
        if tf not in available:
            rejected[tf] = "TIMEFRAME_UNAVAILABLE"
            continue
        if not _bool(ev, "setup_complete"):
            rejected[tf] = "SETUP_INCOMPLETE"
            continue
        if not _bool(ev, "confirmation_complete"):
            rejected[tf] = "CONFIRMATION_INCOMPLETE"
            continue
        if not _bool(ev, "risk_feasible"):
            rejected[tf] = "RISK_NOT_FEASIBLE"
            continue
        if ev.get("higher_timeframe_conflict") is True:
            rejected[tf] = "HIGHER_TIMEFRAME_CONFLICT"
            continue
        candidates.append(tf)

    # The policy requires a preference for the timeframe with a complete,
    # internally consistent evidence chain. If more than one candidate is
    # equally complete, this V1 does not invent a priority/score; it fails closed.
    if len(candidates) == 1:
        tf = candidates[0]
        reason = (
            "selected because setup, confirmation, and risk gates are complete "
            "and no higher-timeframe conflict is present"
        )
        return MTFResolution(
            status="RESOLVED",
            selected_execution_timeframe=tf,
            context_timeframes_used=context_used,
            confirmation_timeframes_used=confirmation_used,
            holding_horizon=event.get("holding_horizon"),
            selection_reasons=(reason,),
            rejected_candidate_reasons=rejected,
        )

    if len(candidates) == 0:
        return MTFResolution(
            status="NO_TRADE_NO_VALID_EXECUTION_CANDIDATE",
            selected_execution_timeframe=None,
            context_timeframes_used=context_used,
            confirmation_timeframes_used=confirmation_used,
            holding_horizon=event.get("holding_horizon"),
            selection_reasons=("no execution candidate satisfies the policy gates",),
            rejected_candidate_reasons=rejected,
        )

    for tf in candidates:
        rejected[tf] = "AMBIGUOUS_MULTIPLE_VALID_CANDIDATES_NO_FROZEN_TIE_BREAK"
    return MTFResolution(
        status="NO_TRADE_MTF_AMBIGUOUS",
        selected_execution_timeframe=None,
        context_timeframes_used=context_used,
        confirmation_timeframes_used=confirmation_used,
        holding_horizon=event.get("holding_horizon"),
        selection_reasons=("multiple execution candidates are valid; no tie-break is frozen in V1",),
        rejected_candidate_reasons=rejected,
    )
