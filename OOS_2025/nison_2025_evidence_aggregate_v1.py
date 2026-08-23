from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = {"timestamp", "rule_id", "status", "direction"}
ALLOWED_STATUSES = {"PASS", "FAIL", "NOT_EVALUABLE"}
DIRECTIONAL = {"BULLISH", "BEARISH"}


def aggregate_nison_evidence(evidence: pd.DataFrame) -> pd.DataFrame:
    """Compress per-rule Nison evidence to one governed record per timestamp.

    This is an evidence normalization layer only. It never creates direction,
    upgrades missing evidence to PASS, or reinterprets existing rule semantics.
    A timestamp has confirmation available only when an existing Nison runtime
    produced a directional PASS. A directional FAIL is treated as contradiction
    only when that direction is explicitly present in the runtime output.
    """
    missing = REQUIRED_COLUMNS - set(evidence.columns)
    if missing:
        raise ValueError(f"Missing required evidence columns: {sorted(missing)}")

    work = evidence.copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True)
    bad_status = ~work["status"].isin(ALLOWED_STATUSES)
    if bad_status.any():
        raise ValueError("Evidence contains unsupported status values")

    rows: list[dict[str, Any]] = []
    for timestamp, group in work.groupby("timestamp", sort=True):
        directional_pass = sorted({str(x) for x in group.loc[group["status"].eq("PASS"), "direction"] if str(x) in DIRECTIONAL})
        directional_fail = sorted({str(x) for x in group.loc[group["status"].eq("FAIL"), "direction"] if str(x) in DIRECTIONAL})

        contradiction = bool(directional_fail)
        if directional_pass:
            confirmation = directional_pass[0] if len(directional_pass) == 1 else "CONFLICTED"
        else:
            confirmation = "ABSENT"

        rows.append(
            {
                "timestamp": timestamp.isoformat(),
                "confirmation": confirmation,
                "confirmation_available": bool(directional_pass),
                "contradiction": contradiction,
                "directional_pass_count": int(len(directional_pass)),
                "directional_fail_count": int(len(directional_fail)),
                "rule_pass_count": int((group["status"] == "PASS").sum()),
                "rule_fail_count": int((group["status"] == "FAIL").sum()),
                "rule_not_evaluable_count": int((group["status"] == "NOT_EVALUABLE").sum()),
                "rules_seen": int(group["rule_id"].nunique()),
                "source": "Nison runtime evidence aggregate",
                "lookahead": "none",
            }
        )

    return pd.DataFrame(rows)


def write_aggregate(
    evidence_csv: str | Path,
    output_csv: str | Path,
    output_manifest: str | Path,
) -> dict[str, Any]:
    evidence = pd.read_csv(evidence_csv)
    aggregate = aggregate_nison_evidence(evidence)
    output_csv = Path(output_csv)
    output_manifest = Path(output_manifest)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    aggregate.to_csv(output_csv, index=False)

    manifest = {
        "input_rows": int(len(evidence)),
        "timestamp_rows": int(len(aggregate)),
        "confirmation_available_timestamps": int(aggregate["confirmation_available"].sum()),
        "contradiction_timestamps": int(aggregate["contradiction"].sum()),
        "confirmation_counts": aggregate["confirmation"].value_counts().to_dict(),
        "oos_policy": "2025 is evaluation-only; no tuning or threshold selection",
        "direction_creation_policy": "Nison aggregate never creates standalone direction",
    }
    output_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return manifest


if __name__ == "__main__":
    raise SystemExit(0)
