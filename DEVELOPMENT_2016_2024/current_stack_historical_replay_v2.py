from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MURPHY_IDS = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}
NISON_IDS = {f"NISON_{i:04d}" for i in range(1,45)}
MTF_FIELDS = ["mtf_trend_score","M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"]

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="raise", format="mixed")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)

def split_ids(value: Any) -> list[str]:
    return [x.strip() for x in str(value or "").split("|") if x.strip() and x.strip().upper() not in {"NONE","NULL","NAN","NISON_NONE"}]

def asof_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates("timestamp", keep="last").set_index("timestamp").sort_index()

def asof_row(frame: pd.DataFrame, ts: pd.Timestamp) -> pd.Series | None:
    if frame.empty:
        return None
    pos = frame.index.searchsorted(ts, side="right") - 1
    return None if pos < 0 else frame.iloc[pos]

def scalar(row: pd.Series, names: tuple[str, ...]) -> float:
    for name in names:
        if name in row.index and pd.notna(row[name]) and str(row[name]).strip() != "":
            return float(row[name])
    raise ValueError(f"missing {names}")

def simulate_exit(bars: pd.DataFrame, entry_idx: int, direction: str, stop: float, target: float) -> tuple[str, float | None, pd.Timestamp | None]:
    for j in range(entry_idx + 1, len(bars)):
        b = bars.iloc[j]
        hit_sl = float(b.low) <= stop if direction == "BUY" else float(b.high) >= stop
        hit_tp = float(b.high) >= target if direction == "BUY" else float(b.low) <= target
        if hit_sl and hit_tp:
            return "AMBIGUOUS", None, b.timestamp
        if hit_tp:
            return "TP", 2.0, b.timestamp
        if hit_sl:
            return "SL", -1.0, b.timestamp
    return "TIMEOUT", None, None

