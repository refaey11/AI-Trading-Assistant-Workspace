"""One-cell Kaggle runner for the final governed OOS preparation.

This runner clones the current final-test-prep branch so the notebook does not
need a manually refreshed Kaggle dataset. It then runs structural tests and,
when the governed GBPUSD H1/M1 sources are attached, executes the PIT-safe
Murphy 0022/0023 producer.

It does not tune 2025, invent evidence, or claim profitability.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "https://github.com/refaey11/AI-Trading-Assistant-Workspace.git"
BRANCH = "final-test-prep-2026-08-24"
WORK = Path("/kaggle/working/AI-Trading-Assistant-Workspace")

if WORK.exists():
    shutil.rmtree(WORK)
subprocess.run(["git", "clone", "--depth", "1", "--branch", BRANCH, REPO, str(WORK)], check=True)
os.chdir(WORK)
sys.path.insert(0, str(WORK))

print("PROJECT =", WORK)
print("BRANCH  =", BRANCH)
print("COMMIT  =", subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip())

TESTS = [
    "tests/evaluation/test_cftc_6b_oi_pit_bound_v1.py",
    "tests/evaluation/test_murphy_0021_0023_runtime_dispatch_v1.py",
]
existing = [t for t in TESTS if (WORK / t).exists()]
print("\n=== GOVERNANCE / RUNTIME TESTS ===")
print(existing)
if existing:
    rc = subprocess.call([sys.executable, "-m", "pytest", "-q", *existing])
    if rc != 0:
        raise SystemExit(rc)

print("\n=== MARKET DATA DISCOVERY ===")
files = []
for root in [Path("/kaggle/input"), Path("/kaggle/working")]:
    if not root.exists():
        continue
    for p in root.rglob("*.csv"):
        if p.is_file():
            files.append(p)

for p in files[:200]:
    print(p)

h1 = next((p for p in files if p.name == "GBPUSD_H1_2016_2025_MASTER.csv"), None)
m1 = next((p for p in files if p.suffix.lower() == ".csv" and "M1" in p.name.upper()), None)

if h1 is None or m1 is None:
    print("\nBLOCKED: governed GBPUSD H1 and/or M1 source not attached to Kaggle.")
    print("Attach the existing project datasets, rerun this same cell, and it will continue automatically.")
    raise SystemExit(0)

print("H1 =", h1)
print("M1 =", m1)

out_dir = WORK / "artifacts" / "kaggle_final_test"
out_dir.mkdir(parents=True, exist_ok=True)
out_csv = out_dir / "MURPHY_0022_0023_2025.csv"
out_manifest = out_dir / "MURPHY_0022_0023_2025_MANIFEST.json"
oi = WORK / "evidence/cftc/2025/6b_oi_pit_bound_v1.json"

cmd = [
    sys.executable,
    "OOS_2025/run_murphy_0022_0023_2025_pit_v1.py",
    "--h1", str(h1),
    "--m1", str(m1),
    "--oi", str(oi),
    "--output", str(out_csv),
    "--manifest", str(out_manifest),
]

print("\n=== MURPHY 0022/0023 2025 PIT RUN ===")
print(" ".join(cmd))
subprocess.run(cmd, check=True)

print("\n=== MANIFEST ===")
print(out_manifest.read_text(encoding="utf-8"))
print("\nFINAL TEST PREP COMPLETE")
