from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = 'https://github.com/refaey11/AI-Trading-Assistant-Workspace.git'
BRANCH = 'final-test-prep-2026-08-24'
WORK = Path('/kaggle/working/AI-Trading-Assistant-Workspace')

# Always execute the exact current final-test-prep branch so the Kaggle dataset
# does not need to be manually refreshed after a GitHub commit.
if WORK.exists():
    shutil.rmtree(WORK)
subprocess.run(['git', 'clone', '--depth', '1', '--branch', BRANCH, REPO, str(WORK)], check=True)
os.chdir(WORK)
sys.path.insert(0, str(WORK))

print('PROJECT =', WORK)
print('BRANCH =', BRANCH)
print('COMMIT =', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())

# 1) Structural/governance tests that do not require market-data files.
TESTS = [
    'tests/evaluation/test_cftc_6b_oi_pit_bound_v1.py',
    'tests/evaluation/test_murphy_0021_0023_runtime_dispatch_v1.py',
    'tests/evaluation/test_frozen_2025_oos_stream_contract_v1.py',
    'tests/evaluation/test_frozen_decision_execution_bridge_v1.py',
    'tests/evaluation/test_three_book_decision_evaluator_v1.py',
    'tests/evaluation/test_tiz_optional_execution_adapter_v2.py',
]
existing = [t for t in TESTS if (WORK / t).exists()]
print('\n=== GOVERNANCE / RUNTIME TESTS ===')
print('Selected tests:', existing)
if existing:
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-q', *existing])
    print('pytest_rc =', rc)
else:
    print('No selected tests found')

# 2) Locate governed market data attached to this Kaggle notebook.
print('\n=== MARKET DATA DISCOVERY ===')
found = []
seen = set()
for base in [Path('/kaggle/input'), Path('/kaggle/working')]:
    if not base.exists():
        continue
    for p in base.rglob('*.csv'):
        if p.is_file() and str(p) not in seen:
            seen.add(str(p))
            found.append(p)
for p in found[:200]:
    print(p)

h1 = next((p for p in found if p.name == 'GBPUSD_H1_2016_2025_MASTER.csv'), None)
m1 = next((p for p in found if p.suffix.lower() == '.csv' and 'M1' in p.name.upper()), None)

if h1 is None:
    print('\nBLOCKED: GBPUSD_H1_2016_2025_MASTER.csv is not attached to Kaggle.')
    print('The project branch and PIT OI are ready, but the real 2025 Murphy 0022/0023 rerun needs the governed H1 source.')
    raise SystemExit(0)
if m1 is None:
    print('\nBLOCKED: GBPUSD M1 source is not attached to Kaggle.')
    print('The current 0022/0023 producer rebuilds H1 volume direction from the governed M1 source.')
    raise SystemExit(0)

print('\nH1 =', h1)
print('M1 =', m1)

# 3) Execute the actual PIT-safe Murphy 0022/0023 producer over all 2025 H1 rows.
out_dir = WORK / 'artifacts' / 'kaggle_final_test'
out_dir.mkdir(parents=True, exist_ok=True)
out_csv = out_dir / 'MURPHY_0022_0023_2025.csv'
out_manifest = out_dir / 'MURPHY_0022_0023_2025_MANIFEST.json'
oi = WORK / 'evidence/cftc/2025/6b_oi_pit_bound_v1.json'

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
