"""Runtime contract for existing Memory subsystems.

This is an integration boundary only. It does not rebuild Similarity or
Context-Aware Retrieval and does not create trading direction. A caller must
supply source-backed provider callables for each memory subsystem.

Development is limited to query timestamps <= 2024-12-31. 2025 remains OOS.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

LOCKED_OOS_YEAR = 2025

Provider = Callable[[Any, Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class MemoryRuntimeReceipt:
    query_as_of: str
    development_mode: bool
    oos_2025_locked: bool
    historical_context_status: str
    historical_outcome_status: str
    similarity_status: str
    context_aware_retrieval_status: str
    memory_generated_direction: bool
    final_trade_decision_generated: bool
    lookahead_violations: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_ts(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    else:
        raise ValueError("query_as_of must be a datetime or ISO-8601 string")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _status(value: Any) -> str:
    text = str(value or "").strip().upper()
    return text or "NOT_AVAILABLE"


def _validate_evidence(payload: Mapping[str, Any] | None, query_dt: datetime) -> int:
    """Count explicit future/lookahead flags; no inference is added."""
    if not isinstance(payload, Mapping):
        return 0
    violations = int(bool(payload.get("lookahead_violation", False)))
    violations += int(bool(payload.get("future_data_used", False)))
    q = payload.get("query_as_of")
    if q:
        try:
            if _parse_ts(q) > query_dt:
                violations += 1
        except (TypeError, ValueError):
            violations += 1
    return violations


def query_existing_memory_runtime(
    *,
    query_as_of: Any,
    event: Mapping[str, Any],
    providers: Mapping[str, Provider | None],
) -> dict[str, Any]:
    """Query source-backed memory providers and package evidence-only output.

    Providers are deliberately mandatory for runtime consumption: this function
    refuses to fabricate Similarity/Retrieval data from stored snapshots.
    """
    query_dt = _parse_ts(query_as_of)
    if query_dt.year >= LOCKED_OOS_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "2025_OOS_LOCKED"}

    required = (
        "historical_context",
        "historical_outcome",
        "similarity",
        "context_aware_retrieval",
    )
    outputs: dict[str, Mapping[str, Any]] = {}
    missing: list[str] = []
    lookahead = 0

    for name in required:
        provider = providers.get(name)
        if provider is None:
            missing.append(name)
            continue
        payload = provider(query_as_of, event)
        if not isinstance(payload, Mapping):
            return {"status": "NOT_EVALUABLE", "reason": f"INVALID_PROVIDER_OUTPUT:{name}"}
        outputs[name] = dict(payload)
        lookahead += _validate_evidence(payload, query_dt)

    if missing:
        return {
            "status": "NOT_READY",
            "reason": "RUNTIME_PROVIDER_MISSING",
            "missing_providers": missing,
            "memory_role": "EVIDENCE_ONLY",
            "memory_generated_direction": False,
            "final_trade_decision_generated": False,
            "oos_2025_locked": True,
        }

    receipt = MemoryRuntimeReceipt(
        query_as_of=query_dt.isoformat(),
        development_mode=True,
        oos_2025_locked=True,
        historical_context_status=_status(outputs["historical_context"].get("status")),
        historical_outcome_status=_status(outputs["historical_outcome"].get("status")),
        similarity_status=_status(outputs["similarity"].get("status")),
        context_aware_retrieval_status=_status(outputs["context_aware_retrieval"].get("status")),
        memory_generated_direction=False,
        final_trade_decision_generated=False,
        lookahead_violations=lookahead,
    )

    return {
        "status": "PASS",
        "memory_role": "EVIDENCE_ONLY",
        "sources": outputs,
        "receipt": receipt.to_dict(),
        "memory_generated_direction": False,
        "final_trade_decision_generated": False,
        "2025_used_for_tuning": False,
        "historical_memory_used_for_direction": False,
    }
