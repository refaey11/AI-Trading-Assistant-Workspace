from __future__ import annotations

import os
import subprocess
from pathlib import Path

Path("artifacts/integration_gate").mkdir(parents=True, exist_ok=True)
cmd = [
    "python", "BACKTEST/GOVERNED_INTEGRATION_GATE_V3.py",
    "--h1", os.environ["H1"],
    "--market-state", "artifacts/raw/market_state.csv",
    "--mtf", os.environ["MTF"],
    "--murphy", os.environ["MURPHY"],
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
