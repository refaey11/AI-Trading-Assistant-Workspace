from __future__ import annotations

from typing import Any, Iterable, Mapping

import pandas as pd

NISON_RULE_IDS = tuple(f"NISON_{i:04d}" for i in range(1, 45))

_OHLC_ALIASES = {
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
}

_CONTEXT_SCALARS = ("trend", "location", "volume_high")


def _pick_column(frame: pd.DataFrame, name: str) -> str | None:
    wanted = _OHLC_ALIASES[name]
    lowered = {str(c).strip().lower(): c for c in frame.columns}
    return lowered.get(wanted)


def build_payload_rows(
    bars: pd.DataFrame,
    context: pd.DataFrame | None = None,
    *,
    timestamp_column: str = "timestamp",
) -> list[dict[str, Any]]:
    """Map source-backed 2025 OHLC/context into existing Nison producer inputs.

    This adapter deliberately does not derive Nison semantics. It copies only
    raw OHLC fields and explicit context/confirmation fields already present in
    the supplied source. Missing facts remain absent and therefore fail closed
    inside the existing Nison runtime as NOT_EVALUABLE where required.
    """
    if timestamp_column not in bars.columns:
        raise ValueError(f"missing timestamp column: {timestamp_column}")
    cols = {name: _pick_column(bars, name) for name in _OHLC_ALIASES}
    missing = [name for name, col in cols.items() if col is None]
    if missing:
        raise ValueError(f"missing OHLC columns: {', '.join(missing)}")

    source = bars.copy()
    source["timestamp"] = pd.to_datetime(source[timestamp_column], utc=True)
    source = source[source["timestamp"].dt.year.eq(2025)].sort_values("timestamp")

    ctx = None
    if context is not None:
        if "timestamp" not in context.columns:
            raise ValueError("context must contain timestamp")
        ctx = context.copy()
        ctx["timestamp"] = pd.to_datetime(ctx["timestamp"], utc=True)
        ctx = ctx[ctx["timestamp"].dt.year.eq(2025)].drop_duplicates("timestamp", keep="last")

    rows: list[dict[str, Any]] = []
    history: list[dict[str, float]] = []
    for _, row in source.iterrows():
        candle = {name: float(row[col]) for name, col in cols.items()}
        history.append(candle)
        facts: dict[str, Any] = {"candles": history[-3:]}

        if ctx is not None:
            match = ctx.loc[ctx["timestamp"].eq(row["timestamp"])]
            if not match.empty:
                record = match.iloc[-1].to_dict()

                # Preserve an explicit nested context object when supplied.
                context_value = record.get("context")
                context_payload: dict[str, Any] = dict(context_value) if isinstance(context_value, Mapping) else {}
                for key in _CONTEXT_SCALARS:
                    if key in record and not pd.isna(record[key]):
                        context_payload[key] = record[key]
                if context_payload:
                    facts["context"] = context_payload

                # Confirmation is a source fact, never derived here.
                confirmation_value = record.get("confirmation")
                if isinstance(confirmation_value, Mapping):
                    facts["confirmation"] = dict(confirmation_value)

        for rule_id in NISON_RULE_IDS:
            rows.append({
                "timestamp": row["timestamp"].isoformat(),
                "rule_id": rule_id,
                "payload": dict(facts),
            })
    return rows


def iter_payload_rows(rows: Iterable[Mapping[str, Any]]) -> Iterable[dict[str, Any]]:
    """Validate the producer input contract without altering source facts."""
    for row in rows:
        if "timestamp" not in row or "rule_id" not in row:
            raise ValueError("each row requires timestamp and rule_id")
        if str(row["rule_id"]) not in NISON_RULE_IDS:
            raise ValueError(f"unsupported Nison rule id: {row['rule_id']!r}")
        payload = row.get("payload") or {}
        yield {"timestamp": row["timestamp"], "rule_id": str(row["rule_id"]), "payload": dict(payload)}
