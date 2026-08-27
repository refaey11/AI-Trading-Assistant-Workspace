"""Governed runtime resolver for the existing Dynamic MTF contract.

This module fills the missing runtime-resolution gate identified by the
2026-08-26 preflight. It does not create BUY/SELL decisions and does not
introduce performance-based timeframe weights. It selects timeframes only from
available source evidence, evidence-chain completeness, and the frozen Risk
feasibility flag supplied by upstream runtime components.

The resolver is intentionally fail-closed: missing required evidence produces
NOT_EVALUABLE rather than silently substituting another timeframe.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

AVAILABLE_TIMEFRAMES = ("M5", "M15", "M30", "H1", "H4", "D1")

# Contract candidate order, used only as a deterministic higher-timeframe-first
# tie-break among otherwise equally complete candidates. No performance data is
# consulted.
ROLE_CANDIDATES = {
    "macro_context": ("D1", "H4", "H1", "M30", "M15", "M5"),
    "context": ("D1", "H4", "H1", "M30", "M15", "M5"),
    "setup": ("H4", "H1", "M30", "M15", "M5"),
    "confirmation": ("H1", "M30", "M15", "M5"),
    "execution": ("M30", "M15", "M5"),
}

ROLE_ORDER = (
    "macro_context",
    "context",
    "setup",
    "confirmation",
    "execution",
)


@dataclass(frozen=True)
class ResolutionResult:
    status: str
    alignment_state: str
    selected_execution_timeframe: str | None
    context_timeframes_used: tuple[str, ...]
    confirmation_timeframes_used: tuple[str, ...]
    setup_timeframe: str | None
    macro_timeframe: str | None
    holding_horizon: str | None
    selection_reasons: tuple[str, ...]
    rejected_candidate_reasons: tuple[str, ...]
    evidence_trace: tuple[str, ...]


def _bool_value(value: Any) -> bool:
    return value is True


def _available(data: Mapping[str, Mapping[str, Any]]) -> set[str]:
    return {str(k).upper() for k in data if str(k).upper() in AVAILABLE_TIMEFRAMES}


def _complete_setup(item: Mapping[str, Any]) -> bool:
    return _bool_value(item.get("structure_complete")) and _bool_value(item.get("setup_complete"))


def _complete_confirmation(item: Mapping[str, Any]) -> bool:
    return _bool_value(item.get("confirmation_complete")) and not _bool_value(item.get("contradicted"))


def _risk_feasible(item: Mapping[str, Any]) -> bool:
    return _bool_value(item.get("risk_feasible"))


def _candidate_reason(tf: str, item: Mapping[str, Any]) -> str:
    missing: list[str] = []
    if not _bool_value(item.get("structure_complete")):
        missing.append("structure_complete")
    if not _bool_value(item.get("setup_complete")):
        missing.append("setup_complete")
    if not _bool_value(item.get("confirmation_complete")):
        missing.append("confirmation_complete")
    if _bool_value(item.get("contradicted")):
        missing.append("contradicted")
    if not _bool_value(item.get("risk_feasible")):
        missing.append("risk_feasible")
    return f"{tf}: incomplete/blocked ({', '.join(missing) or 'unknown'})"


def resolve_mtf_event(
    *,
    timeframe_evidence: Mapping[str, Mapping[str, Any]],
    holding_horizon: str | None = None,
) -> ResolutionResult:
    """Resolve MTF roles for one event from already-derived evidence.

    Upstream components provide the evidence facts. This resolver only applies
    the frozen role candidate sets and higher-timeframe-first deterministic
    selection. It never creates direction and never uses historical
    performance/2025 data.
    """
    data = {str(k).upper(): dict(v) for k, v in timeframe_evidence.items()}
    available = _available(data)
    if not available:
        return ResolutionResult(
            "NOT_EVALUABLE", "NOT_EVALUABLE", None, (), (), None, None,
            holding_horizon, ("No supported native timeframe evidence supplied.",), (), ()
        )

    selection_reasons: list[str] = []
    rejected: list[str] = []
    trace: list[str] = [f"available={','.join(sorted(available))}"]

    # Context roles: use the highest available timeframe with explicit context
    # completeness. No performance-based selection is performed.
    def choose_context(role: str) -> str | None:
        for tf in ROLE_CANDIDATES[role]:
            if tf not in available:
                continue
            item = data[tf]
            if _bool_value(item.get("context_complete")):
                selection_reasons.append(f"{role}: selected {tf} from available complete context evidence")
                trace.append(f"{role}<-{tf}:context_complete")
                return tf
            rejected.append(f"{tf}: context evidence incomplete for {role}")
        return None

    macro_tf = choose_context("macro_context")
    context_tf = choose_context("context")

    setup_tf: str | None = None
    for tf in ROLE_CANDIDATES["setup"]:
        if tf not in available:
            continue
        item = data[tf]
        if _complete_setup(item):
            setup_tf = tf
            selection_reasons.append(f"setup: selected {tf} from complete structure/setup evidence")
            trace.append(f"setup<-{tf}:structure+setup_complete")
            break
        rejected.append(_candidate_reason(tf, item))

    confirmation_tf: str | None = None
    for tf in ROLE_CANDIDATES["confirmation"]:
        if tf not in available:
            continue
        item = data[tf]
        if _complete_confirmation(item):
            confirmation_tf = tf
            selection_reasons.append(f"confirmation: selected {tf} from complete non-contradicted confirmation evidence")
            trace.append(f"confirmation<-{tf}:confirmation_complete")
            break
        rejected.append(_candidate_reason(tf, item))

    execution_tf: str | None = None
    if setup_tf and confirmation_tf:
        for tf in ROLE_CANDIDATES["execution"]:
            if tf not in available:
                continue
            item = data[tf]
            if _complete_setup(item) and _complete_confirmation(item) and _risk_feasible(item):
                execution_tf = tf
                selection_reasons.append(f"execution: selected {tf} where setup + confirmation + risk are feasible")
                trace.append(f"execution<-{tf}:chain_complete+risk_feasible")
                break
            rejected.append(_candidate_reason(tf, item))

    if not execution_tf:
        return ResolutionResult(
            "NOT_EVALUABLE",
            "NOT_EVALUABLE",
            None,
            (context_tf,) if context_tf else (),
            (confirmation_tf,) if confirmation_tf else (),
            setup_tf,
            macro_tf,
            holding_horizon,
            tuple(selection_reasons) or ("No execution candidate satisfied the complete evidence chain and risk feasibility gate.",),
            tuple(rejected),
            tuple(trace),
        )

    # Alignment is intentionally based only on an explicit upstream state, if
    # supplied. Otherwise it remains MIXED rather than inferring direction here.
    explicit_states = {
        str(data[tf].get("alignment_state")).upper()
        for tf in available
        if data[tf].get("alignment_state") is not None
    }
    if "CONFLICTED" in explicit_states:
        alignment = "CONFLICTED"
    elif explicit_states == {"ALIGNED"}:
        alignment = "ALIGNED"
    elif explicit_states:
        alignment = "MIXED"
    else:
        alignment = "MIXED"

    return ResolutionResult(
        "PASS",
        alignment,
        execution_tf,
        tuple(x for x in (macro_tf, context_tf, setup_tf) if x),
        tuple(x for x in (confirmation_tf,) if x),
        setup_tf,
        macro_tf,
        holding_horizon,
        tuple(selection_reasons),
        tuple(rejected),
        tuple(trace),
    )
