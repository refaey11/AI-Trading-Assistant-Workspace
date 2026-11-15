from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "gate3c_candidate_selector",
    ROOT / "tools" / "gate3c_select_valid_event_candidate_v1.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

MTF_FIELDS = MODULE.MTF_FIELDS
TIMES = ["2020-01-02T01:00:00Z", "2020-01-03T01:00:00Z"]


def write_inputs(root: Path, *, first_event_mtf_missing: bool = True):
    murphy = root / "murphy"
    mtf = root / "mtf"
    murphy.mkdir()
    mtf.mkdir()
    pd.DataFrame([{
        "rule_id": "MURPHY_0021",
        "historical_status": "SOURCE_BACKED_HISTORICAL_EVALUATION",
        "decision_eligible": "YES",
    }]).to_csv(root / "registry.csv", index=False)
    pd.DataFrame([
        {"timestamp": ts, "direction": "BULLISH", "status": "PASS",
         "source_rule_id": "MURPHY_0021|MURPHY_0022", "pass_rule_id": "MURPHY_0021"}
        for ts in TIMES
    ]).to_csv(murphy / "MURPHY_2016_2024_FULL_EVIDENCE.csv", index=False)
    pd.DataFrame([{"timestamp": ts, "close": 1.25} for ts in TIMES]).to_csv(root / "h1.csv", index=False)
    pd.DataFrame([{"timestamp": ts, "atr": 0.01} for ts in TIMES]).to_csv(root / "market.csv", index=False)
    nison_rows = []
    for ts in TIMES:
        for i in range(1, 45):
            nison_rows.append({"timestamp": ts, "source_rule_id": f"NISON_{i:04d}"})
    pd.DataFrame(nison_rows).to_csv(root / "nison.csv", index=False)
    mtf_rows = []
    for index, ts in enumerate(TIMES):
        row = {"timestamp": ts}
        for field in MTF_FIELDS:
            row[field] = None if index == 0 and first_event_mtf_missing and field == "D1_trend_regime" else 1
        mtf_rows.append(row)
    pd.DataFrame(mtf_rows).to_csv(mtf / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv", index=False)
    return {
        "murphy_root": murphy, "registry_path": root / "registry.csv",
        "h1_path": root / "h1.csv", "market_state_path": root / "market.csv",
        "nison_path": root / "nison.csv", "mtf_root": mtf,
    }


def test_selector_skips_earlier_murphy_pass_with_incomplete_mtf_and_selects_next_valid_event(tmp_path, capsys):
    kwargs = write_inputs(tmp_path)

    selected = MODULE.select_candidate(**kwargs)

    assert selected == "2020-01-03T01:00:00Z"
    assert "SELECTED_EVENT=2020-01-03T01:00:00+00:00" in capsys.readouterr().out


def test_selector_fails_closed_when_every_candidate_has_missing_mtf(tmp_path):
    kwargs = write_inputs(tmp_path)
    frame = pd.read_csv(kwargs["mtf_root"] / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv")
    frame.loc[:, "D1_trend_regime"] = float("nan")
    frame.to_csv(kwargs["mtf_root"] / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv", index=False)

    with pytest.raises(ValueError, match="BLOCKED_NO_COMPLETE_EVENT_CANDIDATE"):
        MODULE.select_candidate(**kwargs)


def test_selector_does_not_promote_noneligible_murphy_rule(tmp_path):
    kwargs = write_inputs(tmp_path)
    registry = pd.read_csv(kwargs["registry_path"])
    registry.loc[:, "decision_eligible"] = "NO"
    registry.to_csv(kwargs["registry_path"], index=False)

    with pytest.raises(ValueError, match="BLOCKED_NO_ELIGIBLE_MURPHY_DIRECTIONAL_PASS"):
        MODULE.select_candidate(**kwargs)
