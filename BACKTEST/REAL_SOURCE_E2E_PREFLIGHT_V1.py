from __future__ import annotations

"""Deterministic preflight for the real-source Decision Brain path.

This gate is validation-only. It never creates evidence, directions, SL/TP,
trades, or tuning parameters. It exists to stop an incomplete/shadow runner
from being mistaken for a valid end-to-end backtest.
"""

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SIX_TF = ("M5", "M15", "M30", "H1", "H4", "D1")
ROLE_ORDER = ("macro_context", "context", "setup", "confirmation", "execution")


def read_columns(path: Path) -> set[str]:
    return set(pd.read_csv(path, nrows=0).columns)


def scan_years(path: Path, timestamp_col: str = "timestamp") -> tuple[bool, list[int]]:
    years: set[int] = set()
    found = False
    for chunk in pd.read_csv(path, usecols=[timestamp_col], chunksize=200_000, low_memory=False):
        found = True
        ts = pd.to_datetime(chunk[timestamp_col], utc=True, errors="coerce", format="mixed")
        if ts.isna().any():
            raise ValueError(f"{path}: invalid timestamp")
        years.update(int(x) for x in ts.dt.year.unique())
    return found, sorted(years)


def infer_timeframes(root: Path) -> set[str]:
    found: set[str] = set()
    if not root.exists():
        return found
    pattern = re.compile(r"(?<![A-Z0-9])(D1|H4|H1|M30|M15|M5)(?![A-Z0-9])", re.I)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        match_text = f"{path.name} {path.parent.name}".upper()
        found.update(m.upper() for m in pattern.findall(match_text))
    return found


def ast_has_call(tree: ast.AST, function_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == function_name:
                return True
            if isinstance(node.func, ast.Attribute) and node.func.attr == function_name:
                return True
    return False


def ast_defines(tree: ast.AST, function_name: str) -> bool:
    return any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function_name for n in ast.walk(tree))


