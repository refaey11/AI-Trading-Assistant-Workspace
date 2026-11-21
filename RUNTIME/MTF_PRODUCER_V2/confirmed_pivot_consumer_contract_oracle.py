"""TEST-ONLY synthetic oracle for the proposed confirmed-pivot consumer contract.

Validates structural compatibility on synthetic fixtures only. It does not
authenticate source IDs, clocks, provenance, continuity, or production eligibility.
Never import this module from runtime or Decision Brain code.
"""
import math
from numbers import Real
from typing import Any

STREAM_FIELDS = {
    "contract_version", "producer_name", "producer_version", "schema_version",
    "symbol", "timeframe", "source_namespace", "identity_model",
    "detector_config_id", "precision_evidence_ref", "clock_evidence_ref",
    "continuity_evidence_ref", "fixture_mode",
}
PIVOT_FIELDS = {
    "pivot_id", "kind", "price", "source_bar_id", "source_index",
    "final_confirming_bar_id", "final_confirming_index", "right_window",
    "available_index", "symbol", "timeframe", "source_namespace",
    "producer_name", "producer_version", "schema_version",
    "detector_config_id", "confirmation_status", "precision_evidence_ref",
    "clock_evidence_ref", "continuity_evidence_ref",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _finite_number(value: Any) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(float(value))


def validate_synthetic_consumer_contract(*, stream, bars, source_history, pivots,
                                          decision_snapshot_index) -> dict:
    """Validate structural invariants against explicitly synthetic source history.

    source_history may include bars before the current replay window to model
    warm-start references. Evidence references are opaque fixture labels only.
    Their presence is not authentication.
    """
    if not isinstance(stream, dict) or not STREAM_FIELDS.issubset(stream):
        raise ValueError("source stream envelope is incomplete")
    if stream["fixture_mode"] is not True:
        raise ValueError("test oracle accepts synthetic fixtures only")
    for key in STREAM_FIELDS - {"fixture_mode"}:
        if not _nonempty_string(stream[key]):
            raise ValueError(f"stream field {key} must be a non-empty string")
    if stream["identity_model"] != "MODEL_A_SYNTHETIC":
        raise ValueError("only synthetic Model A-shaped IDs are accepted")
    if not _strict_int(decision_snapshot_index):
        raise ValueError("decision snapshot index must be an integer")
    if not bars or not source_history:
        raise ValueError("bars and source history must not be empty")

    history_by_id, history_by_index = {}, {}
    for bar in source_history:
        required = {"bar_id", "index", "symbol", "timeframe", "source_namespace",
                    "open", "high", "low", "close", "completed"}
        if not isinstance(bar, dict) or not required.issubset(bar):
            raise ValueError("source-history bar is incomplete")
        if not _nonempty_string(bar["bar_id"]) or not _strict_int(bar["index"]):
            raise ValueError("source-history identity/index is invalid")
        if bar["bar_id"] in history_by_id or bar["index"] in history_by_index:
            raise ValueError("source-history IDs and indices must be unique")
        if (bar["symbol"], bar["timeframe"], bar["source_namespace"]) != (
            stream["symbol"], stream["timeframe"], stream["source_namespace"]
        ):
            raise ValueError("source-history bar is bound to another stream")
        if bar["completed"] is not True:
            raise ValueError("only completed source-history bars are accepted")
        values = [bar[k] for k in ("open", "high", "low", "close")]
        if not all(_finite_number(v) for v in values):
            raise ValueError("source-history OHLC must be finite numeric values")
        o, h, l, c = map(float, values)
        if not (l <= min(o, c) <= max(o, c) <= h):
            raise ValueError("source-history OHLC envelope is invalid")
        history_by_id[bar["bar_id"]] = bar
        history_by_index[bar["index"]] = bar

    if any(not _strict_int(b.get("index")) for b in bars):
        raise ValueError("consumer bars require integer indices")
    indices = [b["index"] for b in bars]
    if indices != list(range(indices[0], indices[0] + len(indices))):
        raise ValueError("consumer replay window indices must be contiguous")
    for bar in bars:
        known = history_by_index.get(bar["index"])
        if known is None or known["bar_id"] != bar.get("bar_id"):
            raise ValueError("consumer bar does not match source-history identity")

    pivot_ids, accepted = set(), []
    for pivot in pivots:
        if not isinstance(pivot, dict) or not PIVOT_FIELDS.issubset(pivot):
            raise ValueError("confirmed-pivot record is incomplete")
        string_fields = ("pivot_id", "source_bar_id", "final_confirming_bar_id",
                         "symbol", "timeframe", "source_namespace", "producer_name",
                         "producer_version", "schema_version", "detector_config_id",
                         "precision_evidence_ref", "clock_evidence_ref",
                         "continuity_evidence_ref")
        for key in string_fields:
            if not _nonempty_string(pivot[key]):
                raise ValueError(f"pivot field {key} must be a non-empty string")
        if pivot["pivot_id"] in pivot_ids:
            raise ValueError("pivot IDs must be unique within this synthetic fixture")
        pivot_ids.add(pivot["pivot_id"])
        binding = ("symbol", "timeframe", "source_namespace", "producer_name",
                   "producer_version", "schema_version", "detector_config_id")
        expected = (stream["symbol"], stream["timeframe"], stream["source_namespace"],
                    stream["producer_name"], stream["producer_version"],
                    stream["schema_version"], stream["detector_config_id"])
        if tuple(pivot[k] for k in binding) != expected:
            raise ValueError("pivot is not bound to the consumer source stream")
        evidence = ("precision_evidence_ref", "clock_evidence_ref", "continuity_evidence_ref")
        if tuple(pivot[k] for k in evidence) != tuple(stream[k] for k in evidence):
            raise ValueError("pivot evidence references do not match source stream")
        if pivot["kind"] not in ("HIGH", "LOW") or pivot["confirmation_status"] != "CONFIRMED":
            raise ValueError("only confirmed HIGH/LOW pivots are accepted")
        for key in ("source_index", "final_confirming_index", "right_window", "available_index"):
            if not _strict_int(pivot[key]):
                raise ValueError(f"pivot {key} must be a strict integer")
        if pivot["right_window"] < 1:
            raise ValueError("right window must be positive")
        if pivot["final_confirming_index"] != pivot["source_index"] + pivot["right_window"]:
            raise ValueError("final confirming bar does not match configured right window")
        if pivot["available_index"] != pivot["final_confirming_index"]:
            raise ValueError("availability must equal the final confirming bar index")
        if pivot["available_index"] > decision_snapshot_index:
            raise ValueError("pivot is not yet available at the decision snapshot")
        source = history_by_id.get(pivot["source_bar_id"])
        confirming = history_by_id.get(pivot["final_confirming_bar_id"])
        if source is None or confirming is None:
            raise ValueError("pivot source or final confirming bar identity is missing")
        if source["index"] != pivot["source_index"]:
            raise ValueError("pivot source index does not match source-bar identity")
        if confirming["index"] != pivot["final_confirming_index"]:
            raise ValueError("final confirming index does not match bar identity")
        if not _finite_number(pivot["price"]):
            raise ValueError("pivot price must be finite numeric")
        expected_price = source["high"] if pivot["kind"] == "HIGH" else source["low"]
        if float(pivot["price"]) != float(expected_price):
            raise ValueError("pivot price does not equal source bar extreme")
        accepted.append(pivot["pivot_id"])

    return {
        "status": "SYNTHETIC_STRUCTURAL_CHECKS_PASSED",
        "accepted_pivot_ids": accepted,
        "production_eligible": False,
        "source_identity_authenticated": False,
        "clock_authenticated": False,
        "continuity_authenticated": False,
    }
