from __future__ import annotations

from typing import Any, Iterable, Iterator, Mapping

import pandas as pd


# The adapter only packages source facts for the existing Nison evaluators.
# It does not create pattern facts, direction, or confirmation labels.
REQUIRED_OHLC = {"timestamp", "open", "high", "low", "close"}
_TREND_TRANSLATION = {"BULL_TREND": "Uptrend", "BEAR_TREND": "Downtrend"}


def _as_candle(row: pd.Series) -> dict[str, Any]:
    # Evaluator Candle contracts accept OHLC plus their declared optional
    # categorical compatibility fields; timestamp belongs to the enclosing
    # evidence row, not inside Candle(**c).
    candle = {
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
    }
    for key in ("volume", "tick_volume", "spread"):
        if key in row.index and pd.notna(row[key]):
            candle[key] = float(row[key])
    return candle


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (dict, list, tuple)):
        return bool(value)
    try:
        return bool(pd.notna(value))
    except (TypeError, ValueError):
        return True


def _context_at_timestamp(
    context: pd.DataFrame | None, ts: pd.Timestamp
) -> tuple[dict[str, Any], dict[str, Any]]:
    if context is None or context.empty or "timestamp" not in context.columns:
        return {}, {}
    c = context.copy()
    c["timestamp"] = pd.to_datetime(c["timestamp"], utc=True, errors="coerce")
    c = c.dropna(subset=["timestamp"])
    matches = c.loc[c["timestamp"].eq(ts)]
    if matches.empty:
        return {}, {}
    record = matches.iloc[-1].to_dict()
    record.pop("timestamp", None)
    explicit_confirmation = record.pop("confirmation", {})
    normalized = {k: v for k, v in record.items() if _has_value(v)}
    trend = normalized.get("trend")
    if isinstance(trend, str):
        normalized["trend"] = _TREND_TRANSLATION.get(trend, trend)
    confirmation = explicit_confirmation if isinstance(explicit_confirmation, dict) else {}
    return normalized, confirmation


def build_payload_rows(
    bars: pd.DataFrame,
    context: pd.DataFrame | None = None,
    *,
    evaluation_year: int = 2025,
    lookback_bars: int = 60,
) -> list[dict[str, Any]]:
    """Package historical source facts for the existing 44-rule Nison runtime.

    Each output row contains the current timestamp, a governed rule id, and a
    payload made only from source OHLCV candles plus any supplied context row.
    Explicit context and confirmation facts remain separate at the runtime
    boundary; neither is synthesized by this adapter.
    """
    missing = sorted(REQUIRED_OHLC - set(bars.columns))
    if missing:
        raise ValueError(f"Missing required OHLC columns: {missing}")

    src = bars.copy()
    src["timestamp"] = pd.to_datetime(src["timestamp"], utc=True, errors="coerce")
    if src["timestamp"].isna().any() or src["timestamp"].duplicated().any():
        raise ValueError("Invalid or duplicated source timestamps")
    src = src.sort_values("timestamp").reset_index(drop=True)

    out: list[dict[str, Any]] = []
    year_rows = src.loc[src["timestamp"].dt.year.eq(int(evaluation_year))]
    for idx, row in year_rows.iterrows():
        ts = row["timestamp"]
        prior = src.iloc[max(0, idx - (lookback_bars - 1)): idx + 1]
        candles = [_as_candle(r) for _, r in prior.iterrows()]
        payload_context, payload_confirmation = _context_at_timestamp(context, ts)
        for i in range(1, 45):
            rule_id = f"NISON_{i:04d}"
            payload = {"candles": candles}
            if payload_context:
                payload["context"] = payload_context
            if payload_confirmation:
                payload["confirmation"] = payload_confirmation
            out.append({"timestamp": ts.isoformat(), "rule_id": rule_id, "payload": payload})
    return out


_VALID_NISON_RULE_IDS = {f"NISON_{i:04d}" for i in range(1, 45)}


def iter_payload_rows(rows: Iterable[Mapping[str, Any]]) -> Iterator[dict[str, Any]]:
    """Yield source payload rows after validating the canonical Nison rule id.

    This compatibility iterator validates identity only; it does not infer or
    synthesize pattern, confirmation, or directional evidence.
    """
    for row in rows:
        rule_id = str(row.get("rule_id") or "")
        if rule_id not in _VALID_NISON_RULE_IDS:
            raise ValueError(f"Invalid Nison rule id: {rule_id}")
        yield dict(row)
