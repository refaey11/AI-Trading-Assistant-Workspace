"""Source-bounded structural gate for Nison rules 0003-0007.

The implementation deliberately returns NOT_EVALUABLE where Nison's
qualitative language (strong, well within, near, slightly, small, longer,
stronger) lacks an approved project comparator. It never invents a numeric
threshold.
"""
from dataclasses import dataclass
from typing import Literal, Optional

Status = Literal["PASS", "FAIL", "NOT_EVALUABLE"]

@dataclass(frozen=True)
class Candle:
    open: float
    high: float
    low: float
    close: float

    @property
    def bullish(self) -> bool:
        return self.close > self.open

    @property
    def bearish(self) -> bool:
        return self.close < self.open

    @property
    def body_low(self) -> float:
        return min(self.open, self.close)

    @property
    def body_high(self) -> float:
        return max(self.open, self.close)


def _missing(*values: object) -> bool:
    return any(v is None for v in values)


def evaluate_0003_dark_cloud(prior: Optional[Candle], current: Optional[Candle], trend: Optional[str]) -> dict:
    if _missing(prior, current, trend):
        return {"rule_id": "NISON_0003", "status": "NOT_EVALUABLE", "reason": "Missing candle or trend context"}
    if trend != "uptrend":
        return {"rule_id": "NISON_0003", "status": "FAIL", "reason": "Dark Cloud Cover requires the source's uptrend/top-reversal context"}
    if not prior.bullish or not current.bearish:
        return {"rule_id": "NISON_0003", "status": "FAIL", "reason": "Required white then black candle polarity is absent"}
    if current.open <= prior.high:
        return {"rule_id": "NISON_0003", "status": "FAIL", "reason": "Second session did not open above prior high"}
    if current.close >= prior.body_high:
        return {"rule_id": "NISON_0003", "status": "FAIL", "reason": "Second session did not close within prior white real body"}
    return {"rule_id": "NISON_0003", "status": "NOT_EVALUABLE", "reason": "Strong/well-within penetration comparator and confirmation are not source-locked project operators"}


def evaluate_0004_piercing(prior: Optional[Candle], current: Optional[Candle], trend: Optional[str]) -> dict:
    if _missing(prior, current, trend):
        return {"rule_id": "NISON_0004", "status": "NOT_EVALUABLE", "reason": "Missing candle or trend context"}
    if trend != "downtrend":
        return {"rule_id": "NISON_0004", "status": "FAIL", "reason": "Piercing Pattern requires the source's falling-market context"}
    if not prior.bearish or not current.bullish:
        return {"rule_id": "NISON_0004", "status": "FAIL", "reason": "Required black then white candle polarity is absent"}
    if current.close <= (prior.open + prior.close) / 2:
        return {"rule_id": "NISON_0004", "status": "FAIL", "reason": "White candle did not close above the prior black body's midpoint"}
    return {"rule_id": "NISON_0004", "status": "NOT_EVALUABLE", "reason": "Long-candle/gap ideality and confirmation remain source-locked qualitative requirements"}


def _neck_base(prior: Optional[Candle], current: Optional[Candle], trend: Optional[str], rule_id: str) -> Optional[dict]:
    if _missing(prior, current, trend):
        return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "reason": "Missing candle or trend context"}
    if trend != "downtrend":
        return {"rule_id": rule_id, "status": "FAIL", "reason": "Source describes these as bearish patterns in a declining market"}
    if not prior.bearish or not current.bullish:
        return {"rule_id": rule_id, "status": "FAIL", "reason": "Required black then white candle polarity is absent"}
    if current.close > (prior.open + prior.close) / 2:
        return {"rule_id": rule_id, "status": "FAIL", "reason": "Close is above the prior black body's midpoint; this is outside the neck/thrusting family boundary"}
    return None


def evaluate_0005_on_neck(prior: Optional[Candle], current: Optional[Candle], trend: Optional[str]) -> dict:
    base = _neck_base(prior, current, trend, "NISON_0005")
    if base:
        return base
    return {"rule_id": "NISON_0005", "status": "NOT_EVALUABLE", "reason": "Near-low and small-white-candle comparator are qualitative; confirmation/invalidation are not yet source-locked"}


def evaluate_0006_in_neck(prior: Optional[Candle], current: Optional[Candle], trend: Optional[str]) -> dict:
    base = _neck_base(prior, current, trend, "NISON_0006")
    if base:
        return base
    return {"rule_id": "NISON_0006", "status": "NOT_EVALUABLE", "reason": "Slight-penetration and small-white-candle comparator are qualitative; confirmation/invalidation are not yet source-locked"}


def evaluate_0007_thrusting(prior: Optional[Candle], current: Optional[Candle], trend: Optional[str]) -> dict:
    base = _neck_base(prior, current, trend, "NISON_0007")
    if base:
        return base
    return {"rule_id": "NISON_0007", "status": "NOT_EVALUABLE", "reason": "Longer/stronger-than-in-neck comparator is qualitative; confirmation/invalidation are not yet source-locked"}
