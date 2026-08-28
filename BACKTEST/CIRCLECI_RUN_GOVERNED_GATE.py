from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
Path("artifacts/integration_gate").mkdir(parents=True, exist_ok=True)

# First normalize the governed Murphy source into the canonical event boundary.
# Missing/non-evaluable rules are preserved as governance states; no synthetic
# market evidence is generated.
compile_cmd = [
    "python", "BACKTEST/MURPHY_CANONICAL_EVENT_COMPILER_V2.py",
    "--source", os.environ["MURPHY"],
    "--output", "artifacts/integration_gate/MURPHY_CANONICAL_EVENT_EVIDENCE_2016_2024.csv",
    "--allowlist", "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json",
    "--registry", "BACKTEST/MURPHY_34_SOURCE_BACKED_FANIN_V2_2026-08-28.csv",
]
subprocess.run(compile_cmd, check=True)

canonical_murphy = str(ROOT / "artifacts/integration_gate/MURPHY_CANONICAL_EVENT_EVIDENCE_2016_2024.csv")

cmd = [
    "python", "BACKTEST/GOVERNED_INTEGRATION_GATE_V3.py",
    "--h1", os.environ["H1"],
    "--market-state", "artifacts/raw/market_state.csv",
    "--mtf", os.environ["MTF"],
    "--murphy", canonical_murphy,
    "--nison", "artifacts/raw/nison.csv",
    "--historical-context", os.environ["HC"],
    "--historical-outcome", os.environ["HO"],
    "--similarity", os.environ["SIM_DIR"],
    "--retrieval", os.environ["RET_DIR"],
    "--handoff", "compatibility/knowledge_decision_handoff.py",
    "--decision-brain", "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "--output", "artifacts/integration_gate/GOVERNED_INTEGRATION_GATE_V3.json",
]
subprocess.run(cmd, check=True)
