from dataclasses import dataclass
from typing import Optional

PASS = 'PASS'
FAIL = 'FAIL'
NOT_EVALUABLE = 'NOT_EVALUABLE'

@dataclass(frozen=True)
class WedgeGeometryEvidence:
    converges: Optional[bool] = None
    upper_slope: Optional[float] = None
    lower_slope: Optional[float] = None
    geometry_evaluable: bool = False

def _missing(e: WedgeGeometryEvidence) -> bool:
    return (
        not e.geometry_evaluable
        or e.converges is None
        or e.upper_slope is None
        or e.lower_slope is None
    )

def evaluate_0018(e: WedgeGeometryEvidence) -> str:
    """Exact mapped condition: two converging trendlines, both slope downward."""
    if _missing(e):
        return NOT_EVALUABLE
    return PASS if e.converges and e.upper_slope < 0 and e.lower_slope < 0 else FAIL

def evaluate_0019(e: WedgeGeometryEvidence) -> str:
    """Exact mapped condition: two converging trendlines, both slope upward."""
    if _missing(e):
        return NOT_EVALUABLE
    return PASS if e.converges and e.upper_slope > 0 and e.lower_slope > 0 else FAIL

def dispatch(rule_id: str, e: WedgeGeometryEvidence) -> str:
    if rule_id == 'MURPHY_0018':
        return evaluate_0018(e)
    if rule_id == 'MURPHY_0019':
        return evaluate_0019(e)
    raise KeyError(rule_id)
