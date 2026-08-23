from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event

REQUIRED_CONTEXT = {"timestamp"}
REQUIRED_MURPHY = {"timestamp", "status", "direction", "source_rule_id"}
REQUIRED_NISON = {"timestamp", "confirmation", "contradiction", "source_rule_id"}
REQUIRED_RISK = {"timestamp", "risk_status"}
REQUIRED_EXECUTION = {"timestamp", "entry_price", "atr"}
REQUIRED_TIZ = {"timestamp", "process_gate"}


def _read(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp").drop_duplicates("timestamp", keep="last")


def _read_tiz(path: Path | None) -> pd.DataFrame | None:
    if path is None:
        return None
    return _read(path, REQUIRED_TIZ)


def _pick_context_columns(df: pd.DataFrame, ts: pd.Timestamp) -> dict[str, Any]:
    row = df.loc[df["timestamp"] == ts]
    if row.empty:
        # As-of join policy: only use the latest completed context observation.
        row = df.loc[df["timestamp"] <= ts].tail(1)
    if row.empty:
        return {}
    return row.iloc[0].drop(labels=["timestamp"], errors="ignore").to_dict()


def _optional_tiz(ts: pd.Timestamp, tiz: pd.DataFrame | None) -> dict[str, Any]:
    if tiz is None:
        return {"process_gate": "NOT_EVALUABLE"}
    row = tiz.loc[tiz["timestamp"] <= ts].tail(1)
    if row.empty:
        return {"process_gate": "NOT_EVALUABLE"}
    return row.iloc[0].drop(labels=["timestamp"], errors="ignore").to_dict()


def _decision_ready_tiz(tiz_evidence: dict[str, Any], *, optional_tiz: bool) -> dict[str, Any]:
    """Map the frozen optional-TIZ OOS policy without changing canonical semantics."""
    state = str(tiz_evidence.get("process_gate") or tiz_evidence.get("status") or "NOT_EVALUABLE").upper()
    if state in {"PASS", "READY", "AVAILABLE"}:
        return dict(tiz_evidence)
    if optional_tiz and state == "NOT_EVALUABLE":
        # The policy explicitly permits missing TIZ evidence in this isolated OOS
        # evaluation mode, while preserving an auditable unverified flag.
        return {**tiz_evidence, "process_gate": "AVAILABLE", "tiz_verified": False}
    return dict(tiz_evidence)


def build_events(
    *,
    market_context: pd.DataFrame,
    murphy: pd.DataFrame,
    nison: pd.DataFrame,
    risk: pd.DataFrame,
    execution: pd.DataFrame,
    tiz: pd.DataFrame | None,
    year: int,
    optional_tiz: bool,
) -> pd.DataFrame:
    """Assemble already-derived component evidence into timestamp-level events.

    This producer does not evaluate rules, infer missing evidence, or create
    direction. Every directional/confirmation/process/risk input must already
    exist in a governed upstream stream. Missing evidence fails closed.
    """
    timestamps = sorted(
        set(murphy["timestamp"])
        & set(nison["timestamp"])
        & set(risk["timestamp"])
        & set(execution["timestamp"])
    )

    records: list[dict[str, Any]] = []
    for ts in timestamps:
        if ts.year != year:
            continue

        m = murphy.loc[murphy["timestamp"] == ts].iloc[0]
        n = nison.loc[nison["timestamp"] == ts].iloc[0]
        r = risk.loc[risk["timestamp"] == ts].iloc[0]
        e = execution.loc[execution["timestamp"] == ts].iloc[0]
        t = _optional_tiz(ts, tiz)
        t_for_decision = _decision_ready_tiz(t, optional_tiz=optional_tiz)

        source_rule_ids = [str(m["source_rule_id"]), str(n["source_rule_id"])]
        brain_row = _pick_context_columns(market_context, ts)
        result = assemble_decision_event(
            decision_brain_module=decision_brain,
            row=brain_row,
            query_as_of=str(ts),
            murphy_evidence=m.drop(labels=["timestamp"], errors="ignore").to_dict(),
            nison_evidence=n.drop(labels=["timestamp"], errors="ignore").to_dict(),
            tiz_evidence=t_for_decision,
            risk_evidence=r.drop(labels=["timestamp"], errors="ignore").to_dict(),
            historical_evidence=None,
            source_rule_ids=source_rule_ids,
            entry_price=float(e["entry_price"]),
            atr=float(e["atr"]),
            mode="oos_evaluation",
            provenance={
                "producer": "full_decision_brain_historical_event_producer_v1",
                "evaluation_year": year,
                "optional_tiz": optional_tiz,
            },
        )
        records.append(
            {
                "timestamp": ts,
                "evaluation_year": year,
                "status": result.get("status"),
                "direction": result.get("decision", {}).get("decision", {}).get("final"),
                "execution_status": result.get("execution_plan", {}).get("status"),
                "entry_price": result.get("execution_plan", {}).get("entry_price"),
                "stop_loss": result.get("execution_plan", {}).get("stop_loss"),
                "take_profit": result.get("execution_plan", {}).get("take_profit"),
                "risk_pass": r.get("risk_status"),
                "tiz_verified": bool(t.get("tiz_verified", False)),
                "tiz_status": t.get("process_gate", t.get("status", "NOT_EVALUABLE")),
                "nison_confirmation": n.get("confirmation"),
                "nison_contradiction": bool(n.get("contradiction", False)),
                "murphy_direction": m.get("direction"),
                "murphy_status": m.get("status"),
                "source_rule_ids": json.dumps(source_rule_ids),
                "reason": result.get("reason") or result.get("decision", {}).get("decision", {}).get("reasons_against", []),
            }
        )

    columns = [
        "timestamp", "evaluation_year", "status", "direction", "execution_status",
        "entry_price", "stop_loss", "take_profit", "risk_pass", "tiz_verified",
        "tiz_status", "nison_confirmation", "nison_contradiction", "murphy_direction",
        "murphy_status", "source_rule_ids", "reason",
    ]
    return pd.DataFrame(records, columns=columns)


def run(*, context_path: Path, murphy_path: Path, nison_path: Path, risk_path: Path,
        execution_path: Path, tiz_path: Path | None, year: int, output: Path,
        manifest: Path, optional_tiz: bool) -> dict[str, Any]:
    context = _read(context_path, REQUIRED_CONTEXT)
    murphy = _read(murphy_path, REQUIRED_MURPHY)
    nison = _read(nison_path, REQUIRED_NISON)
    risk = _read(risk_path, REQUIRED_RISK)
    execution = _read(execution_path, REQUIRED_EXECUTION)
    tiz = _read_tiz(tiz_path)

    events = build_events(
        market_context=context, murphy=murphy, nison=nison, risk=risk,
        execution=execution, tiz=tiz, year=year, optional_tiz=optional_tiz,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output, index=False)

    result = {
        "status": "PASS",
        "evaluation_year": year,
        "events": int(len(events)),
        "executable": int((events["status"] == "EXECUTABLE").sum()) if not events.empty else 0,
        "no_trade": int((events["status"] == "NO_TRADE").sum()) if not events.empty else 0,
        "not_evaluable": int((events["status"] == "NOT_EVALUABLE").sum()) if not events.empty else 0,
        "tiz_verified_events": int(events["tiz_verified"].fillna(False).astype(bool).sum()) if not events.empty else 0,
        "optional_tiz": bool(optional_tiz),
        "oos_tuning": False,
        "new_rule_semantics": False,
        "source_backed_components_only": True,
    }
    manifest.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--risk", required=True, type=Path)
    p.add_argument("--execution", required=True, type=Path)
    p.add_argument("--tiz", type=Path)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--optional-tiz", action="store_true")
    args = p.parse_args()
    result = run(
        context_path=args.context, murphy_path=args.murphy, nison_path=args.nison,
        risk_path=args.risk, execution_path=args.execution, tiz_path=args.tiz,
        year=args.year, output=args.output, manifest=args.manifest,
        optional_tiz=args.optional_tiz,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
