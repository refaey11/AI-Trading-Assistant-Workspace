from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py"

spec = importlib.util.spec_from_file_location("current_stack_historical_replay_v4_impl_v5_2", V4)
if not spec or not spec.loader:
    raise RuntimeError(f"cannot load {V4}")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

# Canonical Decision Brain V1 MTF inputs: six real-data timeframes.
# The source must provide these fields; no unsupported timeframe is fabricated.
mod.MTF_FIELDS = [
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
]
run = mod.run

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    for name in (
        "h1", "market-state", "murphy", "nison", "mtf",
        "historical-context", "historical-outcome", "similarity-artifact",
        "retrieval-artifact", "scenario-artifact", "output-dir",
    ):
        p.add_argument(f"--{name}", required=True, type=Path)
    a = p.parse_args()
    run(
        a.h1, a.market_state, a.murphy, a.nison, a.mtf,
        a.historical_context, a.historical_outcome,
        a.similarity_artifact, a.retrieval_artifact, a.scenario_artifact,
        a.output_dir,
    )
