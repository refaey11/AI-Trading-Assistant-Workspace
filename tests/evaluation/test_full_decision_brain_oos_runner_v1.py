from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from OOS_2025.run_full_decision_brain_oos_v1 import run


def write(path: Path, rows: list[dict]):
    pd.DataFrame(rows).to_csv(path, index=False)


def test_runner_builds_governed_event_stream(tmp_path: Path):
    ts = "2024-12-31T23:00:00Z"
    context = tmp_path / "context.csv"
    murphy = tmp_path / "murphy.csv"
    nison = tmp_path / "nison.csv"
    risk = tmp_path / "risk.csv"
    output = tmp_path / "events.csv"
    summary = tmp_path / "summary.json"

    write(context, [{
        "timestamp": ts,
        "entry_price": 1.275,
        "atr": 0.002,
        "mtf_trend_score": 0.7,
        "M5_trend_regime": 0.4,
        "M15_trend_regime": 0.5,
        "M30_trend_regime": 0.3,
        "H1_trend_regime": 0.4,
        "H4_trend_regime": 0.2,
        "D1_trend_regime": 0.1,
        "volume_available": True,
        "M5_volume_regime": 0.2,
        "M15_volume_regime": 0.1,
    }])
    write(murphy, [{"timestamp": ts, "status": "PASS", "direction": "BULLISH"}])
    write(nison, [{"timestamp": ts, "confirmation": "CONFIRMED", "contradiction": False}])
    write(risk, [{"timestamp": ts, "risk_status": "PASS", "stop_loss": "1.2735", "take_profit": "1.2780", "rr": 2.0}])

    result = run(
        context_csv=context,
        murphy_csv=murphy,
        nison_csv=nison,
        risk_csv=risk,
        output_csv=output,
        summary_json=summary,
        year=2024,
        source_rule_ids=["MURPHY_0003", "NISON_0001"],
    )

    assert result["status"] == "PASS"
    assert result["output_rows"] == 1
    assert pd.read_csv(output).iloc[0]["decision"] == "BUY"
    saved = json.loads(summary.read_text())
    assert saved["profitability_claim"] is False
