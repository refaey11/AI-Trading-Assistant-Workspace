"""Fail-closed cryptographic lineage between MTF raw bars and derived features."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib, json
from typing import Any, Mapping, Sequence

class FeatureLineageError(ValueError):
    """A raw-bar or derived-feature lineage claim is missing or inconsistent."""

IDENTITY_FIELDS = ("symbol", "timeframe", "bar_time_utc", "source", "producer")

def canonical_payload_hash(payload: Mapping[str, Any], label: str = "PAYLOAD") -> str:
    if not isinstance(payload, Mapping):
        raise FeatureLineageError(f"{label}:PAYLOAD_NOT_MAPPING")
    try:
        raw = json.dumps(dict(payload), sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, OverflowError) as exc:
        raise FeatureLineageError(f"{label}:PAYLOAD_NOT_CANONICAL_JSON") from exc
    return hashlib.sha256(raw).hexdigest()

def _utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise FeatureLineageError(f"{label}:MISSING")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise FeatureLineageError(f"{label}:INVALID") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise FeatureLineageError(f"{label}:TIMEZONE_AWARE_REQUIRED")
    return parsed.astimezone(timezone.utc)

def _identity(payload: Mapping[str, Any], outer: Mapping[str, Any], label: str) -> None:
    if not isinstance(payload, Mapping):
        raise FeatureLineageError(f"{label}:PAYLOAD_NOT_MAPPING")
    for field in IDENTITY_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise FeatureLineageError(f"{label}:{field.upper()}_MISSING")
        if outer.get(field) != value:
            raise FeatureLineageError(f"{label}:{field.upper()}_PAYLOAD_ENVELOPE_MISMATCH")
    _utc(payload["bar_time_utc"], f"{label}:BAR_TIME_UTC")

def _digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise FeatureLineageError(f"{label}:SHA256_INVALID")
    value = value.lower()
    if any(c not in "0123456789abcdef" for c in value):
        raise FeatureLineageError(f"{label}:SHA256_INVALID")
    return value

@dataclass(frozen=True)
class VerifiedFeatureLineage:
    feature_id: str
    feature_payload_hash: str
    raw_payload_hashes: tuple[str, ...]
    source: str
    producer: str
    symbol: str
    timeframe: str
    transform_id: str
    transform_version: str
    computed_at_utc: datetime

def verify_mtf_feature_lineage(feature_record: Mapping[str, Any],
    raw_bar_records: Sequence[Mapping[str, Any]], *, decision_as_of: str) -> VerifiedFeatureLineage:
    """Recompute payload digests and bind each feature to its exact raw-bar inputs."""
    if not isinstance(feature_record, Mapping):
        raise FeatureLineageError("FEATURE_RECORD_NOT_MAPPING")
    if not isinstance(raw_bar_records, Sequence) or isinstance(raw_bar_records, (str, bytes)):
        raise FeatureLineageError("RAW_BAR_RECORDS_INVALID")

    fp = feature_record.get("payload")
    _identity(fp, feature_record, "FEATURE")
    feature_hash = canonical_payload_hash(fp, "FEATURE")
    if feature_hash != _digest(feature_record.get("payload_hash"), "FEATURE_PAYLOAD_HASH"):
        raise FeatureLineageError("FEATURE_PAYLOAD_HASH_MISMATCH")

    fid, tid, tv = (feature_record.get(k) for k in ("feature_id", "transform_id", "transform_version"))
    if not all(isinstance(x, str) and x.strip() for x in (fid, tid, tv)):
        raise FeatureLineageError("FEATURE_TRANSFORM_IDENTITY_MISSING")
    computed = _utc(feature_record.get("computed_at_utc"), "FEATURE_COMPUTED_AT_UTC")
    as_of = _utc(decision_as_of, "DECISION_AS_OF")
    if computed > as_of:
        raise FeatureLineageError("FEATURE_COMPUTED_AFTER_DECISION_AS_OF")

    refs = feature_record.get("input_refs")
    if not isinstance(refs, list) or not refs:
        raise FeatureLineageError("FEATURE_INPUT_REFS_MISSING")
    hashes = [_digest(r.get("raw_payload_hash") if isinstance(r, Mapping) else None,
                      "FEATURE_INPUT_REF") for r in refs]
    if len(hashes) != len(set(hashes)):
        raise FeatureLineageError("FEATURE_INPUT_REF_DUPLICATE")

    raw_by_hash = {}
    for i, raw in enumerate(raw_bar_records):
        if not isinstance(raw, Mapping):
            raise FeatureLineageError(f"RAW_BAR_RECORD_INVALID:{i}")
        rp = raw.get("payload")
        _identity(rp, raw, f"RAW_BAR:{i}")
        actual = canonical_payload_hash(rp, f"RAW_BAR:{i}")
        claimed = _digest(raw.get("payload_hash"), f"RAW_BAR:{i}_PAYLOAD_HASH")
        if actual != claimed:
            raise FeatureLineageError(f"RAW_BAR_PAYLOAD_HASH_MISMATCH:{i}")
        if actual in raw_by_hash:
            raise FeatureLineageError("RAW_BAR_PAYLOAD_HASH_DUPLICATE")
        raw_by_hash[actual] = raw

    expected = {k: fp[k] for k in ("symbol", "source", "producer", "timeframe")}
    latest_input = None
    for digest in hashes:
        raw = raw_by_hash.get(digest)
        if raw is None:
            raise FeatureLineageError("FEATURE_INPUT_RAW_BAR_NOT_FOUND")
        rp = raw["payload"]
        for field, value in expected.items():
            if rp.get(field) != value:
                raise FeatureLineageError(f"FEATURE_INPUT_{field.upper()}_MISMATCH")
        ref = next(r for r in refs if r["raw_payload_hash"].lower() == digest)
        if any(ref.get(k) != raw.get(k) for k in ("symbol", "timeframe", "bar_time_utc")):
            raise FeatureLineageError("FEATURE_INPUT_REF_IDENTITY_MISMATCH")
        bar_time = _utc(raw["bar_time_utc"], "RAW_BAR_TIME_UTC")
        if bar_time > as_of:
            raise FeatureLineageError("RAW_BAR_AFTER_DECISION_AS_OF")
        latest_input = bar_time if latest_input is None else max(latest_input, bar_time)
    if latest_input is not None and computed < latest_input:
        raise FeatureLineageError("FEATURE_COMPUTED_BEFORE_INPUT_BAR")

    return VerifiedFeatureLineage(fid.strip(), feature_hash, tuple(sorted(hashes)),
        str(feature_record["source"]), str(feature_record["producer"]),
        str(feature_record["symbol"]), str(feature_record["timeframe"]),
        tid.strip(), tv.strip(), computed)

__all__ = ["FeatureLineageError", "VerifiedFeatureLineage",
           "canonical_payload_hash", "verify_mtf_feature_lineage"]
