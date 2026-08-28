from __future__ import annotations

"""Canonical E2E integration orchestrator.

This file only orchestrates existing project components. It does not rebuild
book semantics or modify Decision Brain V1. Every upstream layer is placed in
one timestamp-bounded evidence envelope before Knowledge/Decision Handoff.
Similarity and Retrieval remain evidence/context only. TIZ remains unresolved
and optional. Risk remains a real execution gate. 2025 is excluded.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Reuse existing orchestration helpers; do not duplicate book logic.
legacy = importlib.util.spec_from_file_location(
    "legacy_orchestrator",
    ROOT / "BACKTEST/GOVERNED_E2E_ORCHESTRATOR_V1.py",
)
if not legacy or not legacy.loader:
    raise RuntimeError("Existing orchestrator helpers unavailable")
legacy_mod = importlib.util.module_from_spec(legacy)
legacy.loader.exec_module(legacy_mod)

ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"


def load_brain():
    spec = importlib.util.spec_from_file_location("recovered_decision_brain_v1", BRAIN)
    if not spec or not spec.loader:
        raise RuntimeError("Decision Brain V1 load failed")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def snapshot_status(root: Path, label: str) -> dict[str, Any]:
    files = [*root.rglob("*.json"), *root.rglob("*.csv")] if root.exists() else []
    return {
        "source": label,
        "status": "CONNECTED_GOVERNED_METADATA" if files else "NOT_EVALUABLE",
        "files_found": len(files),
        "direction": None,
        "final_trade_decision": None,
    }


def compact(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if k != "timestamp" and pd.notna(v)}


def run(a) -> None:
    read = legacy_mod.read
    asof = legacy_mod.asof
    split_ids = legacy_mod.split_ids
    aggregate_murphy = legacy_mod.aggregate_murphy
    aggregate_nison = legacy_mod.aggregate_nison
    build_brain_row = legacy_mod.build_brain_row
    allowlist = legacy_mod.allowlist

    bars = read(a.h1, {"timestamp", "open", "high", "low", "close"})
    bars = bars[(bars.timestamp.dt.year >= 2016) & (bars.timestamp.dt.year <= 2024)].reset_index(drop=True)
    market = read(a.market, {"timestamp"})
    mtf = read(a.mtf, {"timestamp"})
    murphy_raw = read(a.murphy, {"timestamp", "status", "direction", "source_rule_id"})
    nison_raw = read(a.nison, {"timestamp", "status", "direction", "rule_id"}, chunksize=400000)
    hc = read(a.historical_context, {"timestamp", "context_signature"})
    ho = read(a.historical_outcome, {"timestamp", "context_signature"})

    if "pair" in hc.columns:
        hc = hc[hc.pair.astype(str).str.upper().eq("GBPUSD")]
    if "pair" in ho.columns:
        ho = ho[ho.pair.astype(str).str.upper().eq("GBPUSD")]
    hc = hc[hc.timestamp.dt.year <= 2024].reset_index(drop=True)
    ho = ho[ho.timestamp.dt.year <= 2024].reset_index(drop=True)

    allowed_m, allowed_n = allowlist()
    actual_m = split_ids(murphy_raw.source_rule_id)
    actual_n = set(nison_raw.rule_id.dropna().astype(str))
    if not actual_m.issubset(allowed_m):
        raise ValueError(f"Unknown Murphy rule id(s): {sorted(actual_m - allowed_m)}")
    if not actual_n.issubset(allowed_n):
        raise ValueError(f"Unknown Nison rule id(s): {sorted(actual_n - allowed_n)}")

    murphy = aggregate_murphy(murphy_raw)
    nison = aggregate_nison(nison_raw)
    base = bars[["timestamp", "close"]].copy()
    p_market = asof(base, market)
    p_mtf = asof(base, mtf)
    p_murphy = asof(base, murphy)
    p_nison = asof(base, nison)
    p_hc = asof(base, hc[["timestamp", "context_signature"]])
    p_ho = asof(base, ho[["timestamp", "context_signature"]])

    brain = load_brain()
    from compatibility.knowledge_decision_handoff import build_handoff
    from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk

    sim_meta = snapshot_status(a.similarity, "Similarity V2")
    ret_meta = snapshot_status(a.retrieval, "Context-Aware Retrieval V2")

    events: list[dict[str, Any]] = []
    eligible: list[dict[str, Any]] = []

    for i, bar in bars.iterrows():
        ts = bar.timestamp
        mr = compact(p_market.iloc[i].to_dict())
        xr = compact(p_mtf.iloc[i].to_dict())
        mu = p_murphy.iloc[i].to_dict()
        ni = p_nison.iloc[i].to_dict()
        hc_row = compact(p_hc.iloc[i].to_dict())
        ho_row = compact(p_ho.iloc[i].to_dict())

        murphy_direction = mu.get("murphy_direction")
        nison_contradiction = bool(ni.get("nison_contradiction", False))
        nison_confirmation = str(ni.get("nison_confirmation") or "ABSENT")
        brain_row = build_brain_row(mr, xr)

        # Candidate execution direction comes only from Murphy. Risk cannot create direction.
        candidate_direction = "BUY" if murphy_direction == "BULLISH" else ("SELL" if murphy_direction == "BEARISH" else None)
        atr = xr.get("atr")
        risk_status, risk_reason = "NOT_EVALUABLE", "MISSING_CANDIDATE_OR_ATR"
        sl = tp = None
        risk_payload: dict[str, Any] = {"status": "NOT_EVALUABLE", "direction": None, "final_trade_decision": None}
        if candidate_direction and pd.notna(atr) and float(atr) > 0:
            entry = float(bar.close)
            stop_dist = 0.75 * float(atr)
            target_dist = 3.0 * stop_dist
            sl, tp = ((entry - stop_dist, entry + target_dist) if candidate_direction == "BUY" else (entry + stop_dist, entry - target_dist))
            rr = evaluate_risk(
                equity=100000.0,
                entry=entry,
                stop_loss=sl,
                take_profit=tp,
                atr=float(atr),
                prior_loss_streak=0,
                peak_equity=100000.0,
            )
            risk_status = "PASS" if rr.risk_pass else "FAIL"
            risk_reason = rr.reason
            risk_payload = {
                "status": risk_status,
                "reason": risk_reason,
                "risk_percent": rr.risk_percent,
                "rr": rr.rr,
                "position_size": rr.position_size,
                "direction": None,
                "final_trade_decision": None,
            }

        alignment_state = "NISON_CONTRADICTION" if nison_contradiction else (
            "ALIGNED" if candidate_direction else "NEEDS_REVIEW"
        )
        evidence_envelope = {
            "h1": {"timestamp": ts, "close": float(bar.close)},
            "market_state": mr,
            "mtf": xr,
            "murphy": {
                "direction": murphy_direction,
                "rule_count": int(mu.get("murphy_rule_count", 0) or 0),
                "rule_ids": json.loads(mu.get("murphy_rule_ids", "[]")) if mu.get("murphy_rule_ids") else [],
            },
            "nison": {
                "confirmation": nison_confirmation,
                "contradiction": nison_contradiction,
                "rule_count": int(ni.get("nison_rule_count", 0) or 0),
                "direction_generated": False,
            },
            "historical_context": {**hc_row, "direction": None, "final_trade_decision": None},
            "historical_outcome": {**ho_row, "direction": None, "final_trade_decision": None},
            "similarity": sim_meta,
            "context_aware_retrieval": ret_meta,
            "tiz": {"status": "UNRESOLVED_OPTIONAL", "direction": None, "final_trade_decision": None},
            "risk": risk_payload,
        }

        # The Handoff is the single boundary carrying all evidence to Brain V1.
        handoff = build_handoff(
            brain_row,
            {
                "alignment_state": alignment_state,
                "candidate_direction": str(candidate_direction or "neutral").lower(),
                "contradiction_gate": "FAIL" if nison_contradiction else "PASS",
                "process_gate": "NOT_EVALUABLE",
                "book_evidence_status": "CONNECTED",
                "market_evidence_status": "CONNECTED",
                "similarity_record_count": 0,
                "evidence_bundle": evidence_envelope,
            },
            similarity=sim_meta,
        )

        # Decision Brain receives only its canonical row. Memory/retrieval are evidence-only.
        assessment = brain.assess(handoff["decision_brain_row"], similarity=None)
        brain_direction = assessment.directional_bias
        final_direction_ready = (
            candidate_direction is not None
            and brain_direction == murphy_direction.lower()
            and not nison_contradiction
            and risk_status == "PASS"
        )

        events.append({
            "timestamp": ts,
            "murphy_direction": murphy_direction,
            "nison_confirmation": nison_confirmation,
            "nison_contradiction": nison_contradiction,
            "historical_context_asof": bool(hc_row.get("context_signature")),
            "historical_outcome_asof": bool(ho_row.get("context_signature")),
            "similarity_status": sim_meta["status"],
            "retrieval_status": ret_meta["status"],
            "tiz_status": "UNRESOLVED_OPTIONAL",
            "risk_status": risk_status,
            "risk_reason": risk_reason,
            "handoff_routing": handoff["routing"],
            "handoff_abstain": handoff["gates"]["abstain"],
            "brain_bias": brain_direction,
            "brain_confidence": assessment.confidence,
            "candidate_direction": candidate_direction,
            "final_direction_ready": final_direction_ready,
            "evidence_layers_present": len(evidence_envelope),
        })
        if final_direction_ready:
            eligible.append({"timestamp": ts, "direction": candidate_direction, "entry_price": float(bar.close), "stop_loss": sl, "take_profit": tp, "risk_status": risk_status})
        if (i + 1) % 5000 == 0:
            print(f"E2E_PROGRESS events={i+1}/{len(bars)} as_of={ts.isoformat()}", flush=True)

    out = a.output_dir
    out.mkdir(parents=True, exist_ok=True)
    events_df = pd.DataFrame(events)
    eligible_df = pd.DataFrame(eligible)
    events_df.to_csv(out / "unified_78_events_2016_2024.csv", index=False)
    events_df.to_csv(out / "decision_events_2016_2024.csv", index=False)
    eligible_df.to_csv(out / "risk_eligible_events_2016_2024.csv", index=False)

    manifest = {
        "status": "E2E_INTEGRATION_EXECUTED",
        "window": "2016-2024",
        "2025": "LOCKED",
        "murphy_runtime_allowlist": len(allowed_m),
        "murphy_observed_ids": len(actual_m),
        "nison_runtime_allowlist": len(allowed_n),
        "nison_observed_ids": len(actual_n),
        "evidence_path": ["H1", "MarketState", "MTF", "Murphy34", "Nison44", "HistoricalContext", "HistoricalOutcome", "SimilarityV2", "ContextAwareRetrievalV2", "TIZ", "RiskExecution", "KnowledgeDecisionHandoff", "DecisionBrainV1"],
        "similarity_direction_source": False,
        "retrieval_direction_source": False,
        "tiz_status": "UNRESOLVED_OPTIONAL",
        "risk_hard_gate": True,
        "decision_brain_v1_unchanged": True,
    }
    (out / "integration_manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser()
    for name in ["h1", "market", "mtf", "murphy", "nison", "historical-context", "historical-outcome", "similarity", "retrieval", "output-dir"]:
        ap.add_argument("--" + name, type=Path, required=True)
    run(ap.parse_args())


if __name__ == "__main__":
    main()
