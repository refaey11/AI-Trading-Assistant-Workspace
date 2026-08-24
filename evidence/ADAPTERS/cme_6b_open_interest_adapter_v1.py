from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class CME6BOIRecord:
    """Authoritative CME 6B OI observation with explicit point-in-time availability."""

    event_time: datetime
    available_time: datetime
    open_interest: float
    source: str = "CME_6B"
    feature: str = "open_interest"
    quality: str = "AUTHORITATIVE"

    def as_evidence(self) -> dict[str, Any]:
        return {
            "event_time": self.event_time.isoformat(),
            "available_time": self.available_time.isoformat(),
            "source": self.source,
            "feature": self.feature,
            "value": self.open_interest,
            "quality": self.quality,
            "status": "USABLE_POINT_IN_TIME",
            "lineage": {
                "instrument": "6B",
                "contract_family": "British Pound futures",
                "vendor": "CME Group",
            },
        }


def _dt(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise TypeError("timestamp must be datetime or ISO-8601 string")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def adapt_cme_6b_oi(rows: Iterable[Mapping[str, Any]]) -> list[CME6BOIRecord]:
    """Normalize CME 6B OI rows without inventing release timing.

    Required fields: event_time, available_time, open_interest.
    The caller must supply available_time from the authoritative CME delivery
    or a documented delivery manifest. A trade date alone is insufficient.
    """

    out: list[CME6BOIRecord] = []
    for row in rows:
        event_time = _dt(row["event_time"])
        available_time = _dt(row["available_time"])
        if available_time > event_time:
            pass
        if available_time < event_time:
            raise ValueError("available_time cannot precede event_time")
        oi = float(row["open_interest"])
        if oi < 0:
            raise ValueError("open_interest must be non-negative")
        out.append(CME6BOIRecord(event_time, available_time, oi))
    return out


def latest_available_oi(
    records: Iterable[CME6BOIRecord],
    decision_time: datetime,
) -> CME6BOIRecord | None:
    """Return the latest OI whose availability is at/before the decision time."""

    eligible = [r for r in records if r.available_time <= decision_time]
    if not eligible:
        return None
    return max(eligible, key=lambda r: r.available_time)


def direction(current: CME6BOIRecord, previous: CME6BOIRecord | None) -> str:
    if previous is None:
        return "UNKNOWN"
    if current.open_interest > previous.open_interest:
        return "UP"
    if current.open_interest < previous.open_interest:
        return "DOWN"
    return "FLAT"
