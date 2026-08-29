"""Single-event Gate 3C validation scaffold.

This module intentionally contains no trading strategy logic. It validates the
shape and provenance of an already-produced canonical event before it can be
consumed by the existing decision/risk runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

REQUIRED_GROUPS = ("market", "murphy", "nison", "memory", "tiz", "risk")

@dataclass(frozen=True)
class GateResult:
    passed: bool
    checks: tuple[str, ...]
    failures: tuple[str, ...]


def _parse_as_of(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("as_of must be an ISO-8601 string")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("as_of must include timezone information")
    return dt.astimezone(timezone.utc)


def validate_single_event(event: Mapping[str, Any]) -> GateResult:
    checks: list[str] = []
    failures: list[str] = []
    if event.get("symbol") != "GBPUSD":
        failures.append("symbol must be GBPUSD for the Gate 3C fixture")
    else:
        checks.append("symbol")
    try:
        as_of = _parse_as_of(event.get("as_of"))
        checks.append("authoritative as_of")
    except ValueError as exc:
        failures.append(str(exc))
        as_of = None
    for group in REQUIRED_GROUPS:
        value = event.get(group)
        if not isinstance(value, Mapping):
            failures.append(f"{group} group missing or not an object")
            continue
        if "provenance" not in value:
            failures.append(f"{group} provenance missing")
        else:
            checks.append(f"{group} provenance")
        if as_of is not None and isinstance(value.get("as_of"), str):
            try:
                group_time = _parse_as_of(value["as_of"])
                if group_time > as_of:
                    failures.append(f"{group} is future-dated relative to event as_of")
                else:
                    checks.append(f"{group} temporal guard")
            except ValueError:
                failures.append(f"{group} as_of invalid")
    tiz = event.get("tiz")
    if isinstance(tiz, Mapping) and tiz.get("status") == "NOT_EVALUABLE":
        checks.append("TIZ explicit NOT_EVALUABLE")
    decision = event.get("decision")
    if not isinstance(decision, Mapping):
        failures.append("decision output missing")
    elif decision.get("direction") not in {"BUY", "SELL", "NO_TRADE"}:
        failures.append("decision.direction invalid")
    else:
        checks.append("decision output")
    risk = event.get("risk")
    if not isinstance(risk, Mapping) or risk.get("status") not in {"PASS", "BLOCK"}:
        failures.append("risk hard-gate result missing")
    else:
        checks.append("risk hard gate")
    trade_plan = event.get("trade_plan")
    if isinstance(risk, Mapping) and risk.get("status") == "BLOCK" and trade_plan not in (None, {}):
        failures.append("trade_plan must be absent when risk is BLOCK")
    elif isinstance(risk, Mapping):
        checks.append("trade-plan/risk consistency")
    return GateResult(not failures, tuple(checks), tuple(failures))

if __name__ == "__main__":
    fixture = {
        "symbol": "GBPUSD",
        "as_of": "2024-01-08T10:00:00Z",
        "market": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture"},
        "murphy": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture"},
        "nison": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture", "status": "ABSENT"},
        "memory": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture", "status": "ABSENT"},
        "tiz": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture", "status": "NOT_EVALUABLE"},
        "decision": {"direction": "NO_TRADE"},
        "risk": {"status": "BLOCK"},
        "trade_plan": None,
    }
    result = validate_single_event(fixture)
    print(result)
    raise SystemExit(0 if result.passed else 1)
