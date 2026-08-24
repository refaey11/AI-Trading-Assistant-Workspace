#!/usr/bin/env python3
"""Acquire authoritative 2025 CFTC TFF British Pound futures OI.

Governance:
- Source is CFTC Public Reporting dataset gpe5-46if (TFF - Futures Only).
- Instrument filter is CFTC contract market code 096742 (British Pound futures).
- Report date is NOT treated as availability time.
- No proxy OI, interpolation, or inferred release timestamp is permitted.
- This script only materializes raw CFTC observations. PIT binding must use a
  separately governed publication/availability manifest before rule evaluation.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests

API = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
DATASET = "gpe5-46if"
CONTRACT = "096742"
START = "2025-01-01T00:00:00"
END = "2025-12-31T23:59:59"


def fetch_rows(timeout: int = 30) -> list[dict[str, Any]]:
    params = {
        "$select": "report_date_as_yyyy_mm_dd,cftc_contract_market_code,open_interest_all,contract_market_name,market_and_exchange_names,id",
        "$where": (
            f"cftc_contract_market_code='{CONTRACT}' AND "
            f"report_date_as_yyyy_mm_dd between '{START}' and '{END}'"
        ),
        "$order": "report_date_as_yyyy_mm_dd",
        "$limit": "5000",
    }
    r = requests.get(API, params=params, timeout=timeout, headers={"Accept": "application/json"})
    r.raise_for_status()
    rows = r.json()
    if not isinstance(rows, list):
        raise ValueError("CFTC response is not a JSON list")
    return rows


def normalize(rows: list[dict[str, Any]]) -> pd.DataFrame:
    if not rows:
        raise ValueError("CFTC returned zero 2025 observations for contract 096742")
    df = pd.DataFrame(rows)
    required = {
        "report_date_as_yyyy_mm_dd",
        "cftc_contract_market_code",
        "open_interest_all",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required CFTC columns: {sorted(missing)}")
    df["report_date"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"], utc=True)
    df["open_interest"] = pd.to_numeric(df["open_interest_all"], errors="raise")
    if (df["cftc_contract_market_code"].astype(str) != CONTRACT).any():
        raise ValueError("Contract filter leakage detected")
    if df["report_date"].duplicated().any():
        raise ValueError("Duplicate report dates detected")
    if (df["open_interest"] < 0).any():
        raise ValueError("Negative open interest detected")
    return df.sort_values("report_date").reset_index(drop=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--raw-out", type=Path, default=Path("cftc_096742_2025_raw.json"))
    p.add_argument("--csv-out", type=Path, default=Path("cftc_096742_2025_normalized.csv"))
    p.add_argument("--manifest-out", type=Path, default=Path("cftc_096742_2025_acquisition_manifest.json"))
    args = p.parse_args()

    rows = fetch_rows()
    df = normalize(rows)

    args.raw_out.parent.mkdir(parents=True, exist_ok=True)
    args.csv_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)

    args.raw_out.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    df[[
        "report_date",
        "cftc_contract_market_code",
        "open_interest",
        "contract_market_name",
        "market_and_exchange_names",
        "id",
    ]].to_csv(args.csv_out, index=False)

    manifest = {
        "status": "RAW_ACQUIRED_VALIDATED",
        "dataset": DATASET,
        "source": "CFTC Public Reporting",
        "api": API,
        "contract_code": CONTRACT,
        "report_date_window": [START, END],
        "rows": int(len(df)),
        "min_report_date": df["report_date"].min().isoformat(),
        "max_report_date": df["report_date"].max().isoformat(),
        "duplicate_report_dates": int(df["report_date"].duplicated().sum()),
        "report_date_is_available_time": False,
        "pit_binding_status": "REQUIRES_GOVERNED_AVAILABILITY_MANIFEST",
        "proxy_oi": False,
        "interpolation": False,
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    args.manifest_out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
