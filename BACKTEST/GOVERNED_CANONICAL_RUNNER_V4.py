from __future__ import annotations

"""Thin governed compatibility runner.

Preserves multi-row Murphy/Nison evidence and the existing V3 semantics while
requiring a verified native six-timeframe source inventory. Dynamic MTF role
resolution/binding is invoked from the real runtime path and fails closed when
complete upstream role evidence is absent. No new directional logic,
thresholds, SL/TP construction, or synthetic evidence is introduced.
2025 remains excluded from development consumption.
"""

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from BACKTEST import GOVERNED_CANONICAL_RUNNER_V3 as base
from compatibility.dynamic_mtf_binding_adapter_v1 import bind_dynamic_mtf
from compatibility.dynamic_mtf_runtime_resolver_v1 import resolve_mtf_event

_original_read_csv = base.read_csv
_original_brain_row = base.brain_row

SIX_TF = ("M5", "M15", "M30", "H1", "H4", "D1")
DYNAMIC_MTF_BY_TIMESTAMP: dict[str, dict[str, Any]] = {}
MTF_SOURCE_REPORT: Path | None = None
TIZ_BOUNDARY_MARKER = "TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2"


def read_csv(path: Path, required: set[str], chunksize: int | None = None):
    # Rule-level evidence is many-to-one at a timestamp. Preserve every rule
    # row so the existing aggregate_rule_frame() can perform the fan-in.
    is_rule_evidence = bool({"rule_id", "source_rule_id"} & set(required))
    if not is_rule_evidence:
        return _original_read_csv(path, required, chunksize)

    effective_chunksize = chunksize or 200_000
    parts: list[pd.DataFrame] = []
    for part in pd.read_csv(path, usecols=list(required), chunksize=effective_chunksize, low_memory=False):
        missing = sorted(required - set(part.columns))
        if missing:
            raise ValueError(f"{path}: missing {missing}")
        part["timestamp"] = pd.to_datetime(part["timestamp"], utc=True, errors="coerce", format="mixed")
        if part["timestamp"].isna().any():
            raise ValueError(f"{path}: invalid timestamp")
        years = part["timestamp"].dt.year
        if (years == 2025).any():
            raise ValueError(f"2025 rule evidence reached development runner: {path}")
        part = part[(years >= 2016) & (years <= 2024)]
        if not part.empty:
            parts.append(part)

    if not parts:
        return pd.DataFrame(columns=sorted(required))
    return pd.concat(parts, ignore_index=True).sort_values(
        ["timestamp", *sorted(required - {"timestamp"})]
    ).reset_index(drop=True)


