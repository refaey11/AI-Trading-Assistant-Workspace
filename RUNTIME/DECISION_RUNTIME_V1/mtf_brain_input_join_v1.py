from __future__ import annotations

"""Strict, non-directional MTF -> Decision Brain input join.

This adapter does not generate trend values, directions, SL/TP, risk, or trades.
It only joins source-backed MTF fields to a canonical event stream using a
point-in-time (as-of) join and fails closed on missing/ambiguous inputs.
"""

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_MTF_FIELDS = (
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)


def _load_timestamped(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing required columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp values")
    if df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def join_mtf_to_events(events: pd.DataFrame, mtf: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" not in events.columns:
        raise ValueError("events: missing timestamp")
    if events["timestamp"].isna().any():
        raise ValueError("events: invalid timestamps")
    if events["timestamp"].duplicated().any():
        raise ValueError("events: duplicate timestamps")

    mtf = mtf.copy()
    for field in REQUIRED_MTF_FIELDS:
        values = pd.to_numeric(mtf[field], errors="coerce")
        if values.isna().any():
            raise ValueError(f"mtf: non-numeric/NaN values in {field}")
        mtf[field] = values

    events = events.sort_values("timestamp").reset_index(drop=True).copy()
    mtf = mtf.sort_values("timestamp").reset_index(drop=True).copy()

    merged = pd.merge_asof(
        events,
        mtf[["timestamp", *REQUIRED_MTF_FIELDS]],
        on="timestamp",
        direction="backward",
        allow_exact_matches=True,
    )

    for field in REQUIRED_MTF_FIELDS:
        if merged[field].isna().any():
            raise ValueError(f"MISSING_SOURCE_BACKED_MTF_INPUT:{field}")

    # Defensive causality check: selected MTF timestamp may not be after event timestamp.
    mtf_ts = pd.merge_asof(
        events[["timestamp"]].sort_values("timestamp"),
        mtf[["timestamp"]].rename(columns={"timestamp": "mtf_timestamp"}).sort_values("mtf_timestamp"),
        left_on="timestamp",
        right_on="mtf_timestamp",
        direction="backward",
        allow_exact_matches=True,
    )["mtf_timestamp"]
    if (mtf_ts > events["timestamp"].sort_values().reset_index(drop=True)).any():
        raise ValueError("FUTURE_MTF_INPUT_DETECTED")

    return merged


def run(events_path: Path, mtf_path: Path, output_path: Path) -> dict[str, Any]:
    events = _load_timestamped(events_path, {"timestamp"})
    mtf = _load_timestamped(mtf_path, {"timestamp", *REQUIRED_MTF_FIELDS})
    merged = join_mtf_to_events(events, mtf)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_path, index=False)
    result = {
        "status": "PASS",
        "event_rows": int(len(events)),
        "mtf_rows": int(len(mtf)),
        "joined_rows": int(len(merged)),
        "required_mtf_fields": list(REQUIRED_MTF_FIELDS),
        "join": "merge_asof_backward_exact",
        "defaults_used": False,
        "direction_generated": False,
        "risk_generated": False,
    }
    output_path.with_suffix(".json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--mtf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.events, args.mtf, args.output), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
