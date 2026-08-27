from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "OOS_2025" / "full_decision_brain_historical_event_producer_v1.py"

spec = importlib.util.spec_from_file_location("final_event_producer", TARGET)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _frame(rule_count: int, prefix: str) -> pd.DataFrame:
    ts = pd.Timestamp("2025-01-02T00:00:00Z")
    return pd.DataFrame(
        [
            {
                "timestamp": ts,
                "source_rule_id": f"{prefix}_{i:04d}",
                "status": "NOT_EVALUABLE",
                "direction": "UNKNOWN",
            }
            for i in range(rule_count)
        ]
    )


def test_full_evidence_requires_exact_34_murphy_rules(monkeypatch: pytest.MonkeyPatch) -> None:
    ts = pd.Timestamp("2025-01-02T00:00:00Z")
    full = _frame(33, "MURPHY")
    with pytest.raises(AssertionError, match="Murphy full evidence set contains 33 rules"):
        module.build_events(
            market_context=pd.DataFrame([{"timestamp": ts}]),
            murphy=_frame(1, "MURPHY"),
            nison=_frame(1, "NISON").rename(columns={"direction": "confirmation"}).assign(contradiction=False),
            risk=pd.DataFrame([{"timestamp": ts, "risk_status": "PASS"}]),
            execution=pd.DataFrame([{"timestamp": ts, "entry_price": 1.0, "atr": 0.001}]),
            tiz=None,
            year=2025,
            optional_tiz=True,
            murphy_full_evidence=full,
            nison_full_evidence=_frame(44, "NISON").rename(columns={"direction": "confirmation"}).assign(contradiction=False),
        )


def test_full_evidence_requires_exact_44_nison_rules(monkeypatch: pytest.MonkeyPatch) -> None:
    ts = pd.Timestamp("2025-01-02T00:00:00Z")
    with pytest.raises(AssertionError, match="Nison full evidence set contains 43 rules"):
        module.build_events(
            market_context=pd.DataFrame([{"timestamp": ts}]),
            murphy=_frame(1, "MURPHY"),
            nison=_frame(1, "NISON").rename(columns={"direction": "confirmation"}).assign(contradiction=False),
            risk=pd.DataFrame([{"timestamp": ts, "risk_status": "PASS"}]),
            execution=pd.DataFrame([{"timestamp": ts, "entry_price": 1.0, "atr": 0.001}]),
            tiz=None,
            year=2025,
            optional_tiz=True,
            murphy_full_evidence=_frame(34, "MURPHY"),
            nison_full_evidence=_frame(43, "NISON").rename(columns={"direction": "confirmation"}).assign(contradiction=False),
        )


def test_producer_cli_schema_contains_explicit_full_evidence_and_execution_fields() -> None:
    text = TARGET.read_text(encoding="utf-8")
    assert "--murphy-full-evidence" in text
    assert "--nison-full-evidence" in text
    assert '"entry_price": execution_plan.get("entry_price")' in text
    assert '"atr": float(e["atr"])' in text
    assert "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT" in text
    # The two tests above are the behavioral contract for fail-closed 34/44-rule provenance.
