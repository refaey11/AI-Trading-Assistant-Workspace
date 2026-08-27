from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable

import pandas as pd

RUNTIME_DIR = Path(__file__).resolve().parents[1] / "RUNTIME" / "NISON_EVALUATORS_V1"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from nison_0001_0010_router import evaluate_rule  # type: ignore
from bridges.nison_evaluator_to_evidence_bridge import adapt_nison_evaluator_result
from nison_2025_source_adapter_v1 import build_payload_rows

NISON_RULE_IDS = tuple(f"NISON_{i:04d}" for i in range(1, 45))
ROUTER_IDS = {
    f"NISON_{i:04d}": (f"CANDLE_RULE_{i:04d}" if i <= 38 else f"NISON_MODULE_{i:04d}")
    for i in range(1, 45)
}


def _canonical_rule_id(rule_id: str) -> str:
    if rule_id not in NISON_RULE_IDS:
        raise ValueError(f"Unsupported Nison rule id: {rule_id!r}")
    return ROUTER_IDS[rule_id]


def _sanitize_candle_payload(candle: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only fields admitted by the Nison Candle contracts.

    Market metadata such as timestamp/volume belongs outside the candle object.
    This boundary guard prevents accidental leakage of source columns into
    strict dataclass constructors while preserving all source-mapped categorical
    candle facts already supported by the evaluators.
    """
    allowed = {
        "open", "high", "low", "close",
        "body_class", "color", "gap_class", "close_relation",
        "shadow_relation", "doji_isolated", "open_inside_previous_body",
        "equal_extreme", "close_near_low",
    }
    return {key: value for key, value in dict(candle).items() if key in allowed}


def _sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    safe = dict(payload)
    safe["candles"] = [
        _sanitize_candle_payload(candle)
        for candle in payload.get("candles", [])
        if isinstance(candle, dict)
    ]
    return safe


def _evaluate_one(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    safe_payload = _sanitize_payload(payload)
    raw = evaluate_rule(_canonical_rule_id(rule_id), safe_payload)
    raw = dict(raw)
    raw["rule_id"] = rule_id
    evidence = adapt_nison_evaluator_result(raw)
    return {
        "rule_id": rule_id,
        "status": str(raw.get("status", "NOT_EVALUABLE")),
        "timestamp": payload.get("timestamp"),
        "direction": evidence.get("direction"),
        "available": bool(evidence.get("available")),
        "gate": evidence.get("gate"),
        "conflict": evidence.get("conflict"),
        "reason": raw.get("reason", ""),
        "provenance": raw.get("provenance", {"source": "Steve Nison", "lookahead": "none"}),
    }


def run_timestamp(timestamp: Any, payload_by_rule: Dict[str, Dict[str, Any]]) -> list[Dict[str, Any]]:
    """Run every governed Nison rule for one timestamp.

    Missing source-backed rule inputs are intentionally passed as empty payloads,
    which lets the existing runtime return NOT_EVALUABLE rather than inventing
    formation facts, thresholds, or direction.
    """
    rows: list[Dict[str, Any]] = []
    for rule_id in NISON_RULE_IDS:
        payload = dict(payload_by_rule.get(rule_id, {}))
        payload["timestamp"] = timestamp
        rows.append(_evaluate_one(rule_id, payload))
    return rows


def run_payload_rows(rows: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """Evaluate a stream of payload rows."""
    out: list[Dict[str, Any]] = []
    grouped: dict[pd.Timestamp, dict[str, Dict[str, Any]]] = {}
    for row in rows:
        ts = pd.Timestamp(row["timestamp"], tz="UTC")
        rule_id = str(row["rule_id"])
        grouped.setdefault(ts, {})[rule_id] = dict(row.get("payload") or {})

    for ts in sorted(grouped):
        out.extend(run_timestamp(ts, grouped[ts]))

    return pd.DataFrame(out, columns=[
        "timestamp", "rule_id", "status", "direction", "available", "gate",
        "conflict", "reason", "provenance"
    ])


def run_ohlcv_for_year(
    bars: pd.DataFrame,
    context: pd.DataFrame | None = None,
    *,
    evaluation_year: int = 2025,
) -> pd.DataFrame:
    """Run the existing Nison runtime over one specified historical year."""
    return run_payload_rows(build_payload_rows(bars, context, evaluation_year=evaluation_year))


def run_ohlcv_2025(bars: pd.DataFrame, context: pd.DataFrame | None = None) -> pd.DataFrame:
    """Backward-compatible 2025 wrapper; behavior is unchanged."""
    return run_ohlcv_for_year(bars, context, evaluation_year=2025)


def run_jsonl(path: str | Path) -> pd.DataFrame:
    rows = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return run_payload_rows(rows)
