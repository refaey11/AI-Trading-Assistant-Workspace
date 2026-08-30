from __future__ import annotations

import json
from pathlib import Path


def test_final_oos_input_contract_is_strict_and_oos_locked():
    p = Path(__file__).parents[2] / "OOS_2025" / "FINAL_OOS_INPUT_CONTRACT_V1.json"
    spec = json.loads(p.read_text(encoding="utf-8"))
    assert spec["governance"]["same_protocol_across_folds"] is True
    assert spec["governance"]["2025_tuning"] is False
    assert spec["governance"]["2025_oos"] is True
    assert spec["governance"]["missing_inputs_must_block_run"] is True
    required = set(spec["required_columns"])
    assert {"timestamp", "net_r", "cost_r", "outcome"} <= required
