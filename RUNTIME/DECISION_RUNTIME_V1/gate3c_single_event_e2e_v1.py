"""Gate 3C single-real-event E2E runner.

This runner consumes ONE already-extracted, source-backed canonical event.
It does not build rules, invent MTF values, create TIZ state, or synthesize
Risk/account state. It composes the existing governed_78 adapter, recovered
Decision Brain V1 bridge, Three-Book evaluator and execution boundary.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _require_iso(ts: Any) -> str:
    if not isinstance(ts, str) or "T" not in ts:
        raise ValueError("query_as_of must be an ISO timestamp string")
    return ts


def _ids(rows: Any) -> list[str]:
    out: list[str] = []
    for row in rows or []:
        if isinstance(row, Mapping):
            rid = str(row.get("source_rule_id") or row.get("rule_id") or "").strip()
            if rid:
                out.append(rid)
    return out


def run(event: Mapping[str, Any]) -> dict[str, Any]:
    ts = _require_iso(event.get("query_as_of"))
    year = int(ts[:4])
    if not (2016 <= year <= 2024):
        raise ValueError("Gate 3C event must be in development window 2016-2024")

    mtf = dict(event.get("mtf") or {})
    required_mtf = {
        "mtf_trend_score", "M5_trend_regime", "M15_trend_regime",
        "M30_trend_regime", "H1_trend_regime", "H4_trend_regime",
        "D1_trend_regime",
    }
    missing_mtf = sorted(k for k in required_mtf if k not in mtf or mtf[k] in (None, ""))
    if missing_mtf:
        return {"status": "BLOCKED", "stage": "MTF", "reason": "MISSING_MTF_FIELDS", "missing": missing_mtf}

    murphy_rows = list((event.get("murphy") or {}).get("rows") or [])
    nison_rows = list((event.get("nison") or {}).get("rows") or [])
    if len(set(_ids(murphy_rows))) != 34:
        return {"status": "BLOCKED", "stage": "MURPHY", "reason": "MURPHY_34_ENVELOPE_REQUIRED", "observed": sorted(set(_ids(murphy_rows)))}
    if len(set(_ids(nison_rows))) != 44:
        return {"status": "BLOCKED", "stage": "NISON", "reason": "NISON_44_ENVELOPE_REQUIRED", "observed_count": len(set(_ids(nison_rows)))}

    adapter = _load_module(ROOT / "compatibility" / "governed_78_rule_adapter_v1.py", "governed_78")
    pkg = adapter.build_governed_78_package(
        query_as_of=ts,
        murphy_rows=murphy_rows,
        nison_rows=nison_rows,
        mode="development",
        provenance=event.get("provenance") or {"gate": "3C", "symbol": event.get("symbol", "GBPUSD")},
    )
    if pkg.status != "PASS":
        return {"status": "BLOCKED", "stage": "RULE_ADAPTER", "reason": pkg.reason, "adapter_status": pkg.status}
    adapter.assert_governed_78_package(pkg.package)

    risk = dict(event.get("risk") or {})
    if risk.get("authoritative") is not True:
        return {"status": "BLOCKED", "stage": "RISK", "reason": "RISK_ACCOUNT_STATE_OR_RESULT_NOT_AUTHORITATIVE"}
    if risk.get("risk_pass") is not True:
        return {"status": "BLOCKED", "stage": "RISK", "reason": risk.get("reason", "RISK_FAIL"), "risk": risk}

    tiz = dict(event.get("tiz") or {})
    # TIZ is optional/process-only: lack of authoritative TIZ is recorded, not
    # converted into market direction. The existing bridge accepts this mode.
    tiz.setdefault("authoritative", False)
    tiz.setdefault("status", "NOT_EVALUABLE")

    bridge = _load_module(ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "full_brain_runtime_bridge_v1.py", "brain_bridge")
    result = bridge.run_full_brain_cycle(
        row=dict(event.get("brain_row") or {}),
        query_as_of=ts,
        murphy_evidence={"status": "PASS", "rows": murphy_rows, "authoritative": True},
        nison_evidence={"status": "PASS", "rows": nison_rows, "authoritative": True, "confirmation": (event.get("nison") or {}).get("confirmation", "ABSENT"), "contradiction": bool((event.get("nison") or {}).get("contradiction", False))},
        risk_evidence=risk,
        tiz_evidence=tiz,
        historical_evidence=event.get("historical") or {},
        source_rule_ids=sorted(set(_ids(murphy_rows) + _ids(nison_rows))),
        entry_price=event.get("entry_price"),
        atr=event.get("atr"),
        mode="development",
    )

    output = {
        "status": result.get("status"),
        "query_as_of": ts,
        "symbol": event.get("symbol", "GBPUSD"),
        "rule_envelope": {"murphy": 34, "nison": 44},
        "mtf": {k: mtf[k] for k in sorted(required_mtf)},
        "tiz": {"authoritative": tiz.get("authoritative"), "status": tiz.get("status")},
        "risk": {k: risk.get(k) for k in ("authoritative", "risk_pass", "risk_percent", "stop_loss", "take_profit", "rr", "position_size", "reason")},
        "brain_execution_result": result,
        "governance": {
            "brain_v1_unchanged": True,
            "murphy_generates_primary_context": True,
            "nison_generates_direction": False,
            "tiz_generates_direction": False,
            "memory_generates_direction": False,
            "future_data_allowed": False,
            "oos_tuning": False,
        },
    }
    if result.get("status") == "EXECUTABLE":
        output["gate3c"] = "PASS"
    else:
        output["gate3c"] = "BLOCKED"
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    event = json.loads(args.event.read_text(encoding="utf-8"))
    result = run(event)
    args.output.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("gate3c") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
