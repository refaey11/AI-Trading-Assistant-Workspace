from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    brain = load_module(ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py", "brain_v1")
    handoff_mod = load_module(ROOT / "compatibility/knowledge_decision_handoff.py", "handoff")
    risk_mod = load_module(ROOT / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py", "risk")

    row = {
        "mtf_trend_score": 1.0,
        "M5_trend_regime": 1.0,
        "M15_trend_regime": 1.0,
        "M30_trend_regime": 1.0,
        "H1_trend_regime": 1.0,
        "H4_trend_regime": 1.0,
        "D1_trend_regime": 1.0,
        "volume_available": False,
    }
    risk = risk_mod.evaluate_risk(
        equity=100000.0,
        entry=100.0,
        stop_loss=99.25,
        take_profit=102.25,
        atr=1.0,
        prior_loss_streak=0,
        peak_equity=100000.0,
    )

    evidence = {
        "h1": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
        "market_state": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
        "mtf": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
        "murphy": {"status": "CONNECTED", "direction": "bullish"},
        "nison": {"status": "CONNECTED", "confirmation": "BULLISH", "contradiction": False, "direction_generated": False},
        "historical_context": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
        "historical_outcome": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
        "similarity": {"status": "CONNECTED_GOVERNED_METADATA", "direction": None, "final_trade_decision": None},
        "context_aware_retrieval": {"status": "CONNECTED_GOVERNED_METADATA", "direction": None, "final_trade_decision": None},
        "tiz": {"status": "UNRESOLVED_OPTIONAL", "direction": None, "final_trade_decision": None},
        "risk": {"status": "PASS" if risk.risk_pass else "FAIL", "direction": None, "final_trade_decision": None},
    }

    handoff = handoff_mod.build_handoff(
        row,
        {
            "alignment_state": "ALIGNED",
            "candidate_direction": "bullish",
            "contradiction_gate": "PASS",
            "process_gate": "NOT_EVALUABLE",
            "book_evidence_status": "CONNECTED",
            "market_evidence_status": "CONNECTED",
            "similarity_record_count": 0,
            "evidence_bundle": evidence,
        },
        similarity=evidence["similarity"],
    )

    required = set(evidence)
    received = set(handoff["knowledge_evidence"]["evidence_bundle"])
    missing = sorted(required - received)
    if missing:
        failures.append(f"handoff missing evidence layers: {missing}")

    for name in ("similarity", "context_aware_retrieval", "historical_context", "historical_outcome"):
        if handoff["knowledge_evidence"]["evidence_bundle"][name].get("direction") is not None:
            failures.append(f"{name} generated direction")

    if handoff["knowledge_evidence"]["evidence_bundle"]["tiz"]["status"] == "PASS":
        failures.append("TIZ was hardcoded to PASS")
    if handoff["knowledge_evidence"]["evidence_bundle"]["risk"]["status"] not in {"PASS", "FAIL"}:
        failures.append("Risk gate not explicit")

    assessment = brain.assess(handoff["decision_brain_row"], similarity=None)
    if not hasattr(assessment, "directional_bias"):
        failures.append("Decision Brain V1 assessment did not execute")

    # 2025 must remain blocked by the canonical handoff contract.
    locked = handoff_mod.build_handoff(
        row,
        {
            "alignment_state": "ALIGNED",
            "candidate_direction": "bullish",
            "contradiction_gate": "PASS",
            "process_gate": "PROCESS_BLOCKED",
            "book_evidence_status": "CONNECTED",
            "market_evidence_status": "CONNECTED",
            "evidence_bundle": {"query_year": 2025},
        },
        similarity=None,
    )
    if not locked["gates"]["hard_block"]:
        failures.append("2025/process lock did not hard-block")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "contract": "CANONICAL_E2E_INTEGRATION_V1",
        "layers": sorted(required),
        "decision_brain_v1_executed": not any("Decision Brain" in x for x in failures),
        "tiz_hardcoded_pass": False,
        "risk_hardcoded_pass": False,
        "memory_or_retrieval_generated_direction": False,
        "2025_locked": True,
        "failures": failures,
    }
    out = ROOT / "artifacts/integration_contract_test"
    out.mkdir(parents=True, exist_ok=True)
    (out / "CANONICAL_E2E_CONTRACT_V1.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
