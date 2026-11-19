"""Reference-only MTF Pivot V2 identity encoder.

This is an isolated conformance implementation, not a production detector
or a Brain/runtime integration. Inputs must already be canonical upstream IDs.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Mapping

DOMAIN_SEPARATOR = b"MTF_PIVOT_V2_ID_V1\n"
REQUIRED_FIELDS = (
    "config_fingerprint",
    "detector_version",
    "pivot_kind",
    "source_bar_id",
    "symbol",
    "timeframe",
)
_HEX_256 = re.compile(r"^[0-9a-f]{64}$")


def _reject_surrogates(value: str) -> None:
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise ValueError("lone UTF-16 surrogate is not valid JCS input")


def _jcs_string(value: str) -> str:
    _reject_surrogates(value)
    # All values in this schema are strings. ensure_ascii=False follows JCS'
    # UTF-8 output; compact separators and JSON escaping match JCS string rules.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def canonical_payload_bytes(fields: Mapping[str, object]) -> bytes:
    if set(fields) != set(REQUIRED_FIELDS):
        raise ValueError("identity payload must contain exactly the six required fields")
    values: dict[str, str] = {}
    for key in REQUIRED_FIELDS:
        value = fields[key]
        if not isinstance(value, str) or value == "":
            raise ValueError(f"{key} must be a non-empty string")
        values[key] = value

    if values["detector_version"] != "MTF_PIVOT_V2":
        raise ValueError("unsupported detector_version")
    if values["pivot_kind"] not in {"HIGH", "LOW"}:
        raise ValueError("pivot_kind must be HIGH or LOW")
    if not _HEX_256.fullmatch(values["config_fingerprint"]):
        raise ValueError("config_fingerprint must be 64 lowercase SHA-256 hex characters")

    # JCS orders object member names by UTF-16 code units. The six schema keys
    # are fixed ASCII names, so their lexicographic order is identical.
    members = [
        _jcs_string(key) + ":" + _jcs_string(values[key])
        for key in sorted(REQUIRED_FIELDS)
    ]
    return ("{" + ",".join(members) + "}").encode("utf-8")


def make_pivot_id(fields: Mapping[str, object]) -> str:
    canonical = canonical_payload_bytes(fields)
    digest = hashlib.sha256(DOMAIN_SEPARATOR + canonical).hexdigest()
    return "mpv2_" + digest
