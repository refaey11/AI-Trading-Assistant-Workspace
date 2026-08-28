from __future__ import annotations

"""Cheap, deterministic preflight for the governed E2E path.

This intentionally does not run the full backtest. It checks source wiring and
forbidden shortcuts before a manual governed run is allowed.
"""

import argparse
import json
from pathlib import Path


def require(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"MISSING_{label}: {path}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("."))
    args = p.parse_args()
    root = args.root.resolve()

    required = {
        "ORCHESTRATOR": root / "BACKTEST/CANONICAL_E2E_ORCHESTRATOR_V2.py",
        "HANDOFF": root / "compatibility/knowledge_decision_handoff.py",
        "BRAIN": root / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
        "RISK": root / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py",
        "TIZ_BOUNDARY": root / "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json",
        "ALLOWLIST": root / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json",
    }
    for label, path in required.items():
        require(path, label)

    orchestrator = required["ORCHESTRATOR"].read_text(encoding="utf-8")
    handoff = required["HANDOFF"].read_text(encoding="utf-8")
    risk = required["RISK"].read_text(encoding="utf-8")
    tiz = json.loads(required["TIZ_BOUNDARY"].read_text(encoding="utf-8"))

    forbidden = {
        "hardcoded_tiz_pass": "tiz=\"PASS\"" in orchestrator.replace(" ", "").lower(),
        "hardcoded_risk_pass": "risk_status=\"pass\"" in orchestrator.replace(" ", "").lower(),
        "synthetic_sl_tp_comment": "synthetic sl/tp" in orchestrator.lower(),
    }
    if any(forbidden.values()):
        raise SystemExit(f"FORBIDDEN_SHORTCUT_FOUND: {forbidden}")

    checks = {
        "2025_filter_present": "<= 2024" in orchestrator or "<=2024" in orchestrator,
        "memory_direction_block": "direction_generated_by_memory" in handoff,
        "retrieval_direction_block": "direction_generated_by_retrieval" in handoff,
        "risk_requires_upstream_execution": "MISSING_EXECUTION_INPUT" in risk,
        "tiz_no_direction": bool(tiz.get("producer_rules", {}).get("no_direction_generation")),
        "tiz_missing_process_not_evaluable": tiz.get("producer_rules", {}).get("missing_process_evidence") == "NOT_EVALUABLE",
    }

    # This smoke is only a wiring/contract guard; it must not be used as a
    # profitability or integration PASS by itself.
    status = "PASS" if all(checks.values()) and not any(forbidden.values()) else "FAIL"
    print(json.dumps({"status": status, "checks": checks, "forbidden": forbidden}, indent=2))
    if status != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
