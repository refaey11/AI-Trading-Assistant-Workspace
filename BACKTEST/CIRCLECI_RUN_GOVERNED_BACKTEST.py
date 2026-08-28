from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
if not (ROOT / "BACKTEST" / "GOVERNED_E2E_ORCHESTRATOR_V1.py").exists():
    ROOT = Path(__file__).resolve().parents[1]

env = os.environ.copy()
env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT), env.get("PYTHONPATH", "")]))

cmd = [
    "python",
    str(ROOT / "BACKTEST" / "GOVERNED_E2E_ORCHESTRATOR_V1.py"),
    "--h1", os.environ["H1"],
    "--market", str(ROOT / "artifacts/raw/market_state.csv"),
    "--mtf", os.environ["MTF"],
    "--murphy", os.environ["MURPHY"],
    "--nison", str(ROOT / "artifacts/raw/nison.csv"),
    "--historical-context", os.environ["HC"],
    "--historical-outcome", os.environ["HO"],
    "--similarity", os.environ["SIM_DIR"],
    "--retrieval", os.environ["RET_DIR"],
    "--output-dir", str(ROOT / "artifacts/decision_brain_backtest_2016_2024"),
]
subprocess.run(cmd, check=True, env=env)
