"""Canonical bridge from DECISION_RUNTIME_V1 to the existing full Decision Brain.

No new trading logic is defined here. The bridge composes the existing
Decision Brain / Three-Book / Risk / Execution path. TIZ is process evidence
only and remains optional outside production execution when unavailable.
"""
from __future__ import annotations

from importlib import import_module
from typing import Any, Mapping

from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event


_REQUIRED_EVIDENCE = ("murphy", "nison", "risk")


def _is_authoritative(evidence: Mapping[str, Any] | None) -> bool:
    return bool((evidence or {}).get("authoritative", False))


def run_full_brain_cycle(
    *,
    row: Mapping[str, Any],
    query_as_of: Any,
    murphy_evidence: Mapping[str, Any],
    nison_evidence: Mapping[str, Any],
    risk_evidence: Mapping[str, Any],
    tiz_evidence: Mapping[str, Any] | None = None,
    historical_evidence: Mapping[str, Any] | None = None,
    source_rule_ids: list[str] | None = None,
    entry_price: float | None = None,
    atr: float | None = None,
    mode: str = "development",
) -> dict[str, Any]:
    """Run the real Brain->Three-Book->Execution assembly.

    TIZ is not inferred from market data. When unavailable, it is explicitly
    marked UNVERIFIED for development/OOS evaluation. Risk remains mandatory.
    """
    evidence = {"murphy": murphy_evidence, "nison": nison_evidence, "risk": risk_evidence}
    missing = [name for name in _REQUIRED_EVIDENCE if not evidence[name]]
    if missing:
        return {"status": "NOT_EXECUTABLE", "reason": "MISSING_EVIDENCE:" + ",".join(missing), "execution_plan": {"status": "NOT_EXECUTABLE"}}

    if not _is_authoritative(risk_evidence):
        return {"status": "NOT_EXECUTABLE", "reason": "RISK_NOT_PRODUCTION_AUTHORIZED", "execution_plan": {"status": "NOT_EXECUTABLE"}}

    tiz = dict(tiz_evidence or {})
    tiz_available = _is_authoritative(tiz)
    tiz_state = str(tiz.get("process_state") or tiz.get("process_gate") or tiz.get("status") or "NOT_EVALUABLE").upper()
    if not tiz_available and mode not in {"development", "oos_evaluation"}:
        return {"status": "NOT_EXECUTABLE", "reason": "TIZ_NOT_PRODUCTION_AUTHORIZED", "execution_plan": {"status": "NOT_EXECUTABLE"}}

    brain = import_module("RECOVERED_SOURCES.DECISION_BRAIN_V1.decision_brain")
    return assemble_decision_event(
        decision_brain_module=brain,
        row=row,
        query_as_of=query_as_of,
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence={"authoritative": tiz_available, "process_state": tiz_state, "tiz_verified": tiz_available, "unverified": not tiz_available, "source": tiz.get("source", "TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2")},
        risk_evidence=risk_evidence,
        historical_evidence=historical_evidence,
        source_rule_ids=list(source_rule_ids or []),
        entry_price=entry_price,
        atr=atr,
        mode=mode,
        provenance={"bridge": "full_brain_runtime_bridge_v1", "tiz_optional_when_unavailable": not tiz_available},
    )


__all__ = ["run_full_brain_cycle"]
