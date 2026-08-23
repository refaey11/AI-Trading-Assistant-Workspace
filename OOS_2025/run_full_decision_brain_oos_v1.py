from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event


REQUIRED_COMMON = {"timestamp"}


def _load_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def _index(df: pd.DataFrame, name: str) -> dict[pd.Timestamp, dict[str, Any]]:
    return {row["timestamp"]: row.to_dict() for _, row in df.iterrows()}


def _require_columns(df: pd.DataFrame, columns: set[str], name: str) -> None:
    missing = columns - set(df.columns)
    if missing:
        raise ValueError(f"{name}: missing columns: {sorted(missing)}")


def run(
    *,
    context_csv: str | Path,
    murphy_csv: str | Path,
    nison_csv: str | Path,
    risk_csv: str | Path,
    output_csv: str | Path,
    summary_json: str | Path,
    tiz_csv: str | Path | None = None,
    year: int,
    source_rule_ids: list[str],
) -> dict[str, Any]:
    context = _load_csv(context_csv)
    murphy = _load_csv(murphy_csv)
    nison = _load_csv(nison_csv)
    risk = _load_csv(risk_csv)
    tiz = _load_csv(tiz_csv) if tiz_csv else pd.DataFrame(columns=["timestamp"])

    _require_columns(context, {"timestamp", "entry_price", "atr"}, "context")
    _require_columns(murphy, {"timestamp", "status", "direction"}, "murphy")
    _require_columns(nison, {"timestamp", "confirmation", "contradiction"}, "nison")
    _require_columns(risk, {"timestamp", "risk_status", "stop_loss"}, "risk")
    if not tiz.empty:
        _require_columns(tiz, {"timestamp", "process_gate"}, "tiz")

    timestamps = sorted(set(context["timestamp"]) & set(murphy["timestamp"]) & set(nison["timestamp"]) & set(risk["timestamp"]))
    timestamps = [ts for ts in timestamps if ts.year == year]
    if not timestamps:
        raise ValueError(f"No fully joinable timestamps for evaluation year {year}")

    context_i, murphy_i, nison_i, risk_i, tiz_i = map(_index, (context, murphy, nison, risk, tiz))
    brain = importlib.import_module("RECOVERED_SOURCES.DECISION_BRAIN_V1.decision_brain")

    rows: list[dict[str, Any]] = []
    for ts in timestamps:
        c = context_i[ts]
        m = murphy_i[ts]
        n = nison_i[ts]
        r = risk_i[ts]
        t = tiz_i.get(ts, {"timestamp": ts, "process_gate": "NOT_EVALUABLE"})
        row_features = {k: v for k, v in c.items() if k not in {"timestamp", "entry_price", "atr"}}

        result = assemble_decision_event(
            decision_brain_module=brain,
            row=row_features,
            query_as_of=ts.isoformat(),
            murphy_evidence={"status": m.get("status"), "direction": m.get("direction")},
            nison_evidence={"confirmation": n.get("confirmation"), "contradiction": bool(n.get("contradiction", False))},
            tiz_evidence={"process_gate": t.get("process_gate")},
            risk_evidence={
                "risk_status": r.get("risk_status"),
                "stop_loss": r.get("stop_loss"),
                "take_profit": r.get("take_profit"),
                "rr": r.get("rr"),
            },
            historical_evidence=None,
            source_rule_ids=source_rule_ids,
            entry_price=float(c["entry_price"]),
            atr=float(c["atr"]),
            mode="oos_evaluation",
            provenance={"context": str(context_csv), "murphy": str(murphy_csv), "nison": str(nison_csv), "risk": str(risk_csv), "tiz": str(tiz_csv) if tiz_csv else None},
        )

        execution = result.get("execution_plan", {})
        rows.append({
            "timestamp": ts.isoformat(),
            "year": year,
            "status": result.get("status"),
            "decision": result.get("decision", {}).get("decision", {}).get("final"),
            "logic": result.get("decision", {}).get("decision", {}).get("logic"),
            "execution_status": execution.get("status"),
            "direction": execution.get("direction"),
            "entry_price": execution.get("entry_price"),
            "atr": execution.get("atr"),
            "stop_loss": execution.get("stop_loss"),
            "take_profit": execution.get("take_profit"),
            "reason": (result.get("decision", {}).get("decision", {}).get("reasons_against") or [None])[0],
            "tiz_verified": result.get("audit", {}).get("tiz_verified"),
            "nison_generated_direction": result.get("audit", {}).get("nison_generated_direction"),
            "historical_memory_used_for_direction": result.get("audit", {}).get("historical_memory_used_for_direction"),
            "oos_tuning": result.get("audit", {}).get("oos_tuning"),
        })

    out = pd.DataFrame(rows)
    counts = out["status"].value_counts().to_dict()
    summary = {
        "status": "PASS",
        "evaluation_year": year,
        "input_timestamps": int(len(timestamps)),
        "output_rows": int(len(out)),
        "status_counts": {str(k): int(v) for k, v in counts.items()},
        "executable_rows": int((out["status"] == "EXECUTABLE").sum()),
        "no_trade_rows": int((out["status"] == "NO_TRADE").sum()),
        "not_executable_rows": int((out["status"] == "NOT_EXECUTABLE").sum()),
        "tiz_verified_rows": int(out["tiz_verified"].fillna(False).astype(bool).sum()),
        "nison_generated_direction_rows": int(out["nison_generated_direction"].fillna(False).astype(bool).sum()),
        "historical_memory_used_for_direction_rows": int(out["historical_memory_used_for_direction"].fillna(False).astype(bool).sum()),
        "oos_tuning_rows": int(out["oos_tuning"].fillna(False).astype(bool).sum()),
        "source_rule_ids": list(source_rule_ids),
        "fail_closed": True,
        "profitability_claim": False,
        "next_step": "Attach realized trade outcomes/costs to EXECUTABLE rows for Final OOS profitability calculation.",
    }

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    Path(summary_json).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_csv, index=False)
    Path(summary_json).write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True)
    p.add_argument("--murphy", required=True)
    p.add_argument("--nison", required=True)
    p.add_argument("--risk", required=True)
    p.add_argument("--tiz")
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--rules", nargs="+", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--summary", required=True)
    a = p.parse_args()
    run(context_csv=a.context, murphy_csv=a.murphy, nison_csv=a.nison, risk_csv=a.risk, tiz_csv=a.tiz, year=a.year, source_rule_ids=a.rules, output_csv=a.output, summary_json=a.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
