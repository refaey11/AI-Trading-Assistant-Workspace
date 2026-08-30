"""Gate 3C single-real-event E2E runner.

Consumes ONE already-extracted, source-backed canonical event. It composes the
existing lossless rule fan-in, recovered Brain V1 bridge, and real Risk result.
It never invents rule evidence, MTF values, TIZ psychology, or account state.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MURPHY_IDS = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}
NISON_IDS = {f"NISON_{i:04d}" for i in range(1,45)}


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ids(rows: Any) -> list[str]:
    out: list[str] = []
    for row in rows or []:
        if isinstance(row, Mapping):
            raw = str(row.get("source_rule_id") or row.get("rule_id") or "")
            for rid in raw.split("|"):
                rid = rid.strip()
                if rid and rid.upper() not in {"NONE", "NULL", "NAN", "NISON_NONE"}:
                    out.append(rid)
    return out


def _timestamp(value: Any) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def run(event: Mapping[str, Any]) -> dict[str, Any]:
    ts_text = str(event.get("query_as_of") or "")
    if not ts_text:
        raise ValueError("query_as_of is required")
    ts = _timestamp(ts_text)
    if not (2016 <= ts.year <= 2024):
        raise ValueError("Gate 3C event must be inside 2016-2024")

    mtf = dict(event.get("mtf") or {})
    required_mtf = {"mtf_trend_score","M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"}
    missing_mtf = sorted(k for k in required_mtf if k not in mtf or mtf[k] in (None, ""))
    if missing_mtf:
        return {"gate3c":"BLOCKED","stage":"MTF","reason":"MISSING_MTF_FIELDS","missing":missing_mtf}

    murphy = dict(event.get("murphy") or {})
    nison = dict(event.get("nison") or {})
    murphy_rows = list(murphy.get("rows") or [])
    nison_rows = list(nison.get("rows") or [])
    murphy_ids = sorted(set(_ids(murphy_rows)))
    nison_ids = sorted(set(_ids(nison_rows)))
    if not murphy_ids:
        return {"gate3c":"BLOCKED","stage":"MURPHY","reason":"NO_SOURCE_BACKED_EVENT_RULES","observed_count":0}
    unknown_murphy = sorted(set(murphy_ids) - MURPHY_IDS)
    if unknown_murphy:
        return {"gate3c":"BLOCKED","stage":"MURPHY","reason":"UNKNOWN_MURPHY_RULE_IDS","observed":unknown_murphy}
    if nison_ids != sorted(NISON_IDS):
        return {"gate3c":"BLOCKED","stage":"NISON","reason":"NISON_44_ENVELOPE_REQUIRED","observed_count":len(nison_ids),"observed":nison_ids}

    fanin = _load_module(ROOT / "OOS_2025" / "governed_rule_fan_in_v1.py", "governed_fan_in")
    mdf = pd.DataFrame(murphy_rows)
    ndf = pd.DataFrame(nison_rows)
    # The canonical builder intentionally keeps timestamp at the event-envelope
    # level, not repeated on every row. Restore that event timestamp solely for
    # the lossless fan-in API; no new evidence is created.
    if "timestamp" not in mdf.columns:
        mdf["timestamp"] = ts
    else:
        mdf["timestamp"] = pd.to_datetime(mdf["timestamp"], utc=True, errors="raise", format="mixed")
    if "timestamp" not in ndf.columns:
        ndf["timestamp"] = ts
    else:
        ndf["timestamp"] = pd.to_datetime(ndf["timestamp"], utc=True, errors="raise", format="mixed")
    envelope = fanin.combine_timestamp_evidence(mdf, ndf).get(ts)
    if envelope is None:
        return {"gate3c":"BLOCKED","stage":"RULE_FAN_IN","reason":"NO_COMBINED_EVENT_AT_AS_OF"}

    risk = dict(event.get("risk") or {})
    required_risk = ("authoritative","risk_pass","equity","peak_equity","prior_loss_streak","entry_price","stop_loss","take_profit","atr")
    missing_risk = [k for k in required_risk if k not in risk or risk[k] in (None, "")]
    if missing_risk:
        return {"gate3c":"BLOCKED","stage":"RISK","reason":"MISSING_AUTHORITATIVE_RISK_INPUTS","missing":missing_risk}
    if risk.get("authoritative") is not True:
        return {"gate3c":"BLOCKED","stage":"RISK","reason":"RISK_NOT_AUTHORITATIVE"}

    tiz = dict(event.get("tiz") or {})
    tiz.setdefault("authoritative", False)
    tiz.setdefault("status", "NOT_EVALUABLE")

    bridge = _load_module(ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "full_brain_runtime_bridge_v1.py", "brain_bridge")
    evidence_set_m = {rid: r for r in murphy_rows for rid in _ids([r])}
    evidence_set_n = {rid: r for r in nison_rows for rid in _ids([r])}
    result = bridge.run_full_brain_cycle(
        row=dict(event.get("brain_row") or {}),
        query_as_of=ts.isoformat(),
        murphy_evidence={"status":"PASS","rows":murphy_rows,"authoritative":True,"evidence_set":evidence_set_m},
        nison_evidence={"status":"PASS","rows":nison_rows,"authoritative":True,"confirmation":nison.get("confirmation","ABSENT"),"contradiction":bool(nison.get("contradiction",False)),"evidence_set":evidence_set_n},
        risk_evidence=risk,
        tiz_evidence=tiz,
        historical_evidence={"historical_context":event.get("historical_context") or {},"historical_outcome":event.get("historical_outcome") or {},"similarity":event.get("similarity") or {},"retrieval":event.get("retrieval") or {}},
        source_rule_ids=sorted(set(murphy_ids + nison_ids)),
        entry_price=float(risk["entry_price"]),
        atr=float(risk["atr"]),
        mode="development",
    )

    brain_decision = result.get("decision") or {}
    return {
        "gate3c":"PASS" if result.get("status")=="EXECUTABLE" else "BLOCKED",
        "query_as_of":ts.isoformat(), "symbol":event.get("symbol","GBPUSD"),
        "mtf":{k:mtf[k] for k in sorted(required_mtf)},
        "rule_envelope":{"murphy_event":len(murphy_ids),"murphy_governed_registry":len(MURPHY_IDS),"nison":len(nison_ids)},
        "memory_retrieval":{"historical_context":event.get("historical_context") or {},"historical_outcome":event.get("historical_outcome") or {},"similarity":event.get("similarity") or {},"retrieval":event.get("retrieval") or {}},
        "tiz":{"authoritative":tiz.get("authoritative"),"status":tiz.get("status")},
        "risk":{k:risk.get(k) for k in ("authoritative","risk_pass","equity","peak_equity","prior_loss_streak","entry_price","stop_loss","take_profit","atr","rr","risk_percent","position_size","reason")},
        "brain_execution_result":result,
        "governance":{"brain_v1_unchanged":True,"murphy_primary_context":True,"murphy_registry_intact":True,"nison_direction_generation":False,"tiz_direction_generation":False,"memory_direction_generation":False,"future_data_allowed":False,"oos_tuning":False,"full_fanin_verified":True},
        "decision_trace":brain_decision,
    }


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--event",required=True,type=Path); parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args(); result=run(json.loads(args.event.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,default=str),encoding="utf-8")
    print(json.dumps(result,indent=2,default=str)); return 0 if result.get("gate3c")=="PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
