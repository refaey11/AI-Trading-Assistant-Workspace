from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
import pandas as pd

from MURPHY_EVALUATORS_V1.murphy_runtime_entrypoint_v1 import evaluate_rule


@dataclass(frozen=True)
class Pivot:
    index: int
    timestamp: pd.Timestamp
    available_at: pd.Timestamp
    family: str
    price: float


def strict_five_bar_pivots(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Return source-confirmed strict 5-bar pivot flags.

    A pivot centered on bar i becomes known only at bar i+2. No value from
    bars after i+2 is exposed as available at an earlier timestamp.
    """
    lows = df["low"].to_numpy(dtype=float)
    highs = df["high"].to_numpy(dtype=float)
    n = len(df)
    pivot_low = np.zeros(n, dtype=bool)
    pivot_high = np.zeros(n, dtype=bool)
    for i in range(2, n - 2):
        pivot_low[i] = (
            lows[i] < lows[i - 1]
            and lows[i] < lows[i - 2]
            and lows[i] < lows[i + 1]
            and lows[i] < lows[i + 2]
        )
        pivot_high[i] = (
            highs[i] > highs[i - 1]
            and highs[i] > highs[i - 2]
            and highs[i] > highs[i + 1]
            and highs[i] > highs[i + 2]
        )
    return pivot_low, pivot_high


def _line_price(t1: pd.Timestamp, p1: float, t2: pd.Timestamp, p2: float, tx: pd.Timestamp) -> float:
    dt = (t2 - t1).total_seconds()
    if dt == 0:
        raise ValueError("Trendline anchor timestamps must differ.")
    return p1 + (p2 - p1) * ((tx - t1).total_seconds() / dt)


def _line_builder(
    df: pd.DataFrame,
    rule_id: str,
    anchor_1: Pivot,
    anchor_2: Pivot,
) -> Callable[[Any], float]:
    if rule_id == "MURPHY_0006":
        p1, p2 = anchor_1.price, anchor_2.price
    else:
        p1, p2 = anchor_1.price, anchor_2.price

    def line_price_at(value: Any) -> float:
        ts = pd.Timestamp(value)
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")
        else:
            ts = ts.tz_convert("UTC")
        return _line_price(anchor_1.timestamp, p1, anchor_2.timestamp, p2, ts)

    return line_price_at


def _valid_anchor_pair(rule_id: str, a1: Pivot, a2: Pivot) -> bool:
    if a1.family != a2.family:
        return False
    if rule_id == "MURPHY_0006":
        return a2.price > a1.price
    return a2.price < a1.price


def _events_for_runtime(
    df: pd.DataFrame,
    rule_id: str,
    line_available_at: pd.Timestamp,
    third: Pivot,
    reaction: Pivot,
    start_index: int,
    end_index: int,
) -> list[dict[str, Any]]:
    family = "LOW" if rule_id == "MURPHY_0006" else "HIGH"
    opposite = "HIGH" if family == "LOW" else "LOW"
    events: list[dict[str, Any]] = [
        {
            "timestamp": third.timestamp,
            "available_at": third.available_at,
            "family": family,
            "line_available_at": line_available_at,
            "bar_low": float(df.iloc[third.index]["low"]),
            "bar_high": float(df.iloc[third.index]["high"]),
        }
    ]

    # CHECK events preserve the runtime evaluator's exact line-hold contract:
    # every completed bar from third touch through the reaction is visible to
    # the runtime, but no post-reaction bar is included.
    for idx in range(start_index, end_index + 1):
        events.append(
            {
                "timestamp": df.iloc[idx]["timestamp"],
                "available_at": df.iloc[idx]["timestamp"],
                "family": "CHECK",
                "line_available_at": line_available_at,
                "bar_low": float(df.iloc[idx]["low"]),
                "bar_high": float(df.iloc[idx]["high"]),
            }
        )

    events.append(
        {
            "timestamp": reaction.timestamp,
            "available_at": reaction.available_at,
            "family": opposite,
            "line_available_at": line_available_at,
            "bar_low": float(df.iloc[reaction.index]["low"]),
            "bar_high": float(df.iloc[reaction.index]["high"]),
        }
    )
    return events


def build_xau_trendline_evidence(df: pd.DataFrame) -> pd.DataFrame:
    """Build source-backed Murphy 0006/0007 confirmations.

    The adapter creates lines only from consecutive confirmed same-family
    pivots. It applies no invented touch-distance, reaction-size, or ATR
    threshold. Confirmation is delegated to the existing Murphy runtime.
    """
    required = {"timestamp", "open", "high", "low", "close"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required OHLC columns: {missing}")

    source = df.copy()
    source["timestamp"] = pd.to_datetime(source["timestamp"], utc=True, errors="coerce")
    if source["timestamp"].isna().any() or source["timestamp"].duplicated().any():
        raise ValueError("Invalid or duplicated timestamps.")

    source = source.sort_values("timestamp").reset_index(drop=True)
    start = pd.Timestamp("2016-01-01", tz="UTC")
    end = pd.Timestamp("2025-01-01", tz="UTC")
    source = source[(source["timestamp"] >= start) & (source["timestamp"] < end)].reset_index(drop=True)

    pivot_low, pivot_high = strict_five_bar_pivots(source)
    all_pivots: list[Pivot] = []
    for idx in range(len(source)):
        if pivot_low[idx]:
            all_pivots.append(
                Pivot(
                    index=idx,
                    timestamp=source.iloc[idx]["timestamp"],
                    available_at=source.iloc[idx + 2]["timestamp"],
                    family="LOW",
                    price=float(source.iloc[idx]["low"]),
                )
            )
        if pivot_high[idx]:
            all_pivots.append(
                Pivot(
                    index=idx,
                    timestamp=source.iloc[idx]["timestamp"],
                    available_at=source.iloc[idx + 2]["timestamp"],
                    family="HIGH",
                    price=float(source.iloc[idx]["high"]),
                )
            )
    all_pivots.sort(key=lambda p: p.timestamp)

    rows: list[dict[str, Any]] = []
    for rule_id in ("MURPHY_0006", "MURPHY_0007"):
        family = "LOW" if rule_id == "MURPHY_0006" else "HIGH"
        family_pivots = [p for p in all_pivots if p.family == family]

        anchor_1: Pivot | None = None
        anchor_2: Pivot | None = None
        third: Pivot | None = None
        phase = "PAIR"

        for pivot in family_pivots:
            if pivot.index + 2 >= len(source):
                continue

            if phase == "REACTION":
                # The reaction is searched from the full pivot stream so the
                # first opposite confirmed pivot after the third touch wins.
                continue

            if phase == "PAIR":
                if anchor_1 is None:
                    anchor_1 = pivot
                    continue
                if _valid_anchor_pair(rule_id, anchor_1, pivot):
                    anchor_2 = pivot
                    phase = "CANDIDATE"
                else:
                    anchor_1 = pivot
                continue

            # CANDIDATE: first same-family pivot eligible after line creation.
            assert anchor_1 is not None and anchor_2 is not None
            if pivot.index < anchor_2.index + 2:
                continue

            line_available_at = anchor_2.available_at
            line_price_at = _line_builder(source, rule_id, anchor_1, anchor_2)
            line_at_candidate = line_price_at(pivot.timestamp)
            intersects = float(source.iloc[pivot.index]["low"]) <= line_at_candidate <= float(
                source.iloc[pivot.index]["high"]
            )

            if not intersects:
                anchor_1 = pivot
                anchor_2 = None
                phase = "PAIR"
                continue

            # Freeze this line after the first eligible successful third touch.
            third = pivot
            phase = "REACTION"

            # Search the first opposite confirmed pivot after the third touch.
            opposite_family = "HIGH" if family == "LOW" else "LOW"
            for reaction in [p for p in all_pivots if p.family == opposite_family]:
                if reaction.index <= third.index:
                    continue
                if reaction.available_at < third.available_at:
                    continue

                events = _events_for_runtime(
                    source,
                    rule_id,
                    line_available_at,
                    third,
                    reaction,
                    third.index,
                    reaction.index,
                )
                result = evaluate_rule(
                    rule_id,
                    {
                        "events": events,
                        "line_price_at": line_price_at,
                    },
                )

                if result.get("status") == "CONFIRMED":
                    rows.append(
                        {
                            "timestamp": reaction.available_at,
                            "rule_id": rule_id,
                            "status": "PASS",
                            "direction": result.get("direction"),
                            "reason": result.get("reason", "Runtime-confirmed trendline."),
                            "third_touch_timestamp": third.timestamp,
                            "confirmed_at": reaction.available_at,
                            "anchor_1_timestamp": anchor_1.timestamp,
                            "anchor_1_price": anchor_1.price,
                            "anchor_2_timestamp": anchor_2.timestamp,
                            "anchor_2_price": anchor_2.price,
                            "line_available_at": line_available_at,
                            "reaction_timestamp": reaction.timestamp,
                            "as_of_timestamp": reaction.available_at,
                            "2025_excluded": True,
                            "source": "XAUUSD_M1_MASTER_2016_2026_08_V1",
                        }
                    )
                    anchor_1 = pivot
                    anchor_2 = None
                    third = None
                    phase = "PAIR"
                    break

                # A first eligible reaction with a line-hold violation ends the
                # frozen line. Do not skip forward to a later reaction for the
                # same third touch.
                anchor_1 = third
                anchor_2 = None
                third = None
                phase = "PAIR"
                break

    if not rows:
        return pd.DataFrame(
            columns=[
                "timestamp", "rule_id", "status", "direction", "reason",
                "third_touch_timestamp", "confirmed_at", "anchor_1_timestamp",
                "anchor_1_price", "anchor_2_timestamp", "anchor_2_price",
                "line_available_at", "reaction_timestamp", "as_of_timestamp",
                "2025_excluded", "source",
            ]
        )

    return pd.DataFrame(rows).sort_values(["timestamp", "rule_id"]).reset_index(drop=True)
