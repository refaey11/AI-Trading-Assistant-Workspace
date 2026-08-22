from dataclasses import dataclass
from typing import Optional

NOT_EVALUABLE = 'NOT_EVALUABLE'
NO_SIGNAL = 'NO_SIGNAL'
BULLISH = 'BULLISH'
BEARISH = 'BEARISH'

@dataclass(frozen=True)
class WedgeEvidence:
    geometry: Optional[str] = None
    breakout: Optional[str] = None
    geometry_evaluable: bool = False
    breakout_evaluable: bool = False

def evaluate_0018(e: WedgeEvidence) -> str:
    if not (e.geometry_evaluable and e.breakout_evaluable):
        return NOT_EVALUABLE
    if e.geometry == 'FALLING_WEDGE' and e.breakout == 'UPSIDE':
        return BULLISH
    return NO_SIGNAL

def evaluate_0019(e: WedgeEvidence) -> str:
    if not (e.geometry_evaluable and e.breakout_evaluable):
        return NOT_EVALUABLE
    if e.geometry == 'RISING_WEDGE' and e.breakout == 'DOWNSIDE':
        return BEARISH
    return NO_SIGNAL

def dispatch(rule_id: str, e: WedgeEvidence) -> str:
    if rule_id == 'MURPHY_0018':
        return evaluate_0018(e)
    if rule_id == 'MURPHY_0019':
        return evaluate_0019(e)
    raise KeyError(rule_id)
