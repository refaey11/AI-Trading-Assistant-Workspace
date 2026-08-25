from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

from run_final_2025_decision_brain_and_pnl_v1 import (
    backtest,
    build_nison_candidate,
    download_dropbox,
    read_csv,
    run,
)


def normalize_full_evidence(source_csv: Path, output_csv: Path, family: str) -> None:
    df = pd.read_csv(source_csv)
    if "timestamp" not in df.columns:
        raise ValueError(f"{family}: missing timestamp")
    rule_col = "rule_id" if "rule_id" in df.columns else "source_rule_id"
    if rule_col not in df.columns:
        raise ValueError(f"{family}: missing rule_id/source_rule_id")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{family}: invalid timestamps")
    df["source_rule_id"] = df[rule_col].astype(str)
    df = df.sort_values(["timestamp", "source_rule_id"], kind="stable").reset_index(drop=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)


def assert_full_manifest(path: Path, events_path: Path | None = None) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))

    # Accept both the current receipt keys and the older per-event receipt keys.
    # The event stream remains the source of truth when top-level receipt fields
    # are absent. This is bookkeeping compatibility only; it does not alter any
    # rule semantics or the Decision Brain decision path.
    murphy_count = manifest.get("murphy_rule_count")
    nison_count = manifest.get("nison_rule_count")
    if murphy_count is None:
        murphy_count = manifest.get("murphy_rule_count_in_event")
    if nison_count is None:
        nison_count = manifest.get("nison_rule_count_in_event")

    if (murphy_count is None or nison_count is None) and events_path is not None and events_path.exists():
        events = pd.read_csv(events_path)
        required = {"murphy_rule_count", "nison_rule_count"}
        if not required.issubset(events.columns) or events.empty:
            raise AssertionError("Final event stream lacks governed 34+44 rule-count columns")
        if not (events["murphy_rule_count"] == 34).all():
            raise AssertionError("Final event stream contains a row without exactly 34 Murphy rules")
        if not (events["nison_rule_count"] == 44).all():
            raise AssertionError("Final event stream contains a row without exactly 44 Nison rules")
        murphy_count = int(events["murphy_rule_count"].min())
        nison_count = int(events["nison_rule_count"].min())
        manifest["murphy_rule_count"] = murphy_count
        manifest["nison_rule_count"] = nison_count
        manifest["event_stream_rule_counts_derived"] = True
        path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

    if murphy_count != 34:
        raise AssertionError(f"Final manifest Murphy count != 34: {manifest}")
    if nison_count != 44:
        raise AssertionError(f"Final manifest Nison count != 44: {manifest}")

    if manifest.get("fan_in_mode") != "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT":
        raise AssertionError(f"Unexpected fan-in mode: {manifest}")
    if manifest.get("oos_tuning") is not False:
        raise AssertionError(f"2025 tuning guard failed: {manifest}")
    if manifest.get("new_rule_semantics") is not False:
        raise AssertionError(f"Rule semantics guard failed: {manifest}")
    return manifest


