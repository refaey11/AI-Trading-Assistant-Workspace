"""Thin orchestration preflight over existing Decision Brain boundaries.

No rule, TIZ, Risk, or directional semantics are created here. The guard only
checks that authoritative upstream mappings exist and then delegates the
existing Three-Book boundary. Missing process/risk evidence fails closed.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence
import importlib.util
from pathlib import Path

THREE_BOOK_PATH = Path(__file__).with_name("three_book_decision_evaluator_v1.py")


def _load_existing_three_book():
    spec = importlib.util.spec_from_file_location("three_book_decision_evaluator_v1", THREE_BOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("existing Three-Book evaluator could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preflight_event(*, brain_assessment: Mapping[str, Any], murphy_evidence: Mapping[str, Any],
                    nison_evidence: Mapping[str, Any], tiz_evidence: Mapping[str, Any],
                    risk_evidence: Mapping[str, Any], source_rule_ids: Sequence[str],
                    timestamp: str) -> dict[str, Any]:
    """Fail closed on missing authoritative inputs; otherwise delegate existing evaluator."""
    required = {
        "brain_assessment": brain_assessment,
        "murphy_evidence": murphy_evidence,
        "nison_evidence": nison_evidence,
        "tiz_evidence": tiz_evidence,
        "risk_evidence": risk_evidence,
    }
    missing = [name for name, value in required.items() if not isinstance(value, Mapping) or not value]
    if missing:
        return {"status": "NOT_EVALUABLE", "reason": "MISSING_AUTHORITATIVE_INPUT", "missing": missing}

    evaluator = _load_existing_three_book()
    result = evaluator.evaluate_three_book_decision(
        brain_assessment=brain_assessment,
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence=tiz_evidence,
        risk_evidence=risk_evidence,
        source_rule_ids=source_rule_ids,
        timestamp=timestamp,
    )
    return {"status": "EVALUATED", "result": result}
