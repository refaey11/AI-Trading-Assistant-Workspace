from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from BACKTEST.mtf_source_contract_gate_v1 import parse_aware_timestamps
allowlist = json.loads((ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json").read_text(encoding="utf-8"))
expected_murphy = set(allowlist["verified_runtime"]["MURPHY"])
blocked = {x["rule_id"] for x in allowlist.get("explicitly_blocked", [])}

h1 = pd.read_csv(os.environ["H1"], usecols=["timestamp"])
h1t = parse_aware_timestamps(h1["timestamp"], label="H1", error_prefix="BLOCKED_SOURCE")
assert h1t.dt.year.min() <= 2016
assert h1t.dt.year.max() >= 2025

n = pd.read_csv("artifacts/raw/nison.csv", usecols=["timestamp", "rule_id"])
nt = parse_aware_timestamps(n["timestamp"], label="NISON", error_prefix="BLOCKED_SOURCE")
assert nt.dt.year.min() == 2016 and nt.dt.year.max() == 2024
assert set(n["rule_id"].dropna().astype(str)) == {f"NISON_{i:04d}" for i in range(1, 45)}
assert len(n) == 2428448

m = pd.read_csv(os.environ["MURPHY"], usecols=["timestamp", "source_rule_id"])
mt = parse_aware_timestamps(m["timestamp"], label="MURPHY", error_prefix="BLOCKED_SOURCE")
assert mt.dt.year.min() == 2016 and mt.dt.year.max() == 2024

observed_murphy: set[str] = set()
for value in m["source_rule_id"].dropna().astype(str):
    observed_murphy.update(part.strip() for part in value.split("|") if part.strip())

blocked_observed = sorted(blocked & observed_murphy)
unknown = sorted(observed_murphy - expected_murphy)
assert not blocked_observed, f"BLOCKED_MURPHY_RULES_PRESENT={blocked_observed}"
assert not unknown, f"UNKNOWN_MURPHY_RULES={unknown}"

missing_historical = sorted(expected_murphy - observed_murphy)
print(
    "MURPHY_HISTORICAL_COVERAGE",
    "observed=", len(observed_murphy),
    "frozen_runtime=", len(expected_murphy),
    "missing_historical=", len(missing_historical),
)
if missing_historical:
    print("MURPHY_NOT_EVALUABLE_OR_NO_HISTORICAL_EVENT_ARTIFACT", missing_historical)

assert len(observed_murphy) <= len(expected_murphy)
print(
    "FROZEN_SCOPE_PASS",
    "nison_rows=", len(n),
    "nison_rules=", 44,
    "murphy_historical_rule_ids=", len(observed_murphy),
    "murphy_frozen_runtime_rules=", len(expected_murphy),
)
print("OOS_2025_LOCKED")
