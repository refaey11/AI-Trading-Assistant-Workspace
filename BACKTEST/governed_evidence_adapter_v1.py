from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _ts(s):
    return pd.to_datetime(s, utc=True, format="mixed", errors="coerce")


def _normalize_direction(v: Any) -> str | None:
    x = str(v or "").strip().upper()
    if x in {"BUY", "BULL", "BULLISH"}:
        return "BULLISH"
    if x in {"SELL", "BEAR", "BEARISH"}:
        return "BEARISH"
    return None


def _read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = _ts(df["timestamp"])
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df


def load_historical_context(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    required = {"pair", "context_signature"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: missing {sorted(required - set(df.columns))}")
    return df


def load_historical_outcome(path: Path) -> pd.DataFrame:
    df = _read_csv(path)
    required = {"pair", "context_signature"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: missing {sorted(required - set(df.columns))}")
    return df


def load_json_source(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_similarity_context(path: Path) -> Any:
    payload = load_json_source(path)
    if not isinstance(payload, list):
        raise ValueError("Similarity source must be a list")
    return payload


def load_retrieval(path: Path) -> Any:
    payload = load_json_source(path)
    if not isinstance(payload, list):
        raise ValueError("Retrieval source must be a list")
    return payload


def build_event_evidence(
    *,
    market_row: Mapping[str, Any],
    mtf_row: Mapping[str, Any] | None,
    murphy_rows: pd.DataFrame,
    nison_rows: pd.DataFrame,
    historical_context_rows: pd.DataFrame,
    historical_outcome_rows: pd.DataFrame,
    similarity_metadata: Any,
    retrieval_metadata: Any,
    timestamp: pd.Timestamp,
) -> dict[str, Any]:
    pair = str(market_row.get("pair") or "GBPUSD")

    m = murphy_rows[murphy_rows["timestamp"].eq(timestamp)]
    n = nison_rows[nison_rows["timestamp"].eq(timestamp)]
    hc = historical_context_rows[
        historical_context_rows["timestamp"].eq(timestamp) & historical_context_rows["pair"].eq(pair)
    ]
    ho = historical_outcome_rows[
        historical_outcome_rows["timestamp"].eq(timestamp) & historical_outcome_rows["pair"].eq(pair)
    ]

    passed_m = m[m["status"].astype(str).str.upper().eq("PASS")] if not m.empty and "status" in m else m
    dirs = sorted({d for d in (_normalize_direction(x) for x in passed_m.get("direction", [])) if d})
    murphy_direction = dirs[0] if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")

    if not n.empty:
        passed_n = n[n["status"].astype(str).str.upper().eq("PASS")]
        failed_n = n[n["status"].astype(str).str.upper().eq("FAIL")]
        n_dirs = sorted({d for d in (_normalize_direction(x) for x in passed_n.get("direction", [])) if d})
        nison_confirmation = n_dirs[0] if len(n_dirs) == 1 else ("CONFLICTED" if len(n_dirs) > 1 else "ABSENT")
        nison_contradiction = not failed_n.empty
    else:
        nison_confirmation = "ABSENT"
        nison_contradiction = False

    historical_context = None
    if not hc.empty:
        historical_context = hc.iloc[0].to_dict()
        historical_context.pop("timestamp", None)
        historical_context.pop("pair", None)

    historical_outcome = None
    if not ho.empty:
        historical_outcome = ho.iloc[0].to_dict()
        historical_outcome.pop("timestamp", None)
        historical_outcome.pop("pair", None)

    return {
        "timestamp": str(timestamp),
        "pair": pair,
        "market_state": dict(market_row),
        "mtf": dict(mtf_row or {}),
        "murphy": {
            "status": "PASS" if murphy_direction in {"BULLISH", "BEARISH"} else "NOT_EVALUABLE",
            "direction": murphy_direction,
            "rule_count": int(passed_m["source_rule_id"].nunique()) if "source_rule_id" in passed_m.columns else 0,
        },
        "nison": {
            "confirmation": nison_confirmation,
            "contradiction": nison_contradiction,
            "rule_count": int(n["rule_id"].nunique()) if "rule_id" in n.columns else 0,
        },
        "historical_context_memory": historical_context,
        "historical_outcome_memory": historical_outcome,
        "similarity_metadata": {"source_present": bool(similarity_metadata), "direction_allowed": False},
        "context_aware_retrieval": {"source_present": bool(retrieval_metadata), "direction_allowed": False},
        "tiz": {"source": "TIZ_PROCESS_GATE_V1", "direction_allowed": False},
        "risk": {"source": "RISK_ENGINE_INTEGRATION_V1", "hard_gate": True},
    }
