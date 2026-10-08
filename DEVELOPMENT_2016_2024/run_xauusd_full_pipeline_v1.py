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
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
NISON_DIR = ROOT / "RUNTIME" / "NISON_EVALUATORS_V1"
if str(NISON_DIR) not in sys.path:
    sys.path.insert(0, str(NISON_DIR))

from BACKTEST.DEV_BACKTEST_RUNNER_V1 import run as run_decision_brain
from DEVELOPMENT_2016_2024.run_xauusd_murphy_evidence_v1 import emit as emit_murphy
from RUNTIME.NISON_EVALUATORS_V1.nison_0001_0010_router import evaluate_rule as nison_evaluate_rule

XAU_H1_DROPBOX_PATH = "/XAUUSD_H1_2016_2025_MASTER.zip"
XAU_MTF_DROPBOX_PATH = "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1/XAUUSD_MTF_H4_H1.csv"
XAU_MARKET_STATE_DROPBOX_PATH = "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/XAUUSD_MARKET_STATE.csv"

DEV_START = pd.Timestamp("2016-01-01", tz="UTC")
DEV_END = pd.Timestamp("2025-01-01", tz="UTC")
CAL_END = pd.Timestamp("2024-01-01", tz="UTC")


def download_dropbox_file(path: str, output: Path) -> Path:
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
    with urllib.request.urlopen(req, timeout=300) as response, output.open("wb") as handle:
        handle.write(response.read())
    return output


