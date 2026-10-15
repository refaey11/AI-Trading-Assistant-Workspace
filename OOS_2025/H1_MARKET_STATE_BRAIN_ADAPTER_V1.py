from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

TF_KEYS = ["M5", "M15", "M30", "H1", "H4", "D1"]


def norm_direction(v):
    t = str(v or "").strip().upper()
    if t in {"BUY", "BULL", "BULLISH", "UP", "UPTREND", "POSITIVE"}: return 1.0
    if t in {"SELL", "BEAR", "BEARISH", "DOWN", "DOWNTREND", "NEGATIVE"}: return -1.0
    try:
        x = float(v)
        return max(-1.0, min(1.0, x))
    except Exception:
        return 0.0


def volume_value(v):
    t = str(v or "").strip().upper()
    if t in {"STRONG", "HIGH", "EXPANDING", "SUPPORTIVE", "CONFIRMING", "POSITIVE", "BULLISH"}: return 1.0
    if t in {"WEAK", "LOW", "CONTRACTING", "NEGATIVE", "BEARISH"}: return -1.0
    try:
        x = float(v)
        return max(-1.0, min(1.0, x))
    except Exception:
        return 0.0


def main(src: Path, dst: Path):
    d = pd.read_csv(src, low_memory=False)
    required = {"timestamp", "trend"}
    missing = sorted(required - set(d.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce", format="mixed")
    if d.timestamp.isna().any(): raise ValueError("invalid timestamps")
    d = d.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    out = pd.DataFrame({"timestamp": d.timestamp})
    h1 = d["trend"].map(norm_direction)
    out["H1_trend_regime"] = h1
    out["mtf_trend_score"] = h1
    for tf in ["M5", "M15", "M30", "H4", "D1"]:
        out[f"{tf}_trend_regime"] = 0.0
    if "volume_state" in d.columns:
        out["H1_volume_regime"] = d["volume_state"].map(volume_value)
        out["volume_available"] = True
    elif "volume_ratio" in d.columns:
        vr = pd.to_numeric(d["volume_ratio"], errors="coerce").fillna(1.0)
        out["H1_volume_regime"] = (vr - 1.0).clip(-1.0, 1.0)
        out["volume_available"] = True
    else:
        out["H1_volume_regime"] = 0.0
        out["volume_available"] = False
    for tf in ["M5", "M15", "M30", "H4", "D1"]:
        out[f"{tf}_volume_regime"] = 0.0
    for c in ["close", "atr20"]:
        if c in d.columns: out[c] = d[c]
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dst, index=False)
    print({"rows": len(out), "source_mode": "H1_MARKET_STATE_ONLY", "mtf_trend_score_mapped": True, "H1_trend_regime_mapped": True, "volume_available": bool(out.volume_available.any()), "fabricated_timeframes": []})

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--src", type=Path, required=True)
    p.add_argument("--dst", type=Path, required=True)
    a=p.parse_args(); main(a.src,a.dst)
