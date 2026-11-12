"""Frozen Decision -> Execution Evaluation Bridge V1.

This is an evaluation boundary only. It does not modify Decision Brain V1,
rebuild rules, create thresholds, or let Similarity/TIZ generate direction.

The bridge consumes an already-produced decision and authoritative risk
result. TIZ is not part of execution eligibility.
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

    Execution eligibility requires:
    - final direction already exists (LONG/SHORT/NO_TRADE)
    - Risk Engine hard gate passes
    - all referenced source rule IDs are in the frozen allowlist

    Any supplied trading_zone/TIZ payload is ignored for eligibility.
    """
    direction = decision.get("direction")
    if direction not in VALID_DIRECTIONS:
        return {"status": "NOT_EVALUABLE", "execution_allowed": False, "reason": "INVALID_DIRECTION"}

    _validate_rule_ids(decision.get("source_rule_ids", []))

    if direction == "NO_TRADE":
        return {"status": "NO_TRADE", "execution_allowed": False, "reason": "BRAIN_NO_TRADE"}

    risk_engine = decision.get("risk_engine", {}) or {}
    if risk_engine.get("risk_pass") is not True:
        return {"status": "BLOCKED", "execution_allowed": False, "reason": "RISK_GATE"}

    return {
        "status": "EXECUTABLE",
        "execution_allowed": True,
        "direction": direction,
        "risk_pass": True,
        "tiz_decision_authority": False,
    }


def validate_oos_context(*, year: int, mode: str, tuning: bool = False, calibration: bool = False,
                         threshold_selection: bool = False, future_data: bool = False) -> Dict[str, Any]:
    """Enforce the frozen 2025 OOS boundary."""
    if year != 2025 or mode != "oos_evaluation":
        return {"status": "REJECTED", "reason": "2025_OOS_ONLY"}
    if any((tuning, calibration, threshold_selection, future_data)):
        return {"status": "REJECTED", "reason": "OOS_INTEGRITY_VIOLATION"}
    return {"status": "ACCEPTED", "year": 2025, "mode": mode}
