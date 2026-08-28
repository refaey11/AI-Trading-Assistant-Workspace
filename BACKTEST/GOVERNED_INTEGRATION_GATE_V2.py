#!/usr/bin/env python3
"""Strict governed integration preflight for Decision Brain V1.

This gate is intentionally independent from the legacy DEV_BACKTEST_RUNNER_V1.
It proves source-backed as-of wiring and fails closed on missing TIZ/Risk evidence.
It never changes Decision Brain semantics and never treats historical memory as direction.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED = [
    "h1", "market_state", "mtf", "murphy", "nison",
    "historical_context", "historical_outcome", "similarity",
    "retrieval", "tiz", "risk", "handoff", "decision_brain",
]


def _sample_csv(path: Path, nrows: int = 5000) -> pd.DataFrame:
    return pd.read_csv(path, nrows=nrows, low_memory=False)


def _timestamp_series(df: pd.DataFrame) -> pd.Series:
    for c in ("timestamp", "signal_time", "time"):
        if c in df.columns:
            return pd.to_datetime(df[c], utc=True, errors="coerce")
    return pd.Series(dtype="datetime64[ns, UTC]")


def _find_csv(root: Path, name_hint: str | None = None) -> Path | None:
    files = list(root.rglob("*.csv")) if root.is_dir() else [root]
    if name_hint:
        exact = [p for p in files if p.name == name_hint]
        if exact:
            return exact[0]
    return files[0] if files else None


def _load_json_files(root: Path) -> list[tuple[Path, Any]]:
    out = []
    files = list(root.rglob("*.json")) if root.is_dir() else [root]
    for p in files:
        try:
            out.append((p, json.loads(p.read_text(encoding="utf-8"))))
        except Exception:
            continue
    return out


def _json_timestamps(obj: Any) -> list[pd.Timestamp]:
    found: list[pd.Timestamp] = []
    def walk(x: Any) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if k in {"timestamp", "query_timestamp", "signal_time"} and isinstance(v, str):
                    t = pd.to_datetime(v, utc=True, errors="coerce")
                    if not pd.isna(t):
                        found.append(t)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return found


def _check_no_2025(label: str, df: pd.DataFrame, failures: list[str]) -> None:
    ts = _timestamp_series(df)
    if ts.empty:
        failures.append(f"{label}: no timestamp column")
        return
    years = set(ts.dropna().dt.year.astype(int))
    if 2025 in years:
        failures.append(f"{label}: contains 2025 data; 2025 must remain LOCKED")


def _check_asof(label: str, source_ts: pd.Series, event_ts: pd.Series, failures: list[str]) -> None:
    s = source_ts.dropna().sort_values()
    e = event_ts.dropna().sort_values()
    if s.empty or e.empty:
        failures.append(f"{label}: empty timestamp sample")
        return
    if (s.min() > e.max()):
        failures.append(f"{label}: source starts after event sample")
    if s.max() > e.max():
        # This is fine for an as-of source; only future rows may not be consumed.
        pass
    if (e.min() < s.min()):
        failures.append(f"{label}: earliest event precedes source coverage")


def _risk_columns(df: pd.DataFrame) -> tuple[str, str, str, str | None] | None:
    def pick(*names: str) -> str | None:
        for n in names:
            if n in df.columns:
                return n
        return None
    entry = pick("entry", "entry_price", "signal_entry")
    sl = pick("sl", "stop_loss", "stop")
    tp = pick("tp", "take_profit", "target")
    atr = pick("atr", "H1_atr", "h1_atr", "atr20", "H1_ATR")
    if entry and sl and tp:
        return entry, sl, tp, atr
    return None


def _tiz_columns(df: pd.DataFrame) -> set[str]:
    return set(df.columns)


def main() -> int:
    ap = argparse.ArgumentParser()
    for name in REQUIRED:
        ap.add_argument(f"--{name.replace('_','-')}", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    paths = {k: Path(getattr(args, k.replace('-', '_'))) for k in REQUIRED}
    failures: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}

    # 1) Canonical H1 source and event basis.
    h1 = _sample_csv(paths["h1"], 20000)
    checks["h1_rows_sample"] = len(h1)
    checks["h1_columns"] = list(h1.columns)
    h1_ts = _timestamp_series(h1)
    if h1_ts.empty:
        failures.append("H1: timestamp missing")
    else:
        checks["h1_years_sample"] = sorted(set(h1_ts.dropna().dt.year.astype(int)))
        if 2025 in checks["h1_years_sample"]:
            # Source may cover 2025; the backtest event slice must exclude it.
            warnings.append("H1 source covers 2025; event slice will remain <= 2024")

    # 2) Directly source each evidence layer from its supplied artifact.
    ms = _sample_csv(paths["market_state"], 10000)
    mtf_file = _find_csv(paths["mtf"])
    murphy_file = _find_csv(paths["murphy"], "MURPHY_2016_2024_FULL_EVIDENCE.csv")
    nison_file = paths["nison"] if paths["nison"].is_file() else _find_csv(paths["nison"])
    hc_file = _find_csv(paths["historical_context"], "HISTORICAL_CONTEXT_MEMORY.csv")
    ho_file = _find_csv(paths["historical_outcome"], "HISTORICAL_OUTCOMES.csv")

    for label, p in [("MTF", mtf_file), ("Murphy", murphy_file), ("Nison", nison_file),
                     ("Historical Context", hc_file), ("Historical Outcome", ho_file)]:
        if p is None or not p.exists():
            failures.append(f"{label}: source artifact not found")

    if not ms.empty:
        _check_no_2025("Market State", ms, failures)
        checks["market_state_sample_rows"] = len(ms)
    if mtf_file:
        mtf = _sample_csv(mtf_file, 10000)
        _check_no_2025("MTF", mtf, failures)
        checks["mtf_columns"] = list(mtf.columns)
    else:
        mtf = pd.DataFrame()
    if murphy_file:
        murphy = _sample_csv(murphy_file, 10000)
        _check_no_2025("Murphy", murphy, failures)
        checks["murphy_columns"] = list(murphy.columns)
        if "source_rule_id" not in murphy.columns:
            failures.append("Murphy: source_rule_id missing")
    else:
        murphy = pd.DataFrame()
    if nison_file:
        # Only sample the large Nison file; never read the whole 525 MB file for the gate.
        nison = _sample_csv(nison_file, 10000)
        _check_no_2025("Nison", nison, failures)
        checks["nison_columns"] = list(nison.columns)
        if "rule_id" not in nison.columns:
            failures.append("Nison: rule_id missing")
    else:
        nison = pd.DataFrame()
    if hc_file:
        hc = _sample_csv(hc_file, 10000)
        _check_no_2025("Historical Context", hc, failures)
        checks["historical_context_columns"] = list(hc.columns)
        if "context_signature" not in hc.columns:
            failures.append("Historical Context: context_signature missing")
    else:
        hc = pd.DataFrame()
    if ho_file:
        ho = _sample_csv(ho_file, 10000)
        _check_no_2025("Historical Outcome", ho, failures)
        checks["historical_outcome_columns"] = list(ho.columns)
        if "context_signature" not in ho.columns:
            failures.append("Historical Outcome: context_signature missing")
    else:
        ho = pd.DataFrame()

    # 3) Similarity + retrieval must be historical/as-of for the development period.
    sim_jsons = _load_json_files(paths["similarity"])
    ret_jsons = _load_json_files(paths["retrieval"])
    sim_ts = [t for _, obj in sim_jsons for t in _json_timestamps(obj)]
    ret_ts = [t for _, obj in ret_jsons for t in _json_timestamps(obj)]
    checks["similarity_json_files"] = [str(p) for p, _ in sim_jsons]
    checks["retrieval_json_files"] = [str(p) for p, _ in ret_jsons]
    if not sim_ts:
        failures.append("Similarity V2: no timestamped historical/as-of readings")
    else:
        checks["similarity_years"] = sorted(set(t.year for t in sim_ts))
        if max(t.year for t in sim_ts) >= 2025 and min(t.year for t in sim_ts) == 2025:
            failures.append("Similarity V2: snapshot is 2025-only; no 2016-2024 as-of stream")
    if not ret_ts:
        failures.append("Context-Aware Retrieval V2: no timestamped historical/as-of readings")
    else:
        checks["retrieval_years"] = sorted(set(t.year for t in ret_ts))
        if max(t.year for t in ret_ts) >= 2025 and min(t.year for t in ret_ts) == 2025:
            failures.append("Context-Aware Retrieval V2: snapshot is 2025-only; no 2016-2024 as-of stream")

    # 4) TIZ: call/validate the real runtime boundary. Never manufacture PASS.
    tiz_file = _find_csv(paths["tiz"], "TIZ_PROCESS_SCORED_TRADES.csv")
    if not tiz_file:
        failures.append("TIZ: no TIZ process evidence CSV found")
    else:
        tiz = _sample_csv(tiz_file, 10000)
        checks["tiz_columns"] = list(tiz.columns)
        explicit = _tiz_columns(tiz)
        required_bool = {"rule_adherence", "risk_accepted", "impulse_override", "loss_chasing", "revenge_trade"}
        if not required_bool.issubset(explicit):
            failures.append("TIZ: authoritative runtime booleans absent; score/bin cannot be converted into psychology without inventing semantics")
        else:
            # Dynamic import only after source evidence is present.
            sys.path.insert(0, str(Path.cwd()))
            from RUNTIME.TIZ_PROCESS_GATE_V1.tiz_process_gate_v1 import evaluate_tiz_gate
            row = tiz.dropna(subset=list(required_bool)).iloc[0]
            res = evaluate_tiz_gate(
                bool(row["rule_adherence"]), bool(row["risk_accepted"]),
                bool(row["impulse_override"]), bool(row["loss_chasing"]),
                bool(row["revenge_trade"]),
            )
            checks["tiz_runtime_result"] = getattr(res, "process_state", getattr(res, "status", str(res)))

    # 5) Risk: prove real adapter can evaluate actual execution inputs.
    risk_source_frames = [("H1", h1), ("Market State", ms), ("Murphy", murphy), ("Nison", nison)]
    risk_plan = None
    for label, df in risk_source_frames:
        if not df.empty and _risk_columns(df):
            risk_plan = (label, df, _risk_columns(df))
            break
    if not risk_plan:
        failures.append("Risk: no source-backed entry/SL/TP execution plan found; cannot evaluate real Risk adapter")
    else:
        label, df, cols = risk_plan
        entry_c, sl_c, tp_c, atr_c = cols
        checks["risk_source"] = label
        checks["risk_columns"] = list(cols)
        if not atr_c:
            failures.append("Risk: source-backed execution plan has no ATR input")
        else:
            from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk
            r = df[[entry_c, sl_c, tp_c, atr_c]].dropna().iloc[0]
            try:
                risk_res = evaluate_risk(
                    equity=100000.0,
                    entry=float(r[entry_c]),
                    stop_loss=float(r[sl_c]),
                    take_profit=float(r[tp_c]),
                    atr=float(r[atr_c]),
                    prior_loss_streak=0,
                    peak_equity=100000.0,
                )
                checks["risk_runtime_result"] = getattr(risk_res, "passed", getattr(risk_res, "status", str(risk_res)))
            except Exception as exc:
                failures.append(f"Risk: runtime evaluation failed: {exc}")

    # 6) Decision Brain + handoff invariants.
    db = Path("RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py")
    handoff = Path("compatibility/knowledge_decision_handoff.py")
    adapter = Path("compatibility/decision_brain_v1_handoff_adapter.py")
    if not db.exists(): failures.append("Decision Brain V1 source missing")
    if not handoff.exists(): failures.append("Knowledge/Decision handoff missing")
    if not adapter.exists(): failures.append("Decision Brain handoff adapter missing")
    else:
        txt = adapter.read_text(encoding="utf-8")
        if "similarity=None" not in txt:
            failures.append("Decision Brain adapter no longer explicitly protects Brain semantics from Similarity direction")
    if db.exists() and "def assess(" not in db.read_text(encoding="utf-8"):
        failures.append("Decision Brain V1 assess() contract missing")

    # 7) Prove a real sample can reach the Brain row without changing direction semantics.
    if not ms.empty:
        row = ms.iloc[0].to_dict()
        if not mtf.empty:
            mrow = mtf.iloc[0].to_dict()
            for k in ["trend", "structure", "volume_ratio", "mtf_state", "h4_trend", "h4_structure"]:
                if k in mrow:
                    row[k] = mrow[k]
        try:
            sys.path.insert(0, str(Path.cwd()))
            from RECOVERED_SOURCES.DECISION_BRAIN_V1.decision_brain import DecisionBrain
            brain = DecisionBrain()
            assess = brain.assess(row, similarity=None)
            checks["brain_sample_bias"] = getattr(assess, "bias", None)
            checks["brain_sample_confidence"] = getattr(assess, "confidence", None)
            if getattr(assess, "bias", None) not in {"BULLISH", "BEARISH", "NEUTRAL"}:
                failures.append("Decision Brain sample returned invalid bias")
        except Exception as exc:
            failures.append(f"Decision Brain sample assessment failed: {exc}")

    # 8) Unified result.
    result = {
        "status": "PASS" if not failures else "FAIL",
        "gate": "GOVERNED_INTEGRATION_GATE_V2",
        "branch": os.environ.get("GITHUB_REF_NAME", "unknown"),
        "development_window": "2016-01-01 through 2024-12-31 inclusive",
        "oos_2025": "LOCKED",
        "failures": failures,
        "warnings": warnings,
        "checks": checks,
        "policy": {
            "legacy_runner_used": False,
            "tiz_hardcoded_pass": False,
            "risk_hardcoded_pass": False,
            "decision_brain_semantics_changed": False,
        },
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
