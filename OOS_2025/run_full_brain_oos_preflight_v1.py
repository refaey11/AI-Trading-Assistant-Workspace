from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED = {
    "context": {"timestamp", "entry_price", "atr"},
    "murphy": {"timestamp", "status", "direction"},
    "nison": {"timestamp", "confirmation", "contradiction"},
    "risk": {"timestamp", "risk_status", "stop_loss"},
}


def inspect(path: str | Path, required: set[str], name: str) -> dict[str, object]:
    p = Path(path)
    if not p.exists():
        return {"name": name, "path": str(p), "present": False, "usable": False, "reason": "MISSING_FILE"}
    try:
        df = pd.read_csv(p)
    except Exception as exc:
        return {"name": name, "path": str(p), "present": True, "usable": False, "reason": f"READ_ERROR:{exc}"}
    missing = sorted(required - set(df.columns))
    if missing:
        return {"name": name, "path": str(p), "present": True, "usable": False, "reason": f"MISSING_COLUMNS:{missing}"}
    if df["timestamp"].duplicated().any():
        return {"name": name, "path": str(p), "present": True, "usable": False, "reason": "DUPLICATE_TIMESTAMPS"}
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if ts.isna().any():
        return {"name": name, "path": str(p), "present": True, "usable": False, "reason": "INVALID_TIMESTAMPS"}
    return {
        "name": name,
        "path": str(p),
        "present": True,
        "usable": True,
        "rows": int(len(df)),
        "start": ts.min().isoformat(),
        "end": ts.max().isoformat(),
        "years": sorted({int(x.year) for x in ts}),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    for name in REQUIRED:
        p.add_argument(f"--{name}", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--year", action="append", type=int, required=True)
    args = p.parse_args()

    report = {
        "mode": "FULL_DECISION_BRAIN_OOS_PREFLIGHT",
        "years": args.year,
        "streams": [inspect(getattr(args, name), required, name) for name, required in REQUIRED.items()],
        "canonical_policy": {
            "nison_confirmation_only": True,
            "tiz_process_only": True,
            "risk_hard_gate": True,
            "historical_memory_evidence_only": True,
            "2025_is_oos": True,
            "no_tuning": True,
        },
    }

    streams = report["streams"]
    usable = {x["name"]: x["usable"] for x in streams}
    report["fully_joinable_input"] = all(usable.values())
    report["missing_streams"] = [x["name"] for x in streams if not x["usable"]]
    report["profitability_ready"] = bool(report["fully_joinable_input"])
    report["fail_closed"] = True
    report["reason"] = (
        "All required evidence streams are present and structurally usable."
        if report["profitability_ready"]
        else "Do not claim profitability until every required stream is present and joinable."
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["profitability_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
