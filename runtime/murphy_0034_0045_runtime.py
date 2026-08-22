from dataclasses import dataclass
from typing import Any, Callable, Dict

try:
    from murphy_batch_evaluators import (
        wave2, wave3, wave4, fib_zone, cycle_period, system_discipline,
        psar_regime, adx_regime, capital_reserve, single_market_exposure,
        market_risk, total_margin,
    )
except ImportError as exc:
    raise ImportError(
        "Recovered MURPHY_BATCH_0034_0045 evaluator artifact must be present on the runtime path."
    ) from exc

DISPATCH: Dict[str, Callable[..., Any]] = {
    "MURPHY_0034": wave2,
    "MURPHY_0035": wave3,
    "MURPHY_0036": wave4,
    "MURPHY_0037": fib_zone,
    "MURPHY_0038": cycle_period,
    "MURPHY_0039": system_discipline,
    "MURPHY_0040": psar_regime,
    "MURPHY_0041": adx_regime,
    "MURPHY_0042": capital_reserve,
    "MURPHY_0043": single_market_exposure,
    "MURPHY_0044": market_risk,
    "MURPHY_0045": total_margin,
}

@dataclass(frozen=True)
class RuntimeResult:
    rule_id: str
    evaluator_state: str
    adapter_state: str
    reason: str


def evaluate(rule_id: str, confirmation_ok: bool | None = None, **inputs: Any) -> RuntimeResult:
    """Fail-closed bridge for recovered Murphy 0034-0045 evaluators."""
    fn = DISPATCH.get(rule_id)
    if fn is None:
        return RuntimeResult(rule_id, "NOT_EVALUABLE", "NOT_EVALUABLE", "Unknown rule id.")
    try:
        result = fn(**inputs)
    except (TypeError, ValueError):
        return RuntimeResult(rule_id, "NOT_EVALUABLE", "NOT_EVALUABLE", "Required rule inputs are missing or invalid.")
    if result.state != "PASS":
        adapter_state = "NOT_EVALUABLE" if result.state == "NOT_EVALUABLE" else "CONFLICT"
        return RuntimeResult(rule_id, result.state, adapter_state, result.reason)
    if confirmation_ok is None:
        return RuntimeResult(rule_id, "PASS", "NOT_EVALUABLE", "Required confirmation evidence is missing.")
    if not confirmation_ok:
        return RuntimeResult(rule_id, "PASS", "CONFLICT", "Required confirmation evidence did not pass.")
    return RuntimeResult(rule_id, "PASS", "CONFIRMED", result.reason)
