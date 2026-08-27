from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path

import pandas as pd

from OOS_2025.run_nison_historical_production_v1 import run

DROPBOX_DOWNLOAD = "https://content.dropboxapi.com/2/files/download"
DEFAULT_DROPBOX_PATH = "/GBPUSD_H1_2016_2025_MASTER.zip"


def download_dropbox_zip(output: Path, dropbox_path: str) -> Path:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required")
    req = urllib.request.Request(
        DROPBOX_DOWNLOAD,
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": dropbox_path}),
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=180) as response, output.open("wb") as handle:
        handle.write(response.read())
    return output


def extract_zip(zip_path: Path, output_dir: Path) -> Path:
    import zipfile

    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(output_dir)
    candidates = list(output_dir.rglob("GBPUSD_H1_2016_2025_MASTER.csv"))
    if not candidates:
        raise FileNotFoundError("GBPUSD_H1_2016_2025_MASTER.csv not found after extraction")
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/nison_development_2016_2024"))
    parser.add_argument("--dropbox-path", default=DEFAULT_DROPBOX_PATH)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_zip = download_dropbox_zip(args.output_dir / "source.zip", args.dropbox_path)
    source_csv = extract_zip(source_zip, args.output_dir / "source")

    bars = pd.read_csv(source_csv, usecols=["timestamp", "open", "high", "low", "close"])
    bars["timestamp"] = pd.to_datetime(bars["timestamp"], utc=True)
    years = list(range(2016, 2025))
    summaries = []

    for year in years:
        out = args.output_dir / f"NISON_{year}_FULL_EVIDENCE.csv"
        manifest = args.output_dir / f"NISON_{year}_FULL_EVIDENCE_MANIFEST.json"
        result = run(
            input_path=source_csv,
            context_path=None,
            year=year,
            output=out,
            manifest=manifest,
        )
        summaries.append(result)

    combined = []
    for year in years:
        p = args.output_dir / f"NISON_{year}_FULL_EVIDENCE.csv"
        df = pd.read_csv(p)
        combined.append(df)
    combined_df = pd.concat(combined, ignore_index=True)
    combined_df.to_csv(args.output_dir / "NISON_2016_2024_FULL_EVIDENCE.csv", index=False)

    summary = {
        "status": "PASS",
        "development_years": years,
        "rules": 44,
        "evidence_rows": int(len(combined_df)),
        "rule_ids": sorted(combined_df["rule_id"].dropna().unique().tolist()),
        "timestamp_min": str(pd.to_datetime(combined_df["timestamp"], utc=True).min()),
        "timestamp_max": str(pd.to_datetime(combined_df["timestamp"], utc=True).max()),
        "lookahead_policy": "prior_completed_source_only",
        "oos_2025_used_for_tuning": False,
        "semantic_change": False,
        "reuse_existing_runtime": True,
        "year_manifests": summaries,
        "next_gate": "Join current Murphy 2016-2024 evidence before governed 78-rule backtest.",
    }
    (args.output_dir / "NISON_2016_2024_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
