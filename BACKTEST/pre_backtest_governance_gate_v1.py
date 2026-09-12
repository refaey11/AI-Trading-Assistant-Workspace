from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        FAILS.append(message)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


v54 = text(ROOT / "DEVELOPMENT_2016_2024" / "current_stack_historical_replay_v5_4.py")
v4 = text(ROOT / "DEVELOPMENT_2016_2024" / "current_stack_historical_replay_v4.py")
brain = text(ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "full_brain_runtime_bridge_v1.py")
e2e = text(ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "gate3c_single_event_e2e_v1.py")
adapter = text(ROOT / "compatibility" / "decision_brain_v1_handoff_adapter.py")
evaluator = text(ROOT / "evaluation" / "three_book_decision_evaluator_v1.py")
workflow = text(ROOT / ".github" / "workflows" / "current-stack-development-backtest-2016-2024-v5-4.yml")

# V5.4 is a versioned compatibility layer over V4, not a second strategy.
require("source = V4.read_text" in v54, "V5.4 must derive from V4 source")
require("source.replace(" in v54, "V5.4 source-rewrite compatibility layer missing")
require("BASE_RISK_PCT = 0.005" in v54, "BASE risk contract changed")
require("AFTER_TWO_LOSSES_RISK_PCT = 0.0025" in v54, "loss-streak risk contract changed")
require("MAX_RISK_PCT = 0.015" in v54, "MAX risk contract changed")
require("SL_ATR = 0.75" in v54, "SL ATR contract changed")
require("TP_R = 2.0" in v54, "TP R contract changed")
require("TP_R * stop_distance" in v54, "V5.4 2R rewrite missing")
require("if not nids:" in v54, "Nison absence compatibility rule missing")
require('"costs_applied": False' in v4, "development cost policy not explicitly false")
require('"tuning_applied": False' in v4, "development tuning policy not explicitly false")

# Canonical six-TF MTF envelope.
for field in [
    "mtf_trend_score", "M5_trend_regime", "M15_trend_regime", "M30_trend_regime",
    "H1_trend_regime", "H4_trend_regime", "D1_trend_regime",
]:
    require(field in v54, f"missing MTF field in V5.4: {field}")

# Brain boundary: recovered V1 remains untouched and auxiliary evidence is non-directional.
require("RECOVERED_SOURCES" in brain and "DECISION_BRAIN_V1" in brain, "Recovered Brain V1 path missing")
require("similarity=None" in adapter, "Similarity must not be passed as Brain direction input")
require('"predicted_return_used_as_direction": False' in adapter, "Memory predicted-return direction guard missing")
require("historical_memory_consumed_downstream" in adapter, "Historical memory governance metadata missing")
require("nison_contradiction" in evaluator and "nison_confirmation" in evaluator, "Nison must remain confirmation/contradiction evidence")
require('"tiz_execution_gate": "DISABLED"' in evaluator, "TIZ must remain audit/process-only in development evaluator")
require('"tiz_direction_generation": False' in e2e, "TIZ direction governance metadata missing from E2E")
require('"memory_direction_generation": False' in e2e, "Memory direction governance metadata missing from E2E")
require('"nison_direction_generation": False' in e2e, "Nison direction governance metadata missing from E2E")

# Risk authority and OOS lock.
require("risk_engine" in v4 or "risk_engine" in v54, "canonical risk engine not referenced")
require("2016-2024" in workflow, "workflow does not declare development window")
require("2025_OOS_LOCKED" in workflow, "2025 OOS lock missing")
require('"official_profitability_claim": False' in v4, "official profitability claim policy missing")

# Syntax sanity for integration code, including this checker itself.
for path in [
    Path(__file__),
    ROOT / "DEVELOPMENT_2016_2024" / "current_stack_historical_replay_v5_4.py",
    ROOT / "DEVELOPMENT_2016_2024" / "current_stack_historical_replay_v4.py",
    ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "full_brain_runtime_bridge_v1.py",
    ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "gate3c_single_event_e2e_v1.py",
    ROOT / "compatibility" / "decision_brain_v1_handoff_adapter.py",
    ROOT / "evaluation" / "three_book_decision_evaluator_v1.py",
]:
    try:
        ast.parse(text(path), filename=str(path))
    except SyntaxError as exc:
        FAILS.append(f"syntax error {path}: {exc}")

print(json.dumps({
    "status": "PASS" if not FAILS else "BLOCKED",
    "checks_failed": FAILS,
    "scope": "pre-backtest governance only",
    "does_not_claim_profitability": True,
    "development_window": "2016-2024",
}, indent=2))
raise SystemExit(0 if not FAILS else 1)

# Governance checker correction checkpoint.
# Synchronization checkpoint: force a fresh push-triggered validation run.
