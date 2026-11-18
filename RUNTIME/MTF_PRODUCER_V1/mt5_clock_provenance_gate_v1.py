"""Fail-closed per-bar MT5 clock provenance gate.

This gate does not infer broker timezone/DST and does not manufacture UTC.
A bar may enter UTC-aligned MTF processing only when its broker-server wall
clock is accompanied by an explicit per-bar offset, a versioned timezone
policy identifier, and a traceable evidence reference. The offset convention
is: broker_server_time - UTC = timezone_offset_seconds.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping


class ClockProvenanceError(ValueError):
    """Clock lineage is absent, ambiguous, or internally inconsistent."""


def _parse_server_wall_time(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ClockProvenanceError("BAR_TIME_SERVER_MISSING")
    try:
        parsed = datetime.fromisoformat(value.strip())
    except ValueError as exc:
        raise ClockProvenanceError("BAR_TIME_SERVER_INVALID") from exc
    if parsed.tzinfo is not None:
        raise ClockProvenanceError("BAR_TIME_SERVER_MUST_BE_UNOFFSET_WALL_TIME")
    return parsed


def _parse_aware_utc(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ClockProvenanceError(f"{field}_MISSING")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ClockProvenanceError(f"{field}_INVALID") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ClockProvenanceError(f"{field}_MUST_BE_TIMEZONE_AWARE")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class VerifiedClockLineage:
    bar_time_server: datetime
    bar_time_utc: datetime
    observed_at_utc: datetime
    timezone_policy_id: str
    timezone_evidence_ref: str
    timezone_offset_seconds: int


def verify_bar_clock_lineage(record: Mapping[str, Any]) -> VerifiedClockLineage:
    if not isinstance(record, Mapping):
        raise ClockProvenanceError("RECORD_NOT_MAPPING")

    if record.get("bar_time_source_clock") != "BROKER_SERVER":
        raise ClockProvenanceError("BAR_TIME_SOURCE_CLOCK_NOT_BROKER_SERVER")

    server_time = _parse_server_wall_time(record.get("bar_time_server"))
    utc_time = _parse_aware_utc(record.get("bar_time_utc"), "BAR_TIME_UTC")
    observed_at = _parse_aware_utc(record.get("observed_at_utc"), "OBSERVED_AT_UTC")

    policy_id = record.get("timezone_policy_id")
    evidence_ref = record.get("timezone_evidence_ref")
    if not isinstance(policy_id, str) or not policy_id.strip():
        raise ClockProvenanceError("TIMEZONE_POLICY_ID_MISSING")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise ClockProvenanceError("TIMEZONE_EVIDENCE_REF_MISSING")

    offset = record.get("timezone_offset_seconds")
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise ClockProvenanceError("TIMEZONE_OFFSET_SECONDS_INVALID")
    if abs(offset) > 18 * 60 * 60:
        raise ClockProvenanceError("TIMEZONE_OFFSET_SECONDS_OUT_OF_RANGE")

    expected_utc = (server_time - timedelta(seconds=offset)).replace(tzinfo=timezone.utc)
    if utc_time != expected_utc:
        raise ClockProvenanceError("BAR_TIME_UTC_OFFSET_MISMATCH")

    if observed_at < utc_time:
        raise ClockProvenanceError("OBSERVATION_PRECEDES_BAR_OPEN")

    return VerifiedClockLineage(
        bar_time_server=server_time,
        bar_time_utc=utc_time,
        observed_at_utc=observed_at,
        timezone_policy_id=policy_id.strip(),
        timezone_evidence_ref=evidence_ref.strip(),
        timezone_offset_seconds=offset,
    )
