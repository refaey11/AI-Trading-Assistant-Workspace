"""Fail-closed validation for MT5 raw bars with explicit clock provenance.

CopyRates/MqlRates bar timestamps are represented as UTC timestamps by MT5's
Python integration contract. They are retained as such; no broker-server
timezone conversion is attempted. Server and host clock values are separate
observations and are never used as historical conversion rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any, Iterable, Mapping

TIMEFRAMES = {"M5", "M15", "M30", "H1", "H4", "D1"}
REQUIRED_NUMERIC = ("open", "high", "low", "close", "tick_volume", "real_volume", "spread_points")
REQUIRED_TEXT = (
    "symbol", "timeframe", "terminal_time_server", "terminal_time_current_server",
    "broker_server_id", "source_id", "capture_version",
)
REQUIRED_UTC = ("bar_time_mt5_utc", "host_gmt_estimate_utc")


class CaptureValidationError(ValueError):
    """A source record is incomplete, ambiguous, stale, or internally invalid."""


def _aware_utc(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CaptureValidationError(f"{field}:MISSING")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise CaptureValidationError(f"{field}:INVALID_ISO8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CaptureValidationError(f"{field}:NAIVE_TIMESTAMP_REJECTED")
    return parsed.astimezone(timezone.utc)


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise CaptureValidationError(f"{field}:BOOLEAN_NOT_NUMERIC")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise CaptureValidationError(f"{field}:MISSING_OR_NON_NUMERIC") from exc
    if not math.isfinite(number):
        raise CaptureValidationError(f"{field}:NON_FINITE")
    return number


def canonical_payload_hash(record: Mapping[str, Any]) -> str:
    payload = {k: v for k, v in record.items() if k != "payload_hash"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ValidatedBar:
    symbol: str
    timeframe: str
    bar_time_mt5_utc: datetime
    host_gmt_estimate_utc: datetime
    payload_hash: str


def validate_raw_bar(record: Mapping[str, Any]) -> ValidatedBar:
    if not isinstance(record, Mapping):
        raise CaptureValidationError("RECORD_NOT_MAPPING")

    for field in REQUIRED_TEXT:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise CaptureValidationError(f"{field}:MISSING")

    symbol = record["symbol"].strip().upper()
    timeframe = record["timeframe"].strip().upper()
    if timeframe not in TIMEFRAMES:
        raise CaptureValidationError("UNSUPPORTED_TIMEFRAME")
    if not isinstance(record.get("is_closed"), bool) or record["is_closed"] is not True:
        raise CaptureValidationError("UNFINISHED_BAR_REJECTED")

    times = {field: _aware_utc(record.get(field), field) for field in REQUIRED_UTC}
    bar_time = times["bar_time_mt5_utc"]
    host_gmt_estimate = times["host_gmt_estimate_utc"]

    for field in REQUIRED_NUMERIC:
        _number(record.get(field), field)
    o, h, low, c = (_number(record.get(k), k) for k in ("open", "high", "low", "close"))
    if low > min(o, c) or h < max(o, c) or low > h:
        raise CaptureValidationError("OHLC_GEOMETRY_INVALID")

    volume_type = record.get("volume_type")
    if volume_type not in {"TICK", "REAL", "BOTH", "UNAVAILABLE"}:
        raise CaptureValidationError("VOLUME_TYPE_INVALID")
    if volume_type == "UNAVAILABLE" and (
        _number(record.get("tick_volume"), "tick_volume") != 0
        or _number(record.get("real_volume"), "real_volume") != 0
    ):
        raise CaptureValidationError("UNAVAILABLE_VOLUME_MUST_NOT_CARRY_VALUES")

    expected_hash = canonical_payload_hash(record)
    supplied_hash = record.get("payload_hash")
    if supplied_hash is not None and supplied_hash != expected_hash:
        raise CaptureValidationError("PAYLOAD_HASH_MISMATCH")

    return ValidatedBar(
        symbol=symbol,
        timeframe=timeframe,
        bar_time_mt5_utc=bar_time,
        host_gmt_estimate_utc=host_gmt_estimate,
        payload_hash=expected_hash,
    )


def validate_batch(records: Iterable[Mapping[str, Any]]) -> list[ValidatedBar]:
    validated: list[ValidatedBar] = []
    seen: dict[tuple[str, str, datetime], str] = {}
    for record in records:
        bar = validate_raw_bar(record)
        key = (bar.symbol, bar.timeframe, bar.bar_time_mt5_utc)
        prior_hash = seen.get(key)
        if prior_hash is not None:
            if prior_hash != bar.payload_hash:
                raise CaptureValidationError("CONFLICTING_DUPLICATE_BAR")
            continue
        seen[key] = bar.payload_hash
        validated.append(bar)
    return validated
