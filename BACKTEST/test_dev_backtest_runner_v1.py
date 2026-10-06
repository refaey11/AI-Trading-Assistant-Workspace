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



def test_wide_mtf_annual_files_are_concatenated(tmp_path):
    from BACKTEST.DEV_BACKTEST_RUNNER_V1 import load_mtf_context

    mtf_dir = tmp_path / "mtf"
    mtf_dir.mkdir()
    for year, ts in [(2016, "2016-01-04T10:00:00Z"), (2017, "2017-01-04T10:00:00Z")]:
        pd.DataFrame([{
            "timestamp": ts,
            "M5_trend_regime": 1,
            "M15_trend_regime": 1,
            "M30_trend_regime": 1,
            "H1_trend_regime": 1,
            "H4_trend_regime": -1,
            "D1_trend_regime": 1,
        }]).to_csv(mtf_dir / f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv", index=False)

    out = load_mtf_context(mtf_dir)
    assert len(out) == 2
    assert set(c for c in out.columns if c.endswith("_trend_regime")) == {
        "M5_trend_regime","M15_trend_regime","M30_trend_regime",
        "H1_trend_regime","H4_trend_regime","D1_trend_regime",
    }
    assert out["mtf_timeframes_available"].min() == 6



def test_runner_consumes_existing_asof_memory_provider_without_direction(tmp_path):
    ts = "2024-01-02T10:00:00Z"
    prior = "2023-12-30T10:00:00Z"
    h1 = tmp_path / "h1.csv"
    ctx = tmp_path / "context.csv"
    murphy = tmp_path / "murphy.csv"
    nison = tmp_path / "nison.csv"
    historical_context = tmp_path / "historical_context.csv"
    historical_outcome = tmp_path / "historical_outcome.csv"
    similarity = tmp_path / "similarity.json"
    retrieval = tmp_path / "retrieval.json"
    scenario = tmp_path / "scenario.json"
    out = tmp_path / "out"

    pd.DataFrame([
        {"timestamp": ts, "open": 1.1000, "high": 1.1000, "low": 1.1000, "close": 1.1000},
        {"timestamp": "2024-01-02T11:00:00Z", "open": 1.1000, "high": 1.1040, "low": 1.0995, "close": 1.1035},
    ]).to_csv(h1, index=False)

    pd.DataFrame([{
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
    }]).to_csv(ctx, index=False)

    pd.DataFrame(_murphy_rows(ts)).to_csv(murphy, index=False)
    pd.DataFrame(_nison_rows(ts)).to_csv(nison, index=False)

    pd.DataFrame([{
        "pair": "GBPUSD",
        "timestamp": prior,
        "context_signature": "BULL_TREND / INSIDE_RANGE / MID_RANGE / CONTRACTION / NORMAL / no_major_candle",
    }]).to_csv(historical_context, index=False)
    pd.DataFrame([{
        "pair": "GBPUSD",
        "timestamp": prior,
        "context_signature": "BULL_TREND / INSIDE_RANGE / MID_RANGE / CONTRACTION / NORMAL / no_major_candle",
        "return_48h": 0.001,
    }]).to_csv(historical_outcome, index=False)
    similarity.write_text("{}", encoding="utf-8")
    retrieval.write_text("{}", encoding="utf-8")
    scenario.write_text("{}", encoding="utf-8")

    result = run(
        h1=h1,
        murphy=murphy,
        nison=nison,
        context=ctx,
        output_dir=out,
        historical_context=historical_context,
        historical_outcome=historical_outcome,
        similarity_artifact=similarity,
        retrieval_artifact=retrieval,
        scenario_artifact=scenario,
        round_trip_cost_price=0.0002,
    )

    manifest = json.loads((out / "validation_manifest_2016_2024.json").read_text())
    events = pd.read_csv(out / "unified_78_events_2016_2024.csv")

    assert result["validation"]["memory_asof_evidence"] is True
    assert manifest["memory_asof_evidence"] is True
    assert bool(events.iloc[0]["memory_asof_usable"]) is True
    assert bool(events.iloc[0]["memory_shadow_only"]) is True
    assert manifest["official_profitability_claim"] is False
