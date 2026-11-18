"""Strict V1.3 contract: preserve raw MT5 time; never imply UTC alignment."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import hashlib, json, math
from typing import Any, Mapping

TIMEFRAMES = {"M5", "M15", "M30", "H1", "H4", "D1"}
TEXT_FIELDS = ("symbol", "timeframe", "bar_time_source_clock", "bar_time_utc_status",
 "terminal_time_server_observed", "terminal_time_current_server_observed",
 "host_gmt_estimate_observed", "host_local_time_observed", "broker_server_id",
 "source_id", "capture_version", "volume_type")

class CaptureV13Error(ValueError):
    """V1.3 row is malformed or unsafe to use."""

def _wall_time(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CaptureV13Error(f"{field}:MISSING")
    try: return datetime.strptime(value, "%Y.%m.%d %H:%M:%S")
    except ValueError as exc: raise CaptureV13Error(f"{field}:INVALID_SERVER_WALL_TIME") from exc

def _finite(value: Any, field: str) -> float:
    if isinstance(value, bool): raise CaptureV13Error(f"{field}:BOOLEAN_NOT_NUMERIC")
    try: result = float(value)
    except (TypeError, ValueError, OverflowError) as exc: raise CaptureV13Error(f"{field}:NON_NUMERIC") from exc
    if not math.isfinite(result): raise CaptureV13Error(f"{field}:NON_FINITE")
    return result

def payload_hash(record: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "payload_hash"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class RawClockBarV13:
    symbol: str
    timeframe: str
    bar_time_epoch_seconds_raw: int
    payload_hash: str

def validate_raw_bar_v13(record: Mapping[str, Any]) -> RawClockBarV13:
    if not isinstance(record, Mapping): raise CaptureV13Error("RECORD_NOT_MAPPING")
    if "bar_time_utc" in record or "bar_time_mt5_utc" in record:
        raise CaptureV13Error("UTC_ALIGNMENT_FIELD_FORBIDDEN_IN_V1_3")
    for field in TEXT_FIELDS:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise CaptureV13Error(f"{field}:MISSING")
    if record["bar_time_source_clock"] != "MT5_MQLRATES_DATETIME_RAW":
        raise CaptureV13Error("BAR_TIME_SOURCE_CLOCK_UNSUPPORTED")
    if record["bar_time_utc_status"] != "UNVERIFIED":
        raise CaptureV13Error("BAR_TIME_MUST_REMAIN_UNVERIFIED")
    if record["capture_version"] != "1.3.0": raise CaptureV13Error("CAPTURE_VERSION_MISMATCH")
    if record.get("is_closed") is not True: raise CaptureV13Error("UNFINISHED_BAR_REJECTED")
    symbol, timeframe = record["symbol"].strip().upper(), record["timeframe"].strip().upper()
    if timeframe not in TIMEFRAMES: raise CaptureV13Error("UNSUPPORTED_TIMEFRAME")
    raw_time = record.get("bar_time_epoch_seconds_raw")
    if isinstance(raw_time, bool) or not isinstance(raw_time, int) or raw_time <= 0:
        raise CaptureV13Error("RAW_BAR_EPOCH_INVALID")
    for field in ("terminal_time_server_observed", "terminal_time_current_server_observed",
                  "host_gmt_estimate_observed", "host_local_time_observed"):
        _wall_time(record[field], field)
    prices = {key: _finite(record.get(key), key) for key in ("open", "high", "low", "close")}
    if prices["low"] > min(prices["open"], prices["close"]) or prices["high"] < max(prices["open"], prices["close"]) or prices["low"] > prices["high"]:
        raise CaptureV13Error("OHLC_GEOMETRY_INVALID")
    for field in ("tick_volume", "real_volume", "spread_points", "observed_server_minus_host_gmt_seconds"):
        value = record.get(field)
        if isinstance(value, bool) or not isinstance(value, int): raise CaptureV13Error(f"{field}:INTEGER_REQUIRED")
    if min(record["tick_volume"], record["real_volume"], record["spread_points"]) < 0:
        raise CaptureV13Error("NEGATIVE_VOLUME_OR_SPREAD")
    if record["volume_type"] not in {"TICK", "REAL", "BOTH", "UNAVAILABLE"}:
        raise CaptureV13Error("VOLUME_TYPE_INVALID")
    digest = payload_hash(record)
    if record.get("payload_hash") is not None and record["payload_hash"] != digest:
        raise CaptureV13Error("PAYLOAD_HASH_MISMATCH")
    return RawClockBarV13(symbol, timeframe, raw_time, digest)
