from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py"


def load_module_from_text(source: str, name: str):
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader=None))
    sys.modules[name] = mod
    # V4 derives ROOT from __file__. When exec() is used, Python does not inject
    # __file__ automatically, so provide the real V4 path explicitly.
    mod.__dict__["__file__"] = str(V4)
    mod.__dict__["__package__"] = ""
    exec(compile(source, str(V4), "exec"), mod.__dict__)
    return mod


@dataclass(frozen=True)
class FrozenRiskResult:
    risk_pass: bool
    risk_percent: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    position_size: Optional[float]
    reason: str


BASE_RISK_PCT = 0.005
AFTER_TWO_LOSSES_RISK_PCT = 0.0025
MAX_RISK_PCT = 0.015
SL_ATR = 0.75
TP_R = 2.0


def evaluate_frozen_candidate_risk(
    *,
    direction: str,
    equity: float,
    peak_equity: float,
    entry: float,
    atr: float,
    prior_loss_streak: int = 0,
    risk_budget_pct: Optional[float] = None,
) -> FrozenRiskResult:
    if direction not in {"BUY", "SELL"}:
        return FrozenRiskResult(False, 0.0, None, None, None, "INVALID_DIRECTION")
    if equity <= 0 or peak_equity <= 0 or entry <= 0 or atr <= 0:
        return FrozenRiskResult(False, 0.0, None, None, None, "INVALID_EXECUTION_INPUT")

    risk_pct = risk_budget_pct if risk_budget_pct is not None else (
        AFTER_TWO_LOSSES_RISK_PCT if prior_loss_streak >= 2 else BASE_RISK_PCT
    )
    if risk_pct <= 0 or risk_pct > MAX_RISK_PCT:
        return FrozenRiskResult(False, 0.0, None, None, None, "RISK_BUDGET_INVALID")

    stop_distance = SL_ATR * atr
    reward_distance = TP_R * stop_distance
    if direction == "BUY":
        stop_loss = entry - stop_distance
        take_profit = entry + reward_distance
    else:
        stop_loss = entry + stop_distance
        take_profit = entry - reward_distance

    position_size = (equity * risk_pct) / stop_distance
    return FrozenRiskResult(
        True,
        risk_pct,
        stop_loss,
        take_profit,
        position_size,
        "FROZEN_CANDIDATE_RISK_PASS_DEVELOPMENT",
    )


source = V4.read_text(encoding="utf-8")

# Development-only compatibility rule: Nison absence/failure is not a
# contradiction. Only an opposite directional PASS may contradict Murphy.
source = source.replace(
    '        nids = {rid for ids in ng.expanded_ids for rid in ids}\n'
    '        if nids != NISON_IDS:\n'
    '            continue\n',
    '        nids = {rid for ids in ng.expanded_ids for rid in ids}\n'
    '        if not nids:\n'
    '            continue\n'
)

mod = load_module_from_text(source, "current_stack_historical_replay_v5_4_impl")
_original_load_module = mod.load_module


def patched_load_module(path: Path, name: str):
    # Preserve candidate 0.5% / 0.25% risk, 0.75 ATR stop and 2R target,
    # but do not import the frozen profile's drawdown breaker as a hard gate
    # into the development replay. Canonical risk remains authoritative later.
    if path.name == "frozen_candidate_risk_profile_v1.py":

        class FrozenModule:
            evaluate_frozen_candidate_risk = staticmethod(evaluate_frozen_candidate_risk)

        return FrozenModule
    return _original_load_module(path, name)


mod.load_module = patched_load_module
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
    p = argparse.ArgumentParser()
    for name in (
        "h1",
        "market-state",
        "murphy",
        "nison",
        "mtf",
        "historical-context",
        "historical-outcome",
        "similarity-artifact",
        "retrieval-artifact",
        "scenario-artifact",
        "output-dir",
    ):
        p.add_argument(f"--{name}", required=True, type=Path)

    a = p.parse_args()
    run(
        a.h1,
        a.market_state,
        a.murphy,
        a.nison,
        a.mtf,
        a.historical_context,
        a.historical_outcome,
        a.similarity_artifact,
        a.retrieval_artifact,
        a.scenario_artifact,
        a.output_dir,
    )
