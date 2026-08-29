from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
if not (ROOT / "BACKTEST" / "GOVERNED_CANONICAL_RUNNER_V3.py").exists():
    ROOT = Path(__file__).resolve().parents[1]

env = os.environ.copy()
env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT), env.get("PYTHONPATH", "")]))

output_dir = ROOT / "artifacts/decision_brain_backtest_2016_2024"

cmd = [
    "python",
    str(ROOT / "BACKTEST" / "GOVERNED_CANONICAL_RUNNER_V3.py"),
    "--h1", os.environ["H1"],
    "--market", str(ROOT / "artifacts/raw/market_state.csv"),
    "--mtf", os.environ["MTF"],
    "--murphy", os.environ["MURPHY"],
    "--nison", str(ROOT / "artifacts/raw/nison.csv"),
    "--historical-context", os.environ["HC"],
    "--historical-outcome", os.environ["HO"],
    "--similarity", os.environ["SIM_DIR"],
    "--retrieval", os.environ["RET_DIR"],
    "--output-dir", str(output_dir),
]
subprocess.run(cmd, check=True, env=env)

# Backward-compatible output contract only: preserve the canonical event file
# and expose the identical rows under the legacy unified_78 filename expected
# by existing post-run validators. No data, decisions, rules, or semantics are
# changed by this alias.
canonical_events = output_dir / "decision_events_2016_2024.csv"
legacy_events = output_dir / "unified_78_events_2016_2024.csv"
if not canonical_events.exists():
    raise SystemExit(f"MISSING_BACKTEST_OUTPUT {canonical_events}")
shutil.copy2(canonical_events, legacy_events)
print(f"BACKWARD_COMPAT_OUTPUT {legacy_events}")
