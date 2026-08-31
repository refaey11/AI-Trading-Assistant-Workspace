"""Gate 3C diagnostic: audit historical source availability for one calendar year.

This is diagnostic only. It does not alter Decision Brain logic, rules, or tuning.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd


def parse_ts(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce", format="mixed")


def load_similarity_timestamps(root: Path) -> tuple[list[pd.Timestamp], str]:
    files = sorted(p for p in root.rglob("*.json") if "SIMILAR" in p.name.upper() or "CONTEXT" in p.name.upper())
    if not files:
        raise SystemExit(f"BLOCKED_SIMILARITY_SOURCE_NOT_FOUND:{root}")
    path = files[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"BLOCKED_SIMILARITY_SCHEMA:{path.name}")
    out: list[pd.Timestamp] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        for row in item.get("similar_contexts") or []:
            if not isinstance(row, dict) or "timestamp" not in row:
                continue
            ts = pd.to_datetime(row["timestamp"], utc=True, errors="coerce")
            if not pd.isna(ts):
                out.append(ts)
    return sorted(set(out)), str(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--market-state", type=Path, required=True)
    ap.add_argument("--similarity-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()

    if not 2016 <= a.year <= 2024:
        raise SystemExit("FAIL_CLOSED_YEAR_MUST_BE_2016_2024")

    market = pd.read_csv(a.market_state)
    if "timestamp" not in market.columns:
        raise SystemExit("BLOCKED_MARKET_STATE_TIMESTAMP_COLUMN_MISSING")
    market["timestamp"] = parse_ts(market["timestamp"])
    target = market.loc[market["timestamp"].dt.year.eq(a.year), "timestamp"].dropna().drop_duplicates().sort_values()
    if target.empty:
        raise SystemExit(f"BLOCKED_NO_MARKET_STATE_EVENTS_FOR_YEAR:{a.year}")

    sim_ts, sim_source = load_similarity_timestamps(a.similarity_root)
    sim = pd.DatetimeIndex(sim_ts)
    # The current Gate 3C builder treats similarity as available when at least one
    # historical similar-context row has timestamp <= event timestamp.
    first_sim = sim.min() if len(sim) else pd.NaT
    last_sim = sim.max() if len(sim) else pd.NaT
    available = target.map(lambda ts: bool(len(sim) and sim.searchsorted(ts, side="right") > 0))
    n = len(target)
    na = int(available.sum())
    result = {
        "audit": "GATE3C_YEAR_AVAILABILITY_AUDIT_V1",
        "year": a.year,
        "diagnostic_only": True,
        "oos_range": "2016-2024",
        "event_source": str(a.market_state),
        "event_count": n,
        "similarity_source": sim_source,
        "similarity_historical_row_count": len(sim),
        "similarity_first_historical_timestamp": None if pd.isna(first_sim) else first_sim.isoformat(),
        "similarity_last_historical_timestamp": None if pd.isna(last_sim) else last_sim.isoformat(),
        "similarity_available_event_count": na,
        "similarity_blocked_event_count": n - na,
        "similarity_available_rate": round(na / n, 6),
        "first_event": target.iloc[0].isoformat(),
        "last_event": target.iloc[-1].isoformat(),
        "interpretation": (
            "This measures only whether the current similarity as-of contract can find at least one "
            "historical similar row by event time. It is not an E2E pass/fail and does not evaluate direction."
        ),
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
