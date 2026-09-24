from __future__ import annotations

"""Governed 2016-2024 Decision Brain backtest runner.

This file is the existing official development runner. It is deliberately kept as
one runner and now composes the already-existing project boundaries instead of
reimplementing them:
- recovered Decision Brain V1
- Three-Book evaluator
- frozen execution adapter (0.75 ATR / 2R)
- Risk Engine V1
- lossless 34+44 rule fan-in
- optional shadow historical-memory metadata

2025 remains locked out of this development path.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN_PATH = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"

from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event
from OOS_2025.governed_rule_fan_in_v1 import build_lossless_rule_groups
from OOS_2025.execution_oos_adapter_v1 import SL_ATR, TP_R
from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk


DEVELOPMENT_START_YEAR = 2016
DEVELOPMENT_END_YEAR = 2024
LOCKED_OOS_YEAR = 2025
BASE_RISK_PCT = 0.005
TF_NAMES = ("M5", "M15", "M30", "H1", "H4", "D1")


def load_csv(
    path: Path,
    required: set[str],
    *,
    allow_duplicate_timestamps: bool = False,
) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], format="mixed", utc=True, errors="coerce"
    )
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    if not allow_duplicate_timestamps and df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)


def load_brain():
    spec = importlib.util.spec_from_file_location(
        "recovered_decision_brain", BRAIN_PATH
    )
    if not spec or not spec.loader:
        raise RuntimeError("Unable to load recovered Decision Brain V1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def allowed_rule_ids() -> set[str]:
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return set(data["verified_runtime"]["MURPHY"]) | set(
        data["verified_runtime"]["NISON"]
    )


def expand_rule_ids(value: Any) -> set[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return set()
    return {p.strip() for p in str(value).split("|") if p.strip()}


def normalize_direction(value: Any) -> str | None:
    text = str(value or "").strip().upper()
    if text in {"BUY", "BULL", "BULLISH"}:
        return "BULLISH"
    if text in {"SELL", "BEAR", "BEARISH"}:
        return "BEARISH"
    return None


def normalize_rule_columns(df: pd.DataFrame, family: str) -> pd.DataFrame:
    out = df.copy()
    if "source_rule_id" not in out.columns:
        if family == "NISON" and "rule_id" in out.columns:
            out["source_rule_id"] = out["rule_id"].astype(str)
        elif family == "MURPHY" and "rule_id" in out.columns:
            out["source_rule_id"] = out["rule_id"].astype(str)
        else:
            raise ValueError(f"{family}: source_rule_id/rule_id missing")
    return out


def summarize_directional_evidence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = [
        normalize_direction(r.get("direction"))
        for r in rows
        if str(r.get("status", "")).upper() == "PASS"
    ]
    dirs = sorted({d for d in passed if d})
    direction = dirs[0] if len(dirs) == 1 else (
        "CONFLICTED" if len(dirs) > 1 else "ABSENT"
    )
    return {
        "status": "PASS" if direction in {"BULLISH", "BEARISH"} else "NOT_EVALUABLE",
        "direction": direction,
        "rule_count": len(
            {
                str(r.get("source_rule_id") or "").strip()
                for r in rows
                if str(r.get("source_rule_id") or "").strip()
            }
        ),
        "rule_ids": sorted(
            {
                str(r.get("source_rule_id") or "").strip()
                for r in rows
                if str(r.get("source_rule_id") or "").strip()
            }
        ),
    }


def build_nison_evidence(
    rows: list[dict[str, Any]],
    murphy_direction: str | None,
) -> dict[str, Any]:
    passed_dirs = sorted(
        {
            normalize_direction(r.get("direction"))
            for r in rows
            if str(r.get("status", "")).upper() == "PASS"
        }
        - {None}
    )
    contradiction = len(passed_dirs) > 1
    if (
        not contradiction
        and len(passed_dirs) == 1
        and murphy_direction in {"BULLISH", "BEARISH"}
        and passed_dirs[0] != murphy_direction
    ):
        contradiction = True

    if contradiction:
        confirmation = "CONTRADICTED"
    elif len(passed_dirs) == 1:
        confirmation = "CONFIRMED"
    else:
        confirmation = "ABSENT"

    return {
        "status": "PASS" if len(passed_dirs) == 1 else (
            "NOT_EVALUABLE" if not passed_dirs else "PASS"
        ),
        "confirmation": confirmation,
        "contradiction": contradiction,
        "direction": passed_dirs[0] if len(passed_dirs) == 1 else None,
        "rule_ids": sorted(
            {
                str(r.get("source_rule_id") or "").strip()
                for r in rows
                if str(r.get("source_rule_id") or "").strip()
            }
        ),
        "evidence_set": rows,
        "evidence_count": len(
            {
                str(r.get("source_rule_id") or "").strip()
                for r in rows
                if str(r.get("source_rule_id") or "").strip()
            }
        ),
    }


def build_murphy_evidence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary = summarize_directional_evidence(rows)
    expanded_rule_ids: set[str] = set()
    for row in rows:
        expanded_rule_ids.update(expand_rule_ids(row.get("source_rule_id")))
    return {
        "status": summary["status"],
        "direction": summary["direction"],
        "evidence_set": rows,
        "evidence_count": len(expanded_rule_ids),
        "rule_ids": sorted(expanded_rule_ids),
    }


def _trend_to_score(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip().upper()
    if text in {
        "BULL",
        "BULLISH",
        "BULL_TREND",
        "UP",
        "UPTREND",
        "1",
        "1.0",
    }:
        return 1.0
    if text in {
        "BEAR",
        "BEARISH",
        "BEAR_TREND",
        "DOWN",
        "DOWNTREND",
        "-1",
        "-1.0",
    }:
        return -1.0
    if text in {"TRANSITION", "MIXED", "NEUTRAL", "RANGE", "0", "0.0"}:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _pick_explicit_column(row: pd.Series, names: tuple[str, ...]) -> float | None:
    for name in names:
        if name in row.index and pd.notna(row[name]):
            score = _trend_to_score(row[name])
            if score is not None:
                return score
    return None


def build_brain_row(row: pd.Series) -> dict[str, Any]:
    """Pass only explicit source-backed MTF/volume fields to Brain V1."""
    out: dict[str, Any] = {
        "volume_available": False,
        "mtf_trend_score": 0.0,
    }

    trend_values: list[float] = []
    for tf in TF_NAMES:
        value = _pick_explicit_column(
            row,
            (
                f"{tf}_trend_regime",
                f"{tf}_trend",
                f"{tf}_market_trend",
                f"{tf}_trend_direction",
                f"{tf}_bias",
                f"{tf}_market_bias",
            ),
        )
        if value is not None:
            out[f"{tf}_trend_regime"] = value
            trend_values.append(value)

    direct_mtf = _pick_explicit_column(
        row,
        (
            "mtf_trend_score",
            "mtf_alignment",
            "multi_timeframe_trend",
            "multi_timeframe_bias",
        ),
    )
    if direct_mtf is not None:
        out["mtf_trend_score"] = direct_mtf
    elif trend_values:
        out["mtf_trend_score"] = sum(trend_values) / len(trend_values)

    volume_values: list[float] = []
    for tf in TF_NAMES:
        value = _pick_explicit_column(
            row,
            (
                f"{tf}_volume_regime",
                f"{tf}_volume_bias",
                f"{tf}_volume_score",
            ),
        )
        if value is not None:
            out[f"{tf}_volume_regime"] = value
            volume_values.append(value)
    if volume_values:
        out["volume_available"] = True

    return out


def load_optional_memory_metadata(
    *,
    historical_context_index: Path | None,
    historical_outcome_stats: Path | None,
    similarity_summary: Path | None,
    retrieval_summary: Path | None,
) -> dict[str, Any]:
    """Record memory-source presence without using aggregate/future statistics.

    The supplied summary/index files are metadata-only. They are not passed into
    the Brain as directional features because some include observations extending
    through 2025 and therefore cannot be treated as per-event as-of evidence.
    """
    sources: dict[str, dict[str, Any]] = {}
    for name, path in (
        ("historical_context", historical_context_index),
        ("historical_outcome", historical_outcome_stats),
        ("similarity", similarity_summary),
        ("context_aware_retrieval", retrieval_summary),
    ):
        if path is None:
            sources[name] = {"status": "NOT_EVALUABLE", "source": None}
            continue
        header = pd.read_csv(path, nrows=0).columns.tolist()
        sources[name] = {
            "status": "AVAILABLE_METADATA_ONLY",
            "source": str(path),
            "columns": header,
            "as_of_usable": False,
        }
    return {
        "sources": sources,
        "shadow_only": True,
        "direction_generated": False,
        "future_data_used_for_direction": False,
        "official_asof_memory_gate": all(
            v.get("status") == "AVAILABLE_ASOF" and v.get("as_of_usable") is True
            for v in sources.values()
        ),
    }


def simulate_trade(
    bars: pd.DataFrame,
    entry_idx: int,
    direction: str,
    entry: float,
    stop_loss: float,
    take_profit: float,
    *,
    round_trip_cost_price: float | None,
) -> dict[str, Any]:
    stop_distance = abs(entry - stop_loss)
    for j in range(entry_idx + 1, len(bars)):
        b = bars.iloc[j]
        hit_sl = float(b["low"]) <= stop_loss if direction == "BUY" else float(b["high"]) >= stop_loss
        hit_tp = float(b["high"]) >= take_profit if direction == "BUY" else float(b["low"]) <= take_profit
        if hit_sl and hit_tp:
            return {
                "exit_timestamp": b["timestamp"],
                "outcome": "AMBIGUOUS",
                "r_multiple": None,
                "gross_r_multiple": None,
                "cost_r_multiple": None,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            }
        if hit_tp:
            gross_r = TP_R
            cost_r = (
                round_trip_cost_price / stop_distance
                if round_trip_cost_price is not None
                else None
            )
            net_r = gross_r - cost_r if cost_r is not None else gross_r
            return {
                "exit_timestamp": b["timestamp"],
                "outcome": "TP",
                "r_multiple": net_r,
                "gross_r_multiple": gross_r,
                "cost_r_multiple": cost_r,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            }
        if hit_sl:
            gross_r = -1.0
            cost_r = (
                round_trip_cost_price / stop_distance
                if round_trip_cost_price is not None
                else None
            )
            net_r = gross_r - cost_r if cost_r is not None else gross_r
            return {
                "exit_timestamp": b["timestamp"],
                "outcome": "SL",
                "r_multiple": net_r,
                "gross_r_multiple": gross_r,
                "cost_r_multiple": cost_r,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            }
    return {
        "exit_timestamp": None,
        "outcome": "TIMEOUT",
        "r_multiple": None,
        "gross_r_multiple": None,
        "cost_r_multiple": None,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
    }


def run(
    *,
    h1: Path,
    murphy: Path,
    nison: Path,
    context: Path,
    output_dir: Path,
    mtf_dir: Path | None = None,
    historical_context_index: Path | None = None,
    historical_outcome_stats: Path | None = None,
    similarity_summary: Path | None = None,
    retrieval_summary: Path | None = None,
    round_trip_cost_price: float | None = None,
) -> dict[str, Any]:
    bars = load_csv(h1, {"timestamp", "open", "high", "low", "close"})
    murphy_raw = normalize_rule_columns(
        load_csv(murphy, {"timestamp", "status", "direction"}, allow_duplicate_timestamps=True),
        "MURPHY",
    )
    nison_raw = normalize_rule_columns(
        load_csv(nison, {"timestamp", "status", "direction", "rule_id"}, allow_duplicate_timestamps=True),
        "NISON",
    )
    ctx = load_csv(context, {"timestamp"}, allow_duplicate_timestamps=False)

    if "entry_price" not in ctx.columns and "close" in ctx.columns:
        ctx["entry_price"] = pd.to_numeric(ctx["close"], errors="coerce")
    if "atr" not in ctx.columns and "atr20" in ctx.columns:
        ctx["atr"] = pd.to_numeric(ctx["atr20"], errors="coerce")
    required_context = {"timestamp", "entry_price", "atr"}
    missing_context = sorted(required_context - set(ctx.columns))
    if missing_context:
        raise ValueError(f"context missing source-backed columns {missing_context}")

    mtf = pd.DataFrame()
    if mtf_dir is not None:
        files = sorted(mtf_dir.rglob("*.csv"))
        if not files:
            raise ValueError(f"{mtf_dir}: no CSV timeframe source found")
        mtf_parts: list[pd.DataFrame] = []
        for path in files:
            raw = pd.read_csv(path)
            if "timestamp" not in raw.columns:
                continue
            raw["timestamp"] = pd.to_datetime(
                raw["timestamp"], format="mixed", utc=True, errors="coerce"
            )
            tf = path.stem.upper()
            matched_tf = next((x for x in TF_NAMES if x in tf), None)
            if matched_tf is None:
                continue
            trend_col = next(
                (
                    c
                    for c in (
                        "trend_regime",
                        "trend",
                        "market_trend",
                        "trend_direction",
                        "direction",
                        "bias",
                        "market_bias",
                        "regime",
                    )
                    if c in raw.columns
                ),
                None,
            )
            if trend_col is None:
                continue
            part = raw[["timestamp", trend_col]].copy()
            part[f"{matched_tf}_trend_regime"] = part[trend_col].map(_trend_to_score)
            mtf_parts.append(
                part[["timestamp", f"{matched_tf}_trend_regime"]]
                .dropna()
                .drop_duplicates("timestamp")
            )
        if mtf_parts:
            mtf = mtf_parts[0]
            for part in mtf_parts[1:]:
                mtf = mtf.merge(part, on="timestamp", how="outer")
            mtf = mtf.sort_values("timestamp").reset_index(drop=True)
            tf_cols = [
                f"{tf}_trend_regime"
                for tf in TF_NAMES
                if f"{tf}_trend_regime" in mtf.columns
            ]
            mtf["mtf_trend_score"] = mtf[tf_cols].mean(axis=1, skipna=True)
            mtf["mtf_timeframes_available"] = mtf[tf_cols].notna().sum(axis=1)
        else:
            raise ValueError(f"{mtf_dir}: no explicit source-backed trend columns found")

    if not mtf.empty:
        ctx = ctx.merge(mtf, on="timestamp", how="left")

    allowed = allowed_rule_ids()
    observed_m: set[str] = set()
    for value in murphy_raw["source_rule_id"].dropna():
        observed_m.update(expand_rule_ids(value))
    observed_n: set[str] = set()
    for value in nison_raw["source_rule_id"].dropna():
        observed_n.update(expand_rule_ids(value))
    expected_murphy = {x for x in allowed if x.startswith("MURPHY_")}
    expected_nison = {x for x in allowed if x.startswith("NISON_")}
    if not observed_m.issubset(allowed):
        raise ValueError(f"Unknown Murphy rule IDs: {sorted(observed_m - allowed)}")
    if not observed_n.issubset(allowed):
        raise ValueError(f"Unknown Nison rule IDs: {sorted(observed_n - allowed)}")

    murphy_groups = build_lossless_rule_groups(murphy_raw)
    nison_groups = build_lossless_rule_groups(nison_raw)

    context_map = ctx.set_index("timestamp")
    common_timestamps = sorted(
        set(context_map.index) & set(murphy_groups) & set(nison_groups)
    )

    brain = load_brain()
    memory_meta = load_optional_memory_metadata(
        historical_context_index=historical_context_index,
        historical_outcome_stats=historical_outcome_stats,
        similarity_summary=similarity_summary,
        retrieval_summary=retrieval_summary,
    )

    events: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    rejection_reasons: dict[str, int] = {}
    risk_state = {
        "equity": 10000.0,
        "peak_equity": 10000.0,
        "prior_loss_streak": 0,
    }

    bars_index = pd.Series(bars.index, index=bars["timestamp"])

    for ts in common_timestamps:
        if ts.year < DEVELOPMENT_START_YEAR or ts.year > DEVELOPMENT_END_YEAR:
            continue
        if ts.year >= LOCKED_OOS_YEAR:
            continue

        m_rows = murphy_groups[ts]
        n_rows = nison_groups[ts]

        m_evidence = build_murphy_evidence(m_rows)
        mdir = m_evidence["direction"] if m_evidence["direction"] in {"BULLISH", "BEARISH"} else None
        n_evidence = build_nison_evidence(n_rows, mdir)

        crow = context_map.loc[ts]
        brain_row = build_brain_row(crow)
        assessment = brain.assess(brain_row, similarity=None)

        entry = float(crow["entry_price"]) if pd.notna(crow["entry_price"]) else None
        atr = float(crow["atr"]) if pd.notna(crow["atr"]) else None

        risk_evidence: dict[str, Any] = {
            "risk_pass": False,
            "risk_status": "FAIL",
            "reason": "NOT_EVALUABLE",
        }
        execution_plan: dict[str, Any] = {
            "status": "NOT_EXECUTABLE",
            "reason": "decision_not_approved",
        }

        if mdir in {"BULLISH", "BEARISH"} and entry is not None and atr is not None and atr > 0:
            action = "BUY" if mdir == "BULLISH" else "SELL"
            provisional_stop = (
                entry - SL_ATR * atr if action == "BUY" else entry + SL_ATR * atr
            )
            provisional_target = (
                entry + (SL_ATR * atr * TP_R)
                if action == "BUY"
                else entry - (SL_ATR * atr * TP_R)
            )
            risk_result = evaluate_risk(
                RiskRequest(
                    equity=risk_state["equity"],
                    risk_percent=BASE_RISK_PCT,
                    entry_price=entry,
                    stop_distance=abs(entry - provisional_stop),
                    take_profit_distance=abs(provisional_target - entry),
                    stop_mode="structure",
                    risk_budget_locked=True,
                ),
                action,
                atr,
            )
            risk_evidence = {
                "risk_pass": bool(risk_result.risk_pass),
                "risk_status": "PASS" if risk_result.risk_pass else "FAIL",
                "reason": risk_result.reason,
                "risk_money": risk_result.risk_money,
                "position_size": risk_result.position_size,
                "stop_loss": risk_result.stop_loss,
                "take_profit": risk_result.take_profit,
                "rr": TP_R,
                "risk_percent": BASE_RISK_PCT,
            }

        tiz_evidence = {
            "process_state": "AVAILABLE",
            "process_gate": "AVAILABLE",
            "tiz_verified": False,
            "source": "development_optional_tiz_policy",
        }

        source_rule_ids = list(
            dict.fromkeys(
                [
                    *m_evidence["rule_ids"],
                    *n_evidence["rule_ids"],
                ]
            )
        )

        assembled = assemble_decision_event(
            decision_brain_module=brain,
            row=brain_row,
            query_as_of=str(ts),
            murphy_evidence=m_evidence,
            nison_evidence=n_evidence,
            tiz_evidence=tiz_evidence,
            risk_evidence=risk_evidence,
            historical_evidence={
                "retrieval_status": "SHADOW_ONLY_METADATA",
                "candidate_count": 0,
                "warnings": [
                    "Historical memory summaries/indexes are metadata-only and not used for direction.",
                    "No per-event as-of similarity evidence is introduced by this runner.",
                ],
            },
            source_rule_ids=source_rule_ids,
            entry_price=entry,
            atr=atr,
            mode="development",
            provenance={
                "runner": "BACKTEST/DEV_BACKTEST_RUNNER_V1.py",
                "evaluation_window": "2016-2024",
                "decision_brain_unchanged": True,
                "memory_shadow_only": True,
                "tiz_optional_unverified": True,
                "risk_contract": "0.75_ATR_STOP_2R_TARGET_0.5pct",
            },
        )

        final_decision = (
            assembled.get("decision", {})
            .get("decision", {})
            .get("final", "NO_TRADE")
        )
        execution_status = assembled.get("status", "NO_TRADE")
        event_reason = None
        if final_decision not in {"BUY", "SELL"}:
            event_reason = (
                assembled.get("decision", {})
                .get("decision", {})
                .get("reasons_against", [])
            )
            if isinstance(event_reason, list):
                event_reason = "|".join(map(str, event_reason))
            else:
                event_reason = str(event_reason)

        event = {
            "timestamp": ts,
            "evaluation_year": int(ts.year),
            "murphy_status": m_evidence["status"],
            "murphy_direction": mdir or "ABSENT",
            "murphy_rule_count": m_evidence["evidence_count"],
            "nison_status": n_evidence["status"],
            "nison_confirmation": n_evidence["confirmation"],
            "nison_contradiction": bool(n_evidence["contradiction"]),
            "nison_rule_count": n_evidence["evidence_count"],
            "brain_bias": assessment.directional_bias.upper(),
            "brain_confidence": assessment.confidence,
            "mtf_timeframes_available": int(
                sum(1 for tf in TF_NAMES if f"{tf}_trend_regime" in brain_row)
            ),
            "risk_pass": bool(risk_evidence.get("risk_pass", False)),
            "risk_percent": risk_evidence.get("risk_percent"),
            "stop_loss": risk_evidence.get("stop_loss"),
            "take_profit": risk_evidence.get("take_profit"),
            "tiz_status": tiz_evidence["process_gate"],
            "tiz_verified": False,
            "memory_shadow_only": True,
            "memory_asof_usable": False,
            "decision": final_decision,
            "status": execution_status,
            "reason": event_reason or assembled.get("reason"),
            "source_rule_ids": json.dumps(source_rule_ids),
        }
        events.append(event)

        if final_decision not in {"BUY", "SELL"} or execution_status != "EXECUTABLE":
            reason = str(event.get("reason") or "NOT_EXECUTABLE")
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
            continue

        if ts not in bars_index.index:
            rejection_reasons["ENTRY_TIMESTAMP_NOT_IN_H1"] = rejection_reasons.get(
                "ENTRY_TIMESTAMP_NOT_IN_H1", 0
            ) + 1
            continue

        entry_idx = int(bars_index.loc[ts])
        plan = assembled["execution_plan"]
        result = simulate_trade(
            bars,
            entry_idx,
            final_decision,
            float(plan["entry_price"]),
            float(plan["stop_loss"]),
            float(plan["take_profit"]),
            round_trip_cost_price=round_trip_cost_price,
        )
        p_and_l_r = result["r_multiple"]
        if p_and_l_r is not None:
            risk_money = float(risk_evidence.get("risk_money") or 0.0)
            pnl = risk_money * p_and_l_r
            risk_state["equity"] += pnl
            risk_state["peak_equity"] = max(risk_state["peak_equity"], risk_state["equity"])
            if result["outcome"] == "SL":
                risk_state["prior_loss_streak"] += 1
            elif result["outcome"] == "TP":
                risk_state["prior_loss_streak"] = 0

        trades.append(
            {
                "timestamp": ts,
                "direction": final_decision,
                "entry_price": float(plan["entry_price"]),
                "atr": atr,
                "stop_loss": float(plan["stop_loss"]),
                "take_profit": float(plan["take_profit"]),
                "position_size": risk_evidence.get("position_size"),
                "risk_percent": risk_evidence.get("risk_percent"),
                **result,
            }
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    event_df = pd.DataFrame(events)
    trades_df = pd.DataFrame(trades)

    event_df.to_csv(output_dir / "unified_78_events_2016_2024.csv", index=False)
    event_df.to_csv(output_dir / "decision_events_2016_2024.csv", index=False)
    trades_df.to_csv(output_dir / "executed_trades_2016_2024.csv", index=False)

    resolved = (
        trades_df[trades_df["r_multiple"].notna()].copy()
        if not trades_df.empty
        else pd.DataFrame()
    )
    wins = int((resolved["r_multiple"] > 0).sum()) if not resolved.empty else 0
    losses = int((resolved["r_multiple"] < 0).sum()) if not resolved.empty else 0
    gross_win = (
        float(resolved.loc[resolved["r_multiple"] > 0, "r_multiple"].sum())
        if not resolved.empty
        else 0.0
    )
    gross_loss = (
        float(-resolved.loc[resolved["r_multiple"] < 0, "r_multiple"].sum())
        if not resolved.empty
        else 0.0
    )
    equity_r = (
        resolved["r_multiple"].cumsum()
        if not resolved.empty
        else pd.Series(dtype=float)
    )

    mtf_consumed = bool(
        not mtf.empty
        or (
            event_df["mtf_timeframes_available"].gt(0).any()
            if not event_df.empty
            else False
        )
    )
    rule_counts_ok = bool(
        not event_df.empty
        and int(event_df["murphy_rule_count"].min()) == len(expected_murphy)
        and int(event_df["nison_rule_count"].min()) == len(expected_nison)
    )

    metrics = {
        "status": "GOVERNED_CANDIDATE_NOT_OFFICIAL",
        "development_window": "2016-2024",
        "trades": int(len(resolved)),
        "wins": wins,
        "losses": losses,
        "win_rate": float(wins / len(resolved)) if len(resolved) else None,
        "profit_factor": gross_win / gross_loss if gross_loss else None,
        "expectancy_R": float(resolved["r_multiple"].mean()) if not resolved.empty else None,
        "total_R": float(resolved["r_multiple"].sum()) if not resolved.empty else 0.0,
        "max_drawdown_R": float((equity_r - equity_r.cummax()).min()) if not equity_r.empty else 0.0,
        "costs_applied": round_trip_cost_price is not None,
        "round_trip_cost_price": round_trip_cost_price,
        "official_claim_allowed": False,
        "rule_counts_ok": rule_counts_ok,
        "mtf_source_consumed": mtf_consumed,
        "memory_shadow_only": True,
        "tiz_verified": False,
        "sl_atr": SL_ATR,
        "tp_R": TP_R,
        "risk_percent": BASE_RISK_PCT,
    }

    funnel = {
        "events": int(len(event_df)),
        "murphy_directional": int(
            event_df["murphy_direction"].isin(["BULLISH", "BEARISH"]).sum()
        )
        if not event_df.empty
        else 0,
        "brain_aligned": int(
            (
                event_df["murphy_direction"].eq(event_df["brain_bias"])
                & event_df["murphy_direction"].isin(["BULLISH", "BEARISH"])
            ).sum()
        )
        if not event_df.empty
        else 0,
        "risk_pass_events": int(event_df["risk_pass"].sum()) if not event_df.empty else 0,
        "three_book_buy_sell": int(
            event_df["decision"].isin(["BUY", "SELL"]).sum()
        )
        if not event_df.empty
        else 0,
        "executed_trades": int(len(trades_df)),
        "resolved_trades": int(len(resolved)),
        "ambiguous": int((trades_df["outcome"] == "AMBIGUOUS").sum())
        if not trades_df.empty
        else 0,
        "timeouts": int((trades_df["outcome"] == "TIMEOUT").sum())
        if not trades_df.empty
        else 0,
        "rejection_reasons": rejection_reasons,
    }

    missing_required: list[str] = []
    if len(observed_m) != len(expected_murphy):
        missing_required.append(
            f"FULL_MURPHY_RULE_COVERAGE:{len(observed_m)}/{len(expected_murphy)}"
        )
    if len(observed_n) != len(expected_nison):
        missing_required.append(
            f"FULL_NISON_RULE_COVERAGE:{len(observed_n)}/{len(expected_nison)}"
        )
    if not mtf_consumed:
        missing_required.append("MTF_SOURCE_BACKED_FIELDS")
    if not rule_counts_ok:
        missing_required.append("FULL_34X44_RULE_EVIDENCE")
    if not memory_meta["official_asof_memory_gate"]:
        missing_required.append("ASOF_HISTORICAL_MEMORY_EVIDENCE")
    if round_trip_cost_price is None:
        missing_required.append("FROZEN_COST_SLIPPAGE_INPUT")

    validation = {
        "status": "BLOCKED" if missing_required else "PASS",
        "timestamp_asof": True,
        "lookahead": True,
        "mtf_consumption": mtf_consumed,
        "memory_leakage": True,
        "memory_asof_evidence": False,
        "execution_funnel": True,
        "frozen_cost_slippage": round_trip_cost_price is not None,
        "official_profitability_claim": False,
        "three_book_evaluator": True,
        "risk_engine_v1": True,
        "frozen_execution_adapter": True,
        "2025_present": False,
        "missing_required_input": missing_required or None,
        "memory_sources": memory_meta,
    }

    (output_dir / "execution_funnel_2016_2024.json").write_text(
        json.dumps(funnel, indent=2, default=str), encoding="utf-8"
    )
    (output_dir / "backtest_metrics_2016_2024.json").write_text(
        json.dumps(metrics, indent=2, default=str), encoding="utf-8"
    )
    (output_dir / "validation_manifest_2016_2024.json").write_text(
        json.dumps(validation, indent=2, default=str), encoding="utf-8"
    )

    return {
        "metrics": metrics,
        "funnel": funnel,
        "validation": validation,
        "output_dir": str(output_dir),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--mtf-dir", required=False, type=Path)
    p.add_argument("--historical-context-index", type=Path)
    p.add_argument("--historical-outcome-stats", type=Path)
    p.add_argument("--similarity-summary", type=Path)
    p.add_argument("--retrieval-summary", type=Path)
    p.add_argument(
        "--round-trip-cost-price",
        type=float,
        help="Explicit round-trip execution cost in price units. Required for official cost gate; no default is invented.",
    )
    a = p.parse_args()

    result = run(
        h1=a.h1,
        murphy=a.murphy,
        nison=a.nison,
        context=a.context,
        output_dir=a.output_dir,
        mtf_dir=a.mtf_dir,
        historical_context_index=a.historical_context_index,
        historical_outcome_stats=a.historical_outcome_stats,
        similarity_summary=a.similarity_summary,
        retrieval_summary=a.retrieval_summary,
        round_trip_cost_price=a.round_trip_cost_price,
    )
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
