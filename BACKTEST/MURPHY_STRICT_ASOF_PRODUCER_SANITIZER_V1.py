"""Diagnostic-only strict-as-of producer sanitizer for Murphy 34 recovery.

Consumes MURPHY_PRODUCER_FAMILY_INVENTORY_V1.csv or equivalent producer inventory and
emits a deterministic audit report. It does NOT modify fan-in, eligibility, or evidence.

Policy:
- Historical window is 2016-01-01 through 2024-12-31 inclusive.
- Any row whose availability timestamp is >= decision timestamp is rejected.
- Any row with availability timestamp in 2025 is rejected.
- Rows without an explicit availability timestamp are not promoted; they are flagged.
- No imputation or guessing.
"""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("artifacts/murphy_34_workspace_audit")
INPUT = ROOT / "MURPHY_PRODUCER_FAMILY_INVENTORY_V1.csv"
OUT_JSON = ROOT / "MURPHY_STRICT_ASOF_PRODUCER_SANITIZER_V1.json"
OUT_CSV = ROOT / "MURPHY_STRICT_ASOF_PRODUCER_SANITIZER_V1.csv"

FAMILIES = {
    "FOUR_WEEK_LOOKBACK_V1_OUTPUT", "DMI_ADX_V1_OUTPUT", "PARABOLIC_SAR_V1_OUTPUT",
    "OSCILLATOR_DIVERGENCE_V1_OUTPUT", "TRENDLINE_GEOMETRY_V1_OUTPUT", "OBV_V1_OUTPUT",
    "VOLUME_CONFIRMATION_V2_OUTPUT", "VOLUME_CONFIRMATION_INTEGRATION_V1_OUTPUT",
    "OPEN_INTEREST_V1_OUTPUT", "PIVOT_SEQUENCE_V1_OUTPUT", "PIVOT_SEQUENCE_V2_OUTPUT",
}

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")

def parse_dt(s: str):
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except Exception:
        return None

def pick(row, *keys):
    nm = {norm(k): v for k,v in row.items()}
    for k in keys:
        if norm(k) in nm and nm[norm(k)] not in (None, ""):
            return nm[norm(k)]
    return ""

def main():
    rows = []
    with INPUT.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    out = []
    stats = {"rows": len(rows), "in_window": 0, "reject_2025": 0, "reject_equal_or_later": 0, "missing_availability": 0, "passed_strict_asof": 0}
    family_stats = {}
    for r in rows:
        family = pick(r, "producer_family", "family", "producer_family_name")
        decision_ts = parse_dt(pick(r, "decision_timestamp", "bar_timestamp", "signal_timestamp", "event_timestamp"))
        avail_ts = parse_dt(pick(r, "availability_timestamp", "available_at", "producer_availability_timestamp"))
        year_basis = decision_ts.year if decision_ts else None
        status = "UNVERIFIED"
        reason = "missing_decision_timestamp"
        if decision_ts:
            if not (datetime(2016,1,1,tzinfo=timezone.utc) <= decision_ts < datetime(2025,1,1,tzinfo=timezone.utc)):
                status, reason = "OUTSIDE_2016_2024", "decision_timestamp_outside_locked_window"
            else:
                stats["in_window"] += 1
                if avail_ts is None:
                    stats["missing_availability"] += 1
                    status, reason = "UNVERIFIED", "missing_availability_timestamp"
                elif avail_ts >= datetime(2025,1,1,tzinfo=timezone.utc):
                    stats["reject_2025"] += 1
                    status, reason = "REJECT", "availability_timestamp_in_2025"
                elif avail_ts >= decision_ts:
                    stats["reject_equal_or_later"] += 1
                    status, reason = "REJECT", "availability_not_strictly_prior"
                else:
                    stats["passed_strict_asof"] += 1
                    status, reason = "PASS", "strictly_prior_and_in_locked_window"
        family_stats.setdefault(family, {"rows":0,"PASS":0,"REJECT":0,"UNVERIFIED":0,"OUTSIDE_2016_2024":0})
        family_stats[family]["rows"] += 1
        family_stats[family].setdefault(status,0); family_stats[family][status] += 1
        out.append({"producer_family": family, "source_rule_id": pick(r,"source_rule_id","rule_id"), "decision_timestamp": decision_ts.isoformat() if decision_ts else "", "availability_timestamp": avail_ts.isoformat() if avail_ts else "", "status": status, "reason": reason})
    payload = {"policy":{"window":"2016-01-01T00:00:00Z to 2024-12-31T23:59:59.999999Z","strict_asof":"availability_timestamp < decision_timestamp","exclude_2025":True,"imputation":False},"stats":stats,"family_stats":family_stats}
    OUT_JSON.write_text(json.dumps(payload,indent=2),encoding="utf-8")
    with OUT_CSV.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(out[0].keys()) if out else ["producer_family","source_rule_id","decision_timestamp","availability_timestamp","status","reason"])
        w.writeheader(); w.writerows(out)
    print(json.dumps(payload,indent=2))

if __name__ == "__main__": main()
