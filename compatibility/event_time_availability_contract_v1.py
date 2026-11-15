"""Fail-closed event-time availability contract.

This module validates source metadata only. It does not infer timestamp semantics,
shift bars, calculate indicators, generate direction, or authorize a trade.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

TIME_FIELDS = (
    "source_timestamp",
    "bar_open_time",
    "bar_close_time",
    "available_at",
)
LABEL_SEMANTICS = {"BAR_OPEN", "BAR_CLOSE", "EVALUATION_TIME"}


def _parse_aware(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"INVALID_{field.upper()}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"INVALID_{field.upper()}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"TIMEZONE_REQUIRED_{field.upper()}")
    return parsed.astimezone(timezone.utc)


def validate_evidence_timing(
    evidence: Mapping[str, Any],
    decision_time: str,
) -> dict[str, Any]:
    """Validate that one evidence record is closed and available by decision_time.

    Required metadata:
      source_id, producer_id, source_ref, timestamp_label_semantics,
      source_timestamp, bar_open_time, bar_close_time, available_at.

    The source timestamp label must explicitly match the declared semantics.
    Evidence is eligible only when bar_close_time <= available_at <= decision_time.
    """
    required = (
        "source_id",
        "producer_id",
        "source_ref",
        "timestamp_label_semantics",
        *TIME_FIELDS,
    )
    missing = [key for key in required if evidence.get(key) is None or evidence.get(key) == ""]
    if missing:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_MISSING_TIME_METADATA",
            "missing_fields": missing,
            "source_id": evidence.get("source_id"),
            "decision_time": decision_time,
        }

    semantics = str(evidence["timestamp_label_semantics"]).upper()
    if semantics not in LABEL_SEMANTICS:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_UNKNOWN_TIMESTAMP_SEMANTICS",
            "source_id": evidence.get("source_id"),
            "timestamp_label_semantics": semantics,
        }

    try:
        decision = _parse_aware(decision_time, "decision_time")
        source_ts = _parse_aware(evidence["source_timestamp"], "source_timestamp")
        bar_open = _parse_aware(evidence["bar_open_time"], "bar_open_time")
        bar_close = _parse_aware(evidence["bar_close_time"], "bar_close_time")
        available = _parse_aware(evidence["available_at"], "available_at")
    except ValueError as exc:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_INVALID_TIME_METADATA",
            "detail": str(exc),
            "source_id": evidence.get("source_id"),
        }

    expected_label = {
        "BAR_OPEN": bar_open,
        "BAR_CLOSE": bar_close,
        "EVALUATION_TIME": available,
    }[semantics]
    if source_ts != expected_label:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_TIMESTAMP_LABEL_MISMATCH",
            "source_id": evidence["source_id"],
            "timestamp_label_semantics": semantics,
        }

    if not bar_open < bar_close or available < bar_close:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_INVALID_TIME_ORDER",
            "source_id": evidence["source_id"],
        }
    if bar_close > decision:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_BAR_NOT_CLOSED_AT_DECISION",
            "source_id": evidence["source_id"],
            "bar_close_time": bar_close.isoformat(),
            "decision_time": decision.isoformat(),
        }
    if available > decision:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_EVIDENCE_NOT_YET_AVAILABLE",
            "source_id": evidence["source_id"],
            "available_at": available.isoformat(),
            "decision_time": decision.isoformat(),
        }

    return {
        "status": "ELIGIBLE",
        "reason": "SOURCE_CLOSED_AND_AVAILABLE_AS_OF_DECISION",
        "source_id": evidence["source_id"],
        "producer_id": evidence["producer_id"],
        "source_ref": evidence["source_ref"],
        "timestamp_label_semantics": semantics,
        "source_timestamp": source_ts.isoformat(),
        "bar_open_time": bar_open.isoformat(),
        "bar_close_time": bar_close.isoformat(),
        "available_at": available.isoformat(),
        "decision_time": decision.isoformat(),
    }


def validate_event_evidence_bundle(
    evidence_records: Iterable[Mapping[str, Any]],
    decision_time: str,
    required_sources: Iterable[str],
) -> dict[str, Any]:
    """Fail closed unless every required source has valid available evidence."""
    records = list(evidence_records)
    required = list(required_sources)
    results = [validate_evidence_timing(item, decision_time) for item in records]
    present = {str(item.get("source_id")) for item in records}
    missing_sources = [source for source in required if source not in present]
    blocked = [item for item in results if item["status"] != "ELIGIBLE"]
    if missing_sources or blocked:
        return {
            "status": "NOT_EVALUABLE",
            "reason": "BLOCKED_EVENT_EVIDENCE_TIME_CONTRACT",
            "missing_sources": missing_sources,
            "evidence_results": results,
        }
    return {
        "status": "ELIGIBLE_FOR_DOWNSTREAM_EVALUATION",
        "reason": "ALL_REQUIRED_EVIDENCE_CLOSED_AND_AVAILABLE",
        "required_sources": required,
        "evidence_results": results,
    }
