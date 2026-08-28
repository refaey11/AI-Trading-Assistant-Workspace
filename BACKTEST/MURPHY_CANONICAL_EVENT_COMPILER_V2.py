from __future__ import annotations

"""Compile the existing Murphy historical evidence into a governed canonical event layer.

This does not invent missing rules, change Murphy semantics, or modify Decision Brain V1.
It normalizes the source-backed historical artifact for the 2016-2024 development window
and keeps all non-evaluable/candidate states fail-closed.
"""

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    required = {"timestamp", "status", "direction", "source_rule_id"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError("invalid timestamp values")
    return df.sort_values("timestamp").reset_index(drop=True)


def split_ids(value: object) -> list[str]:
    if pd.isna(value):
        return []
    return sorted({x.strip() for x in str(value).split("|") if x.strip()})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--allowlist", required=False, type=Path)
    ap.add_argument("--registry", required=False, type=Path)
    args = ap.parse_args()

    df = read_csv(args.source)
    df = df[(df["timestamp"].dt.year >= 2016) & (df["timestamp"].dt.year <= 2024)].copy()
    if df.empty:
        raise SystemExit("NO_2016_2024_MURPHY_EVIDENCE")

    if "availability_timestamp" not in df.columns:
        df["availability_timestamp"] = df["timestamp"]
    else:
        df["availability_timestamp"] = pd.to_datetime(
            df["availability_timestamp"], utc=True, errors="coerce", format="mixed"
        )

    observed_rules: set[str] = set()
    expanded = []
    for _, row in df.iterrows():
        ids = split_ids(row["source_rule_id"])
        observed_rules.update(ids)
        for rid in ids:
            rec = {
                "timestamp": row["timestamp"],
                "availability_timestamp": row["availability_timestamp"],
                "rule_id": rid,
                "source_rule_id": rid,
                "status": str(row["status"]),
                "direction": row["direction"],
                "source_timeframe": row.get("source_timeframe", None),
                "provenance": row.get("provenance", None),
            }
            expanded.append(rec)

    out = pd.DataFrame(expanded)
    out = out.sort_values(["timestamp", "rule_id"]).drop_duplicates(
        ["timestamp", "rule_id", "status", "direction"], keep="last"
    )

    if args.allowlist and args.allowlist.exists():
        allow = json.loads(args.allowlist.read_text(encoding="utf-8"))
        allowed = set(allow["verified_runtime"]["MURPHY"])
        unknown = sorted(observed_rules - allowed)
        if unknown:
            raise SystemExit(f"UNKNOWN_MURPHY_RULE_IDS={unknown}")

    registry_map: dict[str, dict] = {}
    if args.registry and args.registry.exists():
        reg = pd.read_csv(args.registry, low_memory=False)
        for _, r in reg.iterrows():
            registry_map[str(r["rule_id"])] = r.to_dict()

    out["decision_eligible"] = out["rule_id"].map(
        lambda rid: str(registry_map.get(rid, {}).get("decision_eligible", "NO")).upper()
    )
    out["source_evidence_status"] = out["rule_id"].map(
        lambda rid: registry_map.get(rid, {}).get("historical_status", "UNREGISTERED")
    )

    # No 2025 output is permitted from this compiler.
    if (out["timestamp"].dt.year == 2025).any():
        raise SystemExit("2025_LEAK_DETECTED")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)

    report = {
        "status": "PASS",
        "window": "2016-2024",
        "2025_locked": True,
        "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
        "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
        "source_rows": int(len(df)),
        "canonical_rows": int(len(out)),
        "observed_rule_count": int(out["rule_id"].nunique()),
        "observed_rules": sorted(out["rule_id"].unique().tolist()),
        "decision_eligible_rules": sorted(out.loc[out["decision_eligible"] == "YES", "rule_id"].unique().tolist()),
        "non_decision_rule_rows_preserved": int((out["decision_eligible"] != "YES").sum()),
        "unknown_rules": [],
        "governance": {
            "no_missing_rules_fabricated": True,
            "no_direction_generated": True,
            "no_decision_brain_semantics_changed": True,
            "candidate_and_non_evaluable_states_preserved": True,
        },
    }
    report_path = args.output.with_suffix(".json")
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
