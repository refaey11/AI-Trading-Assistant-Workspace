from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping
import hashlib
import json


MODES = {"BACKTEST", "PAPER", "DEMO", "LIVE"}
DIRECTIONS = {"BUY", "SELL", "NO_TRADE"}


@dataclass(frozen=True)
class MarketSnapshot:
    timestamp: str
    symbol: str
    values: Mapping[str, Any]


@dataclass(frozen=True)
class DecisionEvent:
    decision_id: str
    timestamp: str
    symbol: str
    mode: str
    direction: str
    confidence: float
    status: str
    reason: str
    evidence: Mapping[str, Any]
    gates: Mapping[str, Any]
    execution_plan: Mapping[str, Any]
    provenance: Mapping[str, Any]


def _stable_id(snapshot: MarketSnapshot) -> str:
    payload = json.dumps(
        {"timestamp": snapshot.timestamp, "symbol": snapshot.symbol, "values": snapshot.values},
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:20]


def _norm_direction(value: Any) -> str:
    v = str(value or "").strip().upper()
    if v in {"BULL", "BULLISH", "BUY"}:
        return "BUY"
    if v in {"BEAR", "BEARISH", "SELL"}:
        return "SELL"
    return "NO_TRADE"


def _required(mapping: Mapping[str, Any], name: str) -> Any:
    if name not in mapping or mapping[name] is None:
        raise ValueError(f"missing required evidence: {name}")
    return mapping[name]


def build_decision_event(
    *,
    snapshot: MarketSnapshot,
    mode: str,
    brain_assessment: Mapping[str, Any],
    murphy_evidence: Mapping[str, Any],
    nison_evidence: Mapping[str, Any],
    tiz_evidence: Mapping[str, Any],
    risk_evidence: Mapping[str, Any],
    execution_plan: Mapping[str, Any] | None = None,
    historical_evidence: Mapping[str, Any] | None = None,
    provenance: Mapping[str, Any] | None = None,
) -> DecisionEvent:
    mode = str(mode).upper()
    if mode not in MODES:
        raise ValueError(f"unsupported mode: {mode}")

    # Fail closed: the runtime cannot manufacture a missing decision source.
    direction = _norm_direction(_required(brain_assessment, "directional_bias"))
    confidence = float(brain_assessment.get("confidence", 0.0) or 0.0)
    murphy_status = str(murphy_evidence.get("status", "")).upper()
    risk_pass = bool(risk_evidence.get("risk_pass", False))
    nison_contradiction = bool(nison_evidence.get("contradiction", False))
    process_state = str(
        tiz_evidence.get("process_state")
        or tiz_evidence.get("process_gate")
        or tiz_evidence.get("status")
        or "NOT_EVALUABLE"
    ).upper()

    reasons: list[str] = []
    status = "NO_TRADE"
    final_direction = direction

    if murphy_status != "PASS":
        final_direction = "NO_TRADE"
        reasons.append("MURPHY_CONTEXT_NOT_PASS")
    elif not risk_pass:
        final_direction = "NO_TRADE"
        reasons.append("RISK_GATE_FAIL")
    elif nison_contradiction:
        final_direction = "NO_TRADE"
        reasons.append("NISON_CONTRADICTION")
    elif process_state not in {"READY", "PASS", "AVAILABLE"}:
        final_direction = "NO_TRADE"
        reasons.append("PROCESS_GATE_NOT_READY")
    elif direction not in {"BUY", "SELL"}:
        final_direction = "NO_TRADE"
        reasons.append("BRAIN_DIRECTION_NOT_EXECUTABLE")
    else:
        status = "APPROVED"
        reasons.append("ALL_HARD_GATES_PASS")

    if execution_plan and final_direction in {"BUY", "SELL"}:
        if str(execution_plan.get("status", "")).upper() != "EXECUTABLE":
            status = "NO_TRADE"
            final_direction = "NO_TRADE"
            reasons.append("EXECUTION_PLAN_NOT_EXECUTABLE")

    if final_direction != "NO_TRADE":
        status = "APPROVED"

    event = DecisionEvent(
        decision_id=f"{snapshot.symbol}-{snapshot.timestamp}-{_stable_id(snapshot)}",
        timestamp=snapshot.timestamp,
        symbol=snapshot.symbol,
        mode=mode,
        direction=final_direction,
        confidence=confidence if final_direction != "NO_TRADE" else 0.0,
        status=status,
        reason=";".join(reasons),
        evidence={
            "brain": dict(brain_assessment),
            "murphy": dict(murphy_evidence),
            "nison": dict(nison_evidence),
            "tiz": dict(tiz_evidence),
            "historical": dict(historical_evidence or {}),
        },
        gates={
            "murphy": murphy_status,
            "risk": "PASS" if risk_pass else "FAIL",
            "nison_contradiction": nison_contradiction,
            "process": process_state,
        },
        execution_plan=dict(execution_plan or {}),
        provenance={
            **dict(provenance or {}),
            "runtime": "DECISION_RUNTIME_V1",
            "runtime_semantics": "orchestration_only",
            "oos_tuning": False,
        },
    )
    return event


def to_dict(event: DecisionEvent) -> dict[str, Any]:
    return asdict(event)


if __name__ == "__main__":
    print("Decision Runtime V1 loaded: orchestration-only boundary")
