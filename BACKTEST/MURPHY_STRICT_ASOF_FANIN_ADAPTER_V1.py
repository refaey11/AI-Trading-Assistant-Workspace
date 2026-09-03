from __future__ import annotations

"""Fail-closed Murphy fan-in adapter for producer-level strict-as-of binding.

This adapter does not create new trading evidence. It only binds already-produced
Murphy rows to explicit producer availability timestamps where a governed producer
mapping exists. Rows without a verifiable producer binding are marked
NOT_EVALUABLE and excluded from the strict fan-in output.
"""

import argparse
from pathlib import Path
import json
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
    return [x.strip() for x in str(v).split("|") if x.strip()]


def parse_ts(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce", format="mixed")


def exact_map(path: Path, ts_col: str, avail_col: str | None = None) -> dict[pd.Timestamp, pd.Timestamp]:
    df = pd.read_csv(path, low_memory=False)
    if ts_col not in df.columns:
        raise ValueError(f"MISSING_FIELD:{path}:{ts_col}")
    df[ts_col] = parse_ts(df[ts_col])
    df = df[df[ts_col].notna()].copy()
    if avail_col:
        if avail_col not in df.columns:
            raise ValueError(f"MISSING_FIELD:{path}:{avail_col}")
        df[avail_col] = parse_ts(df[avail_col])
        df = df[df[avail_col].notna()]
        return dict(zip(df[ts_col], df[avail_col]))
    return {t: t for t in df[ts_col]}


def load_sources(root: Path) -> dict[str, dict[pd.Timestamp, pd.Timestamp]]:
    out: dict[str, dict[pd.Timestamp, pd.Timestamp]] = {}
    out["volume"] = exact_map(root / "VOLUME_CONFIRMATION_V2_OUTPUT/GBPUSD_H1_VOLUME_CONTEXT_2020_2024.csv", "bar_close_timestamp")
    out["four_week"] = exact_map(root / "FOUR_WEEK_LOOKBACK_V1_OUTPUT/GBPUSD_H1_2016_2024_FOUR_WEEK_LOOKBACK.csv", "timestamp")
    out["rsi_divergence"] = exact_map(root / "OSCILLATOR_DIVERGENCE_V1_OUTPUT/GBPUSD_H1_STRUCTURE_RSI_DIVERGENCE_V1.csv", "availability_timestamp")
    oi = pd.read_csv(root / "OPEN_INTEREST_V1_OUTPUT/GBPUSD_H1_OI_ALIGNED_2020_2024.csv", low_memory=False)
    if "timestamp" not in oi.columns or "safe_availability_timestamp" not in oi.columns:
        raise ValueError("MISSING_OI_BINDING_FIELDS")
    oi["timestamp"] = parse_ts(oi["timestamp"])
    oi["safe_availability_timestamp"] = parse_ts(oi["safe_availability_timestamp"])
    oi = oi[oi.timestamp.notna() & oi.safe_availability_timestamp.notna()]
    out["oi"] = dict(zip(oi.timestamp, oi.safe_availability_timestamp))
    return out


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

    src = load_sources(args.producer_root)
    kept = []
    audit_rows = []
    for idx, row in df.iterrows():
        decision_ts = row.timestamp
        ids = clean_ids(row.source_rule_id)
        if not ids:
            audit_rows.append({"row_index": int(idx), "decision_timestamp": decision_ts, "status": "NOT_EVALUABLE", "reason": "NO_RULE_ID"})
            continue
        bindings = []
        unresolved = []
        for rid in ids:
            families = RULE_FAMILIES.get(rid)
            if not families:
                unresolved.append(f"NO_PRODUCER_MAPPING:{rid}")
                continue
            family_avails = []
            for family in families:
                a = src[family].get(decision_ts)
                if a is None:
                    unresolved.append(f"NO_SOURCE_BINDING:{rid}:{family}")
                else:
                    family_avails.append(a)
                    bindings.append((rid, family, a))
            if unresolved and any(x.startswith(f"NO_SOURCE_BINDING:{rid}:") for x in unresolved):
                continue
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
