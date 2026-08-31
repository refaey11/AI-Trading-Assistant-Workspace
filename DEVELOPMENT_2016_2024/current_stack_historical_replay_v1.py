from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MURPHY_IDS = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}
NISON_IDS = {f"NISON_{i:04d}" for i in range(1, 45)}
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


def scalar(row: pd.Series, names: tuple[str, ...]) -> float:
    for n in names:
        if n in row.index and pd.notna(row[n]) and str(row[n]).strip() != "":
            return float(row[n])
    raise ValueError(f"missing scalar; tried {names}")


def prepare_asof(df: pd.DataFrame, key_cols: list[str] | None = None) -> pd.DataFrame:
    cols = ["timestamp"] + (key_cols or [])
    cols = [c for c in cols if c in df.columns]
    out = df[cols].drop_duplicates("timestamp", keep="last").sort_values("timestamp")
    out = out.set_index("timestamp")
    return out


def get_asof(indexed: pd.DataFrame, ts: pd.Timestamp) -> pd.Series | None:
    if indexed.empty:
        return None
    pos = indexed.index.searchsorted(ts, side="right") - 1
    if pos < 0:
        return None
    return indexed.iloc[pos]


def simulate_exit(bars: pd.DataFrame, entry_idx: int, direction: str, entry: float, stop: float, target: float) -> tuple[str, float | None, pd.Timestamp | None]:
    for j in range(entry_idx + 1, len(bars)):
        b = bars.iloc[j]
        sl_hit = float(b["low"]) <= stop if direction == "BUY" else float(b["high"]) >= stop
        tp_hit = float(b["high"]) >= target if direction == "BUY" else float(b["low"]) <= target
        if sl_hit and tp_hit:
            return "AMBIGUOUS", None, b["timestamp"]
        if tp_hit:
            return "TP", 2.0, b["timestamp"]
        if sl_hit:
            return "SL", -1.0, b["timestamp"]
    return "TIMEOUT", None, None


