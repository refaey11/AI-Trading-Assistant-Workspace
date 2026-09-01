from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


STAGE_ALIASES = {
    "candidate": ["candidate", "opportunity", "setup_candidate", "is_candidate"],
    "structure": ["structure_pass", "structure_valid", "market_structure_pass"],
    "confirmation": ["confirmation_pass", "nison_confirmation", "nison_pass", "confirmed"],
    "brain": ["brain_eligible", "decision_eligible", "brain_pass", "decision"],
    "risk": ["risk_pass", "risk_eligible", "risk_ok"],
    "execution": ["executable", "execution_allowed", "trade_executed"],
}

REASON_ALIASES = [
    "rejection_reason",
    "reject_reason",
    "blocked_reason",
    "decision_reason",
    "reason",
]


def _find_col(df: pd.DataFrame, names: list[str]) -> str | None:
    lower = {str(c).lower(): c for c in df.columns}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return None


def _truthy(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    s = series.astype("string").str.strip().str.upper()
    return s.isin({"1", "TRUE", "T", "YES", "Y", "PASS", "PASSED", "OK", "EXECUTABLE", "BUY", "SELL"})


def choose_event_file(root: Path, explicit: Path | None) -> Path:
    if explicit:
        return explicit
    candidates: list[Path] = []
    for p in root.rglob("*.csv"):
        try:
            df = pd.read_csv(p, nrows=5)
        except Exception:
            continue
        cols = {str(c).lower() for c in df.columns}
        if "timestamp" in cols and (
            {"risk_pass", "executable"} <= cols
            or {"risk_pass", "execution_allowed"} <= cols
            or "rejection_reason" in cols
            or "decision" in cols
        ):
            candidates.append(p)
    if not candidates:
        raise SystemExit("BLOCKED_NO_DECISION_EVENT_CSV_DISCOVERED")
    candidates.sort(key=lambda p: (p.stat().st_size, str(p)), reverse=True)
    return candidates[0]


def audit(path: Path) -> dict:
    df = pd.read_csv(path, low_memory=False)
    report: dict = {
        "status": "PASS",
        "source": str(path),
        "rows": int(len(df)),
        "stages": {},
        "rejection_reason_counts": {},
        "notes": [],
    }

    if "timestamp" not in {str(c).lower() for c in df.columns}:
        report["status"] = "BLOCKED"
        report["notes"].append("timestamp column missing")
        return report

    ts_col = _find_col(df, ["timestamp"])
    ts = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    valid_ts = ts.notna()
    report["valid_timestamp_rows"] = int(valid_ts.sum())
    if not valid_ts.all():
        report["notes"].append("some rows have invalid timestamps")

    for stage, aliases in STAGE_ALIASES.items():
        col = _find_col(df, aliases)
        if col is None:
            report["stages"][stage] = {"column": None, "available": False}
            continue
        truth = _truthy(df[col])
        report["stages"][stage] = {
            "column": str(col),
            "available": True,
            "pass_rows": int(truth.sum()),
            "pass_rate": float(truth.mean()),
        }

    reason_col = _find_col(df, REASON_ALIASES)
    if reason_col is not None:
        counts = df[reason_col].astype("string").fillna("<EMPTY>").value_counts(dropna=False)
        report["rejection_reason_column"] = str(reason_col)
        report["rejection_reason_counts"] = {str(k): int(v) for k, v in counts.items()}
    else:
        report["notes"].append("no rejection-reason column was found; stage attribution is partial")

    # Daily trade density is observational only; it does not alter any strategy logic.
    exec_col = _find_col(df, STAGE_ALIASES["execution"])
    if exec_col is not None and ts_col is not None:
        executed = _truthy(df[exec_col])
        daily = pd.DataFrame({"ts": ts, "executed": executed}).dropna(subset=["ts"])
        daily = daily[daily["executed"]]
        if not daily.empty:
            per_day = daily.assign(day=daily["ts"].dt.date).groupby("day").size()
            report["executed_trade_density"] = {
                "days_with_trades": int(len(per_day)),
                "mean_trades_per_active_day": float(per_day.mean()),
                "median_trades_per_active_day": float(per_day.median()),
                "max_trades_in_day": int(per_day.max()),
            }

    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--events", type=Path, default=None)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    event_file = choose_event_file(args.root, args.events)
    report = audit(event_file)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
