from __future__ import annotations
import argparse, json, re
from pathlib import Path
import pandas as pd

LOCKED_YEAR = 2025


def quality_flag(row: pd.Series) -> str:
    md = str(row.get("murphy_direction", "NONE")).upper()
    state = str(row.get("brain_state", "unknown")).lower()
    bias = str(row.get("brain_bias", "NONE")).upper()
    if md not in {"BULLISH", "BEARISH"}:
        return "NO_MURPHY_DIRECTION"
    if state == "trend" and bias == md:
        return "HIGH_CONTEXT_ALIGNMENT"
    if state == "trend" and bias in {"BULLISH", "BEARISH"} and bias != md:
        return "LOW_CONTEXT_CONFLICT"
    if state == "uncertain":
        return "REVIEW_UNCERTAIN"
    return "NEUTRAL_CONTEXT"


def runtime_registry_check(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r"MURPHY_(\d{4})", text)))
    expected = {f"{i:04d}" for i in range(1, 52)} - {f"{i:04d}" for i in (1,2,5,10,11,12,13,14,15,16,17,20,24,27)}
    # Project runtime has a curated set; report exact registered IDs rather than inventing missing rule registrations.
    registered = {f"MURPHY_{x}" for x in ids}
    return {
        "runtime_entrypoint_present": True,
        "registered_rule_ids": sorted(registered),
        "registered_rule_count": len(registered),
        "expected_curated_ids_count": len(expected),
        "historical_full_rule_stream_present": False,
        "reason": "Existing runtime entrypoint is available, but no authoritative pre-2025 full per-timestamp 34-rule evidence stream is wired into this shadow job; no synthetic evidence is created.",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--runtime-entrypoint", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    a = p.parse_args()
    if a.year >= LOCKED_YEAR:
        raise ValueError("2025_OOS_LOCKED")

    df = pd.read_csv(a.input)
    required = {"timestamp", "murphy_direction", "brain_state", "brain_bias", "brain_confidence"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError("Invalid timestamps")

    df["quality_flag"] = df.apply(quality_flag, axis=1)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output, index=False)

    directional = df[df["murphy_direction"].isin(["BULLISH", "BEARISH"])].copy()
    counts = directional["quality_flag"].value_counts(dropna=False).to_dict()
    quality_summary = []
    for flag, group in directional.groupby("quality_flag", dropna=False):
        rec = {"quality_flag": flag, "signals": int(len(group))}
        for n in (12, 24, 48):
            col = f"fwd{n}_signed_return"
            if col not in group.columns:
                continue
            x = pd.to_numeric(group[col], errors="coerce").dropna()
            rec[f"fwd{n}_count"] = int(len(x))
            rec[f"fwd{n}_hit_rate_pct"] = round(100.0 * float((x > 0).mean()), 4) if len(x) else 0.0
            rec[f"fwd{n}_mean_signed_return"] = float(x.mean()) if len(x) else 0.0
        quality_summary.append(rec)

    runtime = runtime_registry_check(a.runtime_entrypoint)
    summary = {
        "status": "PASS_SHADOW_ONLY",
        "mode": "REAL_DATA_PRE2025_CONTEXT_QUALITY_SHADOW_V1",
        "evaluation_year": a.year,
        "pair": "GBPUSD",
        "events": int(len(df)),
        "murphy_directional_events": int(len(directional)),
        "quality_flags": quality_summary,
        "quality_flag_definition": {
            "HIGH_CONTEXT_ALIGNMENT": "Brain trend + Brain bias agrees with Murphy direction.",
            "LOW_CONTEXT_CONFLICT": "Brain trend + Brain bias disagrees with Murphy direction.",
            "NEUTRAL_CONTEXT": "Murphy directional event outside the trend-alignment/conflict states.",
            "REVIEW_UNCERTAIN": "Brain market state is uncertain.",
        },
        "policy_changed": False,
        "new_rule_semantics": False,
        "replacement_pnl": False,
        "oos_2025_locked": True,
        "oos_tuning": False,
        "future_feature_leakage": False,
        "runtime_registry": runtime,
        "historical_full_rule_stream_used": False,
    }
    a.output.with_suffix(".json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
