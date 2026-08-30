"""Canonical bridge from DECISION_RUNTIME_V1 to the existing full Decision Brain."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]


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
    if not tiz_available and mode not in {"development", "oos_evaluation"}:
        return {"status": "NOT_EXECUTABLE", "reason": "TIZ_NOT_PRODUCTION_AUTHORIZED", "execution_plan": {"status": "NOT_EXECUTABLE"}}

    brain_spec = importlib.util.spec_from_file_location("gate3c_decision_brain", ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py")
    if not brain_spec or not brain_spec.loader:
        raise RuntimeError("cannot load recovered Decision Brain")
    brain = importlib.util.module_from_spec(brain_spec)
    sys.modules["gate3c_decision_brain"] = brain
    brain_spec.loader.exec_module(brain)

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
