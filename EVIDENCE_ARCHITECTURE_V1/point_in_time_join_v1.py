from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class JoinedEvidence:
    feature: str
    value: Any
    evidence_id: str
    event_time: datetime
    available_time: datetime
    source: str
    quality: str


def parse_dt(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def join_point_in_time(
    records: Iterable[Dict[str, Any]],
    decision_time: str,
    *,
    required_features: Iterable[str],
    allowed_qualities: Iterable[str] = ("AUTHORITATIVE", "VALIDATED", "DERIVED"),
) -> Dict[str, Any]:
    """Select only evidence that was actually available by the decision time.

    Missing required evidence is fail-closed. No proxy substitution is performed here.
    """
    T = parse_dt(decision_time)
    allowed = set(allowed_qualities)
    eligible: List[Dict[str, Any]] = []
    for record in records:
        if record.get("status") != "AVAILABLE":
            continue
        if record.get("quality") not in allowed:
            continue
        if parse_dt(record["available_time"]) > T:
            continue
        eligible.append(record)

    selected: Dict[str, JoinedEvidence] = {}
    for record in sorted(eligible, key=lambda r: parse_dt(r["available_time"])):
        selected[record["feature"]] = JoinedEvidence(
            feature=record["feature"],
            value=record.get("value"),
            evidence_id=record["evidence_id"],
            event_time=parse_dt(record["event_time"]),
            available_time=parse_dt(record["available_time"]),
            source=record["source"],
            quality=record["quality"],
        )

    required = list(required_features)
    missing = [feature for feature in required if feature not in selected]
    if missing:
        return {
            "status": "NOT_EVALUABLE",
            "decision_time": T.isoformat(),
            "selected": {},
            "missing_features": missing,
            "reason": "Required evidence was not available by decision time.",
        }

    return {
        "status": "AVAILABLE",
        "decision_time": T.isoformat(),
        "selected": {k: vars(v) for k, v in selected.items()},
        "missing_features": [],
    }
