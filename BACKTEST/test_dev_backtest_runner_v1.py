from __future__ import annotations

import json

import pandas as pd

from BACKTEST.DEV_BACKTEST_RUNNER_V1 import run


def _murphy_rows(ts: str):
    ids = [
        3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51
    ]
    return [
        {
            "timestamp": ts,
            "source_rule_id": f"MURPHY_{i:04d}",
            "status": "PASS",
            "direction": "BULLISH",
        }
        for i in ids
    ]


def _nison_rows(ts: str):
    return [
        {
            "timestamp": ts,
            "rule_id": f"NISON_{i:04d}",
            "source_rule_id": f"NISON_{i:04d}",
            "status": "FAIL",
            "direction": "BULLISH",
        }
        for i in range(1, 45)
    ]


def test_runner_wires_three_book_risk_execution(tmp_path):
    ts = "2024-01-02T10:00:00Z"
    h1 = tmp_path / "h1.csv"
    ctx = tmp_path / "context.csv"
    murphy = tmp_path / "murphy.csv"
    nison = tmp_path / "nison.csv"
    out = tmp_path / "out"

    pd.DataFrame(
        [
            {"timestamp": ts, "open": 1.1000, "high": 1.1000, "low": 1.1000, "close": 1.1000},
            {"timestamp": "2024-01-02T11:00:00Z", "open": 1.1000, "high": 1.1040, "low": 1.0995, "close": 1.1035},
        ]
    ).to_csv(h1, index=False)

    pd.DataFrame(
        [{
            "timestamp": ts,
            "entry_price": 1.1000,
            "atr": 0.0020,
            "M5_trend_regime": 1,
            "M15_trend_regime": 1,
            "M30_trend_regime": 1,
            "H1_trend_regime": 1,
            "H4_trend_regime": 1,
            "D1_trend_regime": 1,
            "M5_volume_regime": 1,
            "M15_volume_regime": 1,
            "M30_volume_regime": 1,
            "H1_volume_regime": 1,
            "H4_volume_regime": 1,
            "D1_volume_regime": 1,
        }]
    ).to_csv(ctx, index=False)

    pd.DataFrame(_murphy_rows(ts)).to_csv(murphy, index=False)
    pd.DataFrame(_nison_rows(ts)).to_csv(nison, index=False)

    result = run(
        h1=h1,
        murphy=murphy,
        nison=nison,
        context=ctx,
        output_dir=out,
    )

    trades = pd.read_csv(out / "executed_trades_2016_2024.csv")
    funnel = json.loads((out / "execution_funnel_2016_2024.json").read_text())
    manifest = json.loads((out / "validation_manifest_2016_2024.json").read_text())

    assert result["metrics"]["sl_atr"] == 0.75
    assert result["metrics"]["tp_R"] == 2.0
    assert funnel["three_book_buy_sell"] == 1
    assert len(trades) == 1
    assert trades.iloc[0]["outcome"] == "TP"
    assert trades.iloc[0]["gross_r_multiple"] == 2.0
    assert manifest["three_book_evaluator"] is True
    assert manifest["risk_engine_v1"] is True
    assert manifest["frozen_execution_adapter"] is True
    assert manifest["official_profitability_claim"] is False


def test_runner_blocks_2025(tmp_path):
    ts = "2025-01-02T10:00:00Z"
    h1 = tmp_path / "h1.csv"
    ctx = tmp_path / "context.csv"
    murphy = tmp_path / "murphy.csv"
    nison = tmp_path / "nison.csv"
    out = tmp_path / "out"

    pd.DataFrame([{
        "timestamp": ts, "open": 1.1, "high": 1.1, "low": 1.1, "close": 1.1
    }]).to_csv(h1, index=False)
    pd.DataFrame([{
        "timestamp": ts, "entry_price": 1.1, "atr": 0.002,
        "M5_trend_regime": 1, "M15_trend_regime": 1,
        "M30_trend_regime": 1, "H1_trend_regime": 1,
        "H4_trend_regime": 1, "D1_trend_regime": 1
    }]).to_csv(ctx, index=False)
    pd.DataFrame(_murphy_rows(ts)).to_csv(murphy, index=False)
    pd.DataFrame(_nison_rows(ts)).to_csv(nison, index=False)

    result = run(h1=h1, murphy=murphy, nison=nison, context=ctx, output_dir=out)
    assert result["funnel"]["events"] == 0
    assert result["validation"]["2025_present"] is False