def write_no_trade_diagnostic(profitability_manifest: dict, output: Path) -> Path:
    provenance = profitability_manifest.get("final_brain_provenance", {})
    source = provenance.get("source_manifest", {})
    core = profitability_manifest.get("core", {})
    diagnostic = {
        "events": source.get("events"),
        "executable": source.get("executable"),
        "no_trade": source.get("no_trade"),
        "not_evaluable": source.get("not_evaluable"),
        "murphy_rule_count_in_event": source.get("murphy_rule_count_in_event", provenance.get("murphy_rule_count")),
        "nison_rule_count_in_event": source.get("nison_rule_count_in_event", provenance.get("nison_rule_count")),
        "tiz_verified_events": source.get("tiz_verified_events"),
        "primary_reason_counts": source.get("primary_reason_counts", {}),
        "event_status_counts": source.get("event_status_counts", {}),
        "execution_status_counts": source.get("execution_status_counts", {}),
        "risk_pass_counts": source.get("risk_pass_counts", {}),
        "tiz_status_counts": source.get("tiz_status_counts", {}),
        "trades": core.get("trades"),
        "pnl": core.get("pnl"),
        "total_R": core.get("total_R"),
        "expectancy_R": core.get("expectancy_R"),
        "profit_factor": core.get("profit_factor"),
        "status": profitability_manifest.get("status"),
        "read_only": True,
        "oos_tuning": source.get("oos_tuning"),
        "new_rule_semantics": source.get("new_rule_semantics"),
    }
    output.mkdir(parents=True, exist_ok=True)
    path = output / "FINAL_2025_NO_TRADE_DIAGNOSTIC.json"
    path.write_text(json.dumps(diagnostic, indent=2, sort_keys=True, default=str), encoding="utf-8")
    print("FINAL_2025_NO_TRADE_DIAGNOSTIC=" + json.dumps(diagnostic, sort_keys=True, default=str))
    return path


