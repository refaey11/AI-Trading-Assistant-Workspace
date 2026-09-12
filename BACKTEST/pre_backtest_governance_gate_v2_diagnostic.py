from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILS: list[str] = []

def require(ok: bool, msg: str) -> None:
    if not ok:
        FAILS.append(msg)

def read(path: str) -> str:
    p = ROOT / path
    return p.read_text(encoding="utf-8")

v54 = read("DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py")
v4 = read("DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py")
brain = read("RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py")
e2e = read("RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py")
adapter = read("compatibility/decision_brain_v1_handoff_adapter.py")
evaluator = read("evaluation/three_book_decision_evaluator_v1.py")
workflow = read(".github/workflows/current-stack-development-backtest-2016-2024-v5-4.yml")

require("source = V4.read_text" in v54, "V5.4 derivation")
require("BASE_RISK_PCT = 0.005" in v54, "base risk")
require("AFTER_TWO_LOSSES_RISK_PCT = 0.0025" in v54, "loss-streak risk")
require("MAX_RISK_PCT = 0.015" in v54, "max risk")
require("SL_ATR = 0.75" in v54, "SL ATR")
require("TP_R = 2.0" in v54, "TP R")
require("TP_R * stop_distance" in v54, "2R target")
require("if not nids:" in v54, "Nison absence policy")
require('"costs_applied": False' in v4, "cost policy")
require('"tuning_applied": False' in v4, "tuning policy")

for f in ("mtf_trend_score","M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"):
    require(f in v54, f"MTF field {f}")

require("RECOVERED_SOURCES" in brain and "DECISION_BRAIN_V1" in brain, "Brain V1 recovered path")
require('"predicted_return_used_as_direction": False' in adapter, "memory prediction direction guard")
require("historical_memory_consumed_downstream" in adapter, "historical memory downstream metadata")
require("nison_contradiction" in evaluator and "nison_confirmation" in evaluator, "Nison confirmation/contradiction")
require('"tiz_execution_gate": "DISABLED"' in evaluator, "TIZ execution gate disabled")
require('"nison_direction_generation":False' in e2e.replace(" ", ""), "Nison direction generation false")
require('"tiz_direction_generation":False' in e2e.replace(" ", ""), "TIZ direction generation false")
require('"memory_direction_generation":False' in e2e.replace(" ", ""), "Memory direction generation false")

require("risk_engine" in v4 or "risk_engine" in v54, "canonical risk engine reference")
require("2016-2024" in workflow, "development window")
require("2025_OOS_LOCKED" in workflow, "2025 OOS lock")
require('"official_profitability_claim": False' in v4, "no official profitability claim")

for p in [Path(__file__), ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py", ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py", ROOT / "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py", ROOT / "RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py", ROOT / "compatibility/decision_brain_v1_handoff_adapter.py", ROOT / "evaluation/three_book_decision_evaluator_v1.py"]:
    try:
        ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    except SyntaxError as e:
        FAILS.append(f"syntax {p}: {e}")

print("GOVERNANCE_V2_STATUS=PASS" if not FAILS else "GOVERNANCE_V2_STATUS=BLOCKED")
for f in FAILS:
    print(f"GOVERNANCE_V2_FAIL={f}")
raise SystemExit(0 if not FAILS else 1)
