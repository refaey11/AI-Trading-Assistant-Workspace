"""Canonical bridge from DECISION_RUNTIME_V1 to the existing full Decision Brain."""
from __future__ import annotations

import importlib.util
import sys
from math import isclose, isfinite
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import (
    CURRENT_CANONICAL_MIN_RR,
    RR_BOUNDARY_TOLERANCE,
)


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_ASSEMBLER = _load_module(ROOT / "OOS_2025" / "full_decision_brain_assembler_v1.py", "gate3c_full_brain_assembler")
assemble_decision_event = _ASSEMBLER.assemble_decision_event


def _is_authoritative(evidence: Mapping[str, Any] | None) -> bool:
    return bool((evidence or {}).get("authoritative", False))


def _canonical_risk_plan_mismatch(
    execution_plan: Mapping[str, Any],
    risk_evidence: Mapping[str, Any],
) -> str | None:
    """Require development execution levels to be the canonical Risk result."""
    try:
        canonical_rr = float(risk_evidence["rr"])
        canonical_stop = float(risk_evidence["stop_loss"])
        canonical_target = float(risk_evidence["take_profit"])
        execution_stop = float(execution_plan["stop_loss"])
        execution_target = float(execution_plan["take_profit"])
    except (KeyError, TypeError, ValueError, OverflowError):
        return "CANONICAL_RISK_PLAN_INPUTS_MISSING"

    if not all(isfinite(value) for value in (canonical_rr, canonical_stop, canonical_target, execution_stop, execution_target)):
        return "CANONICAL_RISK_PLAN_INPUTS_NON_FINITE"
    if canonical_rr < CURRENT_CANONICAL_MIN_RR - RR_BOUNDARY_TOLERANCE:
        return "CANONICAL_RISK_RR_BELOW_MINIMUM"
    if not isclose(execution_stop, canonical_stop, rel_tol=0.0, abs_tol=RR_BOUNDARY_TOLERANCE):
        return "EXECUTION_PLAN_DIFFERS_FROM_CANONICAL_RISK_LEVELS"
    if not isclose(execution_target, canonical_target, rel_tol=0.0, abs_tol=RR_BOUNDARY_TOLERANCE):
        return "EXECUTION_PLAN_DIFFERS_FROM_CANONICAL_RISK_LEVELS"
    return None


def _enforce_development_risk_contract(
    result: dict[str, Any],
    risk_evidence: Mapping[str, Any],
    *,
    mode: str,
) -> dict[str, Any]:
    # The frozen OOS candidate adapter retains its separately documented 2R
    # protocol. Development mode must instead preserve the canonical Risk result.
    if mode.strip().lower() != "development" or result.get("status") != "EXECUTABLE":
        return result

    mismatch = _canonical_risk_plan_mismatch(
        result.get("execution_plan") or {},
        risk_evidence,
    )
    updated = dict(result)
    audit = dict(updated.get("audit") or {})
    audit["canonical_risk_execution_match"] = mismatch is None
    updated["audit"] = audit
    if mismatch:
        updated["status"] = "NOT_EXECUTABLE"
        updated["reason"] = mismatch
        updated["execution_plan"] = {"status": "NOT_EXECUTABLE", "reason": mismatch}
    return updated


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
    evidence = {"murphy": murphy_evidence, "nison": nison_evidence, "risk": risk_evidence}
    missing = [name for name, value in evidence.items() if not value]
    if missing:
        return {"status": "NOT_EXECUTABLE", "reason": "MISSING_EVIDENCE:" + ",".join(missing), "execution_plan": {"status": "NOT_EXECUTABLE"}}
    if not _is_authoritative(risk_evidence):
        return {"status": "NOT_EXECUTABLE", "reason": "RISK_NOT_PRODUCTION_AUTHORIZED", "execution_plan": {"status": "NOT_EXECUTABLE"}}

    tiz = dict(tiz_evidence or {})
    tiz_available = _is_authoritative(tiz)
    tiz_state = str(tiz.get("process_state") or tiz.get("process_gate") or tiz.get("status") or "NOT_EVALUABLE").upper()

    brain_spec = importlib.util.spec_from_file_location("gate3c_decision_brain", ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py")
    if not brain_spec or not brain_spec.loader:
        raise RuntimeError("cannot load recovered Decision Brain")
    brain = importlib.util.module_from_spec(brain_spec)
    sys.modules["gate3c_decision_brain"] = brain
    brain_spec.loader.exec_module(brain)

    result = assemble_decision_event(
        decision_brain_module=brain,
        row=row,
        query_as_of=query_as_of,
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence={
            **tiz,
            "authoritative": tiz_available,
            "process_state": tiz_state,
            "metadata_only": True,
        },
        risk_evidence=risk_evidence,
        historical_evidence=historical_evidence,
        source_rule_ids=list(source_rule_ids or []),
        entry_price=entry_price,
        atr=atr,
        mode=mode,
        provenance={
            "bridge": "full_brain_runtime_bridge_v1",
            "tiz_metadata_only": True,
            "tiz_authoritative": tiz_available,
        },
    )
    return _enforce_development_risk_contract(result, risk_evidence, mode=mode)


__all__ = ["run_full_brain_cycle"]
