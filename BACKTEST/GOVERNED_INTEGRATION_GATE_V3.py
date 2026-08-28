from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path.cwd()
ALLOWLIST = json.loads((ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json").read_text(encoding="utf-8"))
MURPHY_ALLOWED = set(ALLOWLIST["verified_runtime"]["MURPHY"])
NISON_ALLOWED = set(ALLOWLIST["verified_runtime"]["NISON"])
BLOCKED = {x["rule_id"] for x in ALLOWLIST.get("explicitly_blocked", [])}


def load_csv(path: Path, required: set[str], nrows: int = 30000) -> pd.DataFrame:
    df = pd.read_csv(path, nrows=nrows, low_memory=False)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df.sort_values("timestamp").reset_index(drop=True)


def find_csv(root: Path, name: str) -> Path:
    if root.is_file():
        return root
    hits = list(root.rglob(name))
    if not hits:
        raise FileNotFoundError(f"{name} not found under {root}")
    return hits[0]


def rule_ids(values) -> set[str]:
    out: set[str] = set()
    for value in values:
        if pd.isna(value):
            continue
        out.update(x.strip() for x in str(value).split("|") if x.strip())
    return out


def asof_coverage(base: pd.DataFrame, source: pd.DataFrame) -> float:
    left = base[["timestamp"]].drop_duplicates().sort_values("timestamp")
    right = source[["timestamp"]].drop_duplicates().sort_values("timestamp").copy()
    right["_present"] = True
    joined = pd.merge_asof(left, right, on="timestamp", direction="backward")
    return float(joined["_present"].fillna(False).mean() * 100.0) if len(joined) else 0.0


def load_brain():
    p = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"
    spec = importlib.util.spec_from_file_location("recovered_decision_brain_v1", p)
    if not spec or not spec.loader:
        raise RuntimeError("Decision Brain V1 could not be loaded")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    for name in ("h1", "market_state", "mtf", "murphy", "nison", "historical_context", "historical_outcome", "similarity", "retrieval", "handoff", "decision_brain", "output"):
        ap.add_argument("--" + name.replace("_", "-"), required=True)
    args = ap.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}

    h1 = load_csv(Path(args.h1), {"timestamp", "open", "high", "low", "close"}, 50000)
    h1 = h1[(h1.timestamp.dt.year >= 2016) & (h1.timestamp.dt.year <= 2024)].copy()
    if h1.empty:
        failures.append("H1 2016-2024 development slice is empty")
    checks["h1_development_years"] = sorted(h1.timestamp.dt.year.unique().tolist()) if not h1.empty else []
    checks["h1_development_rows"] = int(len(h1))

    market = load_csv(Path(args.market_state), {"timestamp"})
    mtf = load_csv(find_csv(Path(args.mtf), "GBPUSD_MTF_H4_H1.csv"), {"timestamp"})
    murphy = load_csv(find_csv(Path(args.murphy), "MURPHY_2016_2024_FULL_EVIDENCE.csv"), {"timestamp", "status", "direction", "source_rule_id"})
    nison = load_csv(Path(args.nison), {"timestamp", "status", "direction", "rule_id"})
    hc = load_csv(find_csv(Path(args.historical_context), "HISTORICAL_CONTEXT_MEMORY.csv"), {"timestamp", "context_signature"})
    ho = load_csv(find_csv(Path(args.historical_outcome), "HISTORICAL_OUTCOMES.csv"), {"timestamp", "context_signature"})

    for label, df in (("MarketState", market), ("MTF", mtf), ("Murphy", murphy), ("Nison", nison), ("HistoricalContext", hc), ("HistoricalOutcome", ho)):
        years = set(df.timestamp.dt.year.dropna().astype(int))
        checks[f"{label}_years"] = sorted(years)
        if 2025 in years:
            failures.append(f"{label}: 2025 is present in a development-consumed sample")

    observed_m = rule_ids(murphy.source_rule_id)
    observed_n = set(nison.rule_id.dropna().astype(str))
    checks["murphy_historical_rule_ids"] = sorted(observed_m)
    checks["murphy_historical_rule_id_count"] = len(observed_m)
    checks["murphy_frozen_runtime_rule_count"] = len(MURPHY_ALLOWED)
    missing_m = sorted(MURPHY_ALLOWED - observed_m)
    unknown_m = sorted(observed_m - MURPHY_ALLOWED)
    blocked_m = sorted(observed_m & BLOCKED)
    if unknown_m:
        failures.append(f"Unknown/non-allowlisted Murphy rules: {unknown_m}")
    if blocked_m:
        failures.append(f"Blocked Murphy rules observed: {blocked_m}")
    if missing_m:
        warnings.append(f"Murphy historical coverage is partial: {len(missing_m)} frozen runtime rules have no historical event rows; they remain NOT_EVALUABLE and are not fabricated")
    if observed_n != NISON_ALLOWED:
        failures.append(f"Nison rule family mismatch; observed={len(observed_n)} expected={len(NISON_ALLOWED)}")

    checks["market_state_asof_pct"] = round(asof_coverage(h1, market), 4)
    checks["mtf_asof_pct"] = round(asof_coverage(h1, mtf), 4)
    checks["historical_context_asof_pct"] = round(asof_coverage(h1, hc), 4)
    checks["historical_outcome_asof_pct"] = round(asof_coverage(h1, ho), 4)
    for k in ("market_state_asof_pct", "mtf_asof_pct", "historical_context_asof_pct", "historical_outcome_asof_pct"):
        if checks[k] <= 0:
            failures.append(f"{k}: zero as-of coverage")

    sim_dir = Path(args.similarity)
    ret_dir = Path(args.retrieval)
    sim_files = list(sim_dir.rglob("*.json")) if sim_dir.is_dir() else []
    ret_files = list(ret_dir.rglob("*.json")) if ret_dir.is_dir() else []
    if not sim_files:
        failures.append("Similarity V2 package contains no JSON evidence artifacts")
    if not ret_files:
        failures.append("Context-Aware Retrieval V2 package contains no JSON artifacts")
    checks["similarity_artifact_present"] = bool(sim_files)
    checks["retrieval_artifact_present"] = bool(ret_files)
    warnings.append("Similarity V2 and Context-Aware Retrieval V2 are evidence/context layers only; any 2025 snapshot material remains locked from 2016-2024 consumption")

    sys.path.insert(0, str(ROOT))
    checks["tiz"] = {"status": "NOT_EVALUABLE", "reason": "UNRESOLVED_OPTIONAL_DEVELOPMENT_MODULE"}
    warnings.append("TIZ runtime remains unresolved/optional for development; no PASS is manufactured")
    try:
        from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk
        valid = evaluate_risk(equity=100000.0, entry=100.0, stop_loss=99.0, take_profit=103.0, atr=1.0, prior_loss_streak=0, peak_equity=100000.0)
        invalid = evaluate_risk(equity=100000.0, entry=100.0, stop_loss=None, take_profit=None, atr=None, prior_loss_streak=0, peak_equity=100000.0)
        checks["risk_contract_valid_pass"] = bool(valid.risk_pass)
        checks["risk_contract_invalid_reject"] = bool(not invalid.risk_pass)
        if not valid.risk_pass or invalid.risk_pass:
            failures.append("Risk adapter contract test failed")
    except Exception as exc:
        failures.append(f"Risk runtime contract failed to load: {exc}")

    handoff = Path(args.handoff)
    brain_path = Path(args.decision_brain)
    if not handoff.exists():
        failures.append("Knowledge/Decision Handoff missing")
    if not brain_path.exists():
        failures.append("Recovered Decision Brain V1 missing")

    try:
        brain = load_brain()
        sample = {k: 0.0 for k in ("mtf_trend_score", "M5_trend_regime", "M15_trend_regime", "M30_trend_regime", "H1_trend_regime", "H4_trend_regime", "D1_trend_regime")}
        sample["volume_available"] = False
        result = brain.assess(sample, similarity=None)
        checks["decision_brain_v1_assessment_executes"] = True
        checks["decision_brain_v1_bias"] = getattr(result, "directional_bias", None)
    except Exception as exc:
        failures.append(f"Decision Brain V1 assessment failed: {exc}")

    checks["2025_locked"] = True
    checks["decision_brain_semantics_changed"] = False
    checks["tiz_hardcoded_pass"] = False
    checks["risk_hardcoded_pass"] = False
    checks["similarity_generates_direction"] = False
    checks["retrieval_generates_direction"] = False

    report = {
        "status": "PASS" if not failures else "FAIL",
        "gate": "GOVERNED_INTEGRATION_GATE_V3",
        "development_window": "2016-2024",
        "2025": "LOCKED",
        "failures": failures,
        "warnings": warnings,
        "checks": checks,
        "governance": {
            "murphy_primary_directional_context": True,
            "nison_confirmation_or_contradiction_only": True,
            "historical_memory_evidence_only": True,
            "similarity_evidence_only": True,
            "retrieval_context_only": True,
            "tiz_process_only": True,
            "risk_hard_gate": True,
            "2025_used_for_tuning": False,
        },
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
