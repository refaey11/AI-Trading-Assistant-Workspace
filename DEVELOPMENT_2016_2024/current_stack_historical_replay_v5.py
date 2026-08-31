from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py"

spec = importlib.util.spec_from_file_location("current_stack_historical_replay_v4_impl", V4)
if not spec or not spec.loader:
    raise RuntimeError(f"cannot load {V4}")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

# Governed MTF contract: H4 higher-timeframe context + H1 local structure.
# Do not fabricate unsupported M5/M15/M30/D1 data from H1.
mod.MTF_FIELDS = ["H1_trend_regime", "H4_trend_regime"]
run = mod.run

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--mtf", required=True, type=Path)
    p.add_argument("--historical-context", required=True, type=Path)
    p.add_argument("--historical-outcome", required=True, type=Path)
    p.add_argument("--similarity-artifact", required=True, type=Path)
    p.add_argument("--retrieval-artifact", required=True, type=Path)
    p.add_argument("--scenario-artifact", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    run(a.h1, a.market_state, a.murphy, a.nison, a.mtf,
        a.historical_context, a.historical_outcome,
        a.similarity_artifact, a.retrieval_artifact, a.scenario_artifact,
        a.output_dir)
