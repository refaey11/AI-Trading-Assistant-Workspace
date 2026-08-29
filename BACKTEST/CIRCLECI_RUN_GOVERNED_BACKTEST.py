from __future__ import annotations

import os
import shutil
from argparse import Namespace
from pathlib import Path

from BACKTEST import GOVERNED_CANONICAL_RUNNER_V3 as runner

ROOT = Path.cwd()
if not (ROOT / "BACKTEST" / "GOVERNED_CANONICAL_RUNNER_V3.py").exists():
    ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)
TFS = ("M5", "M15", "M30", "H1", "H4", "D1")
TREND_MAP = {
    "BULL_TREND": 1.0,
    "BEAR_TREND": -1.0,
    "TRANSITION": 0.0,
    "UNKNOWN": 0.0,
    "BULLISH": 1.0,
    "BEARISH": -1.0,
    "NEUTRAL": 0.0,
}


def strict_brain_row(row):
    """Use source-backed MTF inputs only; never zero-fill Brain fields."""
    out = {"volume_available": bool(row.get("volume_available", False))}
    for key in REQUIRED:
        if key not in row.index or row[key] is None:
            raise ValueError(f"MTF_BRAIN_INPUT_CONTRACT_MISSING:{key}")
        value = row[key]
        if key == "mtf_trend_score":
            try:
                out[key] = float(value)
            except Exception as exc:
                raise ValueError(f"MTF_BRAIN_INPUT_NON_NUMERIC:{key}") from exc
        else:
            if isinstance(value, str):
                value = TREND_MAP.get(value.strip().upper())
            if value is None:
                raise ValueError(f"MTF_BRAIN_INPUT_UNKNOWN_ENCODING:{key}")
            try:
                out[key] = float(value)
            except Exception as exc:
                raise ValueError(f"MTF_BRAIN_INPUT_NON_NUMERIC:{key}") from exc
    for tf in TFS:
        vol = f"{tf}_volume_regime"
        if vol in row.index and out["volume_available"]:
            try:
                out[vol] = float(row[vol])
            except Exception as exc:
                raise ValueError(f"MTF_BRAIN_INPUT_NON_NUMERIC:{vol}") from exc
    return out


runner.brain_row = strict_brain_row
env = os.environ.copy()
env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT), env.get("PYTHONPATH", "")]))
output_dir = ROOT / "artifacts/decision_brain_backtest_2016_2024"

args = Namespace(
    h1=Path(env["H1"]),
    market=ROOT / "artifacts/raw/market_state.csv",
    mtf=Path(env["MTF"]),
    murphy=Path(env["MURPHY"]),
    nison=ROOT / "artifacts/raw/nison.csv",
    historical_context=Path(env["HC"]),
    historical_outcome=Path(env["HO"]),
    similarity=Path(env["SIM_DIR"]),
    retrieval=Path(env["RET_DIR"]),
    output_dir=output_dir,
)
if not args.nison.exists():
    raise SystemExit(f"MISSING_NISON_SOURCE:{args.nison}")
runner.run(args)

# Backward-compatible output contract only: expose the identical canonical
# event rows under the legacy filename expected by existing validators.
canonical_events = output_dir / "decision_events_2016_2024.csv"
legacy_events = output_dir / "unified_78_events_2016_2024.csv"
if not canonical_events.exists():
    raise SystemExit(f"MISSING_BACKTEST_OUTPUT {canonical_events}")
shutil.copy2(canonical_events, legacy_events)
print(f"BACKWARD_COMPAT_OUTPUT {legacy_events}")
