from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from frozen_candidate_risk_profile_v1 import evaluate_frozen_candidate_risk
from nison_2025_evidence_aggregate_v1 import aggregate_nison_evidence


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def download_dropbox(token: str, path: str, out: Path) -> Path:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": path}),
        },
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=180) as response, out.open("wb") as fh:
        fh.write(response.read())
    return out


def read_csv(path: Path, required: set[str] | None = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    if required:
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{path}: missing columns {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def build_nison_candidate(nison_csv: Path, out_csv: Path) -> None:
    raw = read_csv(nison_csv, {"timestamp", "rule_id", "status", "direction"})
    raw = raw[raw["timestamp"].dt.year.eq(2025)].copy()
    agg = aggregate_nison_evidence(raw)
    src_rows = []
    for ts, group in raw.groupby("timestamp", sort=True):
        passes = [
            str(x)
            for x in group.loc[
                group["status"].eq("PASS")
                & group["direction"].astype(str).isin({"BULLISH", "BEARISH"}),
                "rule_id",
            ]
        ]
        fails = [
            str(x)
            for x in group.loc[
                group["status"].eq("FAIL")
                & group["direction"].astype(str).isin({"BULLISH", "BEARISH"}),
                "rule_id",
            ]
        ]
        src_rows.append(
            {
                "timestamp": ts,
                "source_rule_id": passes[0] if passes else (fails[0] if fails else "NISON_NONE"),
            }
        )
    src = pd.DataFrame(src_rows)
    agg["timestamp"] = pd.to_datetime(agg["timestamp"], utc=True)
    agg = agg.merge(src, on="timestamp", how="left", validate="one_to_one")
    agg[["timestamp", "confirmation", "contradiction", "source_rule_id"]].to_csv(out_csv, index=False)


def choose_exit(h1: pd.DataFrame, start_index: int, direction: str, sl: float, tp: float) -> tuple[str, int, bool]:
    """Return outcome, exit index, and same-bar ambiguity flag.

    Core outcome excludes ambiguous bars. Worst uses SL, best uses TP.
    """
    for j in range(start_index + 1, len(h1)):
        row = h1.iloc[j]
        high = float(row["high"])
        low = float(row["low"])
        if direction == "BUY":
            stop_hit = low <= sl
            tp_hit = high >= tp
        else:
            stop_hit = high >= sl
            tp_hit = low <= tp
        if stop_hit and tp_hit:
            return "AMBIGUOUS", j, True
        if stop_hit:
            return "LOSS", j, False
        if tp_hit:
            return "WIN", j, False
    return "OPEN", len(h1) - 1, False


def backtest(events_csv: Path, h1_csv: Path, out_dir: Path) -> dict:
    events = read_csv(events_csv)
    h1 = read_csv(h1_csv, {"timestamp", "open", "high", "low", "close"})
    h1 = h1[h1["timestamp"].dt.year.eq(2025)].reset_index(drop=True)
    ts_to_idx = {ts: i for i, ts in enumerate(h1["timestamp"])}

    equity = 10_000.0
    peak = equity
    loss_streak = 0
    last_exit_idx = -1
    records: list[dict] = []

    eligible = events[
        events["status"].astype(str).eq("EXECUTABLE")
        & events["direction"].astype(str).isin({"BUY", "SELL"})
        & (~events["nison_contradiction"].fillna(False).astype(bool))
    ].copy()

    for row in eligible.to_dict("records"):
        ts = pd.Timestamp(row["timestamp"])
        idx = ts_to_idx.get(ts)
        if idx is None or idx <= last_exit_idx:
            continue
        direction = str(row["direction"])
        entry = float(row["entry_price"])
        atr = float(row["atr"] if "atr" in row and pd.notna(row["atr"]) else 0)
        if atr <= 0:
            continue

        risk = evaluate_frozen_candidate_risk(
            direction=direction,
            equity=equity,
            peak_equity=peak,
            entry=entry,
            atr=atr,
            prior_loss_streak=loss_streak,
        )
        if not risk.risk_pass:
            records.append({
                "timestamp": ts,
                "direction": direction,
                "status": "RISK_BLOCKED",
                "reason": risk.reason,
            })
            continue

        outcome, exit_idx, ambiguous = choose_exit(
            h1, idx, direction, float(risk.stop_loss), float(risk.take_profit)
        )
        if outcome == "OPEN":
            records.append({
                "timestamp": ts,
                "direction": direction,
                "status": "OPEN_NO_EXIT_WITHIN_2025",
                "entry_price": entry,
                "atr": atr,
                "stop_loss": risk.stop_loss,
                "take_profit": risk.take_profit,
            })
            last_exit_idx = exit_idx
            continue

        r_core = None if ambiguous else (2.0 if outcome == "WIN" else -1.0)
        r_worst = -1.0 if ambiguous else r_core
        r_best = 2.0 if ambiguous else r_core
        risk_money = equity * risk.risk_percent
        pnl_core = None if r_core is None else risk_money * r_core
        pnl_worst = risk_money * r_worst
        pnl_best = risk_money * r_best

        records.append({
            "timestamp": ts,
            "direction": direction,
            "status": outcome,
            "ambiguous": ambiguous,
            "entry_price": entry,
            "atr": atr,
            "stop_loss": risk.stop_loss,
            "take_profit": risk.take_profit,
            "risk_percent": risk.risk_percent,
            "risk_money": risk_money,
            "r_core": r_core,
            "r_worst": r_worst,
            "r_best": r_best,
            "pnl_core": pnl_core,
            "pnl_worst": pnl_worst,
            "pnl_best": pnl_best,
            "exit_timestamp": h1.iloc[exit_idx]["timestamp"],
        })

        # The account path is driven by the core policy. Ambiguous trades are
        # excluded from core equity and therefore do not alter the core state.
        if r_core is not None:
            equity += pnl_core
            peak = max(peak, equity)
            loss_streak = loss_streak + 1 if r_core < 0 else 0
        last_exit_idx = exit_idx

    trades = pd.DataFrame(records)
    out_dir.mkdir(parents=True, exist_ok=True)
    trades.to_csv(out_dir / "FINAL_2025_TRADES.csv", index=False)

    closed = trades[trades["status"].isin(["WIN", "LOSS", "AMBIGUOUS"])].copy() if not trades.empty else trades
    core = closed[closed["r_core"].notna()].copy() if not closed.empty else closed

    def summary(r_col: str, pnl_col: str) -> dict:
        vals = core[r_col].tolist() if not core.empty else []
        wins = sum(1 for x in vals if x > 0)
        losses = sum(1 for x in vals if x < 0)
        gross_win = sum(x for x in vals if x > 0)
        gross_loss = -sum(x for x in vals if x < 0)
        total = sum(vals)
        return {
            "trades": len(vals),
            "wins": wins,
            "losses": losses,
            "win_rate": (wins / len(vals)) if vals else 0.0,
            "profit_factor": (gross_win / gross_loss) if gross_loss else None,
            "expectancy_R": (total / len(vals)) if vals else 0.0,
            "total_R": total,
            "pnl": float(core[pnl_col].sum()) if pnl_col in core.columns else 0.0,
        }

    if not trades.empty and "r_core" in trades:
        valid_core = trades[trades["r_core"].notna()].copy()
        equity_curve = 10_000 + valid_core["pnl_core"].cumsum()
        max_dd = float((equity_curve - equity_curve.cummax()).min()) if not equity_curve.empty else 0.0
    else:
        max_dd = 0.0

    manifest = {
        "status": "COMPLETED_GOVERNED_OOS_EVALUATION",
        "evaluation_year": 2025,
        "mode": "CORE_PROFITABILITY_EVAL",
        "starting_equity": 10000.0,
        "final_equity_core": float(equity),
        "max_drawdown_core": max_dd,
        "eligible_events": int(len(eligible)),
        "executed_or_attempted_trades": int(len(closed)),
        "ambiguous_trades": int(closed["ambiguous"].sum()) if (not closed.empty and "ambiguous" in closed) else 0,
        "core": summary("r_core", "pnl_core"),
        "worst_case": {
            "total_R": float(closed["r_worst"].sum()) if not closed.empty else 0.0,
            "pnl": float(closed["pnl_worst"].sum()) if not closed.empty else 0.0,
        },
        "best_case": {
            "total_R": float(closed["r_best"].sum()) if not closed.empty else 0.0,
            "pnl": float(closed["pnl_best"].sum()) if not closed.empty else 0.0,
        },
        "risk_protocol": {"risk_pct": 0.005, "after_two_losses_pct": 0.0025, "stop_atr": 0.75, "target_r": 2.0},
        "costs_applied": False,
        "official_baseline": False,
        "oos_tuning": False,
        "new_rule_semantics": False,
        "tiz_generates_direction": False,
        "nison_generates_direction": False,
        "murphy_generates_direction": True,
    }
    (out_dir / "FINAL_2025_PNL_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--murphy-0022-0023", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()

    root = Path(__file__).resolve().parents[1]
    out = a.output_dir
    out.mkdir(parents=True, exist_ok=True)

    nison = out / "NISON_2025_FULL_EVIDENCE.csv"
    nison_manifest = out / "NISON_2025_FULL_EVIDENCE_MANIFEST.json"
    run([
        "python", "OOS_2025/run_nison_2025_full_production_v1.py",
        "--input", str(a.h1),
        "--output", str(nison),
        "--manifest", str(nison_manifest),
    ])

    m21 = out / "MURPHY_0021_2025.csv"
    run([
        "python", "OOS_2025/run_murphy_0021_2025_fresh_v1.py",
        "--input", str(a.h1),
        "--m1-input", str(a.m1),
        "--output", str(m21),
        "--manifest", str(out / "MURPHY_0021_MANIFEST.json"),
    ])

    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required for final market-state acquisition")
    market = out / "GBPUSD_MARKET_STATE.csv"
    download_dropbox(
        token,
        "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv",
        market,
    )

    ctx_dir = out / "context"
    run([
        "python", "OOS_2025/build_historical_context_execution_inputs_v1.py",
        "--source", str(market), "--output-dir", str(ctx_dir), "--year", "2025",
    ])

    # Reuse the existing Murphy 21/22/23 candidate stream contract.
    m21d = read_csv(m21, {"timestamp", "status", "directional_confirmation"})
    m22d = read_csv(a.murphy_0022_0023, {"timestamp", "status", "directional_confirmation", "rule_id"})
    frames = []
    for d in (m21d, m22d):
        w = d.copy()
        w["source_rule_id"] = w["rule_id"].astype(str) if "rule_id" in w else "MURPHY"
        w["direction"] = w["directional_confirmation"].astype(str)
        frames.append(w[["timestamp", "status", "direction", "source_rule_id"]])
    murphy = pd.concat(frames, ignore_index=True)
    priority = {"MURPHY_0022": 0, "MURPHY_0023": 1, "MURPHY_0021": 2}
    murphy["_pass"] = murphy["status"].eq("PASS").astype(int)
    murphy["_prio"] = murphy["source_rule_id"].map(priority).fillna(99)
    murphy = murphy.sort_values(["timestamp", "_pass", "_prio"], ascending=[True, False, True]).drop_duplicates("timestamp", keep="first")
    murphy = murphy.drop(columns=["_pass", "_prio"])
    murphy_csv = out / "MURPHY_2025_CANDIDATE_STREAM.csv"
    murphy.to_csv(murphy_csv, index=False)

    risk_csv = out / "RISK_2025_EVIDENCE.csv"
    run([
        "python", "OOS_2025/build_historical_risk_evidence_v1.py",
        "--context", str(ctx_dir / "execution.csv"),
        "--murphy", str(murphy_csv),
        "--output", str(risk_csv),
        "--manifest", str(out / "RISK_2025_EVIDENCE_MANIFEST.json"),
        "--year", "2025",
    ])

    nison_candidate = out / "NISON_2025_CANDIDATE_STREAM.csv"
    build_nison_candidate(nison, nison_candidate)

    events = out / "FINAL_2025_DECISION_EVENTS.csv"
    run([
        "python", "OOS_2025/full_decision_brain_historical_event_producer_v1.py",
        "--context", str(ctx_dir / "context.csv"),
        "--murphy", str(murphy_csv),
        "--nison", str(nison_candidate),
        "--risk", str(risk_csv),
        "--execution", str(ctx_dir / "execution.csv"),
        "--year", "2025",
        "--output", str(events),
        "--manifest", str(out / "FINAL_2025_DECISION_EVENTS_MANIFEST.json"),
        "--optional-tiz",
    ])

    # Keep the existing final event stream as the source-backed decision layer;
    # P&L is a separate evaluation step and does not alter the decision rules.
    manifest = backtest(events, a.h1, out)
    print(json.dumps(manifest, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
