from __future__ import annotations

"""Canonical governed E2E integration for the 2016-2024 development window.

This is orchestration only: existing book knowledge, evidence semantics and
Decision Brain V1 are not rebuilt. Historical memory is evidence only. Similarity
and Context-Aware Retrieval are consumed as governed evidence metadata; their
current packaged snapshots are not allowed to generate direction or tuning.
TIZ remains unresolved/optional for this development pass. Risk remains a real
execution gate. 2025 is excluded completely.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"


def read(path: Path, required: set[str], chunksize: int | None = None) -> pd.DataFrame:
    if chunksize:
        parts = list(pd.read_csv(path, chunksize=chunksize, low_memory=False))
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    else:
        df = pd.read_csv(path, low_memory=False)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_brain():
    spec = importlib.util.spec_from_file_location("recovered_decision_brain", BRAIN)
    if not spec or not spec.loader:
        raise RuntimeError("Decision Brain V1 load failed")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm_dir(v: Any) -> str | None:
    s = str(v or "").strip().upper()
    if s in {"BUY", "BULL", "BULLISH"}: return "BULLISH"
    if s in {"SELL", "BEAR", "BEARISH"}: return "BEARISH"
    return None


def split_ids(values) -> set[str]:
    out: set[str] = set()
    for v in values:
        if pd.isna(v): continue
        out.update(x.strip() for x in str(v).split("|") if x.strip())
    return out


def allowlist():
    d = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return set(d["verified_runtime"]["MURPHY"]), set(d["verified_runtime"]["NISON"])


def aggregate_murphy(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        p = g[g.status.astype(str).str.upper().eq("PASS")]
        dirs = {d for d in (norm_dir(x) for x in p.direction) if d}
        direction = next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        ids = split_ids(g.source_rule_id)
        rows.append({"timestamp": ts, "murphy_direction": direction, "murphy_rule_count": len(ids), "murphy_rule_ids": json.dumps(sorted(ids))})
    return pd.DataFrame(rows)


def aggregate_nison(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        p = g[g.status.astype(str).str.upper().eq("PASS")]
        f = g[g.status.astype(str).str.upper().eq("FAIL")]
        dirs = {d for d in (norm_dir(x) for x in p.direction) if d}
        conf = next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rows.append({"timestamp": ts, "nison_confirmation": conf, "nison_contradiction": bool(not f.empty), "nison_rule_count": int(g.rule_id.nunique())})
    return pd.DataFrame(rows)


def asof(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    if right.empty:
        return left.copy()
    r = right.sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    return pd.merge_asof(left.sort_values("timestamp"), r, on="timestamp", direction="backward", allow_exact_matches=True)


def build_brain_row(market: dict[str, Any], mtf: dict[str, Any]) -> dict[str, Any]:
    trend = {"BULL_TREND": 1.0, "BEAR_TREND": -1.0, "TRANSITION": 0.0, "UNKNOWN": 0.0}
    keys = ["M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"]
    vkeys = ["M5_volume_regime","M15_volume_regime","M30_volume_regime","H1_volume_regime","H4_volume_regime","D1_volume_regime"]
    row = {k: 0.0 for k in ["mtf_trend_score", *keys, *vkeys]}
    row["volume_available"] = False
    if market:
        row["H1_trend_regime"] = trend.get(str(market.get("trend", "UNKNOWN")).upper(), 0.0)
        for k in row:
            if k in market and pd.notna(market[k]): row[k] = market[k]
    if mtf:
        row["mtf_trend_score"] = trend.get(str(mtf.get("trend", "UNKNOWN")).upper(), 0.0)
        row["H4_trend_regime"] = trend.get(str(mtf.get("h4_trend", "UNKNOWN")).upper(), 0.0)
    return row


def read_snapshot_status(root: Path, label: str) -> dict[str, Any]:
    files = [*root.rglob("*.json"), *root.rglob("*.csv")] if root.exists() else []
    return {"source": label, "files_found": len(files), "status": "CONNECTED_GOVERNED_METADATA" if files else "NOT_EVALUABLE", "direction": None, "final_trade_decision": None}


def run(a) -> None:
    bars = read(a.h1, {"timestamp","open","high","low","close"})
    bars = bars[(bars.timestamp.dt.year >= 2016) & (bars.timestamp.dt.year <= 2024)].reset_index(drop=True)
    market = read(a.market, {"timestamp"})
    mtf = read(a.mtf, {"timestamp"})
    murphy = read(a.murphy, {"timestamp","status","direction","source_rule_id"})
    nison = read(a.nison, {"timestamp","status","direction","rule_id"}, chunksize=400000)
    hc = read(a.historical_context, {"timestamp","context_signature"})
    ho = read(a.historical_outcome, {"timestamp","context_signature"})
    if "pair" in hc.columns: hc = hc[hc.pair.astype(str).str.upper().eq("GBPUSD")]
    if "pair" in ho.columns: ho = ho[ho.pair.astype(str).str.upper().eq("GBPUSD")]
    hc = hc[hc.timestamp.dt.year <= 2024].reset_index(drop=True)
    ho = ho[ho.timestamp.dt.year <= 2024].reset_index(drop=True)

    am, an = allowlist()
    actual_m, actual_n = split_ids(murphy.source_rule_id), set(nison.rule_id.astype(str))
    if not actual_m.issubset(am): raise ValueError(f"Unknown Murphy rule id(s): {sorted(actual_m-am)}")
    if not actual_n.issubset(an): raise ValueError(f"Unknown Nison rule id(s): {sorted(actual_n-an)}")

    mur = aggregate_murphy(murphy)
    nis = aggregate_nison(nison)
    base = bars[["timestamp","close"]].copy()
    p_market = asof(base, market); p_mtf = asof(base, mtf); p_mur = asof(base, mur); p_nis = asof(base, nis)
    p_hc = asof(base, hc[[c for c in hc.columns if c in {"timestamp","context_signature"}]])
    p_ho = asof(base, ho[[c for c in ho.columns if c in {"timestamp","context_signature"}]])

    brain = load_brain()
    from compatibility.knowledge_decision_handoff import build_handoff
    from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk

    sim_meta = read_snapshot_status(a.similarity, "Similarity V2")
    ret_meta = read_snapshot_status(a.retrieval, "Context-Aware Retrieval V2")
    events, trades = [], []
    for i, b in bars.iterrows():
        ts = b.timestamp
        mr = {k:v for k,v in p_market.iloc[i].to_dict().items() if k != "timestamp" and pd.notna(v)}
        xr = {k:v for k,v in p_mtf.iloc[i].to_dict().items() if k != "timestamp" and pd.notna(v)}
        mu = p_mur.iloc[i].to_dict(); ni = p_nis.iloc[i].to_dict(); hc_row = p_hc.iloc[i].to_dict(); ho_row = p_ho.iloc[i].to_dict()
        mur_dir = mu.get("murphy_direction"); ncontra = bool(ni.get("nison_contradiction", False))
        nconf = str(ni.get("nison_confirmation") or "ABSENT")
        brain_row = build_brain_row(mr, xr)

        alignment = "NISON_CONTRADICTION" if ncontra else ("ALIGNED" if mur_dir in {"BULLISH","BEARISH"} else "NEEDS_REVIEW")
        evidence = {
            "historical_context": hc_row,
            "historical_outcome": ho_row,
            "similarity": sim_meta,
            "context_aware_retrieval": ret_meta,
            "tiz": {"status": "UNRESOLVED_OPTIONAL", "direction": None, "final_trade_decision": None},
        }
        handoff = build_handoff(
            brain_row,
            {"alignment_state": alignment, "candidate_direction": str(mur_dir or "neutral").lower(),
             "contradiction_gate": "FAIL" if ncontra else "PASS", "process_gate": "NOT_EVALUABLE",
             "book_evidence_status": "CONNECTED", "market_evidence_status": "CONNECTED",
             "similarity_record_count": 0, "evidence_bundle": evidence},
            similarity=sim_meta,
        )
        assessment = brain.assess(handoff["decision_brain_row"], similarity=None)
        ready = mur_dir in {"BULLISH","BEARISH"} and assessment.directional_bias == str(mur_dir).lower() and not ncontra

        risk_status, risk_reason = "NOT_EVALUABLE", "NOT_READY"
        sl = tp = None
        atr = xr.get("atr")
        if ready and pd.notna(atr) and float(atr) > 0:
            direction = "BUY" if mur_dir == "BULLISH" else "SELL"
            entry = float(b.close); dist = 0.75 * float(atr); target = 3.0 * dist
            sl, tp = ((entry-dist, entry+target) if direction=="BUY" else (entry+dist, entry-target))
            rr = evaluate_risk(equity=100000.0, entry=entry, stop_loss=sl, take_profit=tp, atr=float(atr), prior_loss_streak=0, peak_equity=100000.0)
            risk_status, risk_reason = ("PASS" if rr.risk_pass else "FAIL"), rr.reason

        events.append({"timestamp":ts,"market_state_asof":bool(mr),"mtf_asof":bool(xr),"murphy_direction":mur_dir,"murphy_rule_count":int(mu.get("murphy_rule_count",0) or 0),"nison_confirmation":nconf,"nison_contradiction":ncontra,"nison_rule_count":int(ni.get("nison_rule_count",0) or 0),"historical_context_asof":bool(hc_row.get("context_signature")),"historical_outcome_asof":bool(ho_row.get("context_signature")),"similarity_status":sim_meta["status"],"retrieval_status":ret_meta["status"],"tiz_status":"UNRESOLVED_OPTIONAL","handoff_routing":handoff["routing"],"brain_bias":assessment.directional_bias,"brain_confidence":assessment.confidence,"direction_ready":ready,"risk_status":risk_status,"risk_reason":risk_reason,"stop_loss":sl,"take_profit":tp})
        if ready and risk_status == "PASS":
            trades.append({"timestamp":ts,"direction":direction,"entry_price":entry,"stop_loss":sl,"take_profit":tp,"risk_status":risk_status})
        if (i+1) % 5000 == 0: print(f"E2E_PROGRESS events={i+1} as_of={ts.isoformat()}")

    out = a.output_dir; out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(events).to_csv(out/"unified_78_events_2016_2024.csv", index=False)
    pd.DataFrame(events).to_csv(out/"decision_events_2016_2024.csv", index=False)
    pd.DataFrame(trades).to_csv(out/"risk_eligible_events_2016_2024.csv", index=False)
    manifest = {"status":"E2E_INTEGRATION_EXECUTED","window":"2016-2024","2025":"LOCKED","murphy_rules":len(actual_m),"nison_rules":len(actual_n),"similarity":sim_meta,"retrieval":ret_meta,"tiz":"UNRESOLVED_OPTIONAL","decision_brain_untouched":True,"memory_direction_generated":False,"retrieval_direction_generated":False}
    (out/"integration_manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))


def main():
    p=argparse.ArgumentParser()
    for n in ["h1","market","mtf","murphy","nison","historical-context","historical-outcome","similarity","retrieval","output-dir"]:
        p.add_argument(f"--{n}", type=Path, required=True)
    run(p.parse_args())


if __name__ == "__main__":
    main()
