"""Fail-closed structural gate for MTF Producer V2 evidence envelopes.

This module validates envelope shape, aware timestamps, availability ordering,
payload hashes, six-timeframe coverage, and as-of causality. It does NOT
authenticate broker-clock truth or the provenance attestation. A structurally
valid envelope is never production-authorized by this module.
"""
from __future__ import annotations

from datetime import datetime
import re
from typing import Any, Iterable

REQUIRED_TIMEFRAMES = ("M5", "M15", "M30", "H1", "H4", "D1")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class EvidenceEnvelopeError(ValueError):
    """Raised when evidence is incomplete, malformed, or non-causal."""


def _aware(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise EvidenceEnvelopeError(f"{field} must be a non-empty ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceEnvelopeError(f"{field} is not valid ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EvidenceEnvelopeError(f"{field} must include an explicit UTC offset")
    return parsed


def _hash(value: Any, field: str) -> None:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise EvidenceEnvelopeError(f"{field} must be a lowercase SHA-256 hex digest")


def validate_timeframe_envelope(envelope: dict[str, Any], *, decision_time: str) -> dict[str, Any]:
    """Validate one timeframe envelope against a decision-time as-of boundary.

    Required envelope keys: symbol, timeframe, producer_version, schema_version,
    source_payload_sha256, clock_policy_id, clock_evidence_sha256, rows.
    Each row requires bar_index, bar_open_time, bar_close_time, available_at.
    """
    if not isinstance(envelope, dict):
        raise EvidenceEnvelopeError("envelope must be an object")
    required = ("symbol", "timeframe", "producer_version", "schema_version",
                "source_payload_sha256", "clock_policy_id",
                "clock_evidence_sha256", "rows")
    missing = [key for key in required if key not in envelope]
    if missing:
        raise EvidenceEnvelopeError(f"missing envelope fields: {','.join(missing)}")
    for key in ("symbol", "timeframe", "producer_version", "schema_version", "clock_policy_id"):
        if not isinstance(envelope[key], str) or not envelope[key].strip():
            raise EvidenceEnvelopeError(f"{key} must be a non-empty string")
    _hash(envelope["source_payload_sha256"], "source_payload_sha256")
    _hash(envelope["clock_evidence_sha256"], "clock_evidence_sha256")
    if envelope["timeframe"] not in REQUIRED_TIMEFRAMES:
        raise EvidenceEnvelopeError("unsupported timeframe")
    if not isinstance(envelope["rows"], list) or not envelope["rows"]:
        raise EvidenceEnvelopeError("rows must be a non-empty list")

    decision = _aware(decision_time, "decision_time")
    previous_index = None
    previous_open = None
    for position, row in enumerate(envelope["rows"]):
        if not isinstance(row, dict):
            raise EvidenceEnvelopeError(f"row {position} must be an object")
        for key in ("bar_index", "bar_open_time", "bar_close_time", "available_at"):
            if key not in row:
                raise EvidenceEnvelopeError(f"row {position} missing {key}")
        index = row["bar_index"]
        if not isinstance(index, int) or isinstance(index, bool):
            raise EvidenceEnvelopeError(f"row {position} bar_index must be an integer")
        opened = _aware(row["bar_open_time"], f"rows[{position}].bar_open_time")
        closed = _aware(row["bar_close_time"], f"rows[{position}].bar_close_time")
        available = _aware(row["available_at"], f"rows[{position}].available_at")
        if opened >= closed:
            raise EvidenceEnvelopeError(f"row {position} bar must open before it closes")
        if available < closed:
            raise EvidenceEnvelopeError(f"row {position} cannot be available before bar close")
        if available > decision:
            raise EvidenceEnvelopeError(f"row {position} contains future evidence beyond decision_time")
        if previous_index is not None and index != previous_index + 1:
            raise EvidenceEnvelopeError("bar_index values must be contiguous and increasing")
        if previous_open is not None and opened <= previous_open:
            raise EvidenceEnvelopeError("bar open times must be strictly increasing")
        previous_index, previous_open = index, opened

    return {
        "status": "STRUCTURALLY_VALID_NOT_AUTHENTICATED",
        "symbol": envelope["symbol"],
        "timeframe": envelope["timeframe"],
        "rows_checked": len(envelope["rows"]),
        "decision_time": decision.isoformat(),
        "production_eligible": False,
        "authentication_required": True,
        "direction_generated": False,
    }


def validate_six_timeframe_bundle(
    envelopes: Iterable[dict[str, Any]], *, decision_time: str
) -> dict[str, Any]:
    """Require exactly one structurally valid envelope for each canonical TF."""
    items = list(envelopes)
    by_tf: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            raise EvidenceEnvelopeError("each timeframe envelope must be an object")
        tf = item.get("timeframe")
        if tf not in REQUIRED_TIMEFRAMES:
            raise EvidenceEnvelopeError(f"unsupported or missing timeframe: {tf}")
        if tf in by_tf:
            raise EvidenceEnvelopeError(f"duplicate timeframe: {tf}")
        by_tf[tf] = item
    missing = sorted(set(REQUIRED_TIMEFRAMES) - set(by_tf))
    extra = sorted(set(by_tf) - set(REQUIRED_TIMEFRAMES))
    if missing or extra:
        raise EvidenceEnvelopeError(f"timeframe coverage mismatch; missing={missing}; extra={extra}")
    results = {
        tf: validate_timeframe_envelope(by_tf[tf], decision_time=decision_time)
        for tf in REQUIRED_TIMEFRAMES
    }
    symbols = {by_tf[tf]["symbol"] for tf in REQUIRED_TIMEFRAMES}
    if len(symbols) != 1:
        raise EvidenceEnvelopeError("all timeframe envelopes must refer to the same symbol")
    return {
        "status": "STRUCTURALLY_VALID_NOT_AUTHENTICATED",
        "symbol": next(iter(symbols)),
        "timeframes": list(REQUIRED_TIMEFRAMES),
        "results": results,
        "production_eligible": False,
        "authentication_required": True,
        "direction_generated": False,
    }
