from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"


def read_source(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    required = {"timestamp", "status", "direction", "source_rule_id"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df[(df["timestamp"].dt.year >= 2016) & (df["timestamp"].dt.year <= 2024)].copy()


def split_ids(value: Any) -> list[str]:
    if pd.isna(value):
        return []
    return [x.strip() for x in str(value).split("|") if x.strip()]


def norm_direction(value: Any) -> str | None:
    s = str(value or "").strip().upper()
    if s in {"BUY", "BULL", "BULLISH"}:
        return "BULLISH"
    if s in {"SELL", "BEAR", "BEARISH"}:
        return "BEARISH"
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--murphy", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    allow = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    governed = sorted(set(allow["verified_runtime"]["MURPHY"]))
    blocked = {x["rule_id"] for x in allow.get("explicitly_blocked", [])}
    df = read_source(args.murphy)

    rows: list[dict[str, Any]] = []
    expanded_records: list[tuple[str, pd.Series]] = []
    for _, row in df.iterrows():
        ids = split_ids(row["source_rule_id"])
        for rule_id in ids:
            expanded_records.append((rule_id, row))

    observed = {rid for rid, _ in expanded_records}
    unknown = sorted(observed - set(governed) - blocked)
    if unknown:
        raise ValueError(f"Unknown Murphy rule IDs in source: {unknown}")

    for rule_id in governed:
        recs = [r for rid, r in expanded_records if rid == rule_id]
        if not recs:
            rows.append({
                "rule_id": rule_id,
                "runtime_governed": True,
                "historical_source_present": False,
                "blocked": rule_id in blocked,
                "source_rows": 0,
                "pass_rows": 0,
                "fail_rows": 0,
                "directional_pass_rows": 0,
                "first_source_timestamp": None,
                "last_source_timestamp": None,
                "historical_status": "RUNTIME_ONLY",
            })
            continue
        sdf = pd.DataFrame(recs)
        status = sdf["status"].astype(str).str.upper()
        directions = sdf["direction"].map(norm_direction)
        directional = status.eq("PASS") & directions.notna()
        rows.append({
            "rule_id": rule_id,
            "runtime_governed": True,
            "historical_source_present": True,
            "blocked": rule_id in blocked,
            "source_rows": int(len(sdf)),
            "pass_rows": int(status.eq("PASS").sum()),
            "fail_rows": int(status.eq("FAIL").sum()),
            "directional_pass_rows": int(directional.sum()),
            "first_source_timestamp": sdf["timestamp"].min().isoformat(),
            "last_source_timestamp": sdf["timestamp"].max().isoformat(),
            "historical_status": "SOURCE_BACKED",
        })

    report = pd.DataFrame(rows).sort_values("rule_id").reset_index(drop=True)
    observed_count = int(report["historical_source_present"].sum())
    directional_count = int((report["directional_pass_rows"] > 0).sum())
    summary = {
        "governed_murphy_rules": len(governed),
        "historical_source_backed_rules": observed_count,
        "historical_rules_with_directional_pass": directional_count,
        "runtime_only_rules": len(governed) - observed_count,
        "blocked_rule_ids": sorted(blocked & set(governed)),
        "unknown_source_rule_ids": unknown,
        "development_window": "2016-2024",
        "2025_locked": True,
        "synthetic_evidence_created": False,
        "source_rule_id_fan_in_split_lossless": True,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)
    summary_path = args.output.with_name(args.output.stem + "_SUMMARY.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
