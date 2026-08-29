from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path.cwd()
Path("artifacts/integration_gate").mkdir(parents=True, exist_ok=True)


def slice_to_development_window(source: str, output: str) -> str:
    """Create a 2016-2024 consumption slice without modifying the raw source."""
    src = Path(source)
    dst = Path(output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    wrote = False
    for chunk in pd.read_csv(src, chunksize=250_000, low_memory=False):
        if "timestamp" not in chunk.columns:
            raise ValueError(f"{src}: missing timestamp")
        ts = pd.to_datetime(chunk["timestamp"], utc=True, errors="coerce", format="mixed")
        if ts.isna().any():
            raise ValueError(f"{src}: invalid timestamp")
        keep = (ts.dt.year >= 2016) & (ts.dt.year <= 2024)
        part = chunk.loc[keep].copy()
        if part.empty:
            continue
        part["timestamp"] = ts.loc[keep]
        part.to_csv(dst, mode="a", index=False, header=not wrote)
        wrote = True
    if not wrote:
        raise ValueError(f"{src}: no 2016-2024 development rows")
    return str(dst)


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

# Raw governed sources may contain OOS rows (notably 2025). Preserve the raw
# artifacts, but enforce the 2016-2024 consumption boundary before V3 validation.
market_state_dev = slice_to_development_window(
    os.environ["MARKET_STATE"],
    "artifacts/integration_gate/market_state_2016_2024.csv",
)
mtf_dev = slice_to_development_window(
    os.environ["MTF"],
    "artifacts/integration_gate/mtf_2016_2024.csv",
)
nison_dev = slice_to_development_window(
    "artifacts/raw/nison.csv",
    "artifacts/integration_gate/nison_2016_2024.csv",
)
hc_dev = slice_to_development_window(
    os.environ["HC"],
    "artifacts/integration_gate/historical_context_2016_2024.csv",
)
ho_dev = slice_to_development_window(
    os.environ["HO"],
    "artifacts/integration_gate/historical_outcome_2016_2024.csv",
)

cmd = [
    "python", "BACKTEST/GOVERNED_INTEGRATION_GATE_V3.py",
    "--h1", os.environ["H1"],
    "--market-state", market_state_dev,
    "--mtf", mtf_dev,
    "--murphy", canonical_murphy,
    "--nison", nison_dev,
    "--historical-context", hc_dev,
    "--historical-outcome", ho_dev,
    "--similarity", os.environ["SIM_DIR"],
    "--retrieval", os.environ["RET_DIR"],
    "--handoff", "compatibility/knowledge_decision_handoff.py",
    "--decision-brain", "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "--output", "artifacts/integration_gate/GOVERNED_INTEGRATION_GATE_V3.json",
]
subprocess.run(cmd, check=True)
