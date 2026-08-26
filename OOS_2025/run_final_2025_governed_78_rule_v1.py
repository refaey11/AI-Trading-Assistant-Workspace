from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from OOS_2025.run_final_2025_decision_brain_and_pnl_v1 import backtest


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def build_nison_full_envelope(raw_csv: Path, out_csv: Path) -> None:
    raw = pd.read_csv(raw_csv)
    required = {"timestamp", "rule_id", "status"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Nison raw evidence missing columns: {sorted(missing)}")
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True, errors="coerce")
    raw = raw[raw["timestamp"].dt.year.eq(2025)].copy()
    if raw["rule_id"].nunique() != 44:
        raise AssertionError("Nison full production did not emit all 44 rule IDs")
    raw = raw.rename(columns={"rule_id": "source_rule_id"})
    raw["evidence_available"] = raw.get("available", raw["status"].isin(["PASS", "FAIL"]))
    raw["evidence_source"] = "nison_2025_full_production"
    keep = [c for c in raw.columns if c != "timestamp"]
    out = raw[["timestamp", *keep]].sort_values(["timestamp", "source_rule_id"], kind="stable")
    out.to_csv(out_csv, index=False)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--murphy-0022-0023", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()

    out = a.output_dir
    out.mkdir(parents=True, exist_ok=True)

    nison_raw = out / "NISON_2025_FULL_EVIDENCE.csv"
    run([
        "python", "OOS_2025/run_nison_2025_full_production_v1.py",
        "--input", str(a.h1),
        "--output", str(nison_raw),
        "--manifest", str(out / "NISON_2025_FULL_EVIDENCE_MANIFEST.json"),
    ])
    nison_full = out / "NISON_2025_FULL_EVIDENCE_ENVELOPE.csv"
    build_nison_full_envelope(nison_raw, nison_full)

    m21 = out / "MURPHY_0021_2025.csv"
    run([
        "python", "OOS_2025/run_murphy_0021_2025_fresh_v1.py",
        "--input", str(a.h1),
        "--m1-input", str(a.m1),
        "--output", str(m21),
        "--manifest", str(out / "MURPHY_0021_MANIFEST.json"),
    ])

    m_full = out / "MURPHY_2025_FULL_EVIDENCE.csv"
    run([
        "python", "OOS_2025/build_murphy_2025_full_evidence_v1.py",
        "--h1", str(a.h1),
        "--murphy-0021", str(m21),
        "--murphy-0022-0023", str(a.murphy_0022_0023),
        "--output", str(m_full),
        "--manifest", str(out / "MURPHY_2025_FULL_EVIDENCE_MANIFEST.json"),
    ])

    token = __import__("os").environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required for final market-state acquisition")

    import urllib.request
    market = out / "GBPUSD_MARKET_STATE.csv"
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv"}),
        },
    )
    with urllib.request.urlopen(req, timeout=180) as response, market.open("wb") as fh:
        fh.write(response.read())

    ctx_dir = out / "context"
    run([
        "python", "OOS_2025/build_historical_context_execution_inputs_v1.py",
        "--source", str(market),
        "--output-dir", str(ctx_dir),
        "--year", "2025",
    ])

    m21d = pd.read_csv(m21)
    m22d = pd.read_csv(a.murphy_0022_0023)
    for d in (m21d, m22d):
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
    m21d["source_rule_id"] = "MURPHY_0021"
    m22d["source_rule_id"] = m22d["rule_id"]
    m21d["direction"] = m21d["directional_confirmation"].astype(str)
    m22d["direction"] = m22d["directional_confirmation"].astype(str)
    murphy = pd.concat([
        m21d[["timestamp", "status", "direction", "source_rule_id"]],
        m22d[["timestamp", "status", "direction", "source_rule_id"]],
    ], ignore_index=True)
    murphy["_pass"] = murphy["status"].eq("PASS").astype(int)
    priority = {"MURPHY_0022": 0, "MURPHY_0023": 1, "MURPHY_0021": 2}
    murphy["_prio"] = murphy["source_rule_id"].map(priority).fillna(99)
    murphy = murphy.sort_values(["timestamp", "_pass", "_prio"], ascending=[True, False, True]).drop_duplicates("timestamp", keep="first")
    murphy = murphy.drop(columns=["_pass", "_prio"])
    murphy_csv = out / "MURPHY_2025_CANDIDATE_STREAM.csv"
    murphy.to_csv(murphy_csv, index=False)

    risk_csv = out / "RISK_2025_EVIDENCE.csv"
    run([
        "python", "OOS_2025/build_historical_risk_evidence_v1.py",
        "--context", str(ctx_dir / "execution.csv"),
        "--murphy", str(murphy_csv),
        "--output", str(risk_csv),
        "--manifest", str(out / "RISK_2025_EVIDENCE_MANIFEST.json"),
        "--year", "2025",
    ])

    nison_candidate = out / "NISON_2025_CANDIDATE_STREAM.csv"
    nison_code = (
        "import pandas as pd; "
        "from OOS_2025.nison_2025_evidence_aggregate_v1 import aggregate_nison_evidence; "
        f"f={str(nison_raw)!r}; o={str(nison_candidate)!r}; "
        "r=pd.read_csv(f); r['timestamp']=pd.to_datetime(r['timestamp'],utc=True); "
        "a=aggregate_nison_evidence(r); "
        "p=r[r['status'].eq('PASS') & r['direction'].astype(str).isin(['BULLISH','BEARISH'])].groupby('timestamp')['rule_id'].first().rename('source_rule_id'); "
        "a=a.merge(p,on='timestamp',how='left'); a['source_rule_id']=a['source_rule_id'].fillna('NISON_NONE'); "
        "a[['timestamp','confirmation','contradiction','source_rule_id']].to_csv(o,index=False)"
    )
    run(["python", "-c", nison_code])

    events = out / "FINAL_2025_DECISION_EVENTS.csv"
    run([
        "python", "OOS_2025/full_decision_brain_historical_event_producer_v1.py",
        "--context", str(ctx_dir / "context.csv"),
        "--murphy", str(murphy_csv),
        "--nison", str(nison_candidate),
        "--murphy-full-evidence", str(m_full),
        "--nison-full-evidence", str(nison_full),
        "--risk", str(risk_csv),
        "--execution", str(ctx_dir / "execution.csv"),
        "--year", "2025",
        "--output", str(events),
        "--manifest", str(out / "FINAL_2025_DECISION_EVENTS_MANIFEST.json"),
        "--optional-tiz",
    ])

    manifest = backtest(events, a.h1, out)
    manifest["official_baseline"] = False
    manifest["full_78_rule_provenance"] = True
    (out / "FINAL_2025_GOVERNED_78_RULE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
