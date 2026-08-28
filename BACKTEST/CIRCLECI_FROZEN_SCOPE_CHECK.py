from __future__ import annotations

import os
import pandas as pd

h1 = pd.read_csv(os.environ['H1'], usecols=['timestamp'])
h1t = pd.to_datetime(h1['timestamp'], utc=True, format='mixed')
assert h1t.dt.year.min() <= 2016
assert h1t.dt.year.max() >= 2025

n = pd.read_csv('artifacts/raw/nison.csv', usecols=['timestamp', 'rule_id'])
nt = pd.to_datetime(n['timestamp'], utc=True, format='mixed')
assert nt.dt.year.min() == 2016 and nt.dt.year.max() == 2024
assert n['rule_id'].nunique() == 44
assert len(n) == 2428448

m = pd.read_csv(os.environ['MURPHY'], usecols=['timestamp', 'source_rule_id'])
mt = pd.to_datetime(m['timestamp'], utc=True, format='mixed')
assert mt.dt.year.min() == 2016 and mt.dt.year.max() == 2024
assert m['source_rule_id'].nunique() == 34

print('FROZEN_SCOPE_PASS', 'nison_rows=', len(n), 'nison_rules=', n['rule_id'].nunique(), 'murphy_rules=', m['source_rule_id'].nunique())
print('OOS_2025_LOCKED')
