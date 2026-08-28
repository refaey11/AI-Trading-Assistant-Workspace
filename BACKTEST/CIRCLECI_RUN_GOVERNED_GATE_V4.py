from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
Path("artifacts/integration_gate").mkdir(parents=True, exist_ok=True)

murphy = os.environ["MURPHY"]
h1 = os.environ["H1"]
mtf = os.environ["MTF"]
hc = os.environ["HC"]
ho = os.environ["HO"]

subprocess.run([
    "python", "BACKTEST/MURPHY_CANONICAL_EVENT_COMPILER_V2.py",
    "--source", murphy,
    "--output", "artifacts/integration_gate/MURPHY_CANONICAL_EVENT_EVIDENCE_2016_2024.csv",
    "--allowlist", "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json",
    "--registry", "BACKTEST/MURPHY_34_SOURCE_BACKED_FANIN_V2_2026-08-28.csv",
], check=True)

subprocess.run([
    "python", "BACKTEST/NISON_CANONICAL_STREAM_COMPILER_V1.py",
    "--source", "artifacts/raw/nison.csv",
    "--output", "artifacts/integration_gate/NISON_CANONICAL_EVENT_EVIDENCE_2016_2024.csv",
    "--aggregate-output", "artifacts/integration_gate/NISON_CANONICAL_TIMESTAMP_EVIDENCE_2016_2024.csv",
    "--allowlist", "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json",
], check=True)

subprocess.run([
    "python", "BACKTEST/GOVERNED_INTEGRATION_GATE_V4.py",
    "--h1", h1,
    "--market-state", "artifacts/raw/market_state.csv",
    "--mtf", mtf,
    "--murphy", "artifacts/integration_gate/MURPHY_CANONICAL_EVENT_EVIDENCE_2016_2024.csv",
    "--nison", "artifacts/integration_gate/NISON_CANONICAL_EVENT_EVIDENCE_2016_2024.csv",
    "--historical-context", hc,
    "--historical-outcome", ho,
    "--similarity", os.environ["SIM_DIR"],
    "--retrieval", os.environ["RET_DIR"],
    "--handoff", "compatibility/knowledge_decision_handoff.py",
    "--decision-brain", "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "--output", "artifacts/integration_gate/GOVERNED_INTEGRATION_GATE_V4.json",
], check=True)
