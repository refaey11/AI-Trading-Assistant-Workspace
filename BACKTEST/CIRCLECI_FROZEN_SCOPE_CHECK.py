from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = json.loads((ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json").read_text(encoding="utf-8"))
EXPECTED_MURPHY = set(ALLOWLIST["verified_runtime"]["MURPHY"])
BLOCKED = {x["rule_id"] for x in ALLOWLIST.get("explicitly_blocked", [])}

h1 = pd.read_csv(os.environ["H1"], usecols=["timestamp"])
h1t = pd.to_datetime(h1["timestamp"], utc=True, format="mixed")
assert h1t.dt.year.min() <= 2016
assert h1t.dt.year.max() >= 2025

n = pd.read_csv("artifacts/raw/nison.csv", usecols=["timestamp", "rule_id"])
nt = pd.to_datetime(n["timestamp"], utc=True, format="mixed")
assert nt.dt.year.min() == 2016 and nt.dt.year.max() == 2024
assert set(n["rule_id"].dropna().astype(str)) == {f"NISON_{i:04d}" for i in range(1, 45)}
assert len(n) == 2428448

m = pd.read_csv(os.environ["MURPHY"], usecols=["timestamp", "source_rule_id"])
mt = pd.to_datetime(m["timestamp"], utc=True, format="mixed")
assert mt.dt.year.min() == 2016 and mt.dt.year.max() == 2024

observed_murphy: set[str] = set()
for value in m["source_rule_id"].dropna().astype(str):
    observed_murphy.update(part.strip() for part in value.split("|") if part.strip())

assert BLOCKED.isdisjoint(observed_murphy)
assert observed_murphy <= EXPECTED_MURPHY
missing = EXPECTED_MURPHY - observed_murphy
assert not missing, f"MISSING_FROZEN_MURPHY_RULES={sorted(missing)}"
assert len(observed_murphy) == len(EXPECTED_MURPHY) == 34

print("FROZEN_SCOPE_PASS", "nison_rows=", len(n), "nison_rules=", 44, "murphy_rules=", len(observed_murphy))
print("OOS_2025_LOCKED")
