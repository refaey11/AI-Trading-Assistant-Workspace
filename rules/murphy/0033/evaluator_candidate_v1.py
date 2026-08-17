from dataclasses import dataclass
from typing import Optional, Literal

State = Literal["CONFIRMED", "CONFLICT", "NOT_EVALUABLE"]

@dataclass(frozen=True)
class Input:
    reversal_candle: Optional[bool]
    short_term_trend: Optional[Literal["UP", "DOWN", "FLAT"]]
    oscillator_d: Optional[float]
    candle_direction: Optional[Literal["BULLISH", "BEARISH", "NEUTRAL"]]

@dataclass(frozen=True)
class Evidence:
    state: State
    direction: str
    reason: str

def evaluate(x: Input) -> Evidence:
    if any(v is None for v in (x.reversal_candle, x.short_term_trend, x.oscillator_d, x.candle_direction)):
        return Evidence("NOT_EVALUABLE", "NEUTRAL", "Required input unavailable.")
    d = float(x.oscillator_d)
    if not 0 <= d <= 100:
        return Evidence("NOT_EVALUABLE", "NEUTRAL", "Stochastic %D outside 0..100.")
    if not x.reversal_candle:
        return Evidence("CONFLICT", "NEUTRAL", "Only reversal candles are eligible.")
    if x.short_term_trend == "FLAT":
        return Evidence("CONFLICT", "NEUTRAL", "Short-term trend is required.")
    if not (d < 20 or d > 80):
        return Evidence("CONFLICT", "NEUTRAL", "Oscillator is outside presignal area.")
    if x.candle_direction == "BULLISH" and x.short_term_trend != "DOWN":
        return Evidence("CONFLICT", "NEUTRAL", "Bullish reversal conflicts with prior trend.")
    if x.candle_direction == "BEARISH" and x.short_term_trend != "UP":
        return Evidence("CONFLICT", "NEUTRAL", "Bearish reversal conflicts with prior trend.")
    return Evidence("CONFIRMED", "NEUTRAL", "Reversal candle and contextual presignal conditions satisfied.")