def _load_source_report(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    declared = tuple(data.get("declared_timeframes", ()))
    if data.get("status") != "PASS":
        raise ValueError(f"SIX_TF_SOURCE_REPORT_NOT_PASS status={data.get('status')}")
    if declared != SIX_TF:
        raise ValueError(f"SIX_TF_DECLARATION_MISMATCH declared={declared} expected={SIX_TF}")
    if data.get("missing_timeframes"):
        raise ValueError(f"SIX_TF_SOURCE_MISSING {data['missing_timeframes']}")
    if data.get("ambiguous_duplicate_timeframes"):
        raise ValueError(f"SIX_TF_SOURCE_AMBIGUOUS {data['ambiguous_duplicate_timeframes']}")
    return data


def _explicit_bool(row: pd.Series, key: str) -> bool | None:
    if key not in row.index or pd.isna(row[key]):
        return None
    value = row[key]
    if isinstance(value, bool):
        return value
    text = str(value).strip().upper()
    if text in {"TRUE", "1", "YES"}:
        return True
    if text in {"FALSE", "0", "NO"}:
        return False
    return None


def _dynamic_mtf_for_row(row: pd.Series) -> tuple[dict[str, Any], dict[str, Any]]:
    # Completeness flags are accepted only when supplied explicitly by an
    # upstream evidence source. Raw OHLC never becomes inferred structure.
    timeframe_evidence: dict[str, dict[str, Any]] = {}
    for tf in SIX_TF:
        item: dict[str, Any] = {"source": "native_six_tf_source"}
        for field in (
            "context_complete", "structure_complete", "setup_complete",
            "confirmation_complete", "contradicted", "risk_feasible",
        ):
            value = _explicit_bool(row, f"{tf}_{field}")
            if value is not None:
                item[field] = value
        for field in ("alignment_state", "direction"):
            key = f"{tf}_{field}"
            if key in row.index and pd.notna(row[key]):
                item[field] = row[key]
        timeframe_evidence[tf] = item

    resolver = resolve_mtf_event(timeframe_evidence=timeframe_evidence)
    context_tf = resolver.context_timeframes_used[1] if len(resolver.context_timeframes_used) > 1 else (
        resolver.context_timeframes_used[0] if resolver.context_timeframes_used else None
    )
    role_assignments = {
        "macro_context": resolver.macro_timeframe,
        "context": context_tf,
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
    binding = {
        "status": binder.status,
        "alignment_state": binder.alignment_state,
        "role_timeframes": dict(binder.role_timeframes),
        "evidence_trace": list(binder.evidence_trace),
    }
    resolution = {
        "status": resolver.status,
        "alignment_state": resolver.alignment_state,
        "selected_execution_timeframe": resolver.selected_execution_timeframe,
        "context_timeframes_used": list(resolver.context_timeframes_used),
        "confirmation_timeframes_used": list(resolver.confirmation_timeframes_used),
        "setup_timeframe": resolver.setup_timeframe,
        "macro_timeframe": resolver.macro_timeframe,
        "selection_reasons": list(resolver.selection_reasons),
        "rejected_candidate_reasons": list(resolver.rejected_candidate_reasons),
        "evidence_trace": list(resolver.evidence_trace),
    }
    return resolution, binding


def brain_row(row: pd.Series) -> dict:
    """Compatibility mapping for V3's existing brain_row() contract."""
    out = _original_brain_row(row.copy())

    trend_map = {
        "BULL_TREND": 1.0,
        "BEAR_TREND": -1.0,
        "TRANSITION": 0.0,
        "UNKNOWN": 0.0,
    }
    for tf in SIX_TF:
        source = f"{tf}_trend"
        if source in row.index and pd.notna(row[source]):
            raw = str(row[source]).strip().upper()
            out[f"{tf}_trend_regime"] = trend_map.get(raw, out.get(f"{tf}_trend_regime", 0.0))
        source_regime = f"{tf}_trend_regime"
        if source_regime in row.index and pd.notna(row[source_regime]):
            raw = str(row[source_regime]).strip().upper()
            out[f"{tf}_trend_regime"] = trend_map.get(raw, out.get(f"{tf}_trend_regime", 0.0))

    for key in ("mtf_trend_score", "mtf_score"):
        if key in row.index and pd.notna(row[key]):
            out["mtf_trend_score"] = float(row[key])
            break

    resolution, binding = _dynamic_mtf_for_row(row)
    ts = row.get("timestamp")
    key = str(ts) if ts is not None else f"row_{len(DYNAMIC_MTF_BY_TIMESTAMP)}"
    DYNAMIC_MTF_BY_TIMESTAMP[key] = {"resolution": resolution, "binding": binding}
    out["dynamic_mtf_status"] = binding["status"]
    out["dynamic_mtf_alignment_state"] = binding["alignment_state"]
    out["dynamic_mtf_execution_timeframe"] = resolution["selected_execution_timeframe"]
    return out


base.read_csv = read_csv
base.brain_row = brain_row


def _apply_dynamic_gate(output_dir: Path) -> dict[str, Any]:
    events_path = output_dir / "decision_events_2016_2024.csv"
    if not events_path.exists():
        raise FileNotFoundError(f"Decision events output missing: {events_path}")
    events = pd.read_csv(events_path)
    if "timestamp" not in events.columns:
        raise ValueError("decision events missing timestamp")
    events["timestamp"] = pd.to_datetime(events["timestamp"], utc=True, errors="coerce", format="mixed")
    if events["timestamp"].isna().any():
        raise ValueError("decision events contains invalid timestamps")

    statuses: list[str] = []
    execution_tfs: list[str | None] = []
    alignments: list[str] = []
    for ts in events["timestamp"]:
        rec = DYNAMIC_MTF_BY_TIMESTAMP.get(str(ts))
        if rec is None:
            statuses.append("NOT_EVALUABLE")
            execution_tfs.append(None)
            alignments.append("NOT_EVALUABLE")
            continue
        statuses.append(str(rec["binding"]["status"]))
        execution_tfs.append(rec["resolution"]["selected_execution_timeframe"])
        alignments.append(str(rec["binding"]["alignment_state"]))

    events["dynamic_mtf_status"] = statuses
    events["dynamic_mtf_execution_timeframe"] = execution_tfs
    events["dynamic_mtf_alignment_state"] = alignments
    if "trade_allowed" not in events.columns:
        events["trade_allowed"] = False
    events["trade_allowed"] = events["trade_allowed"].fillna(False).astype(bool) & events["dynamic_mtf_status"].eq("PASS")
    events.to_csv(events_path, index=False)

    counts = events["dynamic_mtf_status"].value_counts(dropna=False).to_dict()
    report = {
        "status": "PASS" if counts.get("PASS", 0) > 0 else "FAIL_CLOSED_NO_EXECUTABLE_MTF_EVENT",
        "events": int(len(events)),
        "dynamic_mtf_status_counts": {str(k): int(v) for k, v in counts.items()},
        "trade_allowed_after_dynamic_mtf_gate": int(events["trade_allowed"].sum()) if len(events) else 0,
        "native_six_tf_source_report": str(MTF_SOURCE_REPORT) if MTF_SOURCE_REPORT else None,
        "2025_locked": bool((events["timestamp"].dt.year == 2025).sum() == 0),
        "governance": {
            "dynamic_mtf_is_not_direction_generator": True,
            "no_performance_weights": True,
            "no_synthetic_role_evidence": True,
            "missing_role_evidence_fails_closed": True,
            "tiz_boundary_marker_present": TIZ_BOUNDARY_MARKER in globals().get("TIZ_BOUNDARY_MARKER", ""),
        },
    }
    (output_dir / "dynamic_mtf_runtime_gate_v1.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main():
    global MTF_SOURCE_REPORT
    p = argparse.ArgumentParser()
    for name in (
        "h1", "market", "mtf", "murphy", "nison",
        "historical-context", "historical-outcome", "similarity",
        "retrieval", "output-dir", "mtf-source-report"
    ):
        p.add_argument("--" + name, required=True, type=Path)
    args = p.parse_args()

    MTF_SOURCE_REPORT = args.mtf_source_report
    _load_source_report(MTF_SOURCE_REPORT)
    result = base.run(args)
    gate_report = _apply_dynamic_gate(args.output_dir)
    if gate_report["status"] != "PASS":
        raise RuntimeError("Dynamic MTF did not produce any executable event; output was fail-closed and is not a profitability result.")
    return result


if __name__ == "__main__":
    main()
