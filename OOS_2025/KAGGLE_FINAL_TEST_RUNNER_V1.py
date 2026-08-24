from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path('/kaggle/input/datasets/fitnesswithmooh/ai-trading-assistant-workspace')
if not ROOT.exists():
    candidates = list(Path('/kaggle/input').glob('*/AI-Trading-Assistant-Workspace'))
    if candidates:
        ROOT = candidates[0]

os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

print('PROJECT_ROOT =', ROOT)
print('EXISTS =', ROOT.exists())

# 1) Structural/project tests that do not require external market-data files.
TESTS = [
    'tests/evaluation/test_cftc_6b_oi_pit_bound_v1.py',
    'tests/evaluation/test_murphy_0021_0023_runtime_dispatch_v1.py',
    'tests/evaluation/test_frozen_2025_oos_stream_contract_v1.py',
    'tests/evaluation/test_frozen_decision_execution_bridge_v1.py',
    'tests/evaluation/test_three_book_decision_evaluator_v1.py',
    'tests/evaluation/test_tiz_optional_execution_adapter_v2.py',
]

existing = [t for t in TESTS if (ROOT / t).exists()]
print('\n=== GOVERNANCE / RUNTIME TESTS ===')
print('Selected tests:', existing)
rc = subprocess.call([sys.executable, '-m', 'pytest', '-q', *existing]) if existing else 2
print('pytest_rc =', rc)

# 2) Locate governed market data if it has been attached to this Kaggle notebook.
print('\n=== MARKET DATA DISCOVERY ===')
search_roots = [Path('/kaggle/input'), ROOT]
patterns = ['GBPUSD_H1_2016_2025_MASTER.csv', '*.csv']
found = []
seen = set()
for base in search_roots:
    if not base.exists():
        continue
    for pat in patterns:
        for p in base.rglob(pat):
            if p.is_file() and str(p) not in seen:
                seen.add(str(p))
                found.append(p)

for p in found[:100]:
    print(p)

h1 = next((p for p in found if p.name == 'GBPUSD_H1_2016_2025_MASTER.csv'), None)
if h1 is None:
    print('\nBLOCKED: governed GBPUSD H1 2016-2025 CSV is not attached to this Kaggle input.')
    print('The project code/PIT OI are present, but final 2025 Murphy/Decision-Brain execution cannot be certified without the governed H1 source.')
    raise SystemExit(0)

# M1 is required for the current Murphy 0022/0023 PIT producer because its volume stream is rebuilt from M1.
m1 = next((p for p in found if p.suffix.lower() == '.csv' and 'M1' in p.name.upper()), None)
if m1 is None:
    print('\nBLOCKED: governed GBPUSD M1 source is not attached to this Kaggle input.')
    raise SystemExit(0)

print('\nH1 =', h1)
print('M1 =', m1)

# 3) Execute the actual PIT-safe Murphy 0022/0023 producer over 2025.
out_dir = ROOT / 'artifacts' / 'kaggle_final_test'
out_dir.mkdir(parents=True, exist_ok=True)
out_csv = out_dir / 'MURPHY_0022_0023_2025.csv'
out_manifest = out_dir / 'MURPHY_0022_0023_2025_MANIFEST.json'
oi = ROOT / 'evidence/cftc/2025/6b_oi_pit_bound_v1.json'

cmd = [
    sys.executable,
    'OOS_2025/run_murphy_0022_0023_2025_pit_v1.py',
    '--h1', str(h1),
    '--m1', str(m1),
    '--oi', str(oi),
    '--output', str(out_csv),
    '--manifest', str(out_manifest),
]
print('\n=== MURPHY 0022/0023 2025 PIT RERUN ===')
print(' '.join(cmd))
subprocess.run(cmd, check=True)

print('\n=== MANIFEST ===')
print(out_manifest.read_text())
print('\nFINAL TEST RUNNER COMPLETE')
