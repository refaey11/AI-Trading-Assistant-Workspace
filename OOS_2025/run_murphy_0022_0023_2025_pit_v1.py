from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0022, evaluate_0023

REQUIRED_H1 = {"timestamp", "open", "high", "low", "close"}
REQUIRED_M1 = {"timestamp", "open", "high", "low", "close", "volume"}


def _load_ohlcv(path: str | Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError("Invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps")
    for col in sorted(required - {"timestamp"}):
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col!r} is not numeric")
    bad_ohlc = (df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))
    if bad_ohlc.any():
        raise ValueError(f"Invalid OHLC rows: {int(bad_ohlc.sum())}")
    return df.sort_values("timestamp").reset_index(drop=True)


def _load_pit_oi(path: str | Path) -> pd.DataFrame:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = pd.DataFrame(data["observations"])
    if int(data["observation_count"]) != len(rows):
        raise ValueError("OI observation_count mismatch")
    if rows["report_date"].duplicated().any():
        raise ValueError("Duplicate OI report dates")
    rows["report_date"] = pd.to_datetime(rows["report_date"], utc=True)
    rows["available_time"] = pd.to_datetime(rows["available_time"], utc=True)
    if (rows["available_time"] < rows["report_date"]).any():
        raise ValueError("OI available_time precedes report_date")
    rows = rows.sort_values("available_time").reset_index(drop=True)
    rows["previous_open_interest"] = rows["open_interest"].shift(1)
    rows["oi_direction"] = None
    rows.loc[rows["previous_open_interest"] < rows["open_interest"], "oi_direction"] = "UP"
    rows.loc[rows["previous_open_interest"] > rows["open_interest"], "oi_direction"] = "DOWN"
    rows.loc[rows["previous_open_interest"] == rows["open_interest"], "oi_direction"] = "FLAT"
    return rows


def _build_h1_volume_direction(m1_path: str | Path) -> pd.DataFrame:
    m1 = _load_ohlcv(m1_path, REQUIRED_M1)
    m1["h1_timestamp"] = m1["timestamp"].dt.floor("h")
    h1 = (
        m1.groupby("h1_timestamp", as_index=False)
        .agg(volume=("volume", "sum"), m1_count=("volume", "size"))
        .sort_values("h1_timestamp")
        .reset_index(drop=True)
    )
    h1["previous_volume"] = h1["volume"].shift(1)
    h1["volume_direction"] = None
    h1.loc[h1["previous_volume"].notna() & (h1["volume"] > h1["previous_volume"]), "volume_direction"] = "UP"
    h1.loc[h1["previous_volume"].notna() & (h1["volume"] < h1["previous_volume"]), "volume_direction"] = "DOWN"
    h1.loc[h1["previous_volume"].notna() & (h1["volume"] == h1["previous_volume"]), "volume_direction"] = "FLAT"
    return h1


def run(h1_path: str | Path, m1_path: str | Path, oi_path: str | Path) -> tuple[pd.DataFrame, dict]:
    h1 = _load_ohlcv(h1_path, REQUIRED_H1)
    h1["previous_close"] = h1["close"].shift(1)
    h1 = h1[h1["timestamp"].dt.year.eq(2025)].copy().reset_index(drop=True)
    if h1.empty:
        raise ValueError("No 2025 H1 rows found")

    volume = _build_h1_volume_direction(m1_path)
    merged = h1.merge(
        volume[["h1_timestamp", "volume_direction", "m1_count"]],
        left_on="timestamp",
        right_on="h1_timestamp",
        how="left",
        validate="one_to_one",
    )

    oi = _load_pit_oi(oi_path)
    oi_for_join = oi[["available_time", "open_interest", "oi_direction", "report_date"]].copy()

    merged = pd.merge_asof(
        merged.sort_values("timestamp"),
        oi_for_join.sort_values("available_time"),
        left_on="timestamp",
        right_on="available_time",
        direction="backward",
        allow_exact_matches=True,
    )

    results: list[dict] = []
    for row in merged.itertuples(index=False):
        base = {
            "close": row.close,
            "previous_close": row.previous_close,
            "volume_direction": row.volume_direction,
            "oi_direction": row.oi_direction,
        }
        r22 = evaluate_0022(base)
        r23 = evaluate_0023(base)
        for result in (r22, r23):
            results.append({
                "timestamp": row.timestamp,
                "rule_id": result["rule_id"],
                "status": result["status"],
                "directional_confirmation": result["directional_confirmation"],
                "reason": result["reason"],
                "oi_report_date": row.report_date,
                "oi_available_time": row.available_time,
                "oi_direction": row.oi_direction,
            })

    out = pd.DataFrame(results)
    if len(out) != len(h1) * 2:
        raise AssertionError("Output row count mismatch")

    manifests: dict[str, dict] = {}
    for rule_id in ("MURPHY_0022", "MURPHY_0023"):
        part = out[out["rule_id"].eq(rule_id)]
        counts = part["status"].value_counts().to_dict()
        manifests[rule_id] = {
            "input_rows_2025": int(len(part)),
            "PASS": int(counts.get("PASS", 0)),
            "FAIL": int(counts.get("FAIL", 0)),
            "NOT_EVALUABLE": int(counts.get("NOT_EVALUABLE", 0)),
            "rows_with_oi_evidence": int(part["oi_direction"].notna().sum()),
            "rows_without_oi_evidence": int(part["oi_direction"].isna().sum()),
        }

    manifest = {
        "status": "FRESH_MURPHY_2025_PIT_OOS_ONLY",
        "input_h1_rows_2025": int(len(h1)),
        "oi_observation_count": int(len(oi)),
        "pit_policy": "latest OI with available_time <= H1 event timestamp",
        "no_lookahead": True,
        "no_proxy": True,
        "no_interpolation": True,
        "tuning": False,
        "rules": manifests,
    }
    return out, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1", required=True)
    parser.add_argument("--m1", required=True)
    parser.add_argument("--oi", default="evidence/cftc/2025/6b_oi_pit_bound_v1.json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    out, manifest = run(args.h1, args.m1, args.oi)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))

    # CircleCI already downloads the authoritative H1/M1 sources and provides
    # DROPBOX_ACCESS_TOKEN. Reuse this successful OOS job as the execution host
    # for the final Decision Brain evaluation, without changing any rule logic.
    if os.environ.get("CIRCLECI", "").lower() == "true":
        final_dir = Path(args.output).parent / "final_2025_evaluation"
        final_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "python",
                "OOS_2025/run_final_2025_decision_brain_and_pnl_v1.py",
                "--h1", args.h1,
                "--m1", args.m1,
                "--murphy-0022-0023", args.output,
                "--output-dir", str(final_dir),
            ],
            check=True,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
