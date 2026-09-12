from __future__ import annotations

"""Range-reversal ablation plan/runner scaffold.

Research-only. This isolates the V1.2 Range Reversal components without
changing the governed Decision Brain. The runner is intentionally parameterized
so future walk-forward runs can test component contributions without tuning
2025 OOS.
"""

import argparse
import json
from pathlib import Path

import pandas as pd

from INDEPENDENT_FOUR_SYSTEM_COMPARATOR_V1_2 import run

COMPONENTS = [
    "range_regime",
    "location",
    "nison",
    "rsi_reversal",
    "mtf_filter",
]


def build_plan() -> dict:
    return {
        "status": "RESEARCH_PLAN",
        "base": "V1.2 Range Reversal",
        "components": COMPONENTS,
        "baseline": "range_regime + location + nison + rsi_reversal",
        "ablation": "remove exactly one component at a time; compare development and untouched OOS",
        "walk_forward": [
            {"train": "2016-2019", "validation": "2020", "oos": "2021"},
            {"train": "2016-2020", "validation": "2021", "oos": "2022"},
            {"train": "2016-2021", "validation": "2022", "oos": "2023"},
            {"train": "2016-2022", "validation": "2023", "oos": "2024"},
            {"train": "2016-2023", "validation": "2024", "oos": "2025"},
        ],
        "cost_pips_round_trip": 0.8,
        "risk_model": "ATR14 * 1.2 stop, 2.0R target",
        "entry_policy": "signal_on_close_next_bar_open",
        "ambiguous_policy": "LOSS",
        "lookahead_off": True,
        "oos_tuning": False,
        "note": "Scaffold only: V1.2 implementation remains unchanged; do not treat the existing 2025 result as proof of robustness.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--plan-only", action="store_true")
    p.add_argument("--output", type=Path, default=Path("range_reversal_ablation_plan_v1.json"))
    args = p.parse_args()
    result = build_plan()
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
