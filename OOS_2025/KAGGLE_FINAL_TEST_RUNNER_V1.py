from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = 'https://github.com/refaey11/AI-Trading-Assistant-Workspace.git'
BRANCH = 'main'
WORK = Path('/kaggle/working/AI-Trading-Assistant-Workspace')
ARTIFACTS = WORK / 'artifacts' / 'kaggle_final_test'
YEAR = 2025

if WORK.exists():
    shutil.rmtree(WORK)
subprocess.run(['git', 'clone', '--depth', '1', '--branch', BRANCH, REPO, str(WORK)], check=True)
os.chdir(WORK)
sys.path.insert(0, str(WORK))
ARTIFACTS.mkdir(parents=True, exist_ok=True)

print('PROJECT =', WORK)
print('BRANCH =', BRANCH)
print('COMMIT =', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())

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
    if rc != 0:
        raise SystemExit(f'Governance/runtime pytest failed with rc={rc}')

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
for p in found[:300]:
    print(p)

h1 = next((p for p in found if p.name == 'GBPUSD_H1_2016_2025_MASTER.csv'), None)
m1 = next((p for p in found if p.suffix.lower() == '.csv' and 'GBPUSD' in p.name.upper() and 'M1' in p.name.upper()), None)
market_state = next((p for p in found if p.name == 'GBPUSD_MARKET_STATE.csv'), None)

if h1 is None:
    raise SystemExit('BLOCKED: GBPUSD_H1_2016_2025_MASTER.csv is not attached to Kaggle.')
if m1 is None:
    raise SystemExit('BLOCKED: GBPUSD M1 source is not attached to Kaggle.')

print('\nH1 =', h1)
print('M1 =', m1)
print('MARKET_STATE =', market_state)

# ---- Murphy PIT rerun already supported by the current repository ----
out_murphy = ARTIFACTS / 'MURPHY_0022_0023_2025.csv'
out_murphy_manifest = ARTIFACTS / 'MURPHY_0022_0023_2025_MANIFEST.json'
oi = WORK / 'evidence' / 'cftc' / '2025' / '6b_oi_pit_bound_v1.json'
cmd = [
    sys.executable,
    'OOS_2025/run_murphy_0022_0023_2025_pit_v1.py',
    '--h1', str(h1),
    '--m1', str(m1),
    '--oi', str(oi),
    '--output', str(out_murphy),
    '--manifest', str(out_murphy_manifest),
]
print('\n=== MURPHY 0022/0023 2025 PIT RERUN ===')
print(' '.join(cmd))
subprocess.run(cmd, check=True)

# ---- Full Nison 44-rule 2025 production ----
out_nison = ARTIFACTS / 'NISON_2025_FULL_PRODUCTION.csv'
out_nison_manifest = ARTIFACTS / 'NISON_2025_FULL_PRODUCTION_MANIFEST.json'
nison_cmd = [
    sys.executable,
    'OOS_2025/run_nison_historical_production_v1.py',
    '--input', str(h1),
    '--year', str(YEAR),
    '--output', str(out_nison),
    '--manifest', str(out_nison_manifest),
]
if market_state is not None:
    nison_cmd += ['--context', str(market_state)]
print('\n=== NISON 44-RULE 2025 PRODUCTION ===')
print(' '.join(nison_cmd))
subprocess.run(nison_cmd, check=True)

summary = {
    'status': 'PASS',
    'evaluation_year': YEAR,
    'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
    'murphy_artifact': str(out_murphy),
    'murphy_manifest': str(out_murphy_manifest),
    'nison_artifact': str(out_nison),
    'nison_manifest': str(out_nison_manifest),
    'note': 'This runner produces governed 2025 Murphy 0022/0023 and full Nison 44-rule artifacts. It does not claim the final 78-rule profitability result until the remaining Murphy rules and Decision Brain event stream are assembled and evaluated.'
}
(ARTIFACTS / 'KAGGLE_FINAL_TEST_SUMMARY.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print('\n=== FINAL SUMMARY ===')
print(json.dumps(summary, indent=2))
