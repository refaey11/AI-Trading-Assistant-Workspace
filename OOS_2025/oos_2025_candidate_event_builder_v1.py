#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

CANDIDATES = {
    "C1_HIGH_STRONG_BEARISH_MTF": lambda d: (d.volatility_state == "HIGH") & (d.mtf_context == "strong_bearish"),
    "C2_HIGH_H4_BEARISH": lambda d: (d.volatility_state == "HIGH") & (d.H4_trend_regime == -1),
    "C3_SELL_HIGH": lambda d: (d.direction == "SELL") & (d.volatility_state == "HIGH"),
}


def first_nonblank(primary, fallback):
    p = primary.astype("string") if primary is not None else pd.Series(pd.NA, index=fallback.index, dtype="string")
    f = fallback.astype("string") if fallback is not None else pd.Series(pd.NA, index=p.index, dtype="string")
    p = p.mask(p.str.strip().eq("") | p.isna())
    return p.fillna(f)


def main():
    ap = argparse.ArgumentParser()
    for n in ["murphy", "h1", "market-state", "mtf", "out-dir"]:
        ap.add_argument("--" + n, required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    mur = pd.read_csv(a.murphy, low_memory=False)
    h1 = pd.read_csv(a.h1, low_memory=False)
    ms = pd.read_csv(a.market_state, low_memory=False)
    mtf = pd.read_csv(a.mtf, low_memory=False)

    for df in [mur, h1, ms, mtf]:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if any(df.timestamp.isna().any() for df in [mur, h1, ms, mtf]):
        raise SystemExit("FAIL_CLOSED_INVALID_TIMESTAMP")
    if set(mur.timestamp.dt.year.astype(int)) - {2025}:
        raise SystemExit("FAIL_CLOSED_MURPHY_NOT_2025_ONLY")

    # Murphy producer files exist in more than one schema. Prefer populated
    # direction, falling back to directional_confirmation when direction is
    # absent or blank. This is schema normalization only; no rule semantics
    # are changed.
    mur["status"] = mur.get("status", pd.Series("", index=mur.index)).astype(str).str.upper().str.strip()
    direction_primary = mur["direction"] if "direction" in mur.columns else None
    direction_fallback = mur["directional_confirmation"] if "directional_confirmation" in mur.columns else None
    mur["direction"] = first_nonblank(direction_primary, direction_fallback).str.upper().str.strip()
    mur["source_rule_id"] = first_nonblank(
        mur["source_rule_id"] if "source_rule_id" in mur.columns else None,
        mur["rule_id"] if "rule_id" in mur.columns else pd.Series(pd.NA, index=mur.index),
    ).fillna("")
    mur = mur[(mur.status == "PASS") & mur.direction.isin(["BUY", "SELL", "BULLISH", "BEARISH"])].copy()
    mur["direction"] = mur.direction.replace({"BULLISH": "BUY", "BEARISH": "SELL"})

    h1 = h1.sort_values("timestamp").reset_index(drop=True)
    required_ohlc = {"open", "high", "low", "close"}
    if required_ohlc - set(h1.columns):
        raise SystemExit("FAIL_CLOSED_H1_MISSING_OHLC")
    for c in required_ohlc:
        h1[c] = pd.to_numeric(h1[c], errors="coerce")
    prev_close = h1["close"].shift(1)
    tr = pd.concat([(h1.high - h1.low), (h1.high - prev_close).abs(), (h1.low - prev_close).abs()], axis=1).max(axis=1)
    # ATR20 is derived only from completed H1 bars and then shifted one bar,
    # so the ATR available at event t cannot include the event bar.
    h1["ATR20"] = tr.rolling(20, min_periods=20).mean().shift(1)

    ms = ms.sort_values("timestamp")
    mtf = mtf.sort_values("timestamp")
    mur = mur.sort_values("timestamp")
    if "volatility_state" not in ms.columns:
        raise SystemExit("FAIL_CLOSED_MARKET_STATE_MISSING_VOLATILITY_STATE")
    mscols = ["timestamp", "volatility_state"] + [c for c in ["trend", "location"] if c in ms.columns]
    x = pd.merge_asof(mur, ms[mscols], on="timestamp", direction="backward", allow_exact_matches=False)

    mtfneed = {"mtf_context", "H4_trend_regime"}
    if mtfneed - set(mtf.columns):
        raise SystemExit("FAIL_CLOSED_MTF_REQUIRED_FIELDS")
    mtfcols = ["timestamp", "mtf_context", "H4_trend_regime"] + [c for c in ["mtf_trend_score"] if c in mtf.columns]
    x = pd.merge_asof(x, mtf[mtfcols], on="timestamp", direction="backward", allow_exact_matches=False)
    x = pd.merge_asof(x, h1[["timestamp", "ATR20"]], on="timestamp", direction="backward", allow_exact_matches=False)

    x["ATR20"] = pd.to_numeric(x.ATR20, errors="coerce")
    x["H4_trend_regime"] = pd.to_numeric(x.H4_trend_regime, errors="coerce")
    x = x.dropna(subset=["ATR20", "volatility_state", "mtf_context", "H4_trend_regime"]).copy()
    x["volatility_state"] = x.volatility_state.astype(str).str.upper().str.strip()
    x["mtf_context"] = x.mtf_context.astype(str).str.lower().str.strip()

    # Strict event-time execution: enter at the next H1 bar open.
    ts = h1.timestamp.astype("int64").to_numpy()
    rows = []
    for r in x.itertuples(index=False):
        j = int(pd.Series(ts).searchsorted(r.timestamp.value, side="right"))
        if j >= len(h1):
            continue
        entry = h1.iloc[j].open
        atr = float(r.ATR20)
        if pd.isna(entry) or atr <= 0:
            continue
        dist = 0.75 * atr
        sl = entry - dist if r.direction == "BUY" else entry + dist
        tp = entry + 2 * dist if r.direction == "BUY" else entry - 2 * dist
        result, exit_time, net = "OPEN", None, None
        for k in range(j, len(h1)):
            b = h1.iloc[k]
            hi, lo = float(b.high), float(b.low)
            hit_sl = (lo <= sl) if r.direction == "BUY" else (hi >= sl)
            hit_tp = (hi >= tp) if r.direction == "BUY" else (lo <= tp)
            if hit_sl and hit_tp:
                result, exit_time = "AMBIGUOUS", b.timestamp
                break
            if hit_tp:
                result, exit_time, net = "TP", b.timestamp, 2.0
                break
            if hit_sl:
                result, exit_time, net = "SL", b.timestamp, -1.0
                break
        rows.append({
            "event_time": r.timestamp,
            "direction": r.direction,
            "source_rule_id": getattr(r, "source_rule_id", ""),
            "volatility_state": r.volatility_state,
            "mtf_context": r.mtf_context,
            "H4_trend_regime": r.H4_trend_regime,
            "entry_time": h1.iloc[j].timestamp,
            "entry_price": entry,
            "ATR20_asof": atr,
            "exit_time": exit_time,
            "outcome": result,
            "net_R": net,
        })

    ev = pd.DataFrame(rows)
    if ev.empty:
        raise SystemExit("FAIL_CLOSED_NO_2025_EVENTS_AFTER_ASOF_EXECUTION_GATES")

    ev.to_csv(out / "oos_2025_candidate_events.csv", index=False)
    stats = []
    for cid, fn in CANDIDATES.items():
        g = ev[fn(ev)]
        r = pd.to_numeric(g.net_R, errors="coerce").dropna()
        wins = r[r > 0].sum()
        losses = -r[r < 0].sum()
        stats.append({
            "candidate_id": cid,
            "events": len(g),
            "evaluated": len(r),
            "TP": int((g.outcome == "TP").sum()),
            "SL": int((g.outcome == "SL").sum()),
            "ambiguous": int((g.outcome == "AMBIGUOUS").sum()),
            "open": int((g.outcome == "OPEN").sum()),
            "win_rate": float((r > 0).mean()) if len(r) else None,
            "expectancy_R": float(r.mean()) if len(r) else None,
            "profit_factor": float(wins / losses) if losses else None,
            "total_net_R": float(r.sum()) if len(r) else 0.0,
        })
    pd.DataFrame(stats).to_csv(out / "oos_2025_candidate_results.csv", index=False)
    manifest = {
        "status": "OOS_2025_EVALUATION_ONLY",
        "window": "2025-only",
        "candidate_set_frozen": True,
        "tuning_applied": False,
        "threshold_sweep": False,
        "future_data_used": False,
        "strict_asof_context": True,
        "murphy_schema_normalization": "direction_fallback_to_directional_confirmation_when_direction_blank",
        "atr20_source": "H1_completed_bars_fallback_when_market_state_missing",
        "entry_next_h1_open": True,
        "stop_atr": 0.75,
        "target_R": 2.0,
        "official_profitability_claim_allowed": False,
        "canonical_three_book_mode": False,
    }
    (out / "oos_2025_candidate_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(pd.DataFrame(stats).to_string(index=False))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
