"""Source-locked bridge for existing British Pound futures OI evidence.

This module adapts the already-built project OI alignment output into the
canonical Evidence Architecture V1 record shape. It does not fetch data,
change Murphy semantics, infer missing OI, or create proxies.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence
import csv

SOURCE = "CFTC_FUTURES_ONLY"
INSTRUMENT = "GBP_FUTURES_096742"
QUALITY_AVAILABLE = "AUTHORITATIVE"
QUALITY_MISSING = "MISSING"
STATUS_AVAILABLE = "AVAILABLE"
STATUS_NOT_EVALUABLE = "NOT_EVALUABLE"
STATUS_INVALID = "NOT_AVAILABLE"

_REQUIRED_ALIASES = {
    "event_time": ("bar_close_timestamp", "event_time", "timestamp"),
    "available_time": (
        "safe_availability_timestamp",
        "oi_safe_availability_timestamp",
        "available_time",
    ),
    "oi_direction": ("oi_direction",),
    "open_interest": ("open_interest", "oi"),
    "oi_change": ("oi_change", "open_interest_change"),
}


def _pick(row: Mapping[str, Any], aliases: Sequence[str]) -> Any:
    for key in aliases:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def _parse_dt(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def adapt_row(row: Mapping[str, Any], *, source_file: str) -> Dict[str, Any]:
    """Convert one existing aligned OI row into one canonical evidence record."""
    event_raw = _pick(row, _REQUIRED_ALIASES["event_time"])
    avail_raw = _pick(row, _REQUIRED_ALIASES["available_time"])
    oi_dir = _pick(row, _REQUIRED_ALIASES["oi_direction"])
    oi_value = _pick(row, _REQUIRED_ALIASES["open_interest"])
    oi_change = _pick(row, _REQUIRED_ALIASES["oi_change"])

    if event_raw is None or avail_raw is None:
        return {
            "evidence_id": f"GBP_FUTURES_OI_096742:{event_raw or 'UNKNOWN'}",
            "event_time": str(event_raw or "1970-01-01T00:00:00+00:00"),
            "available_time": str(avail_raw or "1970-01-01T00:00:00+00:00"),
            "source": SOURCE,
            "instrument": INSTRUMENT,
            "feature": "oi_direction",
            "value": None,
            "quality": QUALITY_MISSING,
            "status": STATUS_NOT_EVALUABLE,
            "source_event_id": None,
            "latency_seconds": None,
            "lineage": [source_file, "OPEN_INTEREST_V1", "MURPHY_0021_0023"],
            "notes": "Missing event_time or safe_availability_timestamp; no inference permitted.",
        }

    event_time = _parse_dt(event_raw)
    available_time = _parse_dt(avail_raw)
    latency = (available_time - event_time).total_seconds()

    if available_time > event_time:
        return {
            "evidence_id": f"GBP_FUTURES_OI_096742:{event_time.isoformat()}",
            "event_time": event_time.isoformat(),
            "available_time": available_time.isoformat(),
            "source": SOURCE,
            "instrument": INSTRUMENT,
            "feature": "oi_direction",
            "value": {"oi_direction": oi_dir, "open_interest": oi_value, "oi_change": oi_change},
            "quality": "INVALID",
            "status": STATUS_INVALID,
            "source_event_id": None,
            "latency_seconds": latency,
            "lineage": [source_file, "OPEN_INTEREST_V1", "MURPHY_0021_0023"],
            "notes": "Existing alignment record violates point-in-time availability; record is rejected.",
        }

    if oi_dir not in {"UP", "DOWN", "FLAT"}:
        status = STATUS_NOT_EVALUABLE
        quality = QUALITY_MISSING
        notes = "OI direction unavailable; preserve NOT_EVALUABLE and fail-closed."
    else:
        status = STATUS_AVAILABLE
        quality = QUALITY_AVAILABLE
        notes = "Existing source-locked 096742 futures OI; no proxy and no rule-semantic changes."

    return {
        "evidence_id": f"GBP_FUTURES_OI_096742:{event_time.isoformat()}:{oi_dir or 'NA'}",
        "event_time": event_time.isoformat(),
        "available_time": available_time.isoformat(),
        "source": SOURCE,
        "instrument": INSTRUMENT,
        "feature": "oi_direction",
        "value": {"oi_direction": oi_dir, "open_interest": oi_value, "oi_change": oi_change},
        "quality": quality,
        "status": status,
        "source_event_id": f"096742:{event_time.date().isoformat()}",
        "latency_seconds": max(0.0, latency),
        "lineage": [source_file, "OPEN_INTEREST_V1", "MURPHY_0021_0023"],
        "notes": notes,
    }


def adapt_csv(csv_path: str | Path) -> list[Dict[str, Any]]:
    """Adapt an existing aligned OI CSV without changing or filling its data."""
    path = Path(csv_path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows: Iterable[Mapping[str, Any]] = csv.DictReader(handle)
        return [adapt_row(row, source_file=str(path)) for row in rows]
