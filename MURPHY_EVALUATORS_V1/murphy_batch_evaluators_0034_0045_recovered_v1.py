from dataclasses import dataclass
from typing import Optional, Literal

State = Literal["PASS", "FAIL", "NOT_EVALUABLE"]


@dataclass(frozen=True)
class Result:
    state: State
    reason: str


def wave2(wave1_high: Optional[float], wave1_low: Optional[float], wave2_extreme: Optional[float]) -> Result:
    if None in (wave1_high, wave1_low, wave2_extreme):
        return Result("NOT_EVALUABLE", "Missing Wave 1/Wave 2 structure.")
    if wave1_high == wave1_low:
        return Result("NOT_EVALUABLE", "Wave 1 has zero range.")
    if wave2_extreme <= wave1_low:
        return Result("FAIL", "Wave 2 reached or exceeded the Wave 1 origin.")
    return Result("PASS", "Wave 2 remains above the Wave 1 origin.")


def wave3(length1: Optional[float], length3: Optional[float], length5: Optional[float]) -> Result:
    if None in (length1, length3, length5):
        return Result("NOT_EVALUABLE", "Missing impulse-wave lengths.")
    if min(length1, length3, length5) <= 0:
        return Result("NOT_EVALUABLE", "Wave lengths must be positive.")
    if length3 < min(length1, length5):
        return Result("FAIL", "Wave 3 is the shortest impulse wave.")
    return Result("PASS", "Wave 3 is not the shortest impulse wave.")


def wave4(wave1_low: Optional[float], wave1_high: Optional[float], wave4_price: Optional[float]) -> Result:
    if None in (wave1_low, wave1_high, wave4_price):
        return Result("NOT_EVALUABLE", "Missing Wave 1/Wave 4 price data.")
    if wave1_low >= wave1_high:
        return Result("NOT_EVALUABLE", "Invalid Wave 1 range.")
    if wave1_low <= wave4_price <= wave1_high:
        return Result("FAIL", "Wave 4 overlaps Wave 1 price territory.")
    return Result("PASS", "Wave 4 does not overlap Wave 1 price territory.")


def fib_zone(retracement_pct: Optional[float]) -> Result:
    if retracement_pct is None:
        return Result("NOT_EVALUABLE", "Missing retracement.")
    if retracement_pct in (38.2, 50.0, 61.8):
        return Result("PASS", "Retracement matches a common project Fibonacci reference.")
    return Result("FAIL", "Retracement is outside the listed common reference levels.")


def cycle_period(previous_trough: Optional[int], current_trough: Optional[int]) -> Result:
    if previous_trough is None or current_trough is None:
        return Result("NOT_EVALUABLE", "Missing consecutive trough timestamps.")
    if current_trough <= previous_trough:
        return Result("NOT_EVALUABLE", "Trough ordering is invalid.")
    return Result("PASS", "Cycle period is measurable between consecutive troughs.")


def system_discipline(system_defined: Optional[bool], regime_checked: Optional[bool]) -> Result:
    if system_defined is None or regime_checked is None:
        return Result("NOT_EVALUABLE", "Missing system/regime gate.")
    if system_defined and regime_checked:
        return Result("PASS", "Systematic process and regime evaluation are present.")
    return Result("FAIL", "Required discipline/regime gate is absent.")


def psar_regime(trending: Optional[bool]) -> Result:
    if trending is None:
        return Result("NOT_EVALUABLE", "Missing market-regime classification.")
    if trending:
        return Result("PASS", "Trending regime is compatible with Parabolic SAR.")
    return Result("FAIL", "Sideways/non-trending regime is not suitable for this trend-following use.")


def adx_regime(adx: Optional[float], threshold: Optional[float]) -> Result:
    if adx is None or threshold is None:
        return Result("NOT_EVALUABLE", "Missing ADX regime inputs.")
    if adx >= threshold:
        return Result("PASS", "ADX is above the supplied trend-regime threshold.")
    return Result("FAIL", "ADX is below the supplied trend-regime threshold.")


def capital_reserve(invested_pct: Optional[float]) -> Result:
    if invested_pct is None:
        return Result("NOT_EVALUABLE", "Missing invested-capital percentage.")
    if invested_pct <= 50:
        return Result("PASS", "Investment is within the 50% guideline.")
    return Result("FAIL", "Investment exceeds the 50% guideline.")


def single_market_exposure(exposure_pct: Optional[float]) -> Result:
    if exposure_pct is None:
        return Result("NOT_EVALUABLE", "Missing single-market exposure.")
    if exposure_pct <= 15:
        return Result("PASS", "Exposure is within the 10–15% guideline.")
    return Result("FAIL", "Exposure exceeds the 15% ceiling.")


def market_risk(risk_pct: Optional[float]) -> Result:
    if risk_pct is None:
        return Result("NOT_EVALUABLE", "Missing single-market risk.")
    if risk_pct <= 5:
        return Result("PASS", "Risk is within the 5% guideline.")
    return Result("FAIL", "Risk exceeds the 5% guideline.")


def total_margin(margin_pct: Optional[float]) -> Result:
    if margin_pct is None:
        return Result("NOT_EVALUABLE", "Missing total-margin percentage.")
    if margin_pct <= 25:
        return Result("PASS", "Margin is within the 20–25% guideline.")
    return Result("FAIL", "Margin exceeds the 25% ceiling.")
