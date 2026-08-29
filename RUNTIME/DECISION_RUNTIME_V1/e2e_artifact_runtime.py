from __future__ import annotations

"""E2E artifact runtime for the supplied project outputs.

This runner composes existing precomputed Market State, H4/H1 MTF, Nison setup,
and historical-memory artifacts into one chronological DecisionEvent stream.
It deliberately does not create new book-rule semantics.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import hashlib
import json
import pandas as pd


@dataclass(frozen=True)
class DecisionEvent:
    decision_id: str
    timestamp: str
    symbol: str
    direction: str
    status: str
    confidence: float
    reason: str
    market_state: dict[str, Any]
    mtf: dict[str, Any]
    nison: dict[str, Any]
    tiz: dict[str, Any]
    historical: dict[str, Any]
    risk: dict[str, Any]
    trade_plan: dict[str, Any]


def _stable_id(symbol: str, timestamp: pd.Timestamp, setup_id: str) -> str:
    """Build a deterministic identity for a symbol/timestamp/setup tuple.

    A timestamp alone is not unique because multiple valid setups may occur on
    the same bar; setup_id is therefore part of the identity.
    """
    return hashlib.sha256(
        f"{symbol}|{timestamp.isoformat()}|{setup_id}".encode()
    ).hexdigest()[:20]


def _load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ("timestamp", "signal_time"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
    return df


def _murphy_direction(trend: str) -> str:
    value = str(trend).upper()
    if value == "BULL_TREND":
        return "BUY"
    if value == "BEAR_TREND":
        return "SELL"
    return "NO_TRADE"


def _context_signature(row: pd.Series) -> str:
    flags = [
        ("bull_engulf", bool(row.get("bull_engulf", False))),
        ("bear_engulf", bool(row.get("bear_engulf", False))),
        ("hammer", bool(row.get("hammer", False))),
        ("shooting_star", bool(row.get("shooting_star", False))),
    ]
    candle = next((name for name, active in flags if active), "no_major_candle")
    return " / ".join(
        str(row.get(k, ""))
        for k in ["trend", "structure_event", "location", "volume_state", "volatility_state"]
    ) + f" / {candle}"


def build_e2e(root: Path, year: int = 2016) -> pd.DataFrame:
    market = _load(root / "AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv")
    mtf = _load(root / "AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1/GBPUSD_MTF_H4_H1.csv")
    nison = _load(root / "AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1/candlestick_engine/PATTERN_SIGNALS_WITH_CANDLE_CONFIRMATION.csv")
    outcomes = _load(root / "AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1/HISTORICAL_OUTCOMES.csv")

    market = market[market.timestamp.dt.year <= year].set_index("timestamp")
    mtf = mtf.set_index("timestamp")
    nison = nison[nison.signal_time.dt.year == year].sort_values("signal_time")

    events: list[DecisionEvent] = []
    for row in nison.itertuples(index=False):
        ts = row.signal_time
        if ts not in market.index or ts not in mtf.index:
            continue
        ms = market.loc[ts]
        tf = mtf.loc[ts]
        direction = _murphy_direction(ms.trend)
        nison_direction = str(row.direction).upper()
        contradiction = (
            direction in {"BUY", "SELL"}
            and nison_direction in {"BUY", "SELL"}
            and direction != nison_direction
        )
        mtf_state = str(tf.mtf_state).upper()
        if direction == "NO_TRADE":
            status, final_direction, reason = "NO_TRADE", "NO_TRADE", "MURPHY_NO_DIRECTION"
        elif contradiction:
            status, final_direction, reason = "NO_TRADE", "NO_TRADE", "NISON_DIRECTION_CONTRADICTION"
        elif mtf_state == "COUNTER_TREND":
            status, final_direction, reason = "NO_TRADE", "NO_TRADE", "MTF_COUNTER_TREND"
        else:
            final_direction = direction
            status = "EXECUTABLE" if bool(row.candlestick_confirmed) and mtf_state == "ALIGNED" else "CANDIDATE"
            reason = "MURPHY_DIRECTION_PLUS_NISON_CONTEXT"

        atr = float(ms.atr20) if pd.notna(ms.atr20) else None
        entry = float(row.entry)
        if status == "EXECUTABLE" and atr and atr > 0:
            distance = 0.75 * atr
            sl = entry - distance if final_direction == "BUY" else entry + distance
            tp = entry + 2.0 * distance if final_direction == "BUY" else entry - 2.0 * distance
            risk = {"status": "PASS", "risk_percent": 0.005, "atr": atr}
            plan = {"status": "EXECUTABLE", "entry_price": entry, "stop_loss": sl, "take_profit": tp, "rr": 2.0}
        else:
            risk = {"status": "NOT_EXECUTABLE", "risk_percent": 0.0, "atr": atr}
            plan = {"status": "NOT_EXECUTABLE"}

        sig = _context_signature(ms)
        hist = outcomes[outcomes.context_signature.eq(sig)] if "context_signature" in outcomes.columns else outcomes.iloc[0:0]
        hist_mean = hist[["return_6h", "return_12h", "return_24h", "return_48h"]].mean().dropna().to_dict() if len(hist) else {}
        confidence = 0.75 if status == "EXECUTABLE" and bool(row.candlestick_confirmed) and mtf_state == "ALIGNED" else 0.0

        events.append(
            DecisionEvent(
                decision_id=f"GBPUSD-{ts.isoformat()}-{_stable_id('GBPUSD', ts, row.setup_id)}",
                timestamp=ts.isoformat(),
                symbol="GBPUSD",
                direction=final_direction,
                status=status,
                confidence=confidence,
                reason=reason,
                market_state={
                    "trend": ms.trend,
                    "structure": ms.structure_event,
                    "location": ms.location,
                    "volume": ms.volume_state,
                    "volatility": ms.volatility_state,
                    "atr": atr,
                },
                mtf={"state": mtf_state, "h4_trend": tf.h4_trend, "h4_structure": tf.h4_structure},
                nison={
                    "setup_id": row.setup_id,
                    "direction": nison_direction,
                    "confirmed": bool(row.candlestick_confirmed),
                    "patterns": row.candlestick_patterns,
                    "contradiction": contradiction,
                },
                tiz={"role": "process_psychology_context_only", "direction_generated": False},
                historical={"context_signature": sig, "matching_outcomes": int(len(hist)), **hist_mean, "direction_generated": False},
                risk=risk,
                trade_plan=plan,
            )
        )

    return pd.DataFrame([asdict(x) for x in events])
