"""Point-in-time adapter for the existing Historical Context Memory V1.

This is a transport/validation boundary only. It does not generate direction,
trade commands, thresholds, or tuning. Candidates are restricted to the same
pair/context and strictly earlier timestamps than the canonical query event,
preventing self-match and future leakage.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_COLUMNS = (
    "pair",
    "timestamp",
    "close",
    "trend",
    "structure_event",
    "location",
    "volume_state",
    "volatility_state",
    "candle_tag",
    "context_signature",
)


@dataclass(frozen=True)
class PITMemoryResult:
    status: str
    query_as_of: str
    pair: str
    context_signature: str
    candidate_count: int
    latest_candidate_timestamp: str | None
    excluded_future_count: int
    excluded_self_count: int
    rows: tuple[dict[str, Any], ...]


def _utc(value: Any) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        raise ValueError("query_as_of must be timezone-aware")
    return ts.tz_convert("UTC")


def lookup_context_pit(
    source_csv: Path,
    *,
    pair: str,
    context_signature: str,
    query_as_of: Any,
    limit: int = 50,
) -> PITMemoryResult:
    """Return only historical memory records strictly before query_as_of."""
    query = _utc(query_as_of)
    if not pair:
        raise ValueError("pair is required")
    if not context_signature:
        raise ValueError("context_signature is required")
    if limit <= 0:
        raise ValueError("limit must be positive")

    selected: list[dict[str, Any]] = []
    excluded_future = 0
    excluded_self = 0

    for chunk in pd.read_csv(source_csv, usecols=list(REQUIRED_COLUMNS), chunksize=500_000):
        chunk = chunk[
            chunk["pair"].eq(pair)
            & chunk["context_signature"].eq(context_signature)
        ].copy()
        if chunk.empty:
            continue

        chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], utc=True, errors="coerce")
        if chunk["timestamp"].isna().any():
            raise ValueError("memory source contains invalid timestamps")

        excluded_future += int((chunk["timestamp"] > query).sum())
        excluded_self += int((chunk["timestamp"] == query).sum())
        eligible = chunk[chunk["timestamp"] < query]
        if not eligible.empty:
            selected.extend(
                eligible.sort_values("timestamp", ascending=False)
                .head(limit)
                .to_dict("records")
            )

    selected = sorted(
        selected,
        key=lambda row: pd.Timestamp(row["timestamp"]),
        reverse=True,
    )[:limit]

    latest = selected[0]["timestamp"] if selected else None
    rows = tuple(
        {
            key: value.isoformat() if isinstance(value, pd.Timestamp) else value
            for key, value in row.items()
        }
        for row in selected
    )

    return PITMemoryResult(
        status="PASS" if selected else "NOT_EVALUABLE",
        query_as_of=query.isoformat(),
        pair=pair,
        context_signature=context_signature,
        candidate_count=len(rows),
        latest_candidate_timestamp=latest.isoformat() if isinstance(latest, pd.Timestamp) else (str(latest) if latest is not None else None),
        excluded_future_count=excluded_future,
        excluded_self_count=excluded_self,
        rows=rows,
    )
