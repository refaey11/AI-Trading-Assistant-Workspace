from pathlib import Path
import json, re, subprocess, sys

ROOT = Path('.')
OUT = ROOT / 'overnight_audit'
OUT.mkdir(exist_ok=True)

TARGET = re.compile(r'(0006|0007|TRENDLINE_GEOMETRY_V1|PIVOT_SEQUENCE_V2|third.?touch|reaction|no.?break|availability)', re.I)
TEXT = {'.md','.txt','.json','.yaml','.yml','.py','.csv','.toml'}

hits=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts or p.suffix.lower() not in TEXT:
        continue
    try:
        s=p.read_text(errors='ignore')
    except Exception:
        continue
    if TARGET.search(s) or TARGET.search(p.name):
        hits.append({'path':str(p), 'size':p.stat().st_size, 'matches':len(TARGET.findall(s))})

# Run available tests without inventing a test command. If none exist, record that fact.
commands=[]
if list(ROOT.rglob('pytest.ini')) or list(ROOT.rglob('pyproject.toml')) or list(ROOT.rglob('tests')):
    commands.append([sys.executable,'-m','pytest','-q'])

results=[]
for cmd in commands:
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=900)
        results.append({'command':' '.join(cmd),'returncode':r.returncode,'stdout':r.stdout[-12000:],'stderr':r.stderr[-12000:]})
    except Exception as e:
        results.append({'command':' '.join(cmd),'error':str(e)})

status='PASS' if results and all(x.get('returncode')==0 for x in results) else ('NO_TEST_SUITE' if not results else 'TEST_FAILURE')

report={
    'scope':'Murphy 0006-0007 only',
    'status':status,
    'targeted_files':sorted(hits,key=lambda x:x['path']),
    'test_results':results,
    'production_freeze':False,
    '2025_used_for_tuning':False,
    'rule': 'Do not invent thresholds, ATR, lookback, 2-day/3% operators, or promote a freeze automatically.',
    'next_gate':'Prove Pivot V2 -> Geometry V1 -> third touch -> reaction -> no-break -> availability lineage, then prepare Freeze Review.'
}
(OUT/'closure_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(OUT/'closure_report.md').write_text(
    '# Overnight 0006-0007 Closure Audit\n\n'
    f"Status: **{status}**\n\n"
    f"Targeted files found: **{len(hits)}**\n\n"
    'This workflow is audit-only. It does not promote production, modify canonical rules, or use 2025 for tuning.\n\n'
    'Next gate: prove the canonical upstream lineage and prepare a Freeze Review.\n',
    encoding='utf-8')

print(json.dumps(report,indent=2))
