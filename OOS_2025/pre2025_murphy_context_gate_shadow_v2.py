from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021

LOCKED_OOS_YEAR = 2025
DIRECTIONAL = {"BULLISH", "BEARISH"}
TREND_SCORE = {
    "BULL_TREND": 1.0, "BULLISH": 1.0, "UPTREND": 1.0,
    "BEAR_TREND": -1.0, "BEARISH": -1.0, "DOWNTREND": -1.0,
    "TRANSITION": 0.0, "RANGE": 0.0, "MIXED": 0.0,
    "INSIDE_RANGE": 0.0, "UNKNOWN": 0.0,
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


def norm_direction(value) -> str:
    v = str(value or "").upper()
    if v in {"BULL", "BULLISH", "UP", "UPTREND"}:
        return "BULLISH"
    if v in {"BEAR", "BEARISH", "DOWN", "DOWNTREND"}:
        return "BEARISH"
    return "NONE"


def score(value) -> float:
    return TREND_SCORE.get(str(value or "").upper(), 0.0)


def build_murphy(h1: pd.DataFrame, m1: pd.DataFrame) -> pd.DataFrame:
    h = h1.copy()
    m = m1.copy()
    h["previous_close"] = h["close"].shift(1)
    m["h1_timestamp"] = m["timestamp"].dt.floor("h")
    v = m.groupby("h1_timestamp", as_index=False).agg(volume=("volume", "sum"))
    v["previous_volume"] = v["volume"].shift(1)
    v["volume_direction"] = None
    v.loc[v["volume"] > v["previous_volume"], "volume_direction"] = "UP"
    v.loc[v["volume"] < v["previous_volume"], "volume_direction"] = "DOWN"
    merged = h.merge(v[["h1_timestamp", "volume_direction"]], left_on="timestamp", right_on="h1_timestamp", how="left")
    out = []
    for r in merged.itertuples(index=False):
        res = evaluate_0021({"close": r.close, "previous_close": r.previous_close, "volume_direction": r.volume_direction})
        out.append({"timestamp": r.timestamp, "direction": norm_direction(res.get("directional_confirmation")), "rule_id": res.get("rule_id")})
    return pd.DataFrame(out)


def mean(xs) -> float:
    vals = [float(x) for x in xs if x is not None and math.isfinite(float(x))]
    return sum(vals) / len(vals) if vals else 0.0


def run(args) -> dict:
    year = int(args.year)
    if year >= LOCKED_OOS_YEAR:
        raise ValueError("2025_OOS_LOCKED")

    state = read_csv(Path(args.market_state), {"timestamp", "close"})
    if "atr20" not in state.columns:
        state["atr20"] = float("nan")
    state = state[state.timestamp.dt.year.eq(year)].copy()

    mtf = read_csv(Path(args.mtf), {"timestamp", "H4_trend", "H1_trend", "MTF_state"})
    h1 = read_csv(Path(args.h1), {"timestamp", "open", "high", "low", "close"})
    m1 = read_csv(Path(args.m1), {"timestamp", "open", "high", "low", "close", "volume"})
    h1["fwd12"] = h1["close"].shift(-12)
    h1["fwd24"] = h1["close"].shift(-24)
    h1["fwd48"] = h1["close"].shift(-48)
    murphy = build_murphy(h1.drop(columns=["fwd12", "fwd24", "fwd48"]), m1)

    state_i = state.set_index("timestamp")
    mtf_i = mtf.set_index("timestamp")
    h1_i = h1.set_index("timestamp")
    murphy_i = murphy.set_index("timestamp")
    rows = []

    for ts, srow in state_i.iterrows():
        if ts not in mtf_i.index or ts not in h1_i.index or ts not in murphy_i.index:
            continue
        mt = mtf_i.loc[ts]
        h = h1_i.loc[ts]
        md = str(murphy_i.loc[ts].get("direction", "NONE"))
        mtf_score = (score(mt["H4_trend"]) + score(mt["H1_trend"])) / 2.0
        assessment = decision_brain.assess({
            "mtf_trend_score": mtf_score,
            "H1_trend_regime": score(mt["H1_trend"]),
            "H4_trend_regime": score(mt["H4_trend"]),
            "volume_available": False,
        }, similarity=None)

        if md not in DIRECTIONAL:
            bucket = "NO_MURPHY_DIRECTION"
        elif assessment.market_state == "trend" and norm_direction(assessment.directional_bias) == md:
            bucket = "TREND_ALIGNED"
        elif assessment.market_state == "trend":
            bucket = "TREND_OPPOSED"
        elif assessment.market_state == "uncertain":
            bucket = "UNCERTAIN"
        else:
            bucket = "RANGE_TRANSITION"

        rec = {
            "timestamp": ts.isoformat(), "murphy_direction": md,
            "brain_state": assessment.market_state, "brain_bias": assessment.directional_bias,
            "brain_confidence": float(assessment.confidence),
            "h4_trend": mt["H4_trend"], "h1_trend": mt["H1_trend"], "mtf_state": mt["MTF_state"],
            "context_bucket": bucket,
        }
        close_now = float(h["close"])
        for hours in (12, 24, 48):
            future = h.get(f"fwd{hours}")
            valid = pd.notna(future) and (pd.Timestamp(ts) + pd.Timedelta(hours=hours)).year < LOCKED_OOS_YEAR
            sr = None
            if valid and md in DIRECTIONAL:
                raw = float(future) / close_now - 1.0
                sr = raw if md == "BULLISH" else -raw
            rec[f"fwd{hours}_signed_return"] = sr
            atr = srow.get("atr20")
            rec[f"fwd{hours}_atr_multiple"] = (sr / float(atr)) if sr is not None and pd.notna(atr) and float(atr) > 0 else None
        rows.append(rec)

    out = pd.DataFrame(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)

    d = out[out.murphy_direction.isin(DIRECTIONAL)]
    buckets = []
    for bucket, g in d.groupby("context_bucket", dropna=False):
        item = {"context_bucket": bucket, "signals": int(len(g))}
        for h in (12, 24, 48):
            s = g[f"fwd{h}_signed_return"].dropna()
            item[f"fwd{h}_count"] = int(len(s))
            item[f"fwd{h}_hit_rate_pct"] = round(100 * float((s > 0).mean()), 4) if len(s) else 0.0
            item[f"fwd{h}_mean_signed_return"] = mean(s)
        a = g["fwd24_atr_multiple"].dropna()
        item["fwd24_mean_atr_multiple"] = mean(a)
        buckets.append(item)

    summary = {
        "status": "PASS_SHADOW_ONLY", "mode": "REAL_DATA_PRE2025_CONTEXT_GATE_SHADOW_V2",
        "evaluation_year": year, "pair": "GBPUSD", "events": int(len(out)),
        "murphy_directional_events": int(len(d)), "context_buckets": buckets,
        "brain_role": "context_and_regime_only", "murphy_role": "directional_anchor_MURPHY_0021",
        "nison_used": False, "memory_used": False, "risk_used": False, "execution_used": False,
        "new_rule_semantics": False, "policy_changed": False, "replacement_pnl": False,
        "oos_2025_locked": True, "oos_tuning": False, "future_feature_leakage": False,
        "atr20_optional": "atr20 is used only when present; forward-return labels remain the primary shadow statistic.",
    }
    output.with_suffix(".json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--mtf", required=True, type=Path)
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--output", required=True, type=Path)
    run(p.parse_args())
