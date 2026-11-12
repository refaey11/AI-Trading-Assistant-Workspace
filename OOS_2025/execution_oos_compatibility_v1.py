from __future__ import annotations

from typing import Any, Dict

from OOS_2025.execution_oos_adapter_v1 import build_execution_plan as _build_execution_plan


def build_execution_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    """Compatibility wrapper preserving the frozen execution semantics.

    TIZ is optional metadata only. This wrapper no longer fabricates an
    AVAILABLE state when TIZ evidence is absent or NOT_EVALUABLE.
    """
    return _build_execution_plan(dict(event))


__all__ = ["build_execution_plan"]
