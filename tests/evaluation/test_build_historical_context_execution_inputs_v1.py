from pathlib import Path

import pandas as pd

from OOS_2025.build_historical_context_execution_inputs_v1 import build


def test_builds_source_backed_context_and_execution(tmp_path: Path):
    source = tmp_path / "GBPUSD_MARKET_STATE.csv"
    pd.DataFrame(
        [
            {"timestamp": "2024-01-02T10:00:00Z", "close": 1.27, "atr20": 0.002, "trend": "BULL_TREND"},
            {"timestamp": "2024-01-02T11:00:00Z", "close": 1.271, "atr20": 0.0021, "trend": "BULL_TREND"},
            {"timestamp": "2025-01-02T10:00:00Z", "close": 1.28, "atr20": 0.0022, "trend": "TRANSITION"},
        ]
    ).to_csv(source, index=False)

    manifest = build(source, tmp_path / "out", 2025)
    assert manifest["rows"] == 1
    context = pd.read_csv(tmp_path / "out" / "context.csv")
    execution = pd.read_csv(tmp_path / "out" / "execution.csv")
    assert context.loc[0, "entry_price"] == 1.28
    assert context.loc[0, "atr"] == 0.0022
    assert execution.loc[0, "entry_price"] == 1.28
    assert execution.loc[0, "atr"] == 0.0022
    assert manifest["direction_created"] is False
