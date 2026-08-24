from __future__ import annotations
import pandas as pd
from OOS_2025.nison_2025_source_adapter_v1 import build_payload_rows

def _bars():
    return pd.DataFrame([
        {"timestamp":"2024-12-31T23:58:00Z","open":1.0,"high":1.1,"low":0.9,"close":1.05},
        {"timestamp":"2024-12-31T23:59:00Z","open":1.05,"high":1.2,"low":1.0,"close":1.1},
        {"timestamp":"2025-01-02T00:00:00Z","open":1.1,"high":1.2,"low":1.0,"close":1.15},
    ])

def test_year_parameter_filters_only_requested_fold():
    rows_2024=build_payload_rows(_bars(),evaluation_year=2024)
    rows_2025=build_payload_rows(_bars(),evaluation_year=2025)
    assert len(rows_2024)==2*44 and len(rows_2025)==1*44
    assert {pd.Timestamp(r["timestamp"]).year for r in rows_2024}=={2024}
    assert {pd.Timestamp(r["timestamp"]).year for r in rows_2025}=={2025}

def test_historical_fold_uses_prior_completed_candles_and_keeps_rule_contracts():
    rows={r["rule_id"]:r for r in build_payload_rows(_bars(),evaluation_year=2025)}
    assert rows["NISON_0031"]["payload"]["candles"][-1]["close"]==1.15
    assert len(rows["NISON_0031"]["payload"]["candles"])==3
    assert len(rows["NISON_0001"]["payload"]["candles"])==2
    assert len(rows["NISON_0021"]["payload"]["candles"])==1

def test_default_behavior_remains_2025_compatible():
    assert build_payload_rows(_bars())==build_payload_rows(_bars(),evaluation_year=2025)
