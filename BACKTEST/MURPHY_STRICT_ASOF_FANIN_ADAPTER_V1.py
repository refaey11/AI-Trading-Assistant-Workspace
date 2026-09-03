from __future__ import annotations

"""Fail-closed Murphy fan-in adapter for producer-level strict-as-of binding.

This adapter does not create new trading evidence. It binds existing producer
observations to the latest producer availability strictly before the decision
timestamp. Rows without a verifiable producer binding remain NOT_EVALUABLE.
"""

import argparse
import bisect
import json
from pathlib import Path
import pandas as pd

RULE_FAMILIES = {
    "MURPHY_0021": ["volume"],
    "MURPHY_0022": ["volume", "oi"],
    "MURPHY_0023": ["volume", "oi"],
    "MURPHY_0025": ["four_week"],
    "MURPHY_0026": ["four_week"],
    "MURPHY_0028": ["rsi_divergence"],
    "MURPHY_0029": ["rsi_divergence"],
}


def clean_ids(v) -> list[str]:
    if pd.isna(v):
        return []
    return [x.strip() for x in str(v).split("|") if x.strip() and x.strip().upper() not in {"NONE", "NULL", "NAN"}]


def parse_ts(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce", format="mixed")


def load_availability(path: Path, time_col: str, availability_col: str | None = None) -> tuple[list[pd.Timestamp], list[pd.Timestamp]]:
    df = pd.read_csv(path, low_memory=False)
    if time_col not in df.columns:
        raise ValueError(f"MISSING_FIELD:{path}:{time_col}")
    keys = parse_ts(df[time_col])
    if availability_col is None:
        vals = keys.copy()
    else:
        if availability_col not in df.columns:
            raise ValueError(f"MISSING_FIELD:{path}:{availability_col}")
        vals = parse_ts(df[availability_col])
    keep = keys.notna() & vals.notna() & (vals.dt.year >= 2016) & (vals.dt.year <= 2024)
    pairs = sorted(zip(keys[keep].tolist(), vals[keep].tolist()), key=lambda x: x[1])
    if not pairs:
        return [], []
    # Availability is the actual lookup key. Duplicate availability instants keep the latest source row.
    by_avail: dict[pd.Timestamp, pd.Timestamp] = {}
    for _, avail in pairs:
        by_avail[avail] = avail
    avail = sorted(by_avail)
    return avail, avail


def load_sources(root: Path) -> dict[str, tuple[list[pd.Timestamp], list[pd.Timestamp]]]:
    return {
        "volume": load_availability(root / "VOLUME_CONFIRMATION_V2_OUTPUT/GBPUSD_H1_VOLUME_CONTEXT_2020_2024.csv", "bar_close_timestamp"),
        "four_week": load_availability(root / "FOUR_WEEK_LOOKBACK_V1_OUTPUT/GBPUSD_H1_2016_2024_FOUR_WEEK_LOOKBACK.csv", "timestamp"),
        "rsi_divergence": load_availability(root / "OSCILLATOR_DIVERGENCE_V1_OUTPUT/GBPUSD_H1_STRUCTURE_RSI_DIVERGENCE_V1.csv", "availability_timestamp"),
        "oi": load_availability(root / "OPEN_INTEREST_V1_OUTPUT/GBPUSD_H1_OI_ALIGNED_2020_2024.csv", "safe_availability_timestamp"),
    }


def latest_strict(avails: list[pd.Timestamp], decision_ts: pd.Timestamp) -> pd.Timestamp | None:
    # bisect_left enforces availability < decision_timestamp; equality is rejected.
    pos = bisect.bisect_left(avails, decision_ts) - 1
    return None if pos < 0 else avails[pos]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--producer-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()

    df = pd.read_csv(args.murphy, low_memory=False)
    required = {"timestamp", "source_rule_id"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_MURPHY_SCHEMA:{missing}")
    df["timestamp"] = parse_ts(df["timestamp"])
    if df.timestamp.isna().any():
        raise SystemExit("BLOCKED_MURPHY_INVALID_TIMESTAMP")
    df = df[(df.timestamp.dt.year >= 2016) & (df.timestamp.dt.year <= 2024)].copy()

    src = load_sources(args.producer_root)
    kept = []
    audit_rows = []
    for idx, row in df.iterrows():
        decision_ts = row.timestamp
        ids = clean_ids(row.source_rule_id)
        if not ids:
            audit_rows.append({"row_index": int(idx), "decision_timestamp": decision_ts, "status": "NOT_EVALUABLE", "reason": "NO_RULE_ID"})
            continue

        bindings: list[tuple[str, str, pd.Timestamp]] = []
        unresolved: list[str] = []
        for rid in ids:
            families = RULE_FAMILIES.get(rid)
            if not families:
                unresolved.append(f"NO_PRODUCER_MAPPING:{rid}")
                continue
            rule_bindings: list[tuple[str, str, pd.Timestamp]] = []
            for family in families:
                a = latest_strict(src[family][0], decision_ts)
                if a is None:
                    unresolved.append(f"NO_SOURCE_BINDING:{rid}:{family}")
                else:
                    rule_bindings.append((rid, family, a))
            if len(rule_bindings) == len(families):
                bindings.extend(rule_bindings)

        if unresolved:
            audit_rows.append({"row_index": int(idx), "decision_timestamp": decision_ts, "source_rule_id": "|".join(ids), "status": "NOT_EVALUABLE", "reason": ";".join(unresolved)})
            continue

        bad = [(rid, fam, a) for rid, fam, a in bindings if not (a < decision_ts)]
        if bad:
            audit_rows.append({"row_index": int(idx), "decision_timestamp": decision_ts, "source_rule_id": "|".join(ids), "status": "REJECT_EQUAL_OR_FUTURE", "reason": ";".join(f"{rid}:{fam}:{a.isoformat()}" for rid, fam, a in bad)})
            continue

        r = row.copy()
        r["availability_timestamp"] = max(a for _, _, a in bindings)
        r["strict_asof_status"] = "PASS"
        kept.append(r)
        audit_rows.append({"row_index": int(idx), "decision_timestamp": decision_ts, "source_rule_id": "|".join(ids), "status": "PASS", "availability_timestamp": r["availability_timestamp"]})

    result = pd.DataFrame(kept)
    if result.empty:
        result = df.iloc[0:0].copy()
        result["availability_timestamp"] = pd.Series(dtype="datetime64[ns, UTC]")
        result["strict_asof_status"] = pd.Series(dtype="object")
    result.to_csv(args.output, index=False)
    audit = pd.DataFrame(audit_rows)
    audit_path = args.output.with_name(args.output.stem + "_BINDING_AUDIT.csv")
    audit.to_csv(audit_path, index=False)

    report = {
        "status": "PASS",
        "input_rows": int(len(df)),
        "strict_pass_rows": int(len(result)),
        "rejected_or_unresolved_rows": int(len(df) - len(result)),
        "rules_with_explicit_mapping": sorted(RULE_FAMILIES),
        "operator": "availability_timestamp < decision_timestamp",
        "lookup_mode": "latest_available_strictly_before_decision",
        "synthetic_evidence_generated": False,
        "direction_generated": False,
        "2025_used": False,
        "output": str(args.output),
        "binding_audit": str(audit_path),
    }
    args.output.with_name(args.output.stem + "_REPORT.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
