"""Live Decision Runtime V1.

Composes existing governed components; it does not reimplement book rules,
create market features, invent SL/TP, or submit broker orders.

Input is a source-backed live event. Output is SIGNAL_READY or a fail-closed
reason. MT5 order execution is deliberately a separate, not-yet-enabled stage.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk
from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision

MTF_FIELDS = (
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)
VOLUME_FIELDS = tuple(f"{tf}_volume_regime" for tf in ("M5", "M15", "M30", "H1", "H4", "D1"))
NISON_IDS = {f"NISON_{i:04d}" for i in range(1, 45)}
VALID_DIRECTIONS = {"BUY", "SELL"}


def _brain_module():
    path = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"
    spec = importlib.util.spec_from_file_location("live_runtime_decision_brain_v1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load recovered Decision Brain: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}:MISSING_TIMESTAMP")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label}:INVALID_TIMESTAMP") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label}:NAIVE_TIMESTAMP_REJECTED")
    return parsed.astimezone(timezone.utc)


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label}:BOOLEAN_NOT_NUMERIC")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{label}:MISSING_OR_NON_NUMERIC") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label}:NON_FINITE")
    return number


def _require_source_envelope(evidence: Mapping[str, Any], label: str, as_of: datetime) -> None:
    if evidence.get("authoritative") is not True:
        raise ValueError(f"{label}:SOURCE_NOT_AUTHORITATIVE")
    if not str(evidence.get("source") or "").strip():
        raise ValueError(f"{label}:SOURCE_ID_MISSING")
    if not str(evidence.get("producer") or "").strip():
        raise ValueError(f"{label}:PRODUCER_ID_MISSING")
    available_at = _timestamp(evidence.get("available_at"), f"{label}.available_at")
    if available_at > as_of:
        raise ValueError(f"{label}:FUTURE_EVIDENCE_NOT_AVAILABLE")


def _row_rule_ids(rows: Any, label: str) -> set[str]:
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{label}:SOURCE_ROWS_MISSING")
    found: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError(f"{label}:INVALID_SOURCE_ROW")
        raw = row.get("source_rule_id") or row.get("rule_id")
        for item in str(raw or "").split("|"):
            rule_id = item.strip().upper()
            if rule_id and rule_id not in {"NONE", "NULL", "NAN"}:
                found.add(rule_id)
    if not found:
        raise ValueError(f"{label}:RULE_IDS_MISSING")
    return found


def _blocked(reason: str, *, symbol: str | None = None, timestamp: str | None = None) -> dict[str, Any]:
    return {
        "status": "BLOCKED",
        "decision": "NO_TRADE",
        "reason": reason,
        "symbol": symbol,
        "query_as_of": timestamp,
        "execution": {
            "mode": "SIGNAL_ONLY",
            "orders_enabled": False,
            "broker_volume": None,
        },
    }


def run_live_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one current, source-backed event and return a non-executing signal."""
    symbol = str(event.get("symbol") or "").strip().upper()
    timestamp_text = str(event.get("query_as_of") or "")
    try:
        if not symbol:
            raise ValueError("SYMBOL_MISSING")
        as_of = _timestamp(timestamp_text, "query_as_of")
        # 2025 is a locked OOS year. This live path accepts only current-era
        # events; historical 2016-2024 work remains on its separate governed path.
        if as_of.year <= 2025:
            raise ValueError("HISTORICAL_OR_2025_OOS_EVENT_NOT_ALLOWED_IN_LIVE_MODE")
        if as_of > datetime.now(timezone.utc) + timedelta(minutes=5):
            raise ValueError("FUTURE_DECISION_TIMESTAMP_REJECTED")

        mtf = event.get("mtf_evidence")
        murphy = event.get("murphy_evidence")
        nison = event.get("nison_evidence")
        risk_input = event.get("risk_inputs")
        tiz_input = event.get("tiz_evidence")
        for name, item in (("mtf", mtf), ("murphy", murphy), ("nison", nison),
                           ("risk", risk_input)):
            if not isinstance(item, Mapping):
                raise ValueError(f"{name.upper()}_EVIDENCE_MISSING")
            _require_source_envelope(item, name.upper(), as_of)

        # TIZ is optional audit metadata only. Its absence, source envelope,
        # process flags, or malformed shape must never authorize or block.
        if isinstance(tiz_input, Mapping):
            tiz_metadata = {
                **dict(tiz_input),
                "role": "OPTIONAL_AUDIT_METADATA_ONLY",
                "provided": True,
            }
        else:
            tiz_metadata = {
                "role": "OPTIONAL_AUDIT_METADATA_ONLY",
                "state": "NOT_EVALUABLE_METADATA_ONLY" if tiz_input is None else "UNPARSEABLE_METADATA_ONLY",
                "provided": tiz_input is not None,
            }

        row = event.get("brain_row")
        if not isinstance(row, Mapping):
            raise ValueError("BRAIN_ROW_MISSING")
        normalized_row = dict(row)
        for field in MTF_FIELDS:
            normalized_row[field] = _finite_number(normalized_row.get(field), f"brain_row.{field}")
        if not isinstance(normalized_row.get("volume_available"), bool):
            raise ValueError("BRAIN_ROW.volume_available_MUST_BE_EXPLICIT_BOOLEAN")
        if normalized_row["volume_available"]:
            for field in VOLUME_FIELDS:
                normalized_row[field] = _finite_number(normalized_row.get(field), f"brain_row.{field}")

        mtf_fields = mtf.get("fields")
        if not isinstance(mtf_fields, Mapping):
            raise ValueError("MTF_SOURCE_FIELDS_MISSING")
        if not isinstance(mtf_fields.get("volume_available"), bool):
            raise ValueError("MTF_SOURCE_VOLUME_AVAILABILITY_MISSING")
        if mtf_fields["volume_available"] is not normalized_row["volume_available"]:
            raise ValueError("MTF_VOLUME_AVAILABILITY_SOURCE_MISMATCH")
        for field in MTF_FIELDS:
            source_value = _finite_number(mtf_fields.get(field), f"mtf_evidence.fields.{field}")
            if source_value != normalized_row[field]:
                raise ValueError(f"MTF_BRAIN_ROW_SOURCE_MISMATCH:{field}")
        if normalized_row["volume_available"]:
            for field in VOLUME_FIELDS:
                source_value = _finite_number(mtf_fields.get(field), f"mtf_evidence.fields.{field}")
                if source_value != normalized_row[field]:
                    raise ValueError(f"MTF_BRAIN_ROW_SOURCE_MISMATCH:{field}")

        murphy_direction = str(murphy.get("direction") or "").strip().upper()
        if murphy.get("status") != "PASS" or murphy_direction not in VALID_DIRECTIONS:
            raise ValueError("MURPHY_DIRECTIONAL_CONTEXT_NOT_PASS")
        murphy_ids = _row_rule_ids(murphy.get("rows"), "MURPHY")
        pass_rule_id = str(murphy.get("pass_rule_id") or "").strip().upper()
        directional_ids = {
            item.strip().upper()
            for item in str(murphy.get("directional_source_rule_id") or "").split("|")
            if item.strip()
        }
        if not pass_rule_id or pass_rule_id not in murphy_ids:
            raise ValueError("MURPHY_PASS_RULE_PROVENANCE_MISMATCH")
        if not directional_ids or not directional_ids.issubset(murphy_ids):
            raise ValueError("MURPHY_DIRECTIONAL_SOURCE_PROVENANCE_MISMATCH")

        nison_rows = nison.get("rows")
        nison_ids = _row_rule_ids(nison_rows, "NISON")
        if not isinstance(nison_rows, list) or len(nison_rows) != 44 or nison_ids != NISON_IDS:
            raise ValueError("NISON_44_RULE_ENVELOPE_REQUIRED")
        nison_confirmation = str(nison.get("confirmation") or "ABSENT").strip().upper()
        if nison_confirmation not in {"CONFIRMED", "ABSENT", "CONTRADICTED", "CONTRADICTION"}:
            raise ValueError("NISON_CONFIRMATION_STATE_INVALID")
        if bool(nison.get("contradiction")) or nison_confirmation in {"CONTRADICTED", "CONTRADICTION"}:
            return _blocked("NISON_CONTRADICTION", symbol=symbol, timestamp=timestamp_text)

        supplied_ids = {str(x).strip().upper() for x in event.get("source_rule_ids", []) if str(x).strip()}
        if supplied_ids != (murphy_ids | nison_ids):
            raise ValueError("SOURCE_RULE_ID_ENVELOPE_MISMATCH")

        risk_direction = str(risk_input.get("direction") or "").strip().upper()
        if risk_direction != murphy_direction:
            raise ValueError("MURPHY_RISK_DIRECTION_CONFLICT")
        entry = _finite_number(risk_input.get("entry_price"), "risk.entry_price")
        stop_loss = _finite_number(risk_input.get("stop_loss"), "risk.stop_loss")
        take_profit = _finite_number(risk_input.get("take_profit"), "risk.take_profit")
        atr = _finite_number(risk_input.get("atr"), "risk.atr")
        equity = _finite_number(risk_input.get("equity"), "risk.equity")
        peak_equity = _finite_number(risk_input.get("peak_equity"), "risk.peak_equity")
        raw_loss_streak = risk_input.get("prior_loss_streak")
        if isinstance(raw_loss_streak, bool) or not isinstance(raw_loss_streak, int) or raw_loss_streak < 0:
            raise ValueError("RISK_PRIOR_LOSS_STREAK_INVALID")
        prior_loss_streak = raw_loss_streak
        risk_budget_pct = risk_input.get("risk_budget_pct")
        if risk_budget_pct is not None:
            risk_budget_pct = _finite_number(risk_budget_pct, "risk.risk_budget_pct")
        if risk_direction == "BUY" and not (stop_loss < entry < take_profit):
            raise ValueError("BUY_STOP_TARGET_GEOMETRY_INVALID")
        if risk_direction == "SELL" and not (take_profit < entry < stop_loss):
            raise ValueError("SELL_STOP_TARGET_GEOMETRY_INVALID")

        risk_result = evaluate_risk(
            equity=equity,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            atr=atr,
            prior_loss_streak=prior_loss_streak,
            peak_equity=peak_equity,
            risk_budget_pct=risk_budget_pct,
        )
        risk_payload = {
            "risk_pass": risk_result.risk_pass,
            "risk_percent": risk_result.risk_percent,
            "rr": risk_result.rr,
            "stop_loss": risk_result.stop_loss,
            "take_profit": risk_result.take_profit,
            "reason": risk_result.reason,
            "authoritative": True,
        }
        if not risk_result.risk_pass:
            return _blocked(f"RISK_GATE:{risk_result.reason}", symbol=symbol, timestamp=timestamp_text)

        brain = _brain_module()
        # Similarity/historical memory is deliberately not passed to assess().
        assessment = brain.assess(normalized_row, similarity=None)
        # Brain assessment is retained as context only. Its directional
        # bias/confidence are derived from MTF/Volume and are not Murphy authority.
        brain_assessment = {
            "market_state": assessment.market_state,
            "directional_bias": "NOT_USED_FOR_DIRECTION",
            "directional_confidence": None,
            "confidence_status": "NOT_EVALUABLE",
            "context_evidence": assessment.evidence,
            "context_contradictions": assessment.contradictions,
            "context_no_trade_reasons": assessment.no_trade_reasons,
            "context_role": "MTF_VOLUME_CONTEXT_ONLY",
        }
        nison_payload = {
            "confirmation": nison_confirmation,
            "contradiction": False,
            "authoritative": True,
        }
        decision = evaluate_three_book_decision(
            brain_assessment=brain_assessment,
            murphy_evidence={
                "status": "PASS",
                "direction": murphy_direction,
                "authoritative": True,
                "pass_rule_id": pass_rule_id,
            },
            nison_evidence=nison_payload,
            tiz_evidence={**tiz_metadata, "decision_authority": False, "role": "OPTIONAL_AUDIT_METADATA_ONLY"},
            risk_evidence=risk_payload,
            source_rule_ids=sorted(supplied_ids),
            timestamp=timestamp_text,
        )
        final = str((decision.get("decision") or {}).get("final") or "NO_TRADE").upper()
        if final not in VALID_DIRECTIONS:
            return {
                "status": "NO_TRADE",
                "decision": "NO_TRADE",
                "reason": (decision.get("decision") or {}).get("reasons_against", ["BRAIN_OR_THREE_BOOK_REJECT"])[0],
                "brain_context": brain_assessment,
                "risk": risk_payload,
                "direction_authority": "MURPHY_ONLY",
                "directional_confidence": "NOT_EVALUABLE",
                "tiz": tiz_metadata,
                "execution": {"mode": "SIGNAL_ONLY", "orders_enabled": False, "broker_volume": None},
            }

        if final != murphy_direction:
            return _blocked("FINAL_DIRECTION_MURPHY_CONFLICT", symbol=symbol, timestamp=timestamp_text)

        return {
            "status": "SIGNAL_READY",
            "decision": final,
            "symbol": symbol,
            "query_as_of": timestamp_text,
            "entry_price": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "atr": atr,
            "risk": risk_payload,
            "brain_context": brain_assessment,
            "murphy": {"direction": murphy_direction, "pass_rule_id": pass_rule_id},
            "direction_authority": "MURPHY_ONLY",
            "directional_confidence": "NOT_EVALUABLE",
            "nison": {"confirmation": nison_confirmation, "contradiction": False},
            "tiz": tiz_metadata,
            "historical_memory": {
                "included_for_audit_only": event.get("historical_evidence") is not None,
                "passed_to_brain_for_direction": False,
            },
            "execution": {
                "mode": "SIGNAL_ONLY",
                "orders_enabled": False,
                "broker_volume": None,
                "reason": "MT5_DEMO_ORDER_ADAPTER_NOT_CONNECTED",
            },
        }
    except (ValueError, TypeError, OverflowError) as exc:
        return _blocked(str(exc), symbol=symbol or None, timestamp=timestamp_text or None)


__all__ = ["run_live_event"]
