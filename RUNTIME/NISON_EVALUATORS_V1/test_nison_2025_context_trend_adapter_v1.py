from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "OOS_2025"))

from nison_2025_source_adapter_v1 import build_payload_rows


def _bars():
    return pd.DataFrame(
        [
            {
                "timestamp": "2025-01-02T00:00:00Z",
                "open": 1.10,
                "high": 1.11,
                "low": 1.09,
                "close": 1.105,
            }
        ]
    )


def test_market_state_trend_is_translated_to_nison_vocabulary():
    ctx = pd.DataFrame(
        [
            {
                "timestamp": "2025-01-02T00:00:00Z",
                "trend": "BULL_TREND",
                "location": "MID_RANGE",
            }
        ]
    )
    rows = build_payload_rows(_bars(), ctx)
    assert rows[0]["payload"]["context"]["trend"] == "Uptrend"


def test_bear_trend_is_translated_and_unknown_states_remain_fail_closed():
    ctx = pd.DataFrame(
        [
            {"timestamp": "2025-01-02T00:00:00Z", "trend": "BEAR_TREND"},
        ]
    )
    rows = build_payload_rows(_bars(), ctx)
    assert rows[0]["payload"]["context"]["trend"] == "Downtrend"

    ctx2 = pd.DataFrame(
        [
            {"timestamp": "2025-01-02T00:00:00Z", "trend": "TRANSITION"},
        ]
    )
    rows2 = build_payload_rows(_bars(), ctx2)
    assert rows2[0]["payload"]["context"]["trend"] == "TRANSITION"
