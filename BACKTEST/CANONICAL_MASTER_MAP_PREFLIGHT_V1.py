from __future__ import annotations

"""Cheap canonical integration preflight.

This intentionally performs no backtest and no large data load. It protects
CircleCI credits by failing fast when the runtime graph is not actually wired.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "decision_brain": ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "handoff": ROOT / "compatibility/knowledge_decision_handoff.py",
    "rule_adapter": ROOT / "ADAPTERS/rule_adapter_execution_bridge_v1.py",
    "tiz": ROOT / "RUNTIME/TIZ_PROCESS_GATE_V1/tiz_process_gate_v1.py",
    "risk": ROOT / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py",
    "murphy_registry": ROOT / "PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json",
    "integration_plan": ROOT / "BACKTEST/CANONICAL_E2E_INTEGRATION_PLAN_2026-08-28.md",
    "master_map_audit": ROOT / "BACKTEST/CANONICAL_MASTER_MAP_COMPATIBILITY_AUDIT_2026-08-28.md",
}


def main() -> int:
    missing = [k for k, p in REQUIRED.items() if not p.exists()]
    registry = {}
    registry_path = REQUIRED["murphy_registry"]
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))

    failures: list[str] = []
    if missing:
        failures.append("missing runtime controls: " + ", ".join(missing))

    rules = registry.get("rules", {})
    if len(rules) != 34:
        failures.append(f"runtime Murphy scope expected 34, observed {len(rules)}")

    if not (ROOT / "PROJECT_INDEX/DO_NOT_TOUCH.md").exists():
        failures.append("protected governance control missing")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "preflight": "CANONICAL_MASTER_MAP_RUNTIME_PREFLIGHT_V1",
        "required_controls": {k: p.exists() for k, p in REQUIRED.items()},
        "murphy_runtime_scope": len(rules),
        "decision_brain_untouched_by_this_preflight": True,
        "2025_locked": True,
        "full_backtest_executed": False,
        "failures": failures,
    }
    out = ROOT / "artifacts/canonical_preflight"
    out.mkdir(parents=True, exist_ok=True)
    (out / "CANONICAL_MASTER_MAP_PREFLIGHT_V1.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