def run(*, h1_path: Path, market_path: Path, murphy_path: Path, nison_path: Path, mtf_path: Path, output_dir: Path) -> dict[str, Any]:
    bars = load_csv(h1_path)
    market = load_csv(market_path)
    murphy = load_csv(murphy_path)
    nison = load_csv(nison_path)
    mtf = load_csv(mtf_path)

    bars = bars[(bars.timestamp.dt.year >= 2016) & (bars.timestamp.dt.year <= 2024)].copy()
    market = market[(market.timestamp.dt.year >= 2016) & (market.timestamp.dt.year <= 2024)].copy()
    murphy = murphy[(murphy.timestamp.dt.year >= 2016) & (murphy.timestamp.dt.year <= 2024)].copy()
    nison = nison[(nison.timestamp.dt.year >= 2016) & (nison.timestamp.dt.year <= 2024)].copy()
    mtf = mtf[(mtf.timestamp.dt.year >= 2016) & (mtf.timestamp.dt.year <= 2024)].copy()

    mdf = murphy.copy()
    if "source_rule_id" not in mdf.columns:
        raise ValueError("Murphy source_rule_id missing")
    mdf["expanded_ids"] = mdf["source_rule_id"].map(split_ids)
    observed = set(rid for ids in mdf.expanded_ids for rid in ids)
    if observed - MURPHY_IDS:
        raise ValueError(f"unknown Murphy IDs: {sorted(observed - MURPHY_IDS)}")

    ndf = nison.copy()
    if "source_rule_id" not in ndf.columns:
        if "rule_id" in ndf.columns:
            ndf["source_rule_id"] = ndf["rule_id"]
        else:
            raise ValueError("Nison rule_id/source_rule_id missing")
    ndf["expanded_ids"] = ndf["source_rule_id"].map(split_ids)

    # Event candidates are source-backed Murphy directional PASS events inside the development window.
    status = mdf.get("status", "").astype(str).str.upper().str.strip()
    direction = mdf.get("direction", "").astype(str).str.upper().str.strip()
    candidates = mdf.loc[status.eq("PASS") & direction.isin({"BUY","SELL","BULLISH","BEARISH"})].copy()
    candidates["direction_norm"] = candidates["direction"].replace({"BULLISH":"BUY","BEARISH":"SELL"})

    market_i = prepare_asof(market)
    mtf_i = prepare_asof(mtf, MTF_FIELDS)
    bars_i = prepare_asof(bars)
    nison_groups = {ts: g.copy() for ts, g in ndf.groupby("timestamp", sort=False)}

    bridge = load_module(ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "full_brain_runtime_bridge_v1.py", "current_full_brain_bridge")
    frozen = load_module(ROOT / "OOS_2025" / "frozen_candidate_risk_profile_v1.py", "frozen_candidate_risk")
    canonical = load_module(ROOT / "risk_engine" / "risk_execution_runtime_v1.py", "canonical_risk")

    events: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    equity = 10000.0
    peak_equity = equity
    loss_streak = 0

    for _, mr in candidates.iterrows():
        ts = mr.timestamp
        market_row = get_asof(market_i, ts)
        mtf_row = get_asof(mtf_i, ts)
        bar_row = get_asof(bars_i, ts)
        if market_row is None or mtf_row is None or bar_row is None:
            continue
        if any(pd.isna(mtf_row.get(k)) for k in MTF_FIELDS):
            continue
        ng = nison_groups.get(ts)
        if ng is None:
            continue
        nids = set(rid for ids in ng.expanded_ids for rid in ids)
        if nids != NISON_IDS:
            continue

        nstatus = ng.get("status", "").astype(str).str.upper().str.strip()
        passed = ng.loc[nstatus.eq("PASS")]
        failed = ng.loc[nstatus.eq("FAIL")]
        ndirs = set(str(x).upper().strip() for x in passed.get("direction", pd.Series(dtype=object)) if str(x).upper().strip() in {"BUY","SELL","BULLISH","BEARISH"})
        confirmation = "ABSENT"
        if len(ndirs) == 1:
            confirmation = "BULLISH" if next(iter(ndirs)) in {"BUY","BULLISH"} else "BEARISH"
        elif len(ndirs) > 1:
            confirmation = "CONFLICTED"
        contradiction = not failed.empty

        entry = scalar(bar_row, ("entry_price", "close"))
        atr = scalar(market_row, ("atr", "atr20", "H1_atr"))
        direction_norm = str(mr.direction_norm)

        frozen_result = frozen.evaluate_frozen_candidate_risk(
            direction=direction_norm,
            equity=equity,
            peak_equity=peak_equity,
            entry=entry,
            atr=atr,
            prior_loss_streak=loss_streak,
        )
        risk_request = canonical.RiskRequest(
            equity=equity,
            risk_percent=frozen_result.risk_percent,
            entry_price=entry,
            stop_distance=0.75 * atr,
            take_profit_distance=1.5 * atr,
            stop_mode="structure",
            risk_budget_locked=True,
        )
        canonical_result = canonical.evaluate_risk(risk_request, direction_norm, atr)
        risk = {
            "authoritative": True,
            "risk_pass": bool(frozen_result.risk_pass and canonical_result.risk_pass),
            "equity": equity,
            "peak_equity": peak_equity,
            "prior_loss_streak": loss_streak,
            "entry_price": entry,
            "atr": atr,
            "risk_percent": float(frozen_result.risk_percent),
            "stop_loss": float(canonical_result.stop_loss),
            "take_profit": float(canonical_result.take_profit),
            "position_size": float(canonical_result.position_size),
            "rr": 2.0,
            "risk_budget_locked": True,
        }
        brain_row = {**market_row.to_dict(), **mtf_row.to_dict()}
        if "entry_price" not in brain_row:
            brain_row["entry_price"] = entry
        if "atr" not in brain_row:
            brain_row["atr"] = atr
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

        status_out = brain_result.get("status")
        final = ((brain_result.get("decision") or {}).get("decision") or {}).get("final")
        event = {
            "timestamp": ts.isoformat(),
            "murphy_direction": direction_norm,
            "murphy_rule_count": len(set(mr.expanded_ids)),
            "nison_rule_count": len(nids),
            "nison_confirmation": confirmation,
            "nison_contradiction": contradiction,
            "risk_pass": risk["risk_pass"],
            "brain_status": status_out,
            "brain_final": final,
            "equity_before": equity,
            "loss_streak_before": loss_streak,
            "entry_price": entry,
            "atr": atr,
            "stop_loss": risk["stop_loss"],
            "take_profit": risk["take_profit"],
            "source_rule_ids": sorted(set(mr.expanded_ids).union(nids)),
            "future_data_used": False,
        }

        if status_out == "EXECUTABLE" and final in {"BUY","SELL"} and risk["risk_pass"] and not contradiction:
            pos = bars.index[bars.timestamp.eq(ts)]
            if len(pos) == 0:
                continue
            outcome, r_mult, exit_ts = simulate_exit(bars, int(pos[0]), final, entry, risk["stop_loss"], risk["take_profit"])
            trade = {**event, "trade": True, "direction": final, "outcome": outcome, "r_multiple": r_mult, "exit_timestamp": exit_ts.isoformat() if exit_ts is not None else None}
            trades.append(trade)
            if r_mult is not None:
                risk_money = equity * risk["risk_percent"]
                equity += float(r_mult) * risk_money
                peak_equity = max(peak_equity, equity)
                loss_streak = loss_streak + 1 if r_mult < 0 else 0
                trade["equity_after"] = equity
                trade["peak_equity_after"] = peak_equity
                trade["loss_streak_after"] = loss_streak
        event["equity_after"] = equity
        event["peak_equity_after"] = peak_equity
        event["loss_streak_after"] = loss_streak
        events.append(event)

    ev = pd.DataFrame(events)
    tr = pd.DataFrame(trades)
    output_dir.mkdir(parents=True, exist_ok=True)
    ev.to_csv(output_dir / "current_stack_decision_events_2016_2024.csv", index=False)
    tr.to_csv(output_dir / "current_stack_executed_trades_2016_2024.csv", index=False)

    if not tr.empty and "r_multiple" in tr.columns:
        closed = tr[tr.r_multiple.notna()].copy()
        wins = int((closed.r_multiple > 0).sum())
        losses = int((closed.r_multiple < 0).sum())
        gross_win = float(closed.loc[closed.r_multiple > 0, "r_multiple"].sum())
        gross_loss = float(-closed.loc[closed.r_multiple < 0, "r_multiple"].sum())
        eq = closed.r_multiple.cumsum()
        metrics = {
            "status": "CURRENT_STACK_DEVELOPMENT_RESULT",
            "window": "2016-2024",
            "candidate_events": int(len(candidates)),
            "evaluated_events": int(len(ev)),
            "executed_trades": int(len(closed)),
            "wins": wins,
            "losses": losses,
            "win_rate": float(wins / len(closed)) if len(closed) else None,
            "profit_factor": (gross_win / gross_loss) if gross_loss else None,
            "expectancy_R": float(closed.r_multiple.mean()) if len(closed) else None,
            "total_R": float(closed.r_multiple.sum()) if len(closed) else 0.0,
            "max_drawdown_R": float((eq - eq.cummax()).min()) if len(eq) else 0.0,
            "costs_applied": False,
            "tuning_applied": False,
            "official_profitability_claim": False,
        }
    else:
        metrics = {"status":"CURRENT_STACK_DEVELOPMENT_RESULT","window":"2016-2024","candidate_events":int(len(candidates)),"evaluated_events":int(len(ev)),"executed_trades":0,"official_profitability_claim":False}

    validation = {
        "window_2016_2024_only": True,
        "future_data_used": False,
        "murphy_governed_rules": 34,
        "nison_governed_rules": 44,
        "nison_generates_direction": False,
        "tiz_generates_direction": False,
        "memory_generates_direction": False,
        "risk_authoritative": True,
        "decision_runtime": "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py",
        "brain_semantics_changed": False,
        "cost_slippage_frozen": False,
        "official_profitability_claim_allowed": False,
    }
    (output_dir / "current_stack_backtest_metrics_2016_2024.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "current_stack_validation_manifest_2016_2024.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps({"metrics":metrics,"validation":validation}, indent=2))
    return {"metrics":metrics,"validation":validation}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--mtf", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    run(h1_path=a.h1, market_path=a.market_state, murphy_path=a.murphy, nison_path=a.nison, mtf_path=a.mtf, output_dir=a.output_dir)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
