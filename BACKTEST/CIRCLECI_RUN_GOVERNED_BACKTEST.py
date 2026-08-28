from __future__ import annotations
import os, subprocess
from pathlib import Path

out = Path('artifacts/decision_brain_backtest_2016_2024')
out.mkdir(parents=True, exist_ok=True)
cmd = [
    'python','BACKTEST/DEV_BACKTEST_RUNNER_V1.py',
    '--h1',os.environ['H1'],
    '--market','artifacts/raw/market_state.csv',
    '--mtf',os.environ['MTF'],
    '--murphy',os.environ['MURPHY'],
    '--nison','artifacts/raw/nison.csv',
    '--historical-context',os.environ['HC'],
    '--historical-outcome',os.environ['HO'],
    '--similarity',os.environ['SIM_DIR'],
    '--retrieval',os.environ['RET_DIR'],
    '--output-dir',str(out),
]
subprocess.run(cmd, check=True)
