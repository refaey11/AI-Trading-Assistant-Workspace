from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable, List, Mapping, Tuple

import pandas as pd

SYNTHETIC_RULE_IDS = {"", "NISON_NONE", "NONE", "NULL", "NAN"}


def _normalize_rule_id(value: Any) -> str:
    return str(value or "").strip()


def _row_payload(row: pd.Series) -> Dict[str, Any]:
    payload = row.to_dict()
    timestamp = payload.pop("timestamp", None)
    if timestamp is not None:
        payload["timestamp"] = timestamp
    return payload


def build_lossless_rule_groups(
    df: pd.DataFrame,
    *,
    rule_column: str = "source_rule_id",
) -> Dict[pd.Timestamp, List[Dict[str, Any]]]:
    """Preserve every real per-rule record at each timestamp.

    No deduplication and no directional aggregation occur here. Synthetic rule
    sentinels are excluded from the governed evidence set rather than treated
    as real rules.
    """
    required = {"timestamp", rule_column}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    groups: Dict[pd.Timestamp, List[Dict[str, Any]]] = defaultdict(list)
    for _, row in df.sort_values("timestamp", kind="stable").iterrows():
        rule_id = _normalize_rule_id(row[rule_column])
        if rule_id.upper() in SYNTHETIC_RULE_IDS:
            continue
        ts = row["timestamp"]
        groups[ts].append(_row_payload(row))
    return dict(groups)


def legacy_selected_row(
    rows: Iterable[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Compatibility selector matching the former keep='last' behavior.

    This function exists only while the downstream frozen evaluator still
    accepts one Murphy/Nison mapping. It does not claim to be multi-rule
    aggregation; the complete evidence remains available separately.
    """
    materialized = [dict(r) for r in rows]
    if not materialized:
        return {}
    return materialized[-1]


def evidence_summary(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    materialized = [dict(r) for r in rows]
    rule_ids = [
        _normalize_rule_id(r.get("source_rule_id"))
        for r in materialized
        if _normalize_rule_id(r.get("source_rule_id")).upper() not in SYNTHETIC_RULE_IDS
    ]
    return {
        "record_count": len(materialized),
        "rule_ids": rule_ids,
        "unique_rule_ids": sorted(set(rule_ids)),
        "duplicate_rule_ids": sorted({rid for rid in rule_ids if rule_ids.count(rid) > 1}),
        "lossless": True,
    }


def combine_timestamp_evidence(
    murphy: pd.DataFrame,
    nison: pd.DataFrame,
) -> Dict[pd.Timestamp, Dict[str, Any]]:
    """Create a lossless timestamp-level evidence envelope.

    The envelope is provenance-only in this version: it does not decide which
    rule wins and does not synthesize direction.
    """
    murphy_groups = build_lossless_rule_groups(murphy)
    nison_groups = build_lossless_rule_groups(nison)
    timestamps = sorted(set(murphy_groups) | set(nison_groups))
    out: Dict[pd.Timestamp, Dict[str, Any]] = {}
    for ts in timestamps:
        m_rows = murphy_groups.get(ts, [])
        n_rows = nison_groups.get(ts, [])
        out[ts] = {
            "timestamp": ts,
            "murphy_evidence": m_rows,
            "nison_evidence": n_rows,
            "murphy_summary": evidence_summary(m_rows),
            "nison_summary": evidence_summary(n_rows),
        }
    return out
