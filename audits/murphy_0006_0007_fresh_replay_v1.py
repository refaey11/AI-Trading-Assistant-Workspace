from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from src.murphy_0006_0007.murphy_event_operator import D1Bar, Line, PivotEvent, evaluate_event_chain


def dt(value: str) -> datetime:
    value = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def rows(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def pick(row: dict, *names: str) -> str:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    raise KeyError(f"missing one of {names}; columns={list(row)}")


def load_pivots(path: Path) -> List[PivotEvent]:
    out = []
    for r in rows(path):
        out.append(PivotEvent(
            timestamp=dt(pick(r, "pivot_timestamp", "timestamp", "pivot_time")),
            available_at=dt(pick(r, "pivot_available_at", "available_at", "availability_timestamp")),
            pivot_type=pick(r, "pivot_type", "type", "family").upper(),
            price=float(pick(r, "pivot_price", "price")),
        ))
    return out


def load_bars(path: Path) -> List[D1Bar]:
    out = []
    for r in rows(path):
        out.append(D1Bar(
            timestamp=dt(pick(r, "timestamp", "date", "bar_timestamp")),
            high=float(pick(r, "high", "High")),
            low=float(pick(r, "low", "Low")),
        ))
    return out


def load_lines(path: Path) -> List[dict]:
    return list(rows(path))


def line_from_row(r: dict) -> Tuple[str, Line, callable]:
    line_id = pick(r, "line_id", "id")
    line_type = pick(r, "line_type", "trendline_type", "family").upper()
    direction = pick(r, "direction", "trendline_direction").upper()
    available = dt(pick(r, "line_availability_timestamp", "available_at", "availability_timestamp"))
    a1t = dt(pick(r, "anchor_1_timestamp", "point_1_timestamp", "anchor1_timestamp"))
    a2t = dt(pick(r, "anchor_2_timestamp", "point_2_timestamp", "anchor2_timestamp"))
    a1p = float(pick(r, "anchor_1_price", "point_1_price", "anchor1_price"))
    a2p = float(pick(r, "anchor_2_price", "point_2_price", "anchor2_price"))

    if a1t == a2t:
        raise ValueError(f"duplicate anchor timestamps for {line_id}")

    def line_price_at(t: datetime) -> float:
        total = (a2t - a1t).total_seconds()
        elapsed = (t - a1t).total_seconds()
        return a1p + (a2p - a1p) * elapsed / total

    return line_id, Line(line_type, direction, available), line_price_at


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pivots", required=True)
    ap.add_argument("--lines", required=True)
    ap.add_argument("--d1", required=True)
    ap.add_argument("--year-max", type=int, default=2024)
    args = ap.parse_args()

    pivots = [p for p in load_pivots(Path(args.pivots)) if p.timestamp.year <= args.year_max]
    bars = [b for b in load_bars(Path(args.d1)) if b.timestamp.year <= args.year_max]
    lines = load_lines(Path(args.lines))

    counts = Counter()
    confirmations = []

    for raw in lines:
        line_id, line, price_fn = line_from_row(raw)
        for rule_id, expected_type, expected_direction in (
            ("MURPHY_0006", "LOW", "UP"),
            ("MURPHY_0007", "HIGH", "DOWN"),
        ):
            if (line.line_type, line.direction) != (expected_type, expected_direction):
                continue
            result = evaluate_event_chain(rule_id, line, price_fn, pivots, bars)
            if result is not None:
                counts[rule_id] += 1
                confirmations.append((rule_id, line_id, result))

    print(f"0006={counts['MURPHY_0006']}")
    print(f"0007={counts['MURPHY_0007']}")
    print(f"total={sum(counts.values())}")
    print("NOTE: this is a fresh replay only if the supplied pivots/lines/d1 are the canonical project inputs; no reference artifact is read by this runner.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
