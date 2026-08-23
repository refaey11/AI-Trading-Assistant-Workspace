from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
from OOS_2025.nison_2025_runtime_producer_v1 import run_ohlcv_for_year

REQUIRED = {"timestamp", "open", "high", "low", "close"}
EXPECTED_RULES = 44
DEFAULT_MARKET_STATE_DROPBOX_PATH = "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv"


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError("Input contains invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError("Input contains duplicate timestamps")
    for col in ["open", "high", "low", "close"]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col!r} is not numeric")
    bad_ohlc = (df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))
    if bad_ohlc.any():
        raise ValueError(f"Invalid OHLC rows: {int(bad_ohlc.sum())}")
    return df.sort_values("timestamp").reset_index(drop=True)


def build_context(path: Optional[Path]) -> Optional[pd.DataFrame]:
    if path is None:
        return None
    ctx = pd.read_csv(path)
    if "timestamp" not in ctx.columns:
        raise ValueError("Context file must contain timestamp")
    ctx["timestamp"] = pd.to_datetime(ctx["timestamp"], utc=True)
    return ctx.sort_values("timestamp").drop_duplicates("timestamp", keep="last")


def download_market_state_context(out_path: Path) -> Path:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required to acquire the existing Market State Reader context")
    dropbox_path = os.environ.get("NISON_MARKET_STATE_DROPBOX_PATH", DEFAULT_MARKET_STATE_DROPBOX_PATH)
    req = Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": dropbox_path}),
        },
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(req, timeout=120) as response, out_path.open("wb") as handle:
        handle.write(response.read())
    return out_path


def acquire_default_context(explicit_path: Optional[Path]) -> tuple[Optional[Path], Optional[str]]:
    if explicit_path is not None:
        return explicit_path, "explicit_context_argument"
    local_default = ROOT / "OOS_2025" / "GBPUSD_HISTORICAL_MARKET_STATE_CONTEXT.csv"
    if local_default.exists():
        return local_default, "committed_market_state_context"
    downloaded = ROOT / "OOS_2025" / ".runtime_cache" / "GBPUSD_MARKET_STATE.csv"
    return download_market_state_context(downloaded), "dropbox_market_state_reader"


def run(*, input_path: Path, context_path: Optional[Path], year: int, output: Path, manifest: Path) -> dict:
    bars_all = load_csv(input_path)
    bars_year = bars_all[bars_all["timestamp"].dt.year.eq(year)].copy()
    if bars_year.empty:
        raise ValueError(f"No rows found for evaluation year {year}")
    context_path, context_source = acquire_default_context(context_path)
    context = build_context(context_path)

    # Pass the full chronologically sorted source into the governed adapter so
    # historical fold rows may use only prior completed candles for context.
    # The adapter emits evidence only for the requested evaluation year.
    evidence = run_ohlcv_for_year(bars_all, context, evaluation_year=year)

    expected_rows = len(bars_year) * EXPECTED_RULES
    if len(evidence) != expected_rows:
        raise AssertionError(f"Evidence row count {len(evidence)} != expected {expected_rows}")
    if evidence["rule_id"].nunique() != EXPECTED_RULES:
        raise AssertionError("Not all 44 Nison rule IDs were emitted")
    if pd.to_datetime(evidence["timestamp"], utc=True).dt.year.ne(year).any():
        raise AssertionError(f"Evidence contains non-{year} timestamps")

    output.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    evidence.to_csv(output, index=False)
    status_counts = evidence["status"].value_counts().to_dict()
    per_rule = evidence.groupby(["rule_id", "status"]).size().unstack(fill_value=0).to_dict(orient="index")
    result = {
        "status": "PASS",
        "evaluation_year": year,
        "input_rows_total": int(len(bars_all)),
        "input_rows_year": int(len(bars_year)),
        "nison_rules": EXPECTED_RULES,
        "evidence_rows": int(len(evidence)),
        "status_counts": {k: int(v) for k, v in status_counts.items()},
        "per_rule_status_counts": {k: {sk: int(sv) for sk, sv in v.items()} for k, v in per_rule.items()},
        "context_source": context_source,
        "context_path": str(context_path),
        "lookahead_policy": "prior_completed_source_only",
        "oos_tuning": False,
        "semantic_change": False,
        "reuse_existing_runtime": True,
    }
    manifest.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    run(input_path=args.input, context_path=args.context, year=args.year, output=args.output, manifest=args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
