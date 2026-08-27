from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from OOS_2025.nison_2025_runtime_producer_v1 import run_ohlcv_for_year

SOURCE_DROPBOX_PATH = "/GBPUSD_H1_2016_2025_MASTER.zip"
MARKET_STATE_DROPBOX_PATH = "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv"
SOURCE_NAME = "GBPUSD_H1_2016_2025_MASTER.csv"
YEARS = tuple(range(2016, 2025))


def _download_dropbox_file(path: str, output: Path) -> Path:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required")
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": path}),
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=180) as response, output.open("wb") as handle:
        handle.write(response.read())
    return output


def download_dropbox_zip(output: Path) -> Path:
    return _download_dropbox_file(SOURCE_DROPBOX_PATH, output)


def load_source(zip_path: Path, work: Path) -> pd.DataFrame:
    unpack = work / "unpacked"
    unpack.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(unpack)
    matches = list(unpack.rglob(SOURCE_NAME))
    if not matches:
        raise FileNotFoundError(f"Cannot find {SOURCE_NAME} in {zip_path}")
    df = pd.read_csv(matches[0])
    required = {"timestamp", "open", "high", "low", "close"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing OHLC columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any() or df["timestamp"].duplicated().any():
        raise ValueError("Invalid or duplicated timestamps in development source")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_market_state(path: Path) -> pd.DataFrame:
    ctx = pd.read_csv(path)
    if "timestamp" not in ctx.columns:
        raise ValueError("Market State context missing timestamp")
    ctx["timestamp"] = pd.to_datetime(ctx["timestamp"], utc=True, errors="coerce")
    if ctx["timestamp"].isna().any() or ctx["timestamp"].duplicated().any():
        raise ValueError("Invalid or duplicated timestamps in Market State context")
    return ctx.sort_values("timestamp").reset_index(drop=True)


def _heartbeat(stop: threading.Event, year: int) -> None:
    started = time.monotonic()
    while not stop.wait(30):
        elapsed = int(time.monotonic() - started)
        print(f"[NISON_DEV] year={year} still running; elapsed={elapsed}s", flush=True)


def run_year(df: pd.DataFrame, context: pd.DataFrame, year: int, out_dir: Path) -> tuple[dict, pd.DataFrame]:
    year_bars = df[df["timestamp"].dt.year.eq(year)].copy()
    if year_bars.empty:
        raise ValueError(f"No bars for development year {year}")
    print(f"[NISON_DEV] year={year} start; bars={len(year_bars)}", flush=True)
    stop = threading.Event()
    watcher = threading.Thread(target=_heartbeat, args=(stop, year), daemon=True)
    watcher.start()
    try:
        evidence = run_ohlcv_for_year(df, context, evaluation_year=year)
    finally:
        stop.set()
        watcher.join(timeout=2)
    expected = len(year_bars) * 44
    if len(evidence) != expected:
        raise AssertionError(f"{year}: evidence rows {len(evidence)} != {expected}")
    if evidence["rule_id"].nunique() != 44:
        raise AssertionError(f"{year}: fewer than 44 Nison rule IDs emitted")
    out = out_dir / f"NISON_{year}_FULL_EVIDENCE.csv"
    evidence.to_csv(out, index=False)
    status_counts = {str(k): int(v) for k, v in evidence["status"].value_counts().to_dict().items()}
    report = {
        "year": year,
        "input_rows": int(len(year_bars)),
        "evidence_rows": int(len(evidence)),
        "rules": 44,
        "status_counts": status_counts,
        "output": str(out),
    }
    print(f"[NISON_DEV] year={year} done; evidence_rows={len(evidence)}", flush=True)
    return report, evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--start-year", type=int, default=2016)
    parser.add_argument("--end-year", type=int, default=2024)
    args = parser.parse_args()

    if args.start_year < 2016 or args.end_year > 2024 or args.start_year > args.end_year:
        raise SystemExit("Development years must be within 2016-2024")

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    source_zip = out_dir / "source" / "GBPUSD_H1_2016_2025_MASTER.zip"
    market_state_path = out_dir / "source" / "GBPUSD_MARKET_STATE.csv"
    download_dropbox_zip(source_zip)
    _download_dropbox_file(MARKET_STATE_DROPBOX_PATH, market_state_path)
    bars = load_source(source_zip, out_dir / "source")
    context = load_market_state(market_state_path)

    reports = []
    evidence_frames = []
    for year in range(args.start_year, args.end_year + 1):
        report, evidence = run_year(bars, context, year, out_dir)
        reports.append(report)
        evidence_frames.append(evidence)

    combined = pd.concat(evidence_frames, ignore_index=True)
    combined = combined.sort_values(["timestamp", "rule_id"]).reset_index(drop=True)
    combined_path = out_dir / "NISON_2016_2024_FULL_EVIDENCE.csv"
    combined.to_csv(combined_path, index=False)

    manifest = {
        "status": "PASS",
        "mode": "DEVELOPMENT_2016_2024_NISON_EVIDENCE_RECOVERY",
        "years": [r["year"] for r in reports],
        "rules": 44,
        "source": SOURCE_DROPBOX_PATH,
        "context_source": MARKET_STATE_DROPBOX_PATH,
        "reuse_existing_runtime": True,
        "semantic_change": False,
        "oos_tuning": False,
        "2025_used": False,
        "lookahead_policy": "prior_completed_source_only",
        "context_wiring": "MARKET_STATE_V1",
        "combined_output": str(combined_path),
        "combined_rows": int(len(combined)),
        "reports": reports,
    }
    (out_dir / "NISON_DEVELOPMENT_2016_2024_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
