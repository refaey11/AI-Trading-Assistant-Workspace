from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from MURPHY_EVALUATORS_V1.murphy_runtime_entrypoint_v1 import evaluate_rule

MURPHY_RULES = [
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007", "MURPHY_0018", "MURPHY_0019",
    "MURPHY_0021", "MURPHY_0022", "MURPHY_0023", "MURPHY_0025", "MURPHY_0026", "MURPHY_0028",
    "MURPHY_0029", "MURPHY_0030", "MURPHY_0031", "MURPHY_0032", "MURPHY_0033", "MURPHY_0034",
    "MURPHY_0035", "MURPHY_0036", "MURPHY_0037", "MURPHY_0038", "MURPHY_0039", "MURPHY_0040",
    "MURPHY_0041", "MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045", "MURPHY_0047",
    "MURPHY_0048", "MURPHY_0049", "MURPHY_0050", "MURPHY_0051",
]
SOURCE_BACKED_RULES = {"MURPHY_0021", "MURPHY_0022", "MURPHY_0023"}


def read_csv(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any() or df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: invalid or duplicated timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_source_rule_output(path: Path, rule_ids: set[str]) -> dict[pd.Timestamp, dict[str, dict]]:
    df = read_csv(path, {"timestamp", "rule_id", "status"})
    out: dict[pd.Timestamp, dict[str, dict]] = {}
    for row in df.to_dict("records"):
        rid = str(row["rule_id"])
        if rid not in rule_ids:
            continue
        ts = pd.Timestamp(row["timestamp"])
        out.setdefault(ts, {})[rid] = row
    return out


def build(h1_path: Path, murphy_0021: Path, murphy_0022_0023: Path, output: Path, manifest_path: Path) -> dict:
    h1 = read_csv(h1_path, {"timestamp", "open", "high", "low", "close"})
    h1 = h1[h1["timestamp"].dt.year.eq(2025)].copy().reset_index(drop=True)
    if h1.empty:
        raise ValueError("No 2025 H1 rows found")

    r21 = load_source_rule_output(murphy_0021, {"MURPHY_0021"})
    r2223 = load_source_rule_output(murphy_0022_0023, {"MURPHY_0022", "MURPHY_0023"})

    rows: list[dict] = []
    for ts, bar in h1.set_index("timestamp").iterrows():
        source_rows = {}
        source_rows.update(r21.get(ts, {}))
        source_rows.update(r2223.get(ts, {}))
        for rid in MURPHY_RULES:
            if rid in source_rows:
                src = source_rows[rid]
                rows.append({
                    "timestamp": ts,
                    "rule_id": rid,
                    "status": str(src.get("status", "NOT_EVALUABLE")),
                    "direction": str(src.get("directional_confirmation", "UNKNOWN")),
                    "directional_confirmation": str(src.get("directional_confirmation", "UNKNOWN")),
                    "reason": str(src.get("reason", "source_backed_runtime_output")),
                    "evidence_available": True,
                    "evidence_source": "source_backed_2025_runtime_producer",
                })
                continue

            # No source-backed payload contract exists for this rule in the current
            # 2025 producer path. Ask the canonical evaluator with an empty payload;
            # this is explicitly fail-closed and must remain NOT_EVALUABLE.
            result = evaluate_rule(rid, {})
            status = str(result.get("status", "NOT_EVALUABLE"))
            if status != "NOT_EVALUABLE":
                raise AssertionError(
                    f"{rid}: empty canonical payload produced {status}; refusing to synthesize evidence"
                )
            rows.append({
                "timestamp": ts,
                "rule_id": rid,
                "status": "NOT_EVALUABLE",
                "direction": "UNKNOWN",
                "directional_confirmation": "UNKNOWN",
                "reason": "No authoritative 2025 evidence payload is available for this rule; fail-closed.",
                "evidence_available": False,
                "evidence_source": "canonical_runtime_no_upstream_evidence",
            })

    out = pd.DataFrame(rows)
    expected = len(h1) * len(MURPHY_RULES)
    if len(out) != expected:
        raise AssertionError(f"Expected {expected} evidence rows, got {len(out)}")
    if out["rule_id"].nunique() != len(MURPHY_RULES):
        raise AssertionError("Not all 34 Murphy rule IDs are present")

    counts = out.groupby(["rule_id", "status"]).size().unstack(fill_value=0)
    manifest = {
        "status": "PASS",
        "evaluation_year": 2025,
        "rows": int(len(out)),
        "timestamps": int(len(h1)),
        "murphy_rules": len(MURPHY_RULES),
        "rule_ids": MURPHY_RULES,
        "source_backed_rules": sorted(SOURCE_BACKED_RULES),
        "fail_closed_rules": sorted(set(MURPHY_RULES) - SOURCE_BACKED_RULES),
        "status_by_rule": {
            rid: {str(k): int(v) for k, v in counts.loc[rid].to_dict().items()} if rid in counts.index else {}
            for rid in MURPHY_RULES
        },
        "oos_tuning": False,
        "new_rule_semantics": False,
        "synthetic_evidence": False,
        "not_evaluable_on_missing_upstream": True,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--murphy-0021", required=True, type=Path)
    p.add_argument("--murphy-0022-0023", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    a = p.parse_args()
    build(a.h1, a.murphy_0021, a.murphy_0022_0023, a.output, a.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
