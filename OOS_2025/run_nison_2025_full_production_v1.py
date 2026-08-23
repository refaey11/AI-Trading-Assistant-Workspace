from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Optional
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from OOS_2025.nison_2025_runtime_producer_v1 import run_ohlcv_2025

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
    return ctx


def download_market_state_context(out_path: Path) -> Path:
    token = __import__("os").environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required to acquire the existing Market State Reader context")
    dropbox_path = __import__("os").environ.get("NISON_MARKET_STATE_DROPBOX_PATH", DEFAULT_MARKET_STATE_DROPBOX_PATH)
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
    local_default = ROOT / "OOS_2025" / "GBPUSD_2025_MARKET_STATE_CONTEXT.csv"
    if local_default.exists():
        return local_default, "committed_market_state_context"
    downloaded = ROOT / "OOS_2025" / ".runtime_cache" / "GBPUSD_MARKET_STATE.csv"
    try:
        return download_market_state_context(downloaded), "dropbox_market_state_reader"
    except Exception as exc:
        raise RuntimeError(f"Unable to acquire existing Market State Reader context: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    bars_all = load_csv(args.input)
    bars_2025 = bars_all[bars_all["timestamp"].dt.year.eq(2025)].copy()
    if bars_2025.empty:
        raise ValueError("No 2025 rows found in input")

    context_path, context_source = acquire_default_context(args.context)
    context = build_context(context_path)
    evidence = run_ohlcv_2025(bars_2025, context)

    expected_rows = len(bars_2025) * EXPECTED_RULES
    if len(evidence) != expected_rows:
        raise AssertionError(f"Evidence row count {len(evidence)} != expected {expected_rows}")
    if evidence["rule_id"].nunique() != EXPECTED_RULES:
        raise AssertionError("Not all 44 Nison rule IDs were emitted")
    if pd.to_datetime(evidence["timestamp"], utc=True).dt.year.ne(2025).any():
        raise AssertionError("Evidence contains non-2025 timestamps")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    evidence.to_csv(args.output, index=False)

    status_counts = evidence["status"].value_counts().to_dict()
    per_rule = evidence.groupby(["rule_id", "status"]).size().unstack(fill_value=0).to_dict(orient="index")
    available = evidence["available"].astype(bool)
    per_rule_available = evidence.groupby("rule_id")["available"].apply(lambda s: int(s.astype(bool).sum())).to_dict()
    per_rule_coverage = {
        str(rule_id): {
            "rows": int(len(group)),
            "available_rows": int(group["available"].astype(bool).sum()),
            "available_rate": float(group["available"].astype(bool).mean()),
            "pass": int((group["status"].astype(str) == "PASS").sum()),
            "fail": int((group["status"].astype(str) == "FAIL").sum()),
            "not_evaluable": int((group["status"].astype(str) == "NOT_EVALUABLE").sum()),
        }
        for rule_id, group in evidence.groupby("rule_id", sort=True)
    }
    rules_with_any_available = sum(v > 0 for v in per_rule_available.values())
    rules_with_full_coverage = sum(v == len(bars_2025) for v in per_rule_available.values())

    manifest = {
        "input": str(args.input),
        "context": str(context_path) if context_path else None,
        "context_source": context_source,
        "market_state_dropbox_path": DEFAULT_MARKET_STATE_DROPBOX_PATH if context_source == "dropbox_market_state_reader" else None,
        "scope": "2025-01-01T00:00:00Z..2025-12-31T23:59:59Z",
        "input_rows_total": int(len(bars_all)),
        "input_rows_2025": int(len(bars_2025)),
        "nison_rules": EXPECTED_RULES,
        "evidence_rows": int(len(evidence)),
        "status_counts": {k: int(v) for k, v in status_counts.items()},
        "per_rule_status_counts": {k: {sk: int(sv) for sk, sv in v.items()} for k, v in per_rule.items()},
        "available_rows": int(available.sum()),
        "available_rate": float(available.mean()),
        "rules_with_any_available_evidence": int(rules_with_any_available),
        "rules_with_full_timestamp_coverage": int(rules_with_full_coverage),
        "rules_with_no_available_evidence": int(EXPECTED_RULES - rules_with_any_available),
        "per_rule_availability": per_rule_coverage,
        "lookahead_policy": "none",
        "oos_policy": "2025 is evaluation-only; no tuning or threshold selection",
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(manifest, indent=2, sort_keys=True))
    print("NISON_2025_FRESH_COVERAGE", json.dumps({
        "rules_with_any_available_evidence": rules_with_any_available,
        "rules_with_full_timestamp_coverage": rules_with_full_coverage,
        "rules_with_no_available_evidence": EXPECTED_RULES - rules_with_any_available,
        "available_rows": int(available.sum()),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
