"""Frozen 2025 OOS decision-event stream contract.

This module does not generate signals, rebuild book rules, or tune 2025.
It only validates an authoritative decision-event stream that was produced
by the existing frozen runtime, then computes metrics from those immutable
raw events. Missing/invalid provenance fails closed.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable, Mapping
from datetime import datetime, timezone

ALLOWLIST_PATH = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")
REQUIRED_COLUMNS = {
    "timestamp",
    "mode",
    "decision",
    "entry_price",
    "exit_price",
    "outcome_r",
    "cost_r",
    "source_rule_ids",
    "tiz_process_state",
    "risk_pass",
    "data_source_hash",
}
VALID_DECISIONS = {"BUY", "SELL", "NO_TRADE"}


class OOSStreamError(ValueError):
    """Raised when the frozen OOS event stream is not admissible."""


def _parse_ts(value: str) -> datetime:
    text = value.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _allowed_rule_ids() -> set[str]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return set(data["verified_runtime"]["MURPHY"]) | set(data["verified_runtime"]["NISON"])


def _rule_ids(text: str) -> list[str]:
    return [part.strip() for part in text.replace(";", ",").split(",") if part.strip()]


def validate_event_stream(
    rows: Iterable[Mapping[str, str]],
    *,
    expected_data_source_hash: str,
) -> list[dict[str, str]]:
    """Validate and return normalized 2025 OOS events.

    The function intentionally refuses to synthesize missing fields or
    decisions. It also rejects any event outside 2025 or any non-OOS mode.
    """
    allowed = _allowed_rule_ids()
    events: list[dict[str, str]] = []
    seen_ts: set[str] = set()

    for index, raw in enumerate(rows, start=1):
        missing = REQUIRED_COLUMNS.difference(raw.keys())
        if missing:
            raise OOSStreamError(f"row {index}: missing required fields: {sorted(missing)}")

        ts = _parse_ts(str(raw["timestamp"]))
        if ts.year != 2025:
            raise OOSStreamError(f"row {index}: timestamp is outside 2025 OOS: {raw['timestamp']}")
        if raw["mode"] != "oos_evaluation":
            raise OOSStreamError(f"row {index}: mode must be oos_evaluation")
        if raw["data_source_hash"] != expected_data_source_hash:
            raise OOSStreamError(f"row {index}: data source fingerprint mismatch")
        if raw["decision"] not in VALID_DECISIONS:
            raise OOSStreamError(f"row {index}: invalid decision {raw['decision']!r}")
        if raw["timestamp"] in seen_ts:
            raise OOSStreamError(f"row {index}: duplicate timestamp")
        seen_ts.add(raw["timestamp"])

        rule_ids = _rule_ids(raw["source_rule_ids"])
        if raw["decision"] in {"BUY", "SELL"}:
            if not rule_ids or any(rule_id not in allowed for rule_id in rule_ids):
                raise OOSStreamError(f"row {index}: rule allowlist rejection")
            if str(raw["tiz_process_state"]).upper() != "READY":
                raise OOSStreamError(f"row {index}: executable decision without READY TIZ state")
            if str(raw["risk_pass"]).lower() != "true":
                raise OOSStreamError(f"row {index}: executable decision without risk_pass=true")

        try:
            float(raw["entry_price"])
            float(raw["exit_price"])
            outcome_r = float(raw["outcome_r"])
            cost_r = float(raw["cost_r"])
        except (TypeError, ValueError) as exc:
            raise OOSStreamError(f"row {index}: numeric event fields invalid") from exc

        if not math.isfinite(outcome_r) or not math.isfinite(cost_r):
            raise OOSStreamError(f"row {index}: non-finite outcome/cost")

        event = dict(raw)
        event["net_r"] = f"{outcome_r - cost_r:.12g}"
        events.append(event)

    if not events:
        raise OOSStreamError("no 2025 OOS decision events supplied")
    return events


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(events: Iterable[Mapping[str, str]]) -> dict[str, float | int]:
    rows = [dict(event) for event in events if event["decision"] in {"BUY", "SELL"}]
    net_r = [float(row["net_r"]) for row in rows]
    wins = [x for x in net_r if x > 0]
    losses = [x for x in net_r if x < 0]
    gross_win = sum(wins)
    gross_loss_abs = abs(sum(losses))

    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    for value in net_r:
        equity += value
        peak = max(peak, equity)
        max_dd = min(max_dd, equity - peak)

    return {
        "events": len(rows),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": (len(wins) / len(rows)) if rows else 0.0,
        "profit_factor": (gross_win / gross_loss_abs) if gross_loss_abs else math.inf,
        "expectancy_r": (sum(net_r) / len(net_r)) if net_r else 0.0,
        "total_r": sum(net_r),
        "max_drawdown_r": max_dd,
    }
