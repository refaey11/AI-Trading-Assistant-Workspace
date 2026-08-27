from __future__ import annotations

import argparse
import json
import os
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from OOS_2025.nison_2025_runtime_producer_v1 import run_ohlcv_for_year

SOURCE_DROPBOX_PATH = "/GBPUSD_H1_2016_2025_MASTER.zip"
SOURCE_NAME = "GBPUSD_H1_2016_2025_MASTER.csv"
YEARS = tuple(range(2016, 2025))


def download_dropbox_zip(output: Path) -> Path:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required")
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": SOURCE_DROPBOX_PATH}),
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=180) as response, output.open("wb") as handle:
        handle.write(response.read())
    return output


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


def run_year(df: pd.DataFrame, year: int, out_dir: Path) -> dict:
    year_bars = df[df["timestamp"].dt.year.eq(year)].copy()
    if year_bars.empty:
        raise ValueError(f"No bars for development year {year}")
    evidence = run_ohlcv_for_year(df, None, evaluation_year=year)
    expected = len(year_bars) * 44
    if len(evidence) != expected:
        raise AssertionError(f"{year}: evidence rows {len(evidence)} != {expected}")
    if evidence["rule_id"].nunique() != 44:
        raise AssertionError(f"{year}: fewer than 44 Nison rule IDs emitted")
    out = out_dir / f"NISON_{year}_FULL_EVIDENCE.csv"
    evidence.to_csv(out, index=False)
    status_counts = {str(k): int(v) for k, v in evidence["status"].value_counts().to_dict().items()}
    return {
        "year": year,
        "input_rows": int(len(year_bars)),
        "evidence_rows": int(len(evidence)),
        "rules": 44,
        "status_counts": status_counts,
        "output": str(out),
    }


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
    download_dropbox_zip(source_zip)
    bars = load_source(source_zip, out_dir / "source")

    reports = [run_year(bars, year, out_dir) for year in range(args.start_year, args.end_year + 1)]
    manifest = {
        "status": "PASS",
        "mode": "DEVELOPMENT_2016_2024_NISON_EVIDENCE_RECOVERY",
        "years": [r["year"] for r in reports],
        "rules": 44,
        "source": SOURCE_DROPBOX_PATH,
        "reuse_existing_runtime": True,
        "semantic_change": False,
        "oos_tuning": False,
        "2025_used": False,
        "lookahead_policy": "prior_completed_source_only",
        "reports": reports,
    }
    (out_dir / "NISON_DEVELOPMENT_2016_2024_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