def static_runner_checks(runner: Path) -> dict[str, Any]:
    source = runner.read_text(encoding="utf-8")
    tree = ast.parse(source)
    return {
        "runner_compiles": True,
        "uses_dynamic_mtf_binding_adapter": "dynamic_mtf_binding_adapter_v1" in source,
        "calls_bind_dynamic_mtf": ast_has_call(tree, "bind_dynamic_mtf"),
        "defines_local_execution_plan": ast_defines(tree, "execution_plan"),
        "passes_similarity_as_real_evidence": "similarity=None" not in source,
        "uses_tiz_boundary_module": "TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2" in source or "tiz_process_gate" in source,
        "writes_executed_trades": "executed_trades_2016_2024.csv" in source,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", type=Path, required=True)
    p.add_argument("--mtf-full-dir", type=Path, required=False)
    p.add_argument("--runner", type=Path, default=ROOT / "BACKTEST/GOVERNED_CANONICAL_RUNNER_V4.py")
    p.add_argument("--brain", type=Path, default=ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py")
    p.add_argument("--tiz-boundary", type=Path, default=ROOT / "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json")
    p.add_argument("--risk", type=Path, default=ROOT / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py")
    p.add_argument("--report", type=Path, default=Path("artifacts/real_source_e2e_preflight_v1.json"))
    args = p.parse_args()

    report: dict[str, Any] = {"status": "PASS", "hard_blockers": [], "warnings": []}

    # Development scope / OOS lock.
    _, h1_years = scan_years(args.h1)
    report["h1_years"] = h1_years
    if any(y == 2025 for y in h1_years):
        report["hard_blockers"].append("2025_PRESENT_IN_DEVELOPMENT_H1")
    if not set(h1_years).intersection(range(2016, 2025)):
        report["hard_blockers"].append("NO_2016_2024_H1_DATA")

    # Six-timeframe source availability is validated separately from role selection.
    if args.mtf_full_dir:
        tf_found = infer_timeframes(args.mtf_full_dir)
        report["six_timeframes_declared"] = list(SIX_TF)
        report["six_timeframes_in_source_paths"] = sorted(tf_found)
        if not set(SIX_TF).issubset(tf_found):
            report["hard_blockers"].append("SIX_TIMEFRAME_SOURCE_NOT_PROVEN")
    else:
        report["hard_blockers"].append("NO_SIX_TIMEFRAME_SOURCE_ROOT_SUPPLIED")

    # Protected Decision Brain must expose all six timeframe fields.
    brain_source = args.brain.read_text(encoding="utf-8")
    missing_brain_fields = [f"{tf}_trend_regime" for tf in SIX_TF if f"{tf}_trend_regime" not in brain_source]
    report["brain_six_tf_fields_missing"] = missing_brain_fields
    if missing_brain_fields:
        report["hard_blockers"].append("DECISION_BRAIN_SIX_TF_INTERFACE_MISSING")

    # Authoritative TIZ boundary must exist and remain process-only.
    if not args.tiz_boundary.exists():
        report["hard_blockers"].append("TIZ_BOUNDARY_FILE_MISSING")
    else:
        tiz = json.loads(args.tiz_boundary.read_text(encoding="utf-8"))
        report["tiz_status"] = tiz.get("status")
        report["tiz_role"] = tiz.get("role")
        report["tiz_direction"] = tiz.get("direction")
        if tiz.get("status") != "AUTHORITATIVE_BOUNDARY" or tiz.get("role") != "process_only" or tiz.get("direction") != "NEUTRAL":
            report["hard_blockers"].append("TIZ_BOUNDARY_NOT_AUTHORITATIVE_PROCESS_ONLY")

    # Current Risk contract: inspect, do not rewrite.
    risk_source = args.risk.read_text(encoding="utf-8")
    rr_match = re.search(r"CURRENT_CANONICAL_MIN_RR\s*=\s*([0-9.]+)", risk_source)
    report["current_risk_min_rr"] = float(rr_match.group(1)) if rr_match else None
    if report["current_risk_min_rr"] is None:
        report["hard_blockers"].append("CURRENT_RISK_RR_CONTRACT_UNRESOLVED")

    # Static integrity of runner wiring.
    runner_checks = static_runner_checks(args.runner)
    report["runner_checks"] = runner_checks
    if not runner_checks["uses_dynamic_mtf_binding_adapter"] or not runner_checks["calls_bind_dynamic_mtf"]:
        report["hard_blockers"].append("DYNAMIC_MTF_ROLE_BINDING_NOT_CONSUMED_BY_RUNNER")
    if runner_checks["defines_local_execution_plan"]:
        report["hard_blockers"].append("RUNNER_OWNS_UNVERIFIED_EXECUTION_PLAN")
    if not runner_checks["passes_similarity_as_real_evidence"]:
        report["hard_blockers"].append("MEMORY_PASSED_AS_NONE_OR_SHADOW_ONLY")
    if not runner_checks["uses_tiz_boundary_module"]:
        report["hard_blockers"].append("TIZ_BOUNDARY_NOT_CONSUMED")
    if not runner_checks["writes_executed_trades"]:
        report["hard_blockers"].append("EXECUTED_TRADES_OUTPUT_NOT_IMPLEMENTED")

    # Never silently accept legacy H4/H1-only MTF projection as six-TF integration.
    try:
        mtf_path_candidates = list((ROOT / "BACKTEST").rglob("*GOVERNED_CANONICAL_RUNNER_V*.py"))
        legacy_projection = any("h4_trend" in f.read_text(encoding="utf-8") and "H4_trend_regime" in f.read_text(encoding="utf-8") for f in mtf_path_candidates)
    except OSError:
        legacy_projection = False
    report["legacy_h4_projection_detected"] = legacy_projection
    if legacy_projection:
        report["warnings"].append("Legacy H4/H1 projection still exists; it cannot be accepted as six-TF consumption.")

    if report["hard_blockers"]:
        report["status"] = "BLOCKED"

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
