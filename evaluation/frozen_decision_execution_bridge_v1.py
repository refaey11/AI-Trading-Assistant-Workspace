"""Frozen Decision -> Execution Evaluation Bridge V1.

This is an evaluation boundary only. It does not modify Decision Brain V1,
rebuild rules, create thresholds, or let Similarity/TIZ generate direction.

The bridge consumes already-produced decision/risk/process fields and returns
an auditable eligibility state for an execution evaluator.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable
import json

ALLOWLIST_PATH = Path(__file__).resolve().parents[1] / "governance" / "DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
VALID_DIRECTIONS = {"LONG", "SHORT", "NO_TRADE"}


def _load_allowlist() -> set[str]:
    with ALLOWLIST_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    ids = set(payload.get("verified_runtime", {}).get("MURPHY", []))
    ids.update(payload.get("verified_runtime", {}).get("NISON", []))
    return ids


def _validate_rule_ids(rule_ids: Iterable[str]) -> None:
    allowed = _load_allowlist()
    unknown = sorted(set(rule_ids) - allowed)
    if unknown:
        raise ValueError(f"RULE_REJECTED_OUTSIDE_ALLOWLIST: {unknown}")


def evaluate_entry_eligibility(decision: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate an already-produced Decision Brain output without generating it.

    Required hard gates:
    - final direction must already exist (LONG/SHORT/NO_TRADE)
    - process state must be READY for execution
    - risk_engine.risk_pass must be True for execution
    - all referenced source rule IDs must be in the frozen allowlist
    """
    direction = decision.get("direction")
    if direction not in VALID_DIRECTIONS:
        return {"status": "NOT_EVALUABLE", "execution_allowed": False, "reason": "INVALID_DIRECTION"}

    _validate_rule_ids(decision.get("source_rule_ids", []))

    if direction == "NO_TRADE":
        return {"status": "NO_TRADE", "execution_allowed": False, "reason": "BRAIN_NO_TRADE"}

    trading_zone = decision.get("trading_zone", {}) or {}
    risk_engine = decision.get("risk_engine", {}) or {}

    if trading_zone.get("process_state") != "READY":
        return {"status": "BLOCKED", "execution_allowed": False, "reason": "PROCESS_GATE"}

    if risk_engine.get("risk_pass") is not True:
        return {"status": "BLOCKED", "execution_allowed": False, "reason": "RISK_GATE"}

    return {
        "status": "EXECUTABLE",
        "execution_allowed": True,
        "direction": direction,
        "risk_pass": True,
        "process_state": "READY",
    }


def validate_oos_context(*, year: int, mode: str, tuning: bool = False, calibration: bool = False,
                         threshold_selection: bool = False, future_data: bool = False) -> Dict[str, Any]:
    """Enforce the frozen 2025 OOS boundary."""
    if year != 2025 or mode != "oos_evaluation":
        return {"status": "REJECTED", "reason": "2025_OOS_ONLY"}
    if any((tuning, calibration, threshold_selection, future_data)):
        return {"status": "REJECTED", "reason": "OOS_INTEGRITY_VIOLATION"}
    return {"status": "ACCEPTED", "year": 2025, "mode": mode}
