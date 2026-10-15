"""Development-only funnel attribution for the current GBPUSD stack.

This is a SHADOW diagnostic. It does not change Decision Brain semantics,
rules, risk limits, or OOS handling. It measures where candidate events are
lost before/at the current three-book decision path.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

EXPECTED_NISON = {f"NISON_{i:04d}" for i in range(1, 45)}
MTF_FIELDS = [
    "mtf_trend_score", "M5_trend_regime", "M15_trend_regime",
    "M30_trend_regime", "H1_trend_regime", "H4_trend_regime", "D1_trend_regime",
]

def load(path: Path) -> pd.DataFrame:
    d = pd.read_csv(path, low_memory=False)
    if "timestamp" not in d.columns:
        raise ValueError(f"{path}: missing timestamp")
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce", format="mixed")
    return d.dropna(subset=["timestamp"]).sort_values("timestamp", kind="stable")

def one_by_ts(d: pd.DataFrame) -> dict[pd.Timestamp, pd.DataFrame]:
    return {ts: g for ts, g in d.groupby("timestamp", sort=False)}

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    r = a.root
    h1 = load(next(r.glob("unpacked/h1/GBPUSD_H1_2016_2025_MASTER.csv")))
    market = load(r / "market_state.csv")
    mtf_files = sorted((r / "unpacked/mtf").rglob("*.csv"))
    mtf_path = next((x for x in mtf_files if set(MTF_FIELDS).issubset(set(pd.read_csv(x, nrows=0).columns))), None)
    if mtf_path is None:
        raise SystemExit("MISSING_SIX_TF_MTF_SOURCE")
    mtf = load(mtf_path)
    murphy = load(next(r.glob("unpacked/murphy/MURPHY_2016_2024_FULL_EVIDENCE.csv")))
    nison = load(r / "nison.csv")
    ncol = "source_rule_id" if "source_rule_id" in nison.columns else "rule_id"
    nison["rule_norm"] = nison[ncol].astype("string").str.strip()
    m_status = murphy.get("status", pd.Series(index=murphy.index, dtype="object")).astype(str).str.upper().str.strip()
    m_dir = murphy.get("direction", pd.Series(index=murphy.index, dtype="object")).astype(str).str.upper().str.strip().replace({"BULLISH":"BUY", "BEARISH":"SELL"})
    murphy_pass = murphy.loc[m_status.eq("PASS") & m_dir.isin({"BUY", "SELL"})].copy()
    murphy_pass["direction_norm"] = m_dir.loc[murphy_pass.index]
    n_groups = one_by_ts(nison)
    market_groups = one_by_ts(market)
    mtf_groups = one_by_ts(mtf)

    rows = []
    for ts, g in one_by_ts(murphy_pass).items():
        if ts.year < 2016 or ts.year > 2024:
            continue
        direction = str(g.iloc[0].direction_norm)
        if len(g) != 1:
            rows.append({"timestamp": ts.isoformat(), "stage":"murphy_unique_directional", "passed":False, "reason":"MULTIPLE_MURPHY_DIRECTIONAL_PASS"})
            continue
        market_g = market_groups.get(ts)
        mtf_g = mtf_groups.get(ts)
        n_g = n_groups.get(ts)
        mtf_ok = mtf_g is not None and len(mtf_g) >= 1 and all(pd.notna(mtf_g.iloc[-1].get(k)) for k in MTF_FIELDS)
        market_ok = market_g is not None and len(market_g) >= 1
        nison_ids = set() if n_g is None else {x for v in n_g.rule_norm.dropna() for x in str(v).split("|") if x.strip()}
        nison_44 = n_g is not None and len(n_g) == 44 and nison_ids == EXPECTED_NISON
        nison_pass_dirs = set()
        n_fail = n_ne = 0
        if n_g is not None:
            ns = n_g.get("status", pd.Series(index=n_g.index, dtype="object")).astype(str).str.upper().str.strip()
            dirs = n_g.get("direction", pd.Series(index=n_g.index, dtype="object")).astype(str).str.upper().str.strip().replace({"BULLISH":"BUY", "BEARISH":"SELL"})
            nison_pass_dirs = {x for x in dirs.loc[ns.eq("PASS")].tolist() if x in {"BUY","SELL"}}
            n_fail = int(ns.eq("FAIL").sum())
            n_ne = int(ns.eq("NOT_EVALUABLE").sum())
        aligned = direction in nison_pass_dirs
        opposite = ("SELL" if direction == "BUY" else "BUY") in nison_pass_dirs
        atr_ok = False
        if market_ok:
            mr = market_g.iloc[-1]
            for k in ("atr", "atr20", "H1_atr"):
                if k in mr.index and pd.notna(mr[k]) and str(mr[k]).strip() != "":
                    try: atr_ok = float(mr[k]) > 0
                    except Exception: atr_ok = False
                    if atr_ok: break
        rows.append({
            "timestamp": ts.isoformat(),
            "stage": "candidate",
            "passed": True,
            "direction": direction,
            "market_state_available": market_ok,
            "six_tf_available": bool(mtf_ok),
            "nison_44_complete": bool(nison_44),
            "nison_fail_count": n_fail,
            "nison_not_evaluable_count": n_ne,
            "nison_confirmed_aligned": bool(aligned and not opposite),
            "nison_contradictory": bool(opposite),
            "risk_inputs_available": bool(market_ok and atr_ok),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        report = {"status":"NO_MURPHY_DIRECTIONAL_CANDIDATES", "window":"2016-2024"}
    else:
        def count(col): return int(df[col].fillna(False).astype(bool).sum())
        cand = len(df)
        report = {
            "status": "SHADOW_FUNNEL_COMPLETE",
            "window": "2016-2024",
            "murphy_directional_candidate_events": cand,
            "market_state_available": count("market_state_available"),
            "six_tf_available": count("six_tf_available"),
            "nison_44_complete": count("nison_44_complete"),
            "nison_confirmed_aligned": count("nison_confirmed_aligned"),
            "nison_contradictory": count("nison_contradictory"),
            "risk_inputs_available": count("risk_inputs_available"),
            "trade_frequency_per_year": round(cand / 9.0, 3),
            "note": "Diagnostic only. No tuning or decision semantics changed.",
        }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output.with_suffix(".csv"), index=False)
    a.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
