from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd

TIME_FIELDS = ("timestamp", "time", "datetime", "bar_open_time", "bar_close_time", "available_at", "close_time")
INTERVALS = {"H1": "1h", "MTF_M5": "5min", "MARKET_STATE": None, "NISON": None, "MURPHY": None}


def extract(zip_path: Path, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(out)
    return out


def csv_candidates(root: Path, required: set[str]) -> list[Path]:
    out = []
    for path in root.rglob("*.csv"):
        try:
            cols = set(pd.read_csv(path, nrows=0).columns)
        except Exception:
            continue
        if required.issubset(cols):
            out.append(path)
    return sorted(out)


def parse_frame(path: Path) -> tuple[pd.DataFrame, str]:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: timestamp column missing")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    return df.dropna(subset=["timestamp"]).sort_values("timestamp", kind="stable"), "timestamp"


def scalar(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def source_snapshot(label: str, path: Path, event: pd.Timestamp, *, interval: str | None = None,
                    required: set[str] | None = None) -> dict[str, Any]:
    df, _ = parse_frame(path)
    exact = df.loc[df["timestamp"].eq(event)]
    prior = df.loc[df["timestamp"].lt(event)].tail(1)
    following = df.loc[df["timestamp"].gt(event)].head(1)
    selected = pd.concat([prior, exact, following]).drop_duplicates(subset=["timestamp"])
    cols = list(df.columns)
    time_metadata = [c for c in cols if c.lower() in TIME_FIELDS or any(x in c.lower() for x in ("bar_open", "bar_close", "available_at", "close_time"))]
    evidence_cols = [c for c in cols if c.lower() in {
        "open", "high", "low", "close", "volume", "volume_direction", "volume_state",
        "volume_ratio", "atr", "atr20", "trend", "structure_event", "mtf_trend_score",
        "m5_trend_regime", "m15_trend_regime", "m30_trend_regime", "h1_trend_regime",
        "h4_trend_regime", "d1_trend_regime", "source_rule_id", "rule_id", "status",
        "direction", "pass_rule_id", "confidence"
    }]
    keep = list(dict.fromkeys(["timestamp", *time_metadata, *evidence_cols]))
    records = []
    for _, row in selected.iterrows():
        records.append({k: scalar(row[k]) for k in keep if k in row.index})
    exact_records = [r for r in records if r.get("timestamp") == event.isoformat()]
    result = {
        "source": label,
        "path": str(path),
        "rows_total": int(len(df)),
        "timestamp_min": df["timestamp"].min().isoformat() if len(df) else None,
        "timestamp_max": df["timestamp"].max().isoformat() if len(df) else None,
        "exact_event_rows": int(len(exact)),
        "nearest_prior_timestamp": prior.iloc[0]["timestamp"].isoformat() if len(prior) else None,
        "nearest_following_timestamp": following.iloc[0]["timestamp"].isoformat() if len(following) else None,
        "declared_time_metadata_columns": time_metadata,
        "rows_near_event": records,
        "interpretation_limit": "Timestamp labels alone do not prove whether a row is available at its label or only after its bar closes.",
    }
    if interval:
        result["nominal_interval"] = interval
    if required:
        result["required_columns_present"] = sorted(required.issubset(set(cols)))
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--event-ts", required=True)
    p.add_argument("--h1-zip", required=True, type=Path)
    p.add_argument("--mtf-zip", required=True, type=Path)
    p.add_argument("--murphy-zip", required=True, type=Path)
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    event = pd.to_datetime(a.event_ts, utc=True)
    if not 2016 <= event.year <= 2024:
        raise SystemExit("FAIL_CLOSED: event must be in 2016-2024")
    h1_root = extract(a.h1_zip, a.output.parent / "h1")
    mtf_root = extract(a.mtf_zip, a.output.parent / "mtf")
    murphy_root = extract(a.murphy_zip, a.output.parent / "murphy")
    h1_files = csv_candidates(h1_root, {"timestamp", "open", "high", "low", "close"})
    if len(h1_files) != 1:
        raise SystemExit(f"BLOCKED_H1_SOURCE_CARDINALITY:{len(h1_files)}")
    mtf_files = sorted(mtf_root.rglob(f"GBPUSD_M5_MTF_ALIGNMENT_{event.year}.csv"))
    if len(mtf_files) != 1:
        raise SystemExit(f"BLOCKED_MTF_SOURCE_CARDINALITY:{len(mtf_files)}")
    murphy_files = csv_candidates(murphy_root, {"timestamp", "source_rule_id"})
    if len(murphy_files) != 1:
        raise SystemExit(f"BLOCKED_MURPHY_SOURCE_CARDINALITY:{len(murphy_files)}")
    market_path = a.market_state
    nison_path = a.nison
    report = {
        "audit": "GATE3C_EVENT_SOURCE_TIMESTAMP_COMPATIBILITY_READ_ONLY",
        "scope": "2016-2024 only; 2025 OOS and 2026 excluded",
        "event_timestamp": event.isoformat(),
        "sources": [
            source_snapshot("H1", h1_files[0], event, interval="1h"),
            source_snapshot("MTF_M5", mtf_files[0], event, interval="5min"),
            source_snapshot("MARKET_STATE", market_path, event),
            source_snapshot("NISON", nison_path, event),
            source_snapshot("MURPHY", murphy_files[0], event),
        ],
        "global_conclusion": "Read-only timestamp-neighborhood inventory. No source is shifted or assigned an availability timestamp without producer/contract evidence.",
        "safety": {"runtime_changed": False, "thresholds_changed": False, "2025_used_for_tuning": False},
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
