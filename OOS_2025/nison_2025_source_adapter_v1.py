from __future__ import annotations

from typing import Any, Iterable, Mapping

import pandas as pd

NISON_RULE_IDS = tuple(f"NISON_{i:04d}" for i in range(1, 45))
_OHLC_ALIASES = {"open": "open", "high": "high", "low": "low", "close": "close"}
_CONTEXT_SCALARS = ("trend", "location", "volume_high")
_TREND_MAP = {"BULL_TREND": "Uptrend", "BEAR_TREND": "Downtrend", "UPTREND": "Uptrend", "DOWNTREND": "Downtrend"}


def _pick_column(frame: pd.DataFrame, name: str) -> str | None:
    return {str(c).strip().lower(): c for c in frame.columns}.get(_OHLC_ALIASES[name])


def _normalize_nison_trend(value: Any) -> Any:
    if value is None or pd.isna(value):
        return value
    text = str(value).strip()
    return _TREND_MAP.get(text.upper(), text)


def _candle_source_facts(history: list[dict[str, Any]], index: int) -> dict[str, Any]:
    """Derive only exact OHLC relationships for the requested candle."""
    c = history[index]
    facts: dict[str, Any] = {}
    if c["close"] > c["open"]:
        facts["color"] = "bullish"
    elif c["close"] < c["open"]:
        facts["color"] = "bearish"
    if index > 0:
        p = history[index - 1]
        p_lo, p_hi = min(p["open"], p["close"]), max(p["open"], p["close"])
        if p_lo <= c["open"] <= p_hi:
            facts["open_inside_previous_body"] = True
        if c["open"] > p["high"]:
            facts["gap_class"] = "gap_above_first"
        elif c["open"] < p["low"]:
            facts["gap_class"] = "gap_below_first"
        elif c["open"] > p["close"]:
            facts["gap_class"] = "gap_above_previous_close"
        elif c["open"] < p["close"]:
            facts["gap_class"] = "gap_below_previous_close"
    return facts


def build_payload_rows(bars: pd.DataFrame, context: pd.DataFrame | None = None, *, timestamp_column: str = "timestamp") -> list[dict[str, Any]]:
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
        # Runtime Candle dataclasses accept OHLC + a small shared set of categorical candle facts.
        # Keep five completed candles because NISON_0031's frozen runtime contract
        # explicitly requires a five-candle continuation structure. This change
        # only widens history availability; it does not invent formation semantics.
        enriched_history: list[dict[str, Any]] = []
        for idx, base in enumerate(history[-5:], start=max(0, len(history) - 5)):
            enriched = dict(base)
            enriched.update(_candle_source_facts(history, idx))
            enriched_history.append(enriched)
        facts: dict[str, Any] = {"candles": enriched_history}

        if ctx is not None:
            match = ctx.loc[ctx["timestamp"].eq(row["timestamp"])]
            if not match.empty:
                record = match.iloc[-1].to_dict()
                context_payload: dict[str, Any] = {}
                context_value = record.get("context")
                if isinstance(context_value, Mapping):
                    context_payload.update(context_value)
                for key in _CONTEXT_SCALARS:
                    if key in record and not pd.isna(record[key]):
                        value = _normalize_nison_trend(record[key]) if key == "trend" else record[key]
                        context_payload[key] = value
                if context_payload:
                    facts["context"] = context_payload
                candlestick_value = record.get("candlestick")
                if isinstance(candlestick_value, Mapping):
                    facts.setdefault("context", {})["candlestick"] = dict(candlestick_value)
                confirmation_value = record.get("confirmation")
                if isinstance(confirmation_value, Mapping):
                    facts["confirmation"] = dict(confirmation_value)
                for key in ("formation_confirmed", "formation_complete", "final_bullish_strong", "final_bearish_strong", "evidence_available", "role", "previous_session", "current_session", "direction"):
                    value = record.get(key)
                    if value is not None and not (isinstance(value, float) and pd.isna(value)):
                        facts.setdefault("context", {})[key] = value

        for rule_id in NISON_RULE_IDS:
            rows.append({"timestamp": row["timestamp"].isoformat(), "rule_id": rule_id, "payload": dict(facts)})
    return rows


def iter_payload_rows(rows: Iterable[Mapping[str, Any]]) -> Iterable[dict[str, Any]]:
    for row in rows:
        if "timestamp" not in row or "rule_id" not in row:
            raise ValueError("each row requires timestamp and rule_id")
        if str(row["rule_id"]) not in NISON_RULE_IDS:
            raise ValueError(f"unsupported Nison rule id: {row['rule_id']!r}")
        yield {"timestamp": row["timestamp"], "rule_id": str(row["rule_id"]), "payload": dict(row.get("payload") or {})}
