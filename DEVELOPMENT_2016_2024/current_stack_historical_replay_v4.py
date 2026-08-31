from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

from current_stack_historical_memory_provider_v1 import HistoricalMemoryProvider

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


def hit_exit(bar: pd.Series, direction: str, stop: float, target: float) -> tuple[str, float | None]:
    if direction == "BUY":
        hit_sl = float(bar.low) <= stop
        hit_tp = float(bar.high) >= target
    else:
        hit_sl = float(bar.high) >= stop
        hit_tp = float(bar.low) <= target
    if hit_sl and hit_tp:
        return "AMBIGUOUS", None
    if hit_tp:
        return "TP", 2.0
    if hit_sl:
        return "SL", -1.0
    return "OPEN", None


def run(
    h1: Path,
    market_state: Path,
    murphy: Path,
    nison: Path,
    mtf: Path,
    historical_context: Path,
    historical_outcome: Path,
    similarity_artifact: Path,
    retrieval_artifact: Path,
    scenario_artifact: Path,
    output_dir: Path,
) -> None:
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
    if unknown_m:
        raise ValueError(f"Murphy governed envelope contains unknown rule IDs: {sorted(unknown_m)}")

    if "source_rule_id" not in ndf.columns:
        ndf["source_rule_id"] = ndf.rule_id
    ndf["expanded_ids"] = ndf.source_rule_id.map(split_ids)

    m_status = mdf.status.astype(str).str.upper().str.strip()
    m_dir = mdf.direction.astype(str).str.upper().str.strip()
    candidates = mdf.loc[m_status.eq("PASS") & m_dir.isin({"BUY","SELL","BULLISH","BEARISH"})].copy()
    candidates["direction_norm"] = candidates.direction.replace({"BULLISH":"BUY","BEARISH":"SELL"})
    candidates_by_ts = {ts:g for ts,g in candidates.groupby("timestamp", sort=False)}
    nison_groups = {ts:g for ts,g in ndf.groupby("timestamp", sort=False)}

    market_i = asof_frame(market)
    mtf_i = asof_frame(mtf_df)

    bridge = load_module(ROOT / "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py", "current_full_brain_bridge_v4")
    frozen = load_module(ROOT / "OOS_2025/frozen_candidate_risk_profile_v1.py", "current_frozen_risk_v4")
    canonical = load_module(ROOT / "risk_engine/risk_execution_runtime_v1.py", "current_canonical_risk_v4")
    provider = HistoricalMemoryProvider(
        context_path=historical_context,
        outcome_path=historical_outcome,
        similarity_artifact=similarity_artifact,
        retrieval_artifact=retrieval_artifact,
        scenario_artifact=scenario_artifact,
    )

    equity = 10000.0
    peak_equity = equity
    loss_streak = 0
    open_positions: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    max_concurrent_positions = 0

    for bar_idx, bar in bars.iterrows():
        ts = bar.timestamp

        # 1) Realize exits BEFORE evaluating new entries at this timestamp.
        still_open: list[dict[str, Any]] = []
        for pos in open_positions:
            outcome, r_mult = hit_exit(bar, pos["direction"], pos["stop_loss"], pos["take_profit"])
            if outcome == "OPEN":
                still_open.append(pos)
                continue
            trade = dict(pos)
            trade["outcome"] = outcome
            trade["r_multiple"] = r_mult
            trade["exit_timestamp"] = ts.isoformat()
            trade["exit_bar_index"] = int(bar_idx)
            if r_mult is not None:
                equity += float(r_mult) * (equity * float(pos["risk_percent"]))
                peak_equity = max(peak_equity, equity)
                loss_streak = loss_streak + 1 if r_mult < 0 else 0
            trades.append(trade)
        open_positions = still_open

        # 2) Generate/score new decisions only from evidence available at this timestamp.
        groups = candidates_by_ts.get(ts)
        if groups is None:
            continue
        market_row = asof_row(market_i, ts)
        mtf_row = asof_row(mtf_i, ts)
        ng = nison_groups.get(ts)
        if market_row is None or mtf_row is None or ng is None or any(pd.isna(mtf_row.get(k)) for k in MTF_FIELDS):
            continue
        nids = {rid for ids in ng.expanded_ids for rid in ids}
        if nids != NISON_IDS:
            continue
        nstatus = ng.status.astype(str).str.upper().str.strip() if "status" in ng.columns else pd.Series(dtype=object)
        passed = ng.loc[nstatus.eq("PASS")]
        ndirs = {str(x).upper().strip() for x in passed.get("direction", pd.Series(dtype=object)) if str(x).upper().strip() in {"BUY","SELL","BULLISH","BEARISH"}}
        normalized_ndirs = {"BUY" if d in {"BUY","BULLISH"} else "SELL" for d in ndirs}

        for _, mr in groups.iterrows():
            murphy_direction = str(mr.direction_norm).upper().strip()
            aligned = normalized_ndirs & {murphy_direction}
            opposite = normalized_ndirs & ({"SELL"} if murphy_direction == "BUY" else {"BUY"})
            if opposite and aligned:
                confirmation = "WEAK"
            elif aligned:
                confirmation = "CONFIRMED"
            else:
                confirmation = "ABSENT"
            contradiction = bool(opposite)

            entry = float(bar.close)
            atr = scalar(market_row, ("atr","atr20","H1_atr"))
            frozen_result = frozen.evaluate_frozen_candidate_risk(
                direction=murphy_direction,
                equity=equity,
                peak_equity=peak_equity,
                entry=entry,
                atr=atr,
                prior_loss_streak=loss_streak,
            )
            rr_target = 1.5 * atr
            rr_request = canonical.RiskRequest(
                equity=equity,
                risk_percent=frozen_result.risk_percent,
                entry_price=entry,
                stop_distance=0.75 * atr,
                take_profit_distance=rr_target,
                stop_mode="structure",
                risk_budget_locked=True,
            )
            cr = canonical.evaluate_risk(rr_request, murphy_direction, atr)
            risk = {
                "authoritative": True,
                "risk_pass": bool(frozen_result.risk_pass and cr.risk_pass),
                "equity": equity,
                "peak_equity": peak_equity,
                "prior_loss_streak": loss_streak,
                "entry_price": entry,
                "atr": atr,
                "risk_percent": float(frozen_result.risk_percent),
                "stop_loss": float(cr.stop_loss),
                "take_profit": float(cr.take_profit),
                "position_size": float(cr.position_size),
                "rr": 2.0,
                "risk_budget_locked": True,
            }
            brain_row = {**market_row.to_dict(), **mtf_row.to_dict(), "entry_price": entry, "atr": atr}
            memory = provider.evidence(ts.isoformat(), brain_row)
            brain_result = bridge.run_full_brain_cycle(
                row=brain_row,
                query_as_of=ts.isoformat(),
                murphy_evidence={"status":"PASS","rows":[mr.drop(labels=["expanded_ids","direction_norm"]).to_dict()],"authoritative":True},
                nison_evidence={"status":"PASS","rows":ng.drop(columns=["expanded_ids"], errors="ignore").to_dict("records"),"authoritative":True,"confirmation":confirmation,"contradiction":contradiction},
                risk_evidence=risk,
                tiz_evidence={"status":"NOT_EVALUABLE","authoritative":False,"source":"TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2"},
                historical_evidence={"status": memory["status"], "memory_role": memory["memory_role"], "sources": memory["sources"], "governance": memory["governance"], "query_as_of": memory["query_as_of"]},
                source_rule_ids=sorted(set(mr.expanded_ids).union(nids)),
                entry_price=entry,
                atr=atr,
                mode="development",
            )
            decision = (brain_result.get("decision") or {}).get("decision") or {}
            final = decision.get("final")
            should_open = brain_result.get("status") == "EXECUTABLE" and final in {"BUY","SELL"} and risk["risk_pass"] and not contradiction

            event = {
                "timestamp": ts.isoformat(),
                "murphy_direction": murphy_direction,
                "murphy_rule_count": len(set(mr.expanded_ids)),
                "nison_rule_count": len(nids),
                "nison_confirmation": confirmation,
                "nison_contradiction": contradiction,
                "nison_pass_direction_count": len(normalized_ndirs),
                "nison_fail_count": int(nstatus.eq("FAIL").sum()),
                "nison_not_evaluable_count": int(nstatus.eq("NOT_EVALUABLE").sum()),
                "risk_pass": risk["risk_pass"],
                "brain_status": brain_result.get("status"),
                "brain_final": final,
                "equity_before": equity,
                "loss_streak_before": loss_streak,
                "equity_after": equity,
                "peak_equity_after": peak_equity,
                "loss_streak_after": loss_streak,
                "open_positions_before": len(open_positions),
                "memory_status": memory["status"],
                "memory_full_stack_wired": True,
                "historical_context_wired": True,
                "historical_outcome_wired": True,
                "similarity_evidence_only": True,
                "retrieval_evidence_only": True,
                "scenario_evidence_only": True,
                "entry_price": entry,
                "atr": atr,
                "stop_loss": risk["stop_loss"],
                "take_profit": risk["take_profit"],
                "source_rule_ids": sorted(set(mr.expanded_ids).union(nids)),
                "future_data_used": False,
            }

            if should_open:
                position = {
                    **event,
                    "trade": True,
                    "direction": final,
                    "entry_timestamp": ts.isoformat(),
                    "entry_bar_index": int(bar_idx),
                    "stop_loss": risk["stop_loss"],
                    "take_profit": risk["take_profit"],
                    "risk_percent": risk["risk_percent"],
                    "equity_at_entry": equity,
                    "loss_streak_at_entry": loss_streak,
                }
                open_positions.append(position)
                max_concurrent_positions = max(max_concurrent_positions, len(open_positions))
                event["trade_opened"] = True
            else:
                event["trade_opened"] = False
            event["open_positions_after"] = len(open_positions)
            events.append(event)

    # 3) End-of-window audit. Unclosed positions are not counted as realized P&L.
    closed = pd.DataFrame(trades)
    if not closed.empty:
        closed_realized = closed[closed["r_multiple"].notna()].copy()
    else:
        closed_realized = closed

    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(events).to_csv(output_dir / "current_stack_decision_events_2016_2024.csv", index=False)
    pd.DataFrame(trades).to_csv(output_dir / "current_stack_executed_trades_2016_2024.csv", index=False)
    metrics: dict[str, Any] = {
        "status": "CURRENT_STACK_DEVELOPMENT_RESULT",
        "window": "2016-2024",
        "candidate_events": int(len(candidates)),
        "evaluated_events": int(len(events)),
        "executed_trades": int(len(closed_realized)),
        "open_positions_at_window_end": int(len(open_positions)),
        "max_concurrent_positions": int(max_concurrent_positions),
        "costs_applied": False,
        "tuning_applied": False,
        "official_profitability_claim": False,
        "murphy_registry_rules": len(MURPHY_IDS),
        "murphy_source_backed_rules_observed": len(observed_m),
        "realized_pnl_update_policy": "EXIT_ONLY",
        "risk_state_update_policy": "REALIZED_EQUITY_ONLY",
    }
    if not closed_realized.empty:
        wins = int((closed_realized.r_multiple > 0).sum())
        losses = int((closed_realized.r_multiple < 0).sum())
        gross_win = float(closed_realized.loc[closed_realized.r_multiple > 0, "r_multiple"].sum())
        gross_loss = float(-closed_realized.loc[closed_realized.r_multiple < 0, "r_multiple"].sum())
        eq_r = closed_realized.r_multiple.cumsum()
        metrics.update({
            "wins": wins,
            "losses": losses,
            "win_rate": wins / len(closed_realized),
            "profit_factor": gross_win / gross_loss if gross_loss else None,
            "expectancy_R": float(closed_realized.r_multiple.mean()),
            "total_R": float(closed_realized.r_multiple.sum()),
            "max_drawdown_R": float((eq_r - eq_r.cummax()).min()),
        })

    yearly = {}
    if not closed_realized.empty:
        tmp = closed_realized.copy()
        tmp["year"] = pd.to_datetime(tmp["exit_timestamp"], utc=True).dt.year
        for year, g in tmp.groupby("year"):
            yearly[str(int(year))] = {
                "trades": int(len(g)),
                "wins": int((g.r_multiple > 0).sum()),
                "losses": int((g.r_multiple < 0).sum()),
                "total_R": float(g.r_multiple.sum()),
            }
    metrics["yearly_realized_results"] = yearly

    validation = {
        "window_2016_2024_only": True,
        "future_data_used": False,
        "murphy_governed_rules": 34,
        "murphy_source_backed_rules_observed": len(observed_m),
        "nison_governed_rules": 44,
        "nison_generates_direction": False,
        "tiz_generates_direction": False,
        "memory_generates_direction": False,
        "risk_authoritative": True,
        "brain_semantics_changed": False,
        "official_profitability_claim_allowed": False,
        "nison_fail_is_not_contradiction": True,
        "nison_contradiction_requires_opposite_directional_pass": True,
        "trade_lifecycle_event_driven": True,
        "pnl_recorded_only_on_exit": True,
        "risk_state_updates_only_on_realized_pnl": True,
        "unclosed_positions_excluded_from_realized_profitability": True,
    }
    (output_dir / "current_stack_backtest_metrics_2016_2024.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "current_stack_validation_manifest_2016_2024.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps({"metrics": metrics, "validation": validation}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--mtf", required=True, type=Path)
    p.add_argument("--historical-context", required=True, type=Path)
    p.add_argument("--historical-outcome", required=True, type=Path)
    p.add_argument("--similarity-artifact", required=True, type=Path)
    p.add_argument("--retrieval-artifact", required=True, type=Path)
    p.add_argument("--scenario-artifact", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    run(a.h1, a.market_state, a.murphy, a.nison, a.mtf, a.historical_context, a.historical_outcome, a.similarity_artifact, a.retrieval_artifact, a.scenario_artifact, a.output_dir)
