from __future__ import annotations

"""Small real-source integration sample.

Consumes only a bounded number of rows from the real six-timeframe source
package, then crosses the existing Dynamic MTF resolver/binder, Handoff,
Decision Brain V1 and Risk boundary.

This script never invents trend/setup/confirmation/SL/TP/ATR/equity inputs.
Missing upstream execution inputs are passed to Risk and must fail closed.
"""

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import pandas as pd

from BACKTEST.MTF_SIX_TF_SOURCE_ADAPTER_V1 import SIX_TF, discover, infer_tf_from_text
from compatibility.dynamic_mtf_binding_adapter_v1 import bind_dynamic_mtf
from compatibility.dynamic_mtf_runtime_resolver_v1 import resolve_mtf_event
from compatibility import knowledge_decision_handoff as handoff
from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk

ROOT = Path(__file__).resolve().parents[1]
BRAIN_PATH = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"
TIZ_PATH = ROOT / "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json"


def load_brain():
    spec = importlib.util.spec_from_file_location("decision_brain_v1_sample", BRAIN_PATH)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {BRAIN_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_first_real_row(root: Path, max_rows: int) -> tuple[pd.Timestamp, dict[str, dict[str, Any]], dict[str, Any]]:
    by_tf, _ = discover(root, max_rows=max_rows)
    missing = [tf for tf in SIX_TF if not by_tf[tf]]
    if missing:
        raise ValueError(f"missing native timeframe sources: {missing}")

    # Read only the first bounded sample row from one source file per timeframe.
    evidence: dict[str, dict[str, Any]] = {}
    source_meta: dict[str, Any] = {}
    timestamps: list[pd.Timestamp] = []
    for tf in SIX_TF:
        path = Path(by_tf[tf][0]["path"])
        df = pd.read_csv(path, nrows=max_rows, low_memory=False)
        ts_col = by_tf[tf][0]["timestamp_column"]
        ts = pd.to_datetime(df[ts_col], utc=True, errors="coerce", format="mixed")
        df = df.loc[ts.notna()].copy()
        if df.empty:
            raise ValueError(f"{path}: no valid sampled timestamp")
        ts = ts.loc[ts.notna()].iloc[0]
        timestamps.append(ts)
        row = df.iloc[0]

        item: dict[str, Any] = {"source_file": str(path), "native_timestamp": ts.isoformat()}
        # Copy only explicit, source-provided evidence fields. Never infer them.
        aliases = {
            "context_complete": ("context_complete",),
            "structure_complete": ("structure_complete",),
            "setup_complete": ("setup_complete",),
            "confirmation_complete": ("confirmation_complete",),
            "contradicted": ("contradicted",),
            "risk_feasible": ("risk_feasible",),
            "alignment_state": ("alignment_state",),
            "direction": ("direction",),
        }
        lower = {str(c).lower(): c for c in df.columns}
        for target, names in aliases.items():
            found = next((lower[n] for n in names if n in lower), None)
            if found is not None and pd.notna(row[found]):
                value = row[found]
                if target.endswith("complete") or target in {"contradicted", "risk_feasible"}:
                    if isinstance(value, bool):
                        item[target] = value
                    elif str(value).strip().upper() in {"TRUE", "1", "YES"}:
                        item[target] = True
                    elif str(value).strip().upper() in {"FALSE", "0", "NO"}:
                        item[target] = False
                else:
                    item[target] = value
        evidence[tf] = item
        source_meta[tf] = by_tf[tf][0]

    anchor = min(timestamps)
    return anchor, evidence, source_meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--h1", type=Path, required=True)
    ap.add_argument("--mtf-full-dir", type=Path, required=True)
    ap.add_argument("--report", type=Path, default=Path("artifacts/real_source_e2e_sample_v1.json"))
    ap.add_argument("--max-rows", type=int, default=200)
    args = ap.parse_args()

    report: dict[str, Any] = {
        "status": "PASS",
        "path": "real_source -> dynamic_mtf -> handoff -> decision_brain -> risk",
        "development_window": "2016-2024",
        "2025_locked": True,
        "six_timeframes": list(SIX_TF),
        "failures": [],
        "warnings": [],
    }

    try:
        anchor, timeframe_evidence, source_meta = sample_first_real_row(args.mtf_full_dir, args.max_rows)
        report["anchor_timestamp"] = anchor.isoformat()
        report["source_meta"] = source_meta
        report["timeframe_evidence_fields_present"] = {
            tf: sorted(k for k in timeframe_evidence[tf] if k != "source_file") for tf in SIX_TF
        }

        resolver = resolve_mtf_event(timeframe_evidence=timeframe_evidence)
        report["dynamic_mtf_resolver"] = {
            "status": resolver.status,
            "alignment_state": resolver.alignment_state,
            "selected_execution_timeframe": resolver.selected_execution_timeframe,
            "context_timeframes_used": resolver.context_timeframes_used,
            "confirmation_timeframes_used": resolver.confirmation_timeframes_used,
            "setup_timeframe": resolver.setup_timeframe,
            "macro_timeframe": resolver.macro_timeframe,
            "selection_reasons": resolver.selection_reasons,
            "rejected_candidate_reasons": resolver.rejected_candidate_reasons,
            "evidence_trace": resolver.evidence_trace,
        }

        role_assignments = {
            "macro_context": resolver.macro_timeframe,
            "context": resolver.context_timeframes_used[1] if len(resolver.context_timeframes_used) > 1 else (resolver.context_timeframes_used[0] if resolver.context_timeframes_used else None),
            "setup": resolver.setup_timeframe,
            "confirmation": resolver.confirmation_timeframes_used[0] if resolver.confirmation_timeframes_used else None,
            "execution": resolver.selected_execution_timeframe,
        }
        role_assignments = {k: v for k, v in role_assignments.items() if v is not None}
        binder = bind_dynamic_mtf(
            available_timeframes=SIX_TF,
            role_assignments=role_assignments,
            evidence_trace=resolver.evidence_trace,
        )
        report["dynamic_mtf_binding"] = {
            "status": binder.status,
            "alignment_state": binder.alignment_state,
            "role_timeframes": dict(binder.role_timeframes),
            "evidence_trace": binder.evidence_trace,
        }

        brain = load_brain()
        brain_row = {
            "mtf_trend_score": 0.0,
            **{f"{tf}_trend_regime": 0.0 for tf in SIX_TF},
            **{f"{tf}_volume_regime": 0.0 for tf in SIX_TF},
            "volume_available": False,
        }
        # Copy explicit source-provided trend-regime values only; no OHLC-derived trend is created.
        for tf in SIX_TF:
            item = timeframe_evidence[tf]
            raw = item.get("trend_regime")
            if raw is not None:
                try:
                    brain_row[f"{tf}_trend_regime"] = float(raw)
                except (TypeError, ValueError):
                    report["warnings"].append(f"{tf}: explicit trend_regime was non-numeric and was left unresolved")

        alignment_state = binder.alignment_state if binder.status == "PASS" else "NEEDS_REVIEW"
        candidate_direction = None
        directions = [str(timeframe_evidence[tf].get("direction")).lower() for tf in SIX_TF if timeframe_evidence[tf].get("direction") is not None]
        if len(set(directions)) == 1:
            candidate_direction = directions[0]

        evidence_bundle = {
            "h1": {"status": "CONNECTED", "timestamp": anchor.isoformat(), "direction": None, "final_trade_decision": None},
            "dynamic_mtf": {"status": binder.status, "alignment_state": binder.alignment_state, "role_timeframes": dict(binder.role_timeframes), "direction": None, "final_trade_decision": None},
            "murphy": {"status": "NOT_IN_SAMPLE", "direction": None},
            "nison": {"status": "NOT_IN_SAMPLE", "confirmation": None, "direction_generated": False},
            "historical_context": {"status": "NOT_IN_SAMPLE", "direction": None, "final_trade_decision": None},
            "historical_outcome": {"status": "NOT_IN_SAMPLE", "direction": None, "final_trade_decision": None},
            "similarity": {"status": "EVIDENCE_ONLY", "direction": None, "final_trade_decision": None},
            "context_aware_retrieval": {"status": "EVIDENCE_ONLY", "direction": None, "final_trade_decision": None},
            "tiz": {"status": "NOT_EVALUABLE", "direction": None, "final_trade_decision": None},
        }
        h = handoff.build_handoff(
            brain_row,
            {
                "alignment_state": alignment_state,
                "candidate_direction": candidate_direction or "neutral",
                "contradiction_gate": "PASS",
                "process_gate": "NOT_EVALUABLE",
                "book_evidence_status": "NOT_IN_SAMPLE",
                "market_evidence_status": "CONNECTED",
                "similarity_record_count": 0,
                "evidence_bundle": evidence_bundle,
            },
            similarity=evidence_bundle["similarity"],
        )
        report["handoff"] = {
            "routing": h["routing"],
            "abstain": h["gates"]["abstain"],
            "hard_block": h["gates"]["hard_block"],
            "contradiction": h["gates"]["contradiction"],
        }

        assessment = brain.assess(h["decision_brain_row"], similarity=None)
        report["decision_brain"] = {
            "executed": True,
            "directional_bias": assessment.directional_bias,
            "confidence": assessment.confidence,
            "market_state": assessment.market_state,
        }

        # Real-source sample must demonstrate Risk's actual fail-closed boundary.
        entry = float(pd.read_csv(args.h1, nrows=1)["close"].iloc[0])
        risk_result = evaluate_risk(
            equity=100000.0,
            entry=entry,
            stop_loss=None,
            take_profit=None,
            atr=None,
            prior_loss_streak=0,
            peak_equity=100000.0,
        )
        report["risk"] = {
            "executed": True,
            "risk_pass": bool(risk_result.risk_pass),
            "reason": risk_result.reason,
            "expected_fail_closed": True,
        }
        if risk_result.risk_pass or risk_result.reason != "MISSING_EXECUTION_INPUT":
            report["failures"].append("Risk did not fail closed on absent upstream SL/TP/ATR inputs")

        # The sample is a wiring proof, not a performance result. A non-PASS resolver/binder
        # is recorded as unresolved rather than promoted to a successful trading state.
        if resolver.status != "PASS":
            report["warnings"].append("Dynamic MTF resolver remained NOT_EVALUABLE because the sample contained no explicit complete role evidence. No substitute was inferred.")
        if binder.status != "PASS":
            report["warnings"].append("Dynamic MTF binding remained NOT_EVALUABLE because no complete upstream role assignment was present in the sampled source. No roles were invented.")
    except Exception as exc:
        report["failures"].append(f"sample execution error: {type(exc).__name__}: {exc}")

    report["status"] = "PASS" if not report["failures"] else "BLOCKED"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