def run(h1: Path, market_state: Path, murphy: Path, nison: Path, mtf: Path, output_dir: Path) -> None:
    bars, market, mdf, ndf, mtf_df = map(load_csv, [h1, market_state, murphy, nison, mtf])
    for name, df in [("H1",bars),("MarketState",market),("Murphy",mdf),("Nison",ndf),("MTF",mtf_df)]:
        df.drop(df.index[(df.timestamp.dt.year < 2016) | (df.timestamp.dt.year > 2024)], inplace=True)
        if df.empty:
            raise ValueError(f"{name}: empty 2016-2024 window")

    if "source_rule_id" not in mdf.columns:
        raise ValueError("Murphy source_rule_id missing")
    mdf["expanded_ids"] = mdf.source_rule_id.map(split_ids)
    observed_m = {rid for ids in mdf.expanded_ids for rid in ids}
    unknown_m = observed_m - MURPHY_IDS
    if not observed_m:
        raise ValueError("Murphy governed envelope has no source-backed rule IDs")
    if unknown_m:
        raise ValueError(f"Murphy governed envelope contains unknown rule IDs: {sorted(unknown_m)}")

    if "source_rule_id" not in ndf.columns:
        if "rule_id" not in ndf.columns:
            raise ValueError("Nison rule_id/source_rule_id missing")
        ndf["source_rule_id"] = ndf.rule_id
    ndf["expanded_ids"] = ndf.source_rule_id.map(split_ids)

    m_status = mdf.status.astype(str).str.upper().str.strip()
    m_dir = mdf.direction.astype(str).str.upper().str.strip()
    candidates = mdf.loc[m_status.eq("PASS") & m_dir.isin({"BUY","SELL","BULLISH","BEARISH"})].copy()
    candidates["direction_norm"] = candidates.direction.replace({"BULLISH":"BUY","BEARISH":"SELL"})

    market_i = asof_frame(market)
    mtf_i = asof_frame(mtf_df)
    bars_i = asof_frame(bars)
    nison_groups = {ts:g for ts,g in ndf.groupby("timestamp", sort=False)}
    exact_bar_pos = {ts:i for i,ts in enumerate(bars.timestamp)}

    bridge = load_module(ROOT / "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py", "current_full_brain_bridge_v2")
    frozen = load_module(ROOT / "OOS_2025/frozen_candidate_risk_profile_v1.py", "current_frozen_candidate_risk_v2")
    canonical = load_module(ROOT / "risk_engine/risk_execution_runtime_v1.py", "current_canonical_risk_v2")

    equity = 10000.0
    peak_equity = equity
    loss_streak = 0
    events: list[dict[str,Any]] = []
    trades: list[dict[str,Any]] = []

    for _, mr in candidates.iterrows():
        ts = mr.timestamp
        market_row = asof_row(market_i, ts)
        mtf_row = asof_row(mtf_i, ts)
        bar_row = asof_row(bars_i, ts)
        ng = nison_groups.get(ts)
        if market_row is None or mtf_row is None or bar_row is None or ng is None:
            continue
        if any(pd.isna(mtf_row.get(k)) for k in MTF_FIELDS):
            continue
        nids = {rid for ids in ng.expanded_ids for rid in ids}
        if nids != NISON_IDS:
            continue

        nstatus = ng.status.astype(str).str.upper().str.strip() if "status" in ng.columns else pd.Series(dtype=object)
        passed = ng.loc[nstatus.eq("PASS")]
        failed = ng.loc[nstatus.eq("FAIL")]
        ndirs = {str(x).upper().strip() for x in passed.get("direction", pd.Series(dtype=object)) if str(x).upper().strip() in {"BUY","SELL","BULLISH","BEARISH"}}
        confirmation = "ABSENT" if not ndirs else ("BULLISH" if len(ndirs)==1 and next(iter(ndirs)) in {"BUY","BULLISH"} else "BEARISH" if len(ndirs)==1 else "CONFLICTED")
        contradiction = not failed.empty

        entry = scalar(bar_row, ("entry_price","close"))
        atr = scalar(market_row, ("atr","atr20","H1_atr"))
        direction = str(mr.direction_norm)
        frozen_result = frozen.evaluate_frozen_candidate_risk(direction=direction, equity=equity, peak_equity=peak_equity, entry=entry, atr=atr, prior_loss_streak=loss_streak)
        rr_target = 1.5 * atr
        rr_request = canonical.RiskRequest(equity=equity, risk_percent=frozen_result.risk_percent, entry_price=entry, stop_distance=0.75*atr, take_profit_distance=rr_target, stop_mode="structure", risk_budget_locked=True)
        cr = canonical.evaluate_risk(rr_request, direction, atr)
        risk = {"authoritative":True,"risk_pass":bool(frozen_result.risk_pass and cr.risk_pass),"equity":equity,"peak_equity":peak_equity,"prior_loss_streak":loss_streak,"entry_price":entry,"atr":atr,"risk_percent":float(frozen_result.risk_percent),"stop_loss":float(cr.stop_loss),"take_profit":float(cr.take_profit),"position_size":float(cr.position_size),"rr":2.0,"risk_budget_locked":True}

        brain_row = {**market_row.to_dict(), **mtf_row.to_dict(), "entry_price":entry, "atr":atr}
        brain_result = bridge.run_full_brain_cycle(
            row=brain_row,
            query_as_of=ts.isoformat(),
            murphy_evidence={"status":"PASS","rows":[mr.drop(labels=["expanded_ids","direction_norm"]).to_dict()],"authoritative":True},
            nison_evidence={"status":"PASS","rows":ng.drop(columns=["expanded_ids"], errors="ignore").to_dict("records"),"authoritative":True,"confirmation":confirmation,"contradiction":contradiction},
            risk_evidence=risk,
            tiz_evidence={"status":"NOT_EVALUABLE","authoritative":False,"source":"TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2"},
            historical_evidence=None,
            source_rule_ids=sorted(set(mr.expanded_ids).union(nids)),
            entry_price=entry,
            atr=atr,
            mode="development",
        )
        decision = (brain_result.get("decision") or {}).get("decision") or {}
        final = decision.get("final")
        event={"timestamp":ts.isoformat(),"murphy_direction":direction,"murphy_rule_count":len(set(mr.expanded_ids)),"nison_rule_count":len(nids),"nison_confirmation":confirmation,"nison_contradiction":contradiction,"risk_pass":risk["risk_pass"],"brain_status":brain_result.get("status"),"brain_final":final,"equity_before":equity,"loss_streak_before":loss_streak,"entry_price":entry,"atr":atr,"stop_loss":risk["stop_loss"],"take_profit":risk["take_profit"],"source_rule_ids":sorted(set(mr.expanded_ids).union(nids)),"future_data_used":False}

        if brain_result.get("status")=="EXECUTABLE" and final in {"BUY","SELL"} and risk["risk_pass"] and not contradiction and ts in exact_bar_pos:
            outcome,r_mult,exit_ts=simulate_exit(bars,exact_bar_pos[ts],final,risk["stop_loss"],risk["take_profit"])
            trade={**event,"trade":True,"direction":final,"outcome":outcome,"r_multiple":r_mult,"exit_timestamp":exit_ts.isoformat() if exit_ts is not None else None}
            trades.append(trade)
            if r_mult is not None:
                equity += float(r_mult)*(equity*frozen_result.risk_percent)
                peak_equity=max(peak_equity,equity)
                loss_streak=loss_streak+1 if r_mult<0 else 0
        event.update({"equity_after":equity,"peak_equity_after":peak_equity,"loss_streak_after":loss_streak})
        events.append(event)

    out=output_dir; out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(events).to_csv(out/"current_stack_decision_events_2016_2024.csv",index=False)
    pd.DataFrame(trades).to_csv(out/"current_stack_executed_trades_2016_2024.csv",index=False)
    closed=pd.DataFrame(trades); closed=closed[closed.r_multiple.notna()] if not closed.empty and "r_multiple" in closed else closed
    metrics={"status":"CURRENT_STACK_DEVELOPMENT_RESULT","window":"2016-2024","candidate_events":int(len(candidates)),"evaluated_events":int(len(events)),"executed_trades":int(len(closed)),"costs_applied":False,"tuning_applied":False,"official_profitability_claim":False,"murphy_registry_rules":len(MURPHY_IDS),"murphy_source_backed_rules_observed":len(observed_m)}
    if not closed.empty:
        wins=int((closed.r_multiple>0).sum()); losses=int((closed.r_multiple<0).sum()); gw=float(closed.loc[closed.r_multiple>0,"r_multiple"].sum()); gl=float(-closed.loc[closed.r_multiple<0,"r_multiple"].sum()); eq=closed.r_multiple.cumsum(); metrics.update({"wins":wins,"losses":losses,"win_rate":wins/len(closed),"profit_factor":gw/gl if gl else None,"expectancy_R":float(closed.r_multiple.mean()),"total_R":float(closed.r_multiple.sum()),"max_drawdown_R":float((eq-eq.cummax()).min())})
    validation={"window_2016_2024_only":True,"future_data_used":False,"murphy_governed_rules":34,"murphy_source_backed_rules_observed":len(observed_m),"nison_governed_rules":44,"nison_generates_direction":False,"tiz_generates_direction":False,"memory_generates_direction":False,"risk_authoritative":True,"brain_semantics_changed":False,"official_profitability_claim_allowed":False}
    (out/"current_stack_backtest_metrics_2016_2024.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    (out/"current_stack_validation_manifest_2016_2024.json").write_text(json.dumps(validation,indent=2),encoding="utf-8")
    print(json.dumps({"metrics":metrics,"validation":validation},indent=2))

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--h1",required=True,type=Path); p.add_argument("--market-state",required=True,type=Path); p.add_argument("--murphy",required=True,type=Path); p.add_argument("--nison",required=True,type=Path); p.add_argument("--mtf",required=True,type=Path); p.add_argument("--output-dir",required=True,type=Path); a=p.parse_args(); run(a.h1,a.market_state,a.murphy,a.nison,a.mtf,a.output_dir)
