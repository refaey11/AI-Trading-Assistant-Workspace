from __future__ import annotations

from typing import Any, Iterable, Mapping

import pandas as pd

MURPHY_PREFIX = "MURPHY_"
NISON_PREFIX = "NISON_"


def _rows_by_timestamp(rows: Iterable[Mapping[str, Any]]) -> dict[pd.Timestamp, list[dict[str, Any]]]:
    grouped: dict[pd.Timestamp, list[dict[str, Any]]] = {}
    for raw in rows:
        ts = pd.Timestamp(raw["timestamp"])
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")
        else:
            ts = ts.tz_convert("UTC")
        grouped.setdefault(ts, []).append(dict(raw))
    return grouped


def _single_direction(directions: Iterable[Any]) -> str:
    vals = {str(v).upper() for v in directions if str(v).upper() in {"BULLISH", "BEARISH"}}
    if vals == {"BULLISH"}:
        return "BULLISH"
    if vals == {"BEARISH"}:
        return "BEARISH"
    return "UNKNOWN"


def build_profitability_events(
    *,
    timestamps: Iterable[Any],
    rule_stream: Iterable[Mapping[str, Any]],
    market_rows: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Convert the frozen 78-rule evidence stream into profitability candidates.

    This adapter does not invent missing evidence. Murphy must provide one
    unambiguous directional PASS at a timestamp. Nison may be absent, but an
    explicit contradiction blocks the candidate. Price/ATR fields come only
    from the supplied market rows.
    """
    stream = _rows_by_timestamp(rule_stream)
    market = _rows_by_timestamp(market_rows)
    out: list[dict[str, Any]] = []

    wanted_ts = sorted({pd.Timestamp(t).tz_localize("UTC") if pd.Timestamp(t).tzinfo is None else pd.Timestamp(t).tz_convert("UTC") for t in timestamps})
    for ts in wanted_ts:
        events = stream.get(ts, [])
        murphy = [r for r in events if str(r.get("rule_id", "")).startswith(MURPHY_PREFIX)]
        nison = [r for r in events if str(r.get("rule_id", "")).startswith(NISON_PREFIX)]

        murphy_pass = [r for r in murphy if str(r.get("status", "")).upper() == "PASS"]
        murphy_dirs = _single_direction(r.get("direction") for r in murphy_pass)
        nison_contradiction = any(
            str(r.get("status", "")).upper() in {"CONTRADICTORY", "CONTRADICTION", "FAIL_CONTRADICTION"}
            or str(r.get("reason", "")).upper() in {"NISON_CONTRADICTION", "CONTRADICTION"}
            for r in nison
        )
        nison_status = "CONTRADICTORY" if nison_contradiction else (
            "PASS" if any(str(r.get("status", "")).upper() == "PASS" for r in nison) else "NOT_EVALUABLE"
        )

        market_rows_at_ts = market.get(ts, [])
        price = None
        atr20 = None
        if market_rows_at_ts:
            m = market_rows_at_ts[-1]
            price = m.get("close", m.get("price"))
            atr20 = m.get("atr20", m.get("atr"))

        out.append({
            "timestamp": ts.isoformat(),
            "murphy_pass": 1 if murphy_pass else 0,
            "directional_confirmation": murphy_dirs,
            "nison_status": nison_status,
            "entry_price": price,
            "atr20": atr20,
            "candidate_source": "frozen_78_rule_stream",
            "2025_tuning": False,
        })

    return out
