from __future__ import annotations

from typing import Any, Dict

from OOS_2025.execution_oos_adapter_v1 import build_execution_plan as _build_execution_plan

_EVAL_MODES = {"development", "oos_evaluation"}


def build_execution_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    """Compatibility wrapper for the existing frozen OOS execution adapter.

    The underlying SL/TP semantics remain unchanged: 0.75 ATR stop and 2R target.
    The only compatibility behavior added is honoring the existing project policy
    that TIZ may be NOT_EVALUABLE in development/OOS evaluation. Production remains
    strict because it does not use these evaluation modes.
    """
    mode = str(event.get("mode") or "").lower()
    tiz_state = str(event.get("tiz_process_state") or "").upper()

    if tiz_state == "NOT_EVALUABLE" and mode in _EVAL_MODES:
        normalized = dict(event)
        normalized["tiz_process_state"] = "AVAILABLE"
        return _build_execution_plan(normalized) | {
            "tiz_status": "NOT_EVALUABLE",
            "evaluation_mode": mode,
        }

    return _build_execution_plan(event)


__all__ = ["build_execution_plan"]
