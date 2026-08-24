from pathlib import Path

import pandas as pd
import pytest

from OOS_2025.full_brain_input_producer_v1 import normalize


def _write(path: Path, rows: list[dict]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def test_normalizes_only_common_timestamps(tmp_path: Path):
    ts1 = "2025-01-02T10:00:00Z"
    ts2 = "2025-01-02T11:00:00Z"
    context = tmp_path / "context.csv"
    murphy = tmp_path / "murphy.csv"
    nison = tmp_path / "nison.csv"
    risk = tmp_path / "risk.csv"
    execution = tmp_path / "execution.csv"

    _write(context, [{"timestamp": ts1, "entry_price": 1.27, "atr": 0.002}, {"timestamp": ts2, "entry_price": 1.28, "atr": 0.002}])
    _write(murphy, [{"timestamp": ts1, "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"}])
    _write(nison, [{"timestamp": ts1, "confirmation": "CONFIRMED", "contradiction": False, "source_rule_id": "NISON_0001"}, {"timestamp": ts2, "confirmation": "CONFIRMED", "contradiction": False, "source_rule_id": "NISON_0001"}])
    _write(risk, [{"timestamp": ts1, "risk_status": "PASS", "stop_loss": 1.268}])
    _write(execution, [{"timestamp": ts1, "entry_price": 1.27, "atr": 0.002}, {"timestamp": ts2, "entry_price": 1.28, "atr": 0.002}])

    manifest = normalize(context=context, murphy=murphy, nison=nison, risk=risk, execution=execution, year=2025, output_dir=tmp_path / "out")
    assert manifest["common_timestamps"] == 1
    assert manifest["ready_for_full_brain_assembler"] is True
    assert pd.read_csv(tmp_path / "out/context.csv").shape[0] == 1


def test_missing_stream_fails_closed(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        normalize(
            context=tmp_path / "context.csv",
            murphy=tmp_path / "murphy.csv",
            nison=tmp_path / "nison.csv",
            risk=tmp_path / "risk.csv",
            execution=tmp_path / "execution.csv",
            year=2025,
            output_dir=tmp_path / "out",
        )
