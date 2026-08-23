from __future__ import annotations

import pandas as pd

from OOS_2025.build_historical_risk_evidence_v1 import build


def test_builds_frozen_risk_evidence(tmp_path):
    ts = "2025-01-02T12:00:00Z"
    context = tmp_path / "context.csv"
    murphy = tmp_path / "murphy.csv"
    output = tmp_path / "risk.csv"

    pd.DataFrame([{"timestamp": ts, "entry_price": 1.25, "atr": 0.002}]).to_csv(context, index=False)
    pd.DataFrame([{"timestamp": ts, "direction": "BUY"}]).to_csv(murphy, index=False)

    manifest = build(context=context, murphy=murphy, output=output, year=2025)
    assert manifest["status"] == "PASS"
    row = pd.read_csv(output).iloc[0]
    assert row["risk_status"] == "PASS"
    assert round(float(row["stop_loss"]), 6) == 1.2485
    assert round(float(row["take_profit"]), 6) == 1.254
