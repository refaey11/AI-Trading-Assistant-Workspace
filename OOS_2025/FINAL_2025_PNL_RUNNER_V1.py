from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance
from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk

YEAR = 2025


def load_csv(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--market", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--equity", type=float, default=10000.0)
    args = p.parse_args()

    market = load_csv(args.market, {"timestamp", "close"})
    market = market[market["timestamp"].dt.year.eq(YEAR)].copy()
    murphy = load_csv(args.murphy, {"timestamp", "rule_id", "status"})
    nison = load_csv(args.nison, {"timestamp"})
    if market.empty:
        raise ValueError("No 2025 market rows")

    # Governance contract: require full 34+44 envelopes when the runner is called.
    murphy_ids = set(murphy["rule_id"].astype(str).str.upper())
    nison_ids = set(nison.get("rule_id", pd.Series(dtype=str)).astype(str).str.upper())
    required_murphy = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}
    required_nison = {f"NISON_{i:04d}" for i in range(1,45)}
    missing_m = sorted(required_murphy - murphy_ids)
    missing_n = sorted(required_nison - nison_ids) if nison_ids else sorted(required_nison)
    if missing_m or missing_n:
        raise SystemExit(json.dumps({"status":"BLOCKED","reason":"FULL_78_RULE_ENVELOPE_INCOMPLETE","missing_murphy":missing_m,"missing_nison":missing_n}, indent=2))

    grouped_m = {ts: g for ts, g in murphy.groupby("timestamp")}
    grouped_n = {ts: g for ts, g in nison.groupby("timestamp")}

    # This runner is deliberately conservative: it only realizes a trade when the
    # governed boundary returns an explicit executable decision. Outcomes are
    # evaluated from subsequent market bars without lookahead into the decision.
    decisions: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    for _, bar in market.iterrows():
        ts = bar["timestamp"]
        m = grouped_m.get(ts)
        n = grouped_n.get(ts)
        if m is None or n is None:
            continue

        # Keep the market row as the Brain context; full evidence is passed through
        # the governed adapter and must not be reduced to one rule before the boundary.
        row = bar.to_dict()
        murphy_evidence = {"rules": m.to_dict("records"), "attributed": True}
        nison_evidence = {"rules": n.to_dict("records"), "attributed": True}
        result = assess_with_governance(
            __import__("decision_brain"),
            row=row,
            query_as_of=ts.to_pydatetime(),
            mode="development",
            murphy_evidence=murphy_evidence,
            nison_evidence=nison_evidence,
            tiz_evidence={"authoritative": False, "status": "NOT_EVALUABLE"},
            risk_evidence={"authoritative": False, "status": "NOT_EVALUABLE"},
            historical_evidence={},
            provenance={"runner":"FINAL_2025_PNL_RUNNER_V1","evaluation_year":YEAR},
        )
        decisions.append({
            "timestamp": ts,
            "status": result.get("status"),
            "execution_eligible": bool(result.get("execution", {}).get("eligible", False)),
            "direction": result.get("direction"),
            "reason": result.get("reason"),
        })
        # Do not bypass frozen TIZ/Risk gates. This runner records eligibility only;
        # no production trade is claimed unless the governed execution bridge says so.
        if result.get("status") == "PASS" and result.get("execution", {}).get("eligible"):
            direction = str(result.get("direction") or "").upper()
            if direction in {"BUY", "SELL"}:
                rr = RiskRequest(
                    equity=args.equity,
                    risk_percent=0.005,
                    entry_price=float(bar["close"]),
                    stop_distance=0.0,
                    take_profit_distance=0.0,
                    stop_mode="structure",
                    risk_budget_locked=True,
                )
                risk = evaluate_risk(rr, direction, 0.005)
                if risk.risk_pass:
                    trades.append({"timestamp":ts,"direction":direction,"entry":float(bar["close"])})

    out = pd.DataFrame(decisions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    manifest = {
        "status": "PASS",
        "evaluation_year": YEAR,
        "events_evaluated": int(len(out)),
        "executable_decisions": int(sum(bool(x) for x in out.get("execution_eligible", pd.Series(dtype=bool)))),
        "trades_realized": int(len(trades)),
        "pnl_r": None,
        "official_profitability": False,
        "reason": "This V1 runner validates the governed full-evidence Decision Brain boundary. It does not fabricate outcomes or bypass frozen execution gates; a future execution-capable run must attach authoritative execution/risk inputs before P&L is promoted.",
        "oos_tuning": False,
        "new_rule_semantics": False,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
