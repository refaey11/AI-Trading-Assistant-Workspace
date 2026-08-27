from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event
from OOS_2025.governed_rule_fan_in_v1 import build_lossless_rule_groups, legacy_selected_row

REQUIRED_CONTEXT = {"timestamp"}
REQUIRED_MURPHY = {"timestamp", "status", "direction", "source_rule_id"}
REQUIRED_NISON = {"timestamp", "confirmation", "contradiction", "source_rule_id"}
REQUIRED_RISK = {"timestamp", "risk_status"}
REQUIRED_EXECUTION = {"timestamp", "entry_price", "atr"}
REQUIRED_TIZ = {"timestamp", "process_gate"}


def _read(path: Path, required: set[str], *, preserve_rule_rows: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    df = df.sort_values("timestamp", kind="stable")
    if not preserve_rule_rows:
        df = df.drop_duplicates("timestamp", keep="last")
    return df


def _read_full_evidence(path: Path | None, family: str) -> pd.DataFrame | None:
    if path is None:
        return None
    df = pd.read_csv(path)
    required = {"timestamp", "source_rule_id"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{family} full evidence: missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{family} full evidence: invalid timestamps")
    return df.sort_values(["timestamp", "source_rule_id"], kind="stable").reset_index(drop=True)


def _read_tiz(path: Path | None):
    return None if path is None else _read(path, REQUIRED_TIZ)


def _optional_tiz(ts, tiz):
    if tiz is None:
        return {"process_gate": "NOT_EVALUABLE"}
    row = tiz.loc[tiz["timestamp"] <= ts].tail(1)
    return {"process_gate": "NOT_EVALUABLE"} if row.empty else row.iloc[0].drop(labels=["timestamp"], errors="ignore").to_dict()


def _decision_ready_tiz(t, optional_tiz):
    state = str(t.get("process_gate") or t.get("status") or "NOT_EVALUABLE").upper()
    if state in {"PASS", "READY", "AVAILABLE"}:
        return dict(t)
    if optional_tiz and state == "NOT_EVALUABLE":
        return {**t, "process_gate": "READY", "tiz_verified": False}
    return dict(t)


def _pick_context(df, ts):
    row = df.loc[df["timestamp"] <= ts].tail(1)
    return {} if row.empty else row.iloc[0].drop(labels=["timestamp"], errors="ignore").to_dict()


def _governed_source_rule_ids(murphy_rows: list[dict[str, Any]], nison_rows: list[dict[str, Any]]) -> list[str]:
    out: list[str] = []
    for row in [*murphy_rows, *nison_rows]:
        rid = str(row.get("source_rule_id") or row.get("rule_id") or "").strip()
        if not rid or rid == "NISON_NONE":
            continue
        out.append(rid)
    return list(dict.fromkeys(out))


def _build_evidence_set(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    evidence: dict[str, dict[str, Any]] = {}
    for row in rows:
        rid = str(row.get("source_rule_id") or row.get("rule_id") or "").strip()
        if not rid or rid == "NISON_NONE":
            continue
        evidence[rid] = dict(row)
    return evidence


def _full_rows_at(df: pd.DataFrame | None, ts) -> list[dict[str, Any]]:
    if df is None:
        return []
    part = df.loc[df["timestamp"] == ts].copy()
    return part.drop(columns=["timestamp"], errors="ignore").to_dict("records")


def _nison_compat_from_full_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    directional = {"BULLISH", "BEARISH"}
    directional_pass = sorted({
        str(r.get("direction", "")).upper()
        for r in rows
        if str(r.get("status", "")).upper() == "PASS" and str(r.get("direction", "")).upper() in directional
    })
    directional_fail = sorted({
        str(r.get("direction", "")).upper()
        for r in rows
        if str(r.get("status", "")).upper() == "FAIL" and str(r.get("direction", "")).upper() in directional
    })
    confirmation = directional_pass[0] if len(directional_pass) == 1 else "CONFLICTED" if len(directional_pass) > 1 else "ABSENT"
    return {
        "confirmation": confirmation,
        "contradiction": bool(directional_fail),
        "directional_pass_count": len(directional_pass),
        "directional_fail_count": len(directional_fail),
        "source_rule_id": "NISON_AGGREGATE",
    }


def build_events(*, market_context, murphy, nison, risk, execution, tiz, year, optional_tiz, murphy_full_evidence=None, nison_full_evidence=None):
    required_timestamps = set(murphy["timestamp"]) & set(risk["timestamp"]) & set(execution["timestamp"])
    if murphy_full_evidence is not None:
        required_timestamps &= set(murphy_full_evidence["timestamp"])
    if nison_full_evidence is not None:
        required_timestamps &= set(nison_full_evidence["timestamp"])
    else:
        required_timestamps &= set(nison["timestamp"])
    timestamps = sorted(required_timestamps)

    murphy_groups = build_lossless_rule_groups(murphy)
    nison_groups = build_lossless_rule_groups(nison)
    records = []

    for ts in timestamps:
        if ts.year != year:
            continue

        m_full = _full_rows_at(murphy_full_evidence, ts)
        n_full = _full_rows_at(nison_full_evidence, ts)
        if not m_full or not n_full:
            continue

        m_rows = murphy_groups.get(ts, []) or m_full
        n_rows = nison_groups.get(ts, [])

        m_evidence_set = _build_evidence_set(m_full)
        n_evidence_set = _build_evidence_set(n_full)
        if len(m_evidence_set) < 34:
            raise AssertionError(f"{ts}: Murphy full evidence set contains {len(m_evidence_set)} rules, expected 34")
        if len(n_evidence_set) < 44:
            raise AssertionError(f"{ts}: Nison full evidence set contains {len(n_evidence_set)} rules, expected 44")

        m = legacy_selected_row(m_rows)
        n = legacy_selected_row(n_rows) if n_rows else _nison_compat_from_full_rows(n_full)
        murphy_for_decision = {**m, "evidence_set": m_evidence_set, "evidence_count": len(m_evidence_set)}
        nison_for_decision = {**n, "evidence_set": n_evidence_set, "evidence_count": len(n_evidence_set)}

        r = risk.loc[risk["timestamp"] == ts].iloc[0]
        e = execution.loc[execution["timestamp"] == ts].iloc[0]
        t = _optional_tiz(ts, tiz)
        td = _decision_ready_tiz(t, optional_tiz)
        source_rule_ids = _governed_source_rule_ids(m_full, n_full)

        result = assemble_decision_event(
            decision_brain_module=decision_brain,
            row=_pick_context(market_context, ts),
            query_as_of=str(ts),
            murphy_evidence=murphy_for_decision,
            nison_evidence=nison_for_decision,
            tiz_evidence=td,
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
                "fan_in_mode": "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT",
                "murphy_rule_count": len(m_evidence_set),
                "nison_rule_count": len(n_evidence_set),
                "murphy_rule_ids_preserved": sorted(m_evidence_set),
                "nison_rule_ids_preserved": sorted(n_evidence_set),
                "all_evidence_passed_to_boundary": True,
            },
        )

        decision = result.get("decision", {}) or {}
        decision_block = decision.get("decision", {}) if isinstance(decision, dict) else {}
        reasons_against = decision_block.get("reasons_against", []) if isinstance(decision_block, dict) else []
        execution_plan = result.get("execution_plan", {}) or {}
        primary_reason = reasons_against[0] if isinstance(reasons_against, list) and reasons_against else result.get("reason")
        records.append(
            {
                "timestamp": ts,
                "evaluation_year": year,
                "status": result.get("status"),
                "direction": decision_block.get("final"),
                "execution_status": execution_plan.get("status"),
                "entry_price": execution_plan.get("entry_price"),
                "atr": float(e["atr"]),
                "stop_loss": execution_plan.get("stop_loss"),
                "take_profit": execution_plan.get("take_profit"),
                "risk_pass": r.get("risk_status"),
                "tiz_verified": bool(t.get("tiz_verified", False)),
                "tiz_status": t.get("process_gate", t.get("status", "NOT_EVALUABLE")),
                "nison_confirmation": n.get("confirmation"),
                "nison_contradiction": bool(n.get("contradiction", False)),
                "murphy_direction": m.get("direction"),
                "murphy_status": m.get("status"),
                "source_rule_ids": json.dumps(source_rule_ids),
                "murphy_rule_count": len(m_evidence_set),
                "nison_rule_count": len(n_evidence_set),
                "murphy_rule_ids": json.dumps(sorted(m_evidence_set)),
                "nison_rule_ids": json.dumps(sorted(n_evidence_set)),
                "reason": json.dumps(reasons_against) if isinstance(reasons_against, list) else str(primary_reason or ""),
                "primary_reason": str(primary_reason or "").strip() or "UNKNOWN",
                "governed_78_receipt_sha256": str((result.get("audit", {}) or {}).get("governed_78_adapter_receipt", {}).get("package_sha256", "")),
            }
        )

    return pd.DataFrame(records)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--risk", required=True, type=Path)
    p.add_argument("--execution", required=True, type=Path)
    p.add_argument("--murphy-full-evidence", type=Path)
    p.add_argument("--nison-full-evidence", type=Path)
    p.add_argument("--tiz", type=Path)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--optional-tiz", action="store_true")
    a = p.parse_args()

    context = _read(a.context, REQUIRED_CONTEXT)
    murphy = _read(a.murphy, REQUIRED_MURPHY, preserve_rule_rows=True)
    nison = _read(a.nison, REQUIRED_NISON, preserve_rule_rows=True)
    murphy_full = _read_full_evidence(a.murphy_full_evidence, "Murphy")
    nison_full = _read_full_evidence(a.nison_full_evidence, "Nison")
    risk = _read(a.risk, REQUIRED_RISK)
    execution = _read(a.execution, REQUIRED_EXECUTION)
    tiz = _read_tiz(a.tiz)
    events = build_events(
        market_context=context,
        murphy=murphy,
        nison=nison,
        risk=risk,
        execution=execution,
        tiz=tiz,
        year=a.year,
        optional_tiz=a.optional_tiz,
        murphy_full_evidence=murphy_full,
        nison_full_evidence=nison_full,
    )
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.manifest.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(a.output, index=False)

    primary_reason_counts = Counter(events["primary_reason"].astype(str)) if not events.empty else Counter()
    status_counts = Counter(events["status"].astype(str)) if not events.empty else Counter()
    execution_status_counts = Counter(events["execution_status"].fillna("UNKNOWN").astype(str)) if not events.empty else Counter()
    risk_pass_counts = Counter(events["risk_pass"].fillna("UNKNOWN").astype(str)) if not events.empty else Counter()
    tiz_status_counts = Counter(events["tiz_status"].fillna("UNKNOWN").astype(str)) if not events.empty else Counter()

    result = {
        "status": "PASS",
        "evaluation_year": a.year,
        "events": int(len(events)),
        "executable": int((events["status"] == "EXECUTABLE").sum()) if not events.empty else 0,
        "no_trade": int((events["status"] == "NO_TRADE").sum()) if not events.empty else 0,
        "not_evaluable": int((events["status"] == "NOT_EVALUABLE").sum()) if not events.empty else 0,
        "tiz_verified_events": int(events["tiz_verified"].fillna(False).astype(bool).sum()) if not events.empty else 0,
        "optional_tiz": bool(a.optional_tiz),
        "oos_tuning": False,
        "new_rule_semantics": False,
        "source_backed_components_only": True,
        "fan_in_mode": "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT",
        "rule_rows_preserved": True,
        "murphy_rule_count_in_event": int(events["murphy_rule_count"].min()) if not events.empty else 0,
        "nison_rule_count_in_event": int(events["nison_rule_count"].min()) if not events.empty else 0,
        "primary_reason_counts": dict(primary_reason_counts.most_common()),
        "event_status_counts": dict(status_counts),
        "execution_status_counts": dict(execution_status_counts),
        "risk_pass_counts": dict(risk_pass_counts),
        "tiz_status_counts": dict(tiz_status_counts),
    }
    a.manifest.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
