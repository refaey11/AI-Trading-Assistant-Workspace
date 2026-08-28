from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pandas as pd

out = Path("artifacts/decision_brain_backtest_2016_2024")
out.mkdir(parents=True, exist_ok=True)

# The recovered Murphy evidence may encode fan-in as composite IDs such as
# MURPHY_0025|MURPHY_0026. DEV_BACKTEST_RUNNER_V1 expects one rule ID per row,
# so normalize the evidence without changing PASS/FAIL/direction semantics.
murphy_src = Path(os.environ["MURPHY"])
murphy_norm = Path("artifacts/raw/MURPHY_2016_2024_FULL_EVIDENCE_NORMALIZED.csv")
m = pd.read_csv(murphy_src, low_memory=False)
if "source_rule_id" not in m.columns:
    raise SystemExit("MURPHY source_rule_id column missing")

m["source_rule_id"] = m["source_rule_id"].fillna("").astype(str)
m["_rule_id"] = m["source_rule_id"].str.split("|")
m = m.explode("_rule_id", ignore_index=True)
m["source_rule_id"] = m["_rule_id"].astype(str).str.strip()
m = m[m["source_rule_id"].ne("")].drop(columns=["_rule_id"])
murphy_norm.parent.mkdir(parents=True, exist_ok=True)
m.to_csv(murphy_norm, index=False)

cmd = [
    "python",
    "BACKTEST/DEV_BACKTEST_RUNNER_V1.py",
    "--h1",
    os.environ["H1"],
    "--market",
    "artifacts/raw/market_state.csv",
    "--mtf",
    os.environ["MTF"],
    "--murphy",
    str(murphy_norm),
    "--nison",
    "artifacts/raw/nison.csv",
    "--historical-context",
    os.environ["HC"],
    "--historical-outcome",
    os.environ["HO"],
    "--similarity",
    os.environ["SIM_DIR"],
    "--retrieval",
    os.environ["RET_DIR"],
    "--output-dir",
    str(out),
]
subprocess.run(cmd, check=True)
