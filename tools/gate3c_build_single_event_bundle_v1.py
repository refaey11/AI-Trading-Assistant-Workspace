"""Build exactly one Gate 3C canonical event from existing source files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

MURPHY_IDS = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}
NISON_IDS = {f"NISON_{i:04d}" for i in range(1,45)}
MTF_FIELDS = ["mtf_trend_score","M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"]
RISK_FIELDS = ["equity","peak_equity","prior_loss_streak","entry_price","stop_loss","take_profit","atr"]


def csv_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.csv")) if root.exists() else []


def find_csv(root: Path, required: set[str], hints: tuple[str, ...] = ()) -> Path:
    candidates: list[tuple[int, Path]] = []
    for path in csv_files(root):
        try:
            cols = set(pd.read_csv(path, nrows=0).columns)
        except Exception:
            continue
        if required.issubset(cols):
            score = sum(1 for h in hints if h.lower() in path.name.lower())
            candidates.append((score, path))
    if not candidates:
        raise FileNotFoundError(f"No CSV under {root} provides {sorted(required)}")
    candidates.sort(key=lambda x: (-x[0], str(x[1])))
    return candidates[0][1]


def read_rows_at(path: Path, ts: pd.Timestamp, *, exact: bool = True) -> list[dict[str, Any]]:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp", kind="stable")
    part = df.loc[df["timestamp"].eq(ts)] if exact else df.loc[df["timestamp"].le(ts)].tail(1)
    return part.drop(columns=["timestamp"]).to_dict("records")


def split_rule_ids(value: Any) -> list[str]:
    return [x.strip() for x in str(value or "").split("|") if x.strip() and x.strip().upper() not in {"NONE","NULL","NAN","NISON_NONE"}]


def similarity_json_asof(root: Path, ts: pd.Timestamp) -> dict[str, Any]:
    files = sorted(root.rglob("*.json")) if root.exists() else []
    files = [p for p in files if "SIMILAR" in p.name.upper() or "CONTEXT" in p.name.upper()]
    if not files:
        raise ValueError(f"BLOCKED_SIMILARITY_SOURCE_NOT_FOUND:{root}")
    path = files[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"BLOCKED_SIMILARITY_SCHEMA:{path.name}")
    historical: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        for row in item.get("similar_contexts") or []:
            if not isinstance(row, dict) or "timestamp" not in row:
                continue
            try:
                rts = pd.Timestamp(row["timestamp"], tz="UTC")
            except Exception:
                continue
            if rts <= ts:
                historical.append(dict(row))
    historical.sort(key=lambda r: float(r.get("similarity", float("inf"))))
    if not historical:
        raise ValueError(f"BLOCKED_SIMILARITY_NOT_AVAILABLE_AS_OF_EVENT:{ts.isoformat()}")
    return {
        "status": "AVAILABLE",
        "source": str(path),
        "row": {"current_context": None, "similar_contexts": historical, "as_of": ts.isoformat()},
        "provenance": {"future_current_context_excluded": True, "historical_rows_retained": len(historical)},
    }


def retrieval_artifact(root: Path) -> dict[str, Any]:
    """Load the retrieval artifact as static RAG context, not PIT market evidence.

    The retrieval artifact is a knowledge-retrieval output and is not a timestamped
    market-memory series. Treating it as an as-of CSV was an invalid schema assumption
    that blocked otherwise valid historical events. It is kept non-authoritative and
    must not generate direction.
    """
    json_files = sorted(root.rglob("CONTEXT_AWARE_READINGS.json")) if root.exists() else []
    if not json_files:
        raise ValueError(f"BLOCKED_RETRIEVAL_ARTIFACT_NOT_FOUND:{root}")
    path = json_files[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"BLOCKED_RETRIEVAL_SCHEMA:{path.name}")
    return {
        "status": "AVAILABLE",
        "source": str(path),
        "row": None,
        "authoritative": False,
        "point_in_time": False,
        "direction_generation": False,
        "artifact_rows": len(data),
    }


def build(event_ts: str, h1: Path, market_state: Path, nison: Path, murphy_root: Path,
          mtf_root: Path, historical_context_root: Path, historical_outcome_root: Path,
          similarity_root: Path, retrieval_root: Path) -> dict[str, Any]:
    ts = pd.Timestamp(event_ts, tz="UTC")
    if not (2016 <= ts.year <= 2024):
        raise ValueError("Gate 3C is restricted to 2016-2024")

    market_row = read_rows_at(market_state, ts, exact=False)
    h1_row = read_rows_at(h1, ts, exact=False)
    if not market_row:
        raise ValueError("BLOCKED_MARKET_STATE_NOT_AVAILABLE_AS_OF_EVENT")
    if not h1_row:
        raise ValueError("BLOCKED_H1_NOT_AVAILABLE_AS_OF_EVENT")

    mtf_csv = find_csv(mtf_root, {"timestamp", *MTF_FIELDS}, hints=("GBPUSD","MTF","ALIGNMENT"))
    mtf_rows = read_rows_at(mtf_csv, ts, exact=False)
    if not mtf_rows:
        raise ValueError("BLOCKED_MTF_NOT_AVAILABLE_AS_OF_EVENT")
    mtf = dict(mtf_rows[0])
    missing = [k for k in MTF_FIELDS if mtf.get(k) in (None, "")]
    if missing:
        raise ValueError(f"BLOCKED_MTF_FIELDS:{missing}")

    ndf = pd.read_csv(nison)
    if "timestamp" not in ndf.columns:
        raise ValueError("BLOCKED_NISON_SCHEMA")
    if "source_rule_id" not in ndf.columns:
        if "rule_id" in ndf.columns:
            ndf = ndf.rename(columns={"rule_id":"source_rule_id"})
        else:
            raise ValueError("BLOCKED_NISON_SCHEMA")
    ndf["timestamp"] = pd.to_datetime(ndf["timestamp"], utc=True, errors="coerce", format="mixed")
    nrows = ndf.loc[ndf["timestamp"].eq(ts)].drop(columns=["timestamp"]).to_dict("records")
    nids = sorted({rid for r in nrows for rid in split_rule_ids(r.get("source_rule_id"))})
    if set(nids) != NISON_IDS:
        raise ValueError(f"BLOCKED_NISON_44_FANIN: observed={len(nids)}")

    m_csv = find_csv(murphy_root, {"timestamp", "source_rule_id"}, hints=("MURPHY","2016_2024","FULL","EVIDENCE"))
    mdf = pd.read_csv(m_csv)
    if "timestamp" not in mdf.columns or "source_rule_id" not in mdf.columns:
        raise ValueError("BLOCKED_MURPHY_SCHEMA")
    mdf["timestamp"] = pd.to_datetime(mdf["timestamp"], utc=True, errors="coerce", format="mixed")
    mrows = mdf.loc[mdf["timestamp"].eq(ts)].drop(columns=["timestamp"]).to_dict("records")
    mids = sorted({rid for r in mrows for rid in split_rule_ids(r.get("source_rule_id"))})
    if not mids:
        raise ValueError("BLOCKED_MURPHY_NO_SOURCE_BACKED_EVENT_RULES")
    unknown = sorted(set(mids) - MURPHY_IDS)
    if unknown:
        raise ValueError(f"BLOCKED_MURPHY_UNKNOWN_RULE_IDS:{unknown}")

    def memory_asof(root: Path, hints: tuple[str, ...]) -> dict[str, Any]:
        path = find_csv(root, {"timestamp"}, hints=hints)
        rows = read_rows_at(path, ts, exact=False)
        if not rows:
            raise ValueError(f"BLOCKED_MEMORY_NOT_AVAILABLE:{path.name}")
        return {"status":"AVAILABLE","source":str(path),"row":rows[0]}

    historical_context = memory_asof(historical_context_root,("HISTORICAL","CONTEXT"))
    historical_outcome = memory_asof(historical_outcome_root,("HISTORICAL","OUTCOME"))
    similarity = similarity_json_asof(similarity_root, ts)
    retrieval = retrieval_artifact(retrieval_root)

    risk_csv = None
    for root in (murphy_root, historical_context_root, historical_outcome_root, similarity_root, retrieval_root):
        for candidate in csv_files(root):
            try:
                cols = set(pd.read_csv(candidate, nrows=0).columns)
            except Exception:
                continue
            if set(RISK_FIELDS).issubset(cols):
                risk_csv = candidate
                break
        if risk_csv:
            break
    if risk_csv is None:
        raise ValueError("BLOCKED_AUTHORITATIVE_RISK_ACCOUNT_STATE_NOT_FOUND")
    risk_rows = read_rows_at(risk_csv, ts, exact=False)
    if not risk_rows:
        raise ValueError("BLOCKED_AUTHORITATIVE_RISK_ACCOUNT_STATE_NOT_AVAILABLE")
    risk = dict(risk_rows[0])
    risk["authoritative"] = True
    if "risk_pass" not in risk:
        raise ValueError("BLOCKED_RISK_RESULT_NOT_PRESENT")

    market = dict(market_row[0])
    h1v = dict(h1_row[0])
    brain_row = {**market, **mtf}
    if "entry_price" not in brain_row and "close" in h1v:
        brain_row["entry_price"] = h1v["close"]
    if "atr" not in brain_row and "atr20" in market:
        brain_row["atr"] = market["atr20"]

    return {
        "symbol":"GBPUSD", "query_as_of":ts.isoformat(), "h1":h1v, "market":market,
        "mtf":mtf, "brain_row":brain_row,
        "murphy":{"status":"PASS","rows":mrows,"authoritative":True,
                  "governed_registry_count":len(MURPHY_IDS),"event_rule_count":len(mids)},
        "nison":{"status":"PASS","rows":nrows,"authoritative":True},
        "historical_context":historical_context,"historical_outcome":historical_outcome,
        "similarity":similarity,"retrieval":retrieval,
        "tiz":{"status":"NOT_EVALUABLE","authoritative":False,"source":"TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2"},
        "risk":risk,"entry_price":risk.get("entry_price"),"atr":risk.get("atr"),
        "provenance":{"builder":"gate3c_build_single_event_bundle_v1","source_backed_only":True,
                       "murphy_governed_registry_count":len(MURPHY_IDS),"murphy_event_rule_count":len(mids),
                       "nison_rule_count":len(nids),"mtf_fields":sorted(MTF_FIELDS),"oos_tuning":False,
                       "similarity_future_context_excluded":True,
                       "retrieval_non_pit_static_context":True,
                       "retrieval_direction_generation":False}
    }


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--timestamp",required=True); p.add_argument("--h1",required=True,type=Path)
    p.add_argument("--market-state",required=True,type=Path); p.add_argument("--nison",required=True,type=Path)
    p.add_argument("--murphy-root",required=True,type=Path); p.add_argument("--mtf-root",required=True,type=Path)
    p.add_argument("--historical-context-root",required=True,type=Path); p.add_argument("--historical-outcome-root",required=True,type=Path)
    p.add_argument("--similarity-root",required=True,type=Path); p.add_argument("--retrieval-root",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path); a=p.parse_args()
    result=build(a.timestamp,a.h1,a.market_state,a.nison,a.murphy_root,a.mtf_root,a.historical_context_root,a.historical_outcome_root,a.similarity_root,a.retrieval_root)
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,default=str),encoding="utf-8")
    print(json.dumps(result,indent=2,default=str)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
