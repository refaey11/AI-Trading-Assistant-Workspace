from dataclasses import dataclass
from typing import Optional

from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk as evaluate_risk_runtime

BASE_RISK_PCT = 0.005
AFTER_TWO_LOSSES_RISK_PCT = 0.0025
MAX_RISK_PCT = 0.015
MIN_STOP_ATR = 0.5
MAX_STOP_ATR = 4.0


@dataclass(frozen=True)
class RiskResult:
    risk_pass: bool
    risk_percent: float
    stop_distance: Optional[float]
    rr: Optional[float]
    position_size: Optional[float]
    reason: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


def evaluate_risk(
    *,
    equity: float,
    entry: float,
    stop_loss: Optional[float],
    take_profit: Optional[float],
    atr: Optional[float],
    prior_loss_streak: int,
    peak_equity: float,
    risk_budget_pct: Optional[float] = None,
    stop_mode: str = "structure",
) -> RiskResult:
    """Thin compatibility adapter over the recovered Risk Engine runtime.

    No RR minimum is invented here. The recovered runtime validates the existing
    hard gates and consumes upstream stop/target distances. RR is returned only
    as audit information.
    """
    del peak_equity  # Drawdown is tracked elsewhere; the recovered runtime does not halt on it.

    risk_pct = (
        risk_budget_pct
        if risk_budget_pct is not None
        else (AFTER_TWO_LOSSES_RISK_PCT if prior_loss_streak >= 2 else BASE_RISK_PCT)
    )
    if risk_pct <= 0 or risk_pct > MAX_RISK_PCT:
        return RiskResult(False, 0.0, None, None, None, "RISK_BUDGET_INVALID", stop_loss, take_profit)

    if stop_loss is None or take_profit is None or atr is None or atr <= 0:
        return RiskResult(False, risk_pct, None, None, None, "MISSING_EXECUTION_INPUT", stop_loss, take_profit)

    stop_distance = abs(entry - stop_loss)
    target_distance = abs(take_profit - entry)
    if stop_distance <= 0:
        return RiskResult(False, risk_pct, stop_distance, None, None, "NON_POSITIVE_STOP_DISTANCE", stop_loss, take_profit)

    rr = target_distance / stop_distance
    runtime_result = evaluate_risk_runtime(
        RiskRequest(
            equity=equity,
            risk_percent=risk_pct,
            entry_price=entry,
            stop_distance=stop_distance,
            take_profit_distance=target_distance,
            stop_mode=stop_mode,
            risk_budget_locked=True,
        ),
        "BUY" if take_profit >= entry else "SELL",
        atr,
    )

    return RiskResult(
        risk_pass=runtime_result.risk_pass,
        risk_percent=risk_pct,
        stop_distance=stop_distance,
        rr=rr,
        position_size=runtime_result.position_size,
        reason=("RISK_GATE_PASS" if runtime_result.risk_pass else runtime_result.reason),
        stop_loss=runtime_result.stop_loss,
        take_profit=runtime_result.take_profit,
    )
