from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain

PAIR = "GBPUSD"
LOCKED_OOS_YEAR = 2025
DIRECTIONAL = {"BULLISH", "BEARISH"}
TREND_SCORE = {
    "BULL_TREND": 1.0,
    "BULLISH": 1.0,
    "UPTREND": 1.0,
    "BEAR_TREND": -1.0,
    "BEARISH": -1.0,
    "DOWNTREND": -1.0,
    "TRANSITION": 0.0,
    "RANGE": 0.0,
    "INSIDE_RANGE": 0.0,
    "MIXED": 0.0,
    "UNKNOWN": 0.0,
}


def read_csv(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def normalize_direction(value) -> str:
    text = str(value or "").upper()
    if text in {"BULL", "BULLISH", "UP", "UPTREND"}:
        return "BULLISH"
    if text in {"BEAR", "BEARISH", "DOWN", "DOWNTREND"}:
        return "BEARISH"
    return "NONE"


def trend_score(value) -> float:
    text = str(value or "").upper()
    return TREND_SCORE.get(text, 0.0)


def build_murphy_0021(h1: pd.DataFrame, m1: pd.DataFrame) -> pd.DataFrame:
    from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021

    h1 = h1.copy()
    m1 = m1.copy()
    h1["previous_close"] = h1["close"].shift(1)
    m1["h1_timestamp"] = m1["timestamp"].dt.floor("h")
    volume = (
        m1.groupby("h1_timestamp", as_index=False)
        .agg(volume=("volume", "sum"))
        .sort_values("h1_timestamp")
    )
    volume["previous_volume"] = volume["volume"].shift(1)
    volume["volume_direction"] = None
    volume.loc[volume["volume"] > volume["previous_volume"], "volume_direction"] = "UP"
    volume.loc[volume["volume"] < volume["previous_volume"], "volume_direction"] = "DOWN"
    merged = h1.merge(
        volume[["h1_timestamp", "volume_direction"]],
        left_on="timestamp",
        right_on="h1_timestamp",
        how="left",
    )
    rows = []
    for row in merged.itertuples(index=False):
        result = evaluate_0021(
            {
                "close": row.close,
                "previous_close": row.previous_close,
                "volume_direction": row.volume_direction,
            }
        )
        rows.append(
            {
                "timestamp": row.timestamp,
                "status": result["status"],
                "direction": normalize_direction(result.get("directional_confirmation")),
                "source_rule_id": result["rule_id"],
            }
        )
    return pd.DataFrame(rows)


def context_bucket(brain, murphy_direction: str, mtf_state: str) -> str:
    if murphy_direction not in DIRECTIONAL:
        return "NO_MURPHY_DIRECTION"
    bias = normalize_direction(brain.directional_bias)
    if brain.market_state == "trend" and bias == murphy_direction:
        return "TREND_ALIGNED"
    if brain.market_state == "trend" and bias in DIRECTIONAL and bias != murphy_direction:
        return "TREND_OPPOSED"
    if brain.market_state == "range/transition":
        return "RANGE_TRANSITION"
    if brain.market_state == "uncertain":
        return "UNCERTAIN"
    if mtf_state == "MIXED":
        return "MTF_MIXED"
    return "OTHER"


def signed_return(close_now: float, close_future: float, direction: str) -> float:
    raw = (close_future / close_now) - 1.0
    return raw if direction == "BULLISH" else -raw


def mean_or_zero(series) -> float:
    vals = [float(v) for v in series if v is not None and math.isfinite(float(v))]
    return sum(vals) / len(vals) if vals else 0.0


def audit(market_state: Path, mtf: Path, h1: Path, m1: Path, year: int, output: Path) -> dict:
    if year >= LOCKED_OOS_YEAR:
        raise ValueError("2025_OOS_LOCKED: context-gating shadow is pre-2025 only")

    state = read_csv(market_state, {"timestamp", "close", "atr20"})
    state = state[state["timestamp"].dt.year.eq(year)].copy()
    mtf_df = read_csv(mtf, {"timestamp", "H4_trend", "H1_trend", "MTF_state"})
    h1_df = read_csv(h1, {"timestamp", "open", "high", "low", "close"})
    m1_df = read_csv(m1, {"timestamp", "open", "high", "low", "close", "volume"})
    h1_df["fwd_12"] = h1_df["close"].shift(-12)
    h1_df["fwd_24"] = h1_df["close"].shift(-24)
    h1_df["fwd_48"] = h1_df["close"].shift(-48)
    murphy = build_murphy_0021(h1_df.drop(columns=["fwd_12", "fwd_24", "fwd_48"]), m1_df)

    mtf_lookup = mtf_df.set_index("timestamp")
    h1_lookup = h1_df.set_index("timestamp")
    murphy_lookup = murphy.set_index("timestamp")
    records = []

    for ts, row in state.set_index("timestamp").iterrows():
        if ts not in mtf_lookup.index or ts not in murphy_lookup.index or ts not in h1_lookup.index:
            continue
        mtf_row = mtf_lookup.loc[ts]
        m = murphy_lookup.loc[ts]
        h = h1_lookup.loc[ts]
        murphy_direction = str(m.get("direction", "NONE"))
        mtf_score = (trend_score(mtf_row.get("H4_trend")) + trend_score(mtf_row.get("H1_trend"))) / 2.0
        brain_row = {
            "mtf_trend_score": mtf_score,
            "H1_trend_regime": trend_score(mtf_row.get("H1_trend")),
            "H4_trend_regime": trend_score(mtf_row.get("H4_trend")),
            "volume_available": False,
        }
        brain = decision_brain.assess(brain_row, similarity=None)
        bucket = context_bucket(brain, murphy_direction, str(mtf_row.get("MTF_state", "UNKNOWN")))
        close_now = float(h["close"])
        rec = {
            "timestamp": ts.isoformat(),
            "murphy_direction": murphy_direction,
            "brain_state": brain.market_state,
            "brain_bias": brain.directional_bias,
            "brain_confidence": float(brain.confidence),
            "h4_trend": mtf_row.get("H4_trend"),
            "h1_trend": mtf_row.get("H1_trend"),
            "mtf_state": mtf_row.get("MTF_state"),
            "context_bucket": bucket,
            "fwd12_signed_return": None,
            "fwd24_signed_return": None,
            "fwd48_signed_return": None,
            "fwd12_atr_multiple": None,
            "fwd24_atr_multiple": None,
            "fwd48_atr_multiple": None,
        }
        for horizon, key in [(12, "fwd12"), (24, "fwd24"), (48, "fwd48")]:
            future = h.get(key)
            if pd.notna(future) and year == pd.Timestamp(ts).year and (pd.Timestamp(ts) + pd.Timedelta(hours=horizon)).year < LOCKED_OOS_YEAR:
                sr = signed_return(close_now, float(future), murphy_direction) if murphy_direction in DIRECTIONAL else None
                rec[f"fwd{horizon}_signed_return"] = sr
                if sr is not None and float(row["atr20"]) > 0:
                    rec[f"fwd{horizon}_atr_multiple"] = sr / float(row["atr20"])
        records.append(rec)

    out = pd.DataFrame(records)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)

    directional = out[out["murphy_direction"].isin(DIRECTIONAL)].copy()
    bucket_rows = []
    for bucket, group in directional.groupby("context_bucket", dropna=False):
        row = {
            "context_bucket": bucket,
            "signals": int(len(group)),
            "fwd12_count": int(group["fwd12_signed_return"].notna().sum()),
            "fwd12_hit_rate_pct": round(100.0 * (group["fwd12_signed_return"] > 0).mean(), 4) if group["fwd12_signed_return"].notna().any() else 0.0,
            "fwd12_mean_signed_return": mean_or_zero(group["fwd12_signed_return"].dropna()),
            "fwd24_count": int(group["fwd24_signed_return"].notna().sum()),
            "fwd24_hit_rate_pct": round(100.0 * (group["fwd24_signed_return"] > 0).mean(), 4) if group["fwd24_signed_return"].notna().any() else 0.0,
            "fwd24_mean_signed_return": mean_or_zero(group["fwd24_signed_return"].dropna()),
            "fwd48_count": int(group["fwd48_signed_return"].notna().sum()),
            "fwd48_hit_rate_pct": round(100.0 * (group["fwd48_signed_return"] > 0).mean(), 4) if group["fwd48_signed_return"].notna().any() else 0.0,
            "fwd48_mean_signed_return": mean_or_zero(group["fwd48_signed_return"].dropna()),
            "fwd24_mean_atr_multiple": mean_or_zero(group["fwd24_atr_multiple"].dropna()),
        }
        bucket_rows.append(row)

    summary = {
        "status": "PASS_SHADOW_ONLY",
        "mode": "REAL_DATA_PRE2025_CONTEXT_GATE_SHADOW",
        "evaluation_year": year,
        "pair": PAIR,
        "events": int(len(out)),
        "murphy_directional_events": int(len(directional)),
        "context_buckets": bucket_rows,
        "purpose": "Measure whether the existing Decision Brain market-state context changes the quality of existing Murphy direction without changing rule semantics.",
        "brain_role": "context_and_regime_only",
        "murphy_role": "directional_anchor_MURPHY_0021",
        "nison_used": False,
        "memory_used": False,
        "risk_used": False,
        "execution_used": False,
        "new_rule_semantics": False,
        "policy_changed": False,
        "replacement_pnl": False,
        "oos_2025_locked": True,
        "oos_tuning": False,
        "future_feature_leakage": False,
        "label_rule": "Forward H1 returns are evaluation labels only; event features are restricted to timestamp t and only horizons fully before 2025 are retained.",
    }
    output.with_suffix(".json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--market-state", required=True, type=Path)
    parser.add_argument("--mtf", required=True, type=Path)
    parser.add_argument("--h1", required=True, type=Path)
    parser.add_argument("--m1", required=True, type=Path)
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.market_state, args.mtf, args.h1, args.m1, args.year, args.output), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
