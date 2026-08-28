from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
runner = (ROOT / "BACKTEST/CANONICAL_E2E_ORCHESTRATOR_V2.py").read_text(encoding="utf-8")
handoff = (ROOT / "compatibility/knowledge_decision_handoff.py").read_text(encoding="utf-8")
risk = (ROOT / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py").read_text(encoding="utf-8")
tiz = (ROOT / "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json").read_text(encoding="utf-8")

errors = []
checks = {
    "runner_has_no_synthetic_sl_tp_literals": all(x not in runner for x in ["0.75", "3R"]),
    "runner_does_not_hardcode_tiz_pass": "tiz_status\": \"PASS\"" not in runner and "tiz": {"status": "PASS"} not in runner,
    "runner_has_fail_closed_risk": "MISSING_UPSTREAM_SL_TP_ATR" in runner,
    "handoff_blocks_memory_direction": "direction_generated_by_memory" in handoff,
    "handoff_blocks_retrieval_direction": "direction_generated_by_retrieval" in handoff,
    "risk_requires_execution_inputs": "MISSING_EXECUTION_INPUT" in risk,
    "tiz_is_process_only": '"role": "process_only"' in tiz and '"no_direction_generation": true' in tiz,
    "runner_2016_2024_scope": 'dt.year >= 2016' in runner and 'dt.year <= 2024' in runner,
}
for name, ok in checks.items():
    if not ok:
        errors.append(name)

if errors:
    print("GOVERNED_RUNNER_STATIC_LINT=FAIL")
    for e in errors:
        print(f"FAIL {e}")
    raise SystemExit(1)

print("GOVERNED_RUNNER_STATIC_LINT=PASS")
for name in checks:
    print(f"PASS {name}")