def load_xau_h1(zip_path: Path, work: Path) -> pd.DataFrame:
    unpack = work / "xau_h1_unpacked"
    unpack.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(unpack)
    matches = list(unpack.rglob("XAUUSD_H1_2016_2025_MASTER.csv"))
    if not matches:
        raise FileNotFoundError("XAUUSD_H1_2016_2025_MASTER.csv not found")
    df = pd.read_csv(matches[0])
    required = {"timestamp", "open", "high", "low", "close"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"XAU H1 missing columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any() or df["timestamp"].duplicated().any():
        raise ValueError("Invalid XAU H1 timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any() or df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: invalid or duplicated timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def atr_wilder(df: pd.DataFrame, period: int = 20) -> np.ndarray:
    close = df["close"].to_numpy(dtype=float)
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    prev_close = np.r_[np.nan, close[:-1]]
    tr = np.maximum.reduce([high - low, np.abs(high - prev_close), np.abs(low - prev_close)])
    return pd.Series(tr).ewm(alpha=1 / period, adjust=False, min_periods=period).mean().to_numpy()


def trend_for_nison(value: Any) -> str:
    text = str(value or "").strip().upper()
    if text == "BULL_TREND":
        return "Uptrend"
    if text == "BEAR_TREND":
        return "Downtrend"
    return ""


def normalize_nison_direction(value: Any) -> str | None:
    text = str(value or "").strip().upper()
    if text in {"BUY", "BULL", "BULLISH", "BUY_CANDIDATE"}:
        return "BULLISH"
    if text in {"SELL", "BEAR", "BEARISH", "SELL_CANDIDATE"}:
        return "BEARISH"
    return None


def build_nison_evidence(
    bars: pd.DataFrame,
    market_state: pd.DataFrame,
    *,
    lookback_bars: int = 60,
) -> pd.DataFrame:
    src = bars.copy().sort_values("timestamp").reset_index(drop=True)
    state = market_state[["timestamp"] + [c for c in market_state.columns if c != "timestamp"]].copy()
    state = state.sort_values("timestamp").drop_duplicates("timestamp").set_index("timestamp")

    nison_ids = tuple(f"CANDLE_RULE_{i:04d}" if i <= 38 else f"NISON_MODULE_{i:04d}" for i in range(1, 45))
    rows: list[dict[str, Any]] = []

    # 0001/0002 are evaluated against the exact frozen runtime. The runtime
    # sees the engulfing pair; the confirmation bar supplies the break trigger,
    # and the evidence timestamp is the confirmation bar, so no future bar is
    # exposed before it exists.
    for i in range(2, len(src)):
        confirmation_bar = src.iloc[i]
        pair = [
            {
                "open": float(src.iloc[i - 2]["open"]),
                "high": float(src.iloc[i - 2]["high"]),
                "low": float(src.iloc[i - 2]["low"]),
                "close": float(src.iloc[i - 2]["close"]),
            },
            {
                "open": float(src.iloc[i - 1]["open"]),
                "high": float(src.iloc[i - 1]["high"]),
                "low": float(src.iloc[i - 1]["low"]),
                "close": float(src.iloc[i - 1]["close"]),
            },
        ]
        pair_ts = src.iloc[i - 1]["timestamp"]
        context_row = state.loc[pair_ts] if pair_ts in state.index else None
        market_trend = trend_for_nison(context_row.get("trend") if context_row is not None else None)
        if not market_trend:
            continue

        prev = pair[0]
        cur = pair[1]
        bull_break = float(confirmation_bar["high"]) > float(cur["high"])
        bear_break = float(confirmation_bar["low"]) < float(cur["low"])
        confirmation = {
            "break_above_engulfing_high": bull_break,
            "break_below_engulfing_low": bear_break,
        }
        for rule_id in ("CANDLE_RULE_0001", "CANDLE_RULE_0002"):
            raw = nison_evaluate_rule(
                rule_id,
                {
                    "candles": pair,
                    "context": {"trend": market_trend},
                    "confirmation": confirmation,
                },
            )
            rows.append(
                {
                    "timestamp": confirmation_bar["timestamp"],
                    "rule_id": rule_id.replace("CANDLE_RULE_", "NISON_"),
                    "status": raw.get("status", "NOT_EVALUABLE"),
                    "direction": normalize_nison_direction(raw.get("direction")),
                    "available": raw.get("status") == "PASS",
                    "gate": "RUNTIME",
                    "conflict": False,
                    "reason": raw.get("reason", ""),
                    "provenance": json.dumps(
                        raw.get("provenance", {"source": "Steve Nison", "lookahead": "none"}),
                        sort_keys=True,
                    ),
                }
            )

    # Preserve the 44-rule governed evidence surface. Rules 0003-0044 are
    # evaluated through their existing router against source OHLC candles and
    # source market context where available. Missing categorical facts remain
    # NOT_EVALUABLE rather than being synthesized.
    for i in range(2, len(src)):
        ts = src.iloc[i]["timestamp"]
        state_row = state.loc[ts] if ts in state.index else None
        ctx = {}
        if state_row is not None:
            ctx = {
                "trend": trend_for_nison(state_row.get("trend")),
                "volume": state_row.get("volume"),
                "volatility": state_row.get("volatility"),
                "location": state_row.get("location"),
            }
        prior = src.iloc[max(0, i - (lookback_bars - 1)) : i + 1]
        candles = [
            {
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
            }
            for _, r in prior.iterrows()
        ]
        for rule_num in range(3, 45):
            rule_id = f"CANDLE_RULE_{rule_num:04d}" if rule_num <= 38 else f"NISON_MODULE_{rule_num:04d}"
            raw = nison_evaluate_rule(rule_id, {"candles": candles, "context": ctx})
            rows.append(
                {
                    "timestamp": ts,
                    "rule_id": f"NISON_{rule_num:04d}",
                    "status": raw.get("status", "NOT_EVALUABLE"),
                    "direction": normalize_nison_direction(raw.get("direction")),
                    "available": raw.get("status") == "PASS",
                    "gate": "RUNTIME",
                    "conflict": False,
                    "reason": raw.get("reason", ""),
                    "provenance": json.dumps(
                        raw.get("provenance", {"source": "Steve Nison", "lookahead": "none"}),
                        sort_keys=True,
                    ),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return pd.DataFrame(
            columns=["timestamp", "rule_id", "status", "direction", "available", "gate", "conflict", "reason", "provenance"]
        )
    return out.sort_values(["timestamp", "rule_id"]).reset_index(drop=True)


def build_context(bars: pd.DataFrame, market_state: pd.DataFrame) -> pd.DataFrame:
    dev = bars[(bars["timestamp"] >= DEV_START) & (bars["timestamp"] < DEV_END)].copy()
    ctx = dev[["timestamp", "close"]].rename(columns={"close": "entry_price"})
    ctx["atr20"] = atr_wilder(dev, 20)

    state_cols = [c for c in ["timestamp", "trend", "structure", "volume", "volatility", "location", "interpretation"] if c in market_state.columns]
    if state_cols:
        state = market_state[state_cols].drop_duplicates("timestamp").copy()
        ctx = ctx.merge(state, on="timestamp", how="left")

    return ctx.sort_values("timestamp").reset_index(drop=True)


def split_mtf_source(mtf: pd.DataFrame, out_dir: Path) -> Path:
    required = {"timestamp", "H1_trend", "H4_trend"}
    missing = sorted(required - set(mtf.columns))
    if missing:
        raise ValueError(f"XAU MTF source missing explicit trend fields: {missing}")

    root = out_dir / "mtf_source"
    h1_dir = root / "H1"
    h4_dir = root / "H4"
    h1_dir.mkdir(parents=True, exist_ok=True)
    h4_dir.mkdir(parents=True, exist_ok=True)

    mtf_dev = mtf[(mtf["timestamp"] >= DEV_START) & (mtf["timestamp"] < DEV_END)].copy()
    mtf_dev[["timestamp", "H1_trend"]].rename(columns={"H1_trend": "trend"}).to_csv(
        h1_dir / "XAUUSD_H1.csv", index=False
    )
    mtf_dev[["timestamp", "H4_trend"]].rename(columns={"H4_trend": "trend"}).to_csv(
        h4_dir / "XAUUSD_H4.csv", index=False
    )
    return root


def year_metrics(trades: pd.DataFrame) -> dict[str, Any]:
    if trades.empty:
        return {}
    valid = trades[trades["r_multiple"].notna()].copy()
    if valid.empty:
        return {}
    valid["year"] = pd.to_datetime(valid["timestamp"], utc=True).dt.year
    out: dict[str, Any] = {}
    for year, g in valid.groupby("year"):
        wins = int((g["r_multiple"] > 0).sum())
        losses = int((g["r_multiple"] < 0).sum())
        gw = float(g.loc[g["r_multiple"] > 0, "r_multiple"].sum())
        gl = float(-g.loc[g["r_multiple"] < 0, "r_multiple"].sum())
        out[str(int(year))] = {
            "trades": int(len(g)),
            "wins": wins,
            "losses": losses,
            "win_rate": float(wins / len(g)) if len(g) else None,
            "profit_factor": float(gw / gl) if gl else None,
            "total_R": float(g["r_multiple"].sum()),
            "max_drawdown_R": float((g["r_multiple"].cumsum() - g["r_multiple"].cumsum().cummax()).min()),
        }
    return out


def run(output_dir: Path) -> dict[str, Any]:
    source_dir = output_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    h1_zip = download_dropbox_file(XAU_H1_DROPBOX_PATH, source_dir / "XAUUSD_H1_2016_2025_MASTER.zip")
    mtf_csv = download_dropbox_file(XAU_MTF_DROPBOX_PATH, source_dir / "XAUUSD_MTF_H4_H1.csv")
    state_csv = download_dropbox_file(XAU_MARKET_STATE_DROPBOX_PATH, source_dir / "XAUUSD_MARKET_STATE.csv")

    bars = load_xau_h1(h1_zip, output_dir)
    mtf = load_csv(mtf_csv)
    market_state = load_csv(state_csv)

    dev_bars = bars[(bars["timestamp"] >= DEV_START) & (bars["timestamp"] < DEV_END)].copy()
    if dev_bars.empty:
        raise ValueError("No 2016-2024 XAU H1 bars")

    context = build_context(bars, market_state)
    context_path = output_dir / "XAUUSD_CONTEXT_2016_2024.csv"
    context.to_csv(context_path, index=False)

    mtf_dir = split_mtf_source(mtf, output_dir)

    murphy = emit_murphy(dev_bars)
    murphy_path = output_dir / "XAUUSD_MURPHY_EVIDENCE_2016_2024.csv"
    murphy.to_csv(murphy_path, index=False)

    nison = build_nison_evidence(dev_bars, market_state)
    nison_path = output_dir / "XAUUSD_NISON_EVIDENCE_2016_2024.csv"
    nison.to_csv(nison_path, index=False)

    decision_dir = output_dir / "DECISION_BRAIN_RUN_2016_2024"
    result = run_decision_brain(
        h1=output_dir / "source" / "xau_h1_unpacked" / "XAUUSD_H1_2016_2025_MASTER.csv",
        murphy=murphy_path,
        nison=nison_path,
        context=context_path,
        output_dir=decision_dir,
        mtf_dir=mtf_dir,
    )

    trades = pd.read_csv(decision_dir / "executed_trades_2016_2024.csv") if (decision_dir / "executed_trades_2016_2024.csv").exists() else pd.DataFrame()

    nison_pass = nison[nison["status"].astype(str).str.upper().eq("PASS")]
    murphy_pass = murphy[murphy["status"].astype(str).str.upper().eq("PASS")]

    summary = {
        "status": "DIAGNOSTIC_NOT_OFFICIAL",
        "development_window": "2016-2024",
        "calibration_window": "2016-2023",
        "oos_window": "2024",
        "2025_used": False,
        "source": {
            "xau_h1_rows_2016_2024": int(len(dev_bars)),
            "mtf_rows_2016_2024": int(len(mtf[(mtf["timestamp"] >= DEV_START) & (mtf["timestamp"] < DEV_END)])),
            "market_state_rows_2016_2024": int(len(market_state[(market_state["timestamp"] >= DEV_START) & (market_state["timestamp"] < DEV_END)])),
        },
        "murphy": {
            "rules": 34,
            "rows": int(len(murphy)),
            "pass_rows": int(len(murphy_pass)),
            "directional_timestamps": int(
                murphy[murphy["direction"].isin(["BULLISH", "BEARISH"]) & murphy["status"].eq("PASS")]["timestamp"].nunique()
            ),
        },
        "nison": {
            "rules": 44,
            "rows": int(len(nison)),
            "pass_rows": int(len(nison_pass)),
            "directional_pass_rows": int(
                nison[nison["direction"].isin(["BULLISH", "BEARISH"]) & nison["status"].eq("PASS")].shape[0]
            ),
            "rule_pass_counts": {
                str(k): int(v)
                for k, v in nison_pass["rule_id"].value_counts().to_dict().items()
            },
        },
        "decision_brain": result.get("metrics", {}),
        "year_breakdown": year_metrics(trades),
        "mtf_source_consumed": True,
        "risk_execution_contract": "existing frozen runner: SL 0.75 ATR, TP 2R",
        "official_profitability_claim": False,
    }
    (output_dir / "XAUUSD_FULL_PIPELINE_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            print(f"[XAU_FULL] running elapsed={int(time.monotonic() - started)}s", flush=True)

    watcher = threading.Thread(target=heartbeat, daemon=True)
    watcher.start()
    try:
        summary = run(args.output_dir)
    finally:
        stop.set()
        watcher.join(timeout=2)

    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