def main() -> int:
    p = argparse.ArgumentParser(description="Run governed 2025 Final Decision Brain with full 34+44 evidence.")
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--murphy-0022-0023", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument(
        "--validation-only",
        action="store_true",
        help="Run the governed 34+44 Final decision path and manifest checks without executing the 2025 profitability backtest.",
    )
    args = p.parse_args()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    nison_full_raw = out / "NISON_2025_FULL_EVIDENCE.csv"
    run([
        "python", "OOS_2025/run_nison_2025_full_production_v1.py",
        "--input", str(args.h1),
        "--output", str(nison_full_raw),
        "--manifest", str(out / "NISON_2025_FULL_EVIDENCE_MANIFEST.json"),
    ])

    murphy_0021 = out / "MURPHY_0021_2025.csv"
    run([
        "python", "OOS_2025/run_murphy_0021_2025_fresh_v1.py",
        "--input", str(args.h1),
        "--m1-input", str(args.m1),
        "--output", str(murphy_0021),
        "--manifest", str(out / "MURPHY_0021_MANIFEST.json"),
    ])

    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DROPBOX_ACCESS_TOKEN is required for final governed 78-rule run")

    market = out / "GBPUSD_MARKET_STATE.csv"
    download_dropbox(
        token,
        "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv",
        market,
    )
    context_dir = out / "context"
    run([
        "python", "OOS_2025/build_historical_context_execution_inputs_v1.py",
        "--source", str(market),
        "--output-dir", str(context_dir),
        "--year", "2025",
    ])

    m21d = read_csv(murphy_0021, {"timestamp", "status", "directional_confirmation"})
    m22d = read_csv(args.murphy_0022_0023, {"timestamp", "status", "directional_confirmation", "rule_id"})
    frames = []
    for d in (m21d, m22d):
        w = d.copy()
        w["source_rule_id"] = w["rule_id"].astype(str) if "rule_id" in w else "MURPHY"
        w["direction"] = w["directional_confirmation"].astype(str)
        frames.append(w[["timestamp", "status", "direction", "source_rule_id"]])
    murphy_legacy = pd.concat(frames, ignore_index=True)
    priority = {"MURPHY_0022": 0, "MURPHY_0023": 1, "MURPHY_0021": 2}
    murphy_legacy["_pass"] = murphy_legacy["status"].eq("PASS").astype(int)
    murphy_legacy["_prio"] = murphy_legacy["source_rule_id"].map(priority).fillna(99)
    murphy_legacy = murphy_legacy.sort_values(
        ["timestamp", "_pass", "_prio"], ascending=[True, False, True]
    ).drop_duplicates("timestamp", keep="first").drop(columns=["_pass", "_prio"])
    murphy_legacy_csv = out / "MURPHY_2025_CANDIDATE_STREAM.csv"
    murphy_legacy.to_csv(murphy_legacy_csv, index=False)

    risk_csv = out / "RISK_2025_EVIDENCE.csv"
    run([
        "python", "OOS_2025/build_historical_risk_evidence_v1.py",
        "--context", str(context_dir / "execution.csv"),
        "--murphy", str(murphy_legacy_csv),
        "--output", str(risk_csv),
        "--manifest", str(out / "RISK_2025_EVIDENCE_MANIFEST.json"),
        "--year", "2025",
    ])

    nison_legacy_csv = out / "NISON_2025_CANDIDATE_STREAM.csv"
    build_nison_candidate(nison_full_raw, nison_legacy_csv)

    murphy_full_raw = out / "MURPHY_2025_FULL_EVIDENCE.csv"
    run([
        "python", "OOS_2025/build_murphy_2025_full_evidence_v1.py",
        "--h1", str(args.h1),
        "--murphy-0021", str(murphy_0021),
        "--murphy-0022-0023", str(args.murphy_0022_0023),
        "--output", str(murphy_full_raw),
        "--manifest", str(out / "MURPHY_2025_FULL_EVIDENCE_MANIFEST.json"),
    ])

    murphy_full_csv = out / "MURPHY_2025_FULL_EVIDENCE_NORMALIZED.csv"
    nison_full_csv = out / "NISON_2025_FULL_EVIDENCE_NORMALIZED.csv"
    normalize_full_evidence(murphy_full_raw, murphy_full_csv, "Murphy")
    normalize_full_evidence(nison_full_raw, nison_full_csv, "Nison")

    events = out / "FINAL_2025_DECISION_EVENTS.csv"
    run([
        "python", "OOS_2025/full_decision_brain_historical_event_producer_v1.py",
        "--context", str(context_dir / "context.csv"),
        "--murphy", str(murphy_legacy_csv),
        "--nison", str(nison_legacy_csv),
        "--risk", str(risk_csv),
        "--execution", str(context_dir / "execution.csv"),
        "--murphy-full-evidence", str(murphy_full_csv),
        "--nison-full-evidence", str(nison_full_csv),
        "--year", "2025",
        "--output", str(events),
        "--manifest", str(out / "FINAL_2025_DECISION_EVENTS_MANIFEST.json"),
        "--optional-tiz",
    ])

    event_manifest = assert_full_manifest(
        out / "FINAL_2025_DECISION_EVENTS_MANIFEST.json",
        events_path=events,
    )

    if args.validation_only:
        validation = {
            "status": "PASS",
            "mode": "GOVERNED_78_RULE_VALIDATION_ONLY",
            "murphy_rule_count": 34,
            "nison_rule_count": 44,
            "fan_in_mode": "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT",
            "oos_tuning": False,
            "new_rule_semantics": False,
            "profitability_executed": False,
            "source_manifest": event_manifest,
        }
        (out / "FINAL_2025_GOVERNED_78_RULE_VALIDATION_MANIFEST.json").write_text(
            json.dumps(validation, indent=2, default=str), encoding="utf-8"
        )
        print(json.dumps(validation, indent=2, default=str))
        return 0

    profitability = backtest(events, args.h1, out)
    profitability["final_brain_provenance"] = {
        "murphy_rule_count": 34,
        "nison_rule_count": 44,
        "fan_in_mode": "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT",
        "source_manifest": event_manifest,
    }
    profitability_manifest_path = out / "FINAL_2025_GOVERNED_78_RULE_MANIFEST.json"
    profitability_manifest_path.write_text(
        json.dumps(profitability, indent=2, default=str), encoding="utf-8"
    )

    # The existing CircleCI final job already stores /tmp/artifacts. Publish the
    # canonical diagnostic there so it survives the CI container and is visible
    # in the job's Artifacts tab without changing the main CI wiring.
    write_no_trade_diagnostic(profitability, Path("/tmp/artifacts"))

    print(json.dumps(profitability, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
