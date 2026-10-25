#!/usr/bin/env python3
"""Frozen three-candidate OOS 2025 evaluator.

This script is evaluation-only. It never tunes thresholds, infers missing MTF
evidence, or enables execution. Source columns must be explicit and auditable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

CANDIDATES = (
    "C1_HIGH_STRONG_BEARISH_MTF",
    "C2_HIGH_H4_BEARISH",
    "C3_SELL_HIGH",
)
STOP_ATR = 0.75
TARGET_R = 2.0


def read_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp column")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp values")
    return df.sort_values("timestamp").reset_index(drop=True)


def find_col(df: pd.DataFrame, aliases: tuple[str, ...], label: str, required: bool = True):
    lookup = {str(c).strip().lower(): c for c in df.columns}
    for alias in aliases:
        if alias.lower() in lookup:
            return lookup[alias.lower()]
    if required:
        raise ValueError(f"missing authoritative {label} column; accepted names={aliases}; available={list(df.columns)}")
    return None


def truthy(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().isin({"true", "1", "yes", "high", "pass"})


def normalized(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().str.replace("-", "_", regex=False).str.replace(" ", "_", regex=False)


def bearish_mtf_mask(mtf: pd.DataFrame) -> pd.Series:
    align_col = find_col(
        mtf,
        ("mtf_alignment", "alignment", "mtf_regime", "alignment_regime", "trend_alignment"),
        "strong bearish MTF alignment",
        required=False,
    )
    if align_col:
        values = normalized(mtf[align_col])
        return values.isin({"strong_bearish", "strongly_bearish", "bearish_strong"})
    # A source-backed boolean flag is accepted only if explicitly present.
    flag_col = find_col(mtf, ("strong_bearish_mtf", "mtf_strong_bearish"), "strong bearish MTF flag", required=False)
    if flag_col:
        return truthy(mtf[flag_col])
    # Source-backed fallback: require every canonical timeframe regime to be
    # present and bearish. Never infer strong alignment from a partial subset.
    canonical = ("M5_trend_regime", "M15_trend_regime", "M30_trend_regime",
                 "H1_trend_regime", "H4_trend_regime", "D1_trend_regime")
    lookup = {str(c).strip().lower(): c for c in mtf.columns}
    cols = [lookup.get(name.lower()) for name in canonical]
    if all(col is not None for col in cols):
        regimes = mtf[cols].apply(pd.to_numeric, errors="coerce")
        return regimes.notna().all(axis=1) & regimes.eq(-1).all(axis=1)
    # Do not infer "strong" from a single timeframe or missing data.
    raise ValueError(
        "MTF source lacks explicit strong-bearish alignment and the complete "
        "six-timeframe trend regime set; refusing to infer from partial evidence"
    )


def h4_bearish_mask(mtf: pd.DataFrame) -> pd.Series:
    col = find_col(mtf, ("H4_trend_regime", "h4_trend_regime", "H4_regime", "h4_regime"), "H4 trend regime")
    values = pd.to_numeric(mtf[col], errors="coerce")
    if values.isna().any():
        # Missing rows remain non-matching, never coerced to bearish.
        return values.eq(-1)
    return values.eq(-1)


def atr_series(h1: pd.DataFrame) -> pd.Series:
    col = find_col(h1, ("atr", "atr14", "atr_14", "ATR_14"), "H1 ATR", required=False)
    if col:
        return pd.to_numeric(h1[col], errors="coerce")
    high = pd.to_numeric(h1[find_col(h1, ("high",), "H1 high")], errors="coerce")
    low = pd.to_numeric(h1[find_col(h1, ("low",), "H1 low")], errors="coerce")
    close = pd.to_numeric(h1[find_col(h1, ("close",), "H1 close")], errors="coerce")
    prev_close = close.shift(1)
    tr = pd.concat([(high - low).abs(), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.rolling(14, min_periods=14).mean()


def evaluate_candidate(candidate_id: str, signals: pd.DataFrame, h1: pd.DataFrame) -> tuple[dict, list[dict]]:
    opens = pd.to_numeric(h1["open"], errors="coerce")
    highs = pd.to_numeric(h1["high"], errors="coerce")
    lows = pd.to_numeric(h1["low"], errors="coerce")
    atrs = atr_series(h1)
    h1_times = list(h1["timestamp"])
    trades: list[dict] = []
    seen_entry_idx = -1
    skipped_overlap = 0

    for signal in signals.sort_values("timestamp").itertuples(index=False):
        signal_ts = signal.timestamp
        # Locate the latest H1 bar at or before the event timestamp. This is
        # strictly as-of; the entry is still the next H1 open after that bar.
        import bisect
        signal_idx = bisect.bisect_right(h1_times, signal_ts) - 1
        if signal_idx < 0:
            trades.append({"candidate_id": candidate_id, "timestamp": signal_ts.isoformat(), "status": "NOT_EVALUABLE", "reason": "NO_PRIOR_H1_BAR"})
            continue
        entry_idx = signal_idx + 1  # frozen next-H1-open entry protocol
        if entry_idx >= len(h1):
            trades.append({"candidate_id": candidate_id, "timestamp": signal_ts.isoformat(), "status": "NOT_EVALUABLE", "reason": "NO_NEXT_H1_BAR"})
            continue
        if entry_idx <= seen_entry_idx:
            skipped_overlap += 1
            continue
        entry = opens.iloc[entry_idx]
        atr = atrs.iloc[signal_idx]
        if pd.isna(entry) or pd.isna(atr) or entry <= 0 or atr <= 0:
            trades.append({"candidate_id": candidate_id, "timestamp": signal_ts.isoformat(), "status": "NOT_EVALUABLE", "reason": "INVALID_ENTRY_OR_ATR"})
            continue
        direction = str(getattr(signal, "direction", "SELL")).upper()
        if direction not in {"BUY", "SELL"}:
            direction = "SELL" if candidate_id in {CANDIDATES[0], CANDIDATES[1], CANDIDATES[2]} else ""
        distance = STOP_ATR * float(atr)
        sl = float(entry) - distance if direction == "BUY" else float(entry) + distance
        tp = float(entry) + TARGET_R * distance if direction == "BUY" else float(entry) - TARGET_R * distance
        outcome, exit_idx, ambiguous = "OPEN", len(h1) - 1, False
        for j in range(entry_idx, len(h1)):
            hi, lo = highs.iloc[j], lows.iloc[j]
            if pd.isna(hi) or pd.isna(lo):
                continue
            stop_hit = lo <= sl if direction == "BUY" else hi >= sl
            target_hit = hi >= tp if direction == "BUY" else lo <= tp
            if stop_hit and target_hit:
                outcome, exit_idx, ambiguous = "AMBIGUOUS", j, True
                break
            if stop_hit:
                outcome, exit_idx = "SL", j
                break
            if target_hit:
                outcome, exit_idx = "TP", j
                break
        r = 2.0 if outcome == "TP" else (-1.0 if outcome == "SL" else None)
        trades.append({
            "candidate_id": candidate_id,
            "timestamp": signal_ts.isoformat(),
            "entry_timestamp": h1.iloc[entry_idx]["timestamp"].isoformat(),
            "exit_timestamp": h1.iloc[exit_idx]["timestamp"].isoformat(),
            "direction": direction,
            "status": outcome,
            "ambiguous": ambiguous,
            "entry_price": float(entry),
            "atr": float(atr),
            "stop_loss": sl,
            "take_profit": tp,
            "R": r,
            "reason": "SAME_BAR_SL_TP_AMBIGUITY" if ambiguous else "",
        })
        seen_entry_idx = exit_idx

    evaluated = [t for t in trades if t["status"] in {"TP", "SL", "AMBIGUOUS"}]
    tp_n = sum(t["status"] == "TP" for t in evaluated)
    sl_n = sum(t["status"] == "SL" for t in evaluated)
    amb_n = sum(t["status"] == "AMBIGUOUS" for t in evaluated)
    closed = tp_n + sl_n
    total_r = sum(float(t["R"]) for t in evaluated if t["R"] is not None)
    wins_r = sum(float(t["R"]) for t in evaluated if t["R"] is not None and t["R"] > 0)
    losses_r = abs(sum(float(t["R"]) for t in evaluated if t["R"] is not None and t["R"] < 0))
    summary = {
        "candidate_id": candidate_id,
        "events": len(signals),
        "signals_skipped_overlap": skipped_overlap,
        "evaluated": len(evaluated),
        "TP": tp_n,
        "SL": sl_n,
        "ambiguous": amb_n,
        "timeout_or_open": sum(t["status"] == "OPEN" for t in trades),
        "not_evaluable": sum(t["status"] == "NOT_EVALUABLE" for t in trades),
        "win_rate": (tp_n / closed) if closed else None,
        "expectancy_R": (total_r / closed) if closed else None,
        "profit_factor": (wins_r / losses_r) if losses_r else (None if wins_r == 0 else "INF"),
        "total_R": total_r,
        "drawdown_R": None,
        "evaluation_status": "EVALUATION_ONLY",
    }
    # Drawdown uses sequential non-ambiguous closed outcomes only.
    equity, peak, max_dd = 0.0, 0.0, 0.0
    for trade in evaluated:
        if trade["R"] is None:
            continue
        equity += float(trade["R"])
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)
    summary["drawdown_R"] = max_dd
    return summary, trades


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--murphy", required=True)
    ap.add_argument("--h1", required=True)
    ap.add_argument("--market-state", required=True)
    ap.add_argument("--mtf", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    mur = read_csv(args.murphy)
    h1 = read_csv(args.h1)
    market = read_csv(args.market_state)
    mtf = read_csv(args.mtf)

    if set(mur["timestamp"].dt.year.unique()) != {2025}:
        raise ValueError("Murphy evidence must contain 2025 only")
    # The H1 master and market-state files may contain earlier history; use only
    # their 2025 rows for this locked OOS evaluation.
    h1 = h1[h1["timestamp"].dt.year.eq(2025)].reset_index(drop=True)
    market = market[market["timestamp"].dt.year.eq(2025)].reset_index(drop=True)
    mtf = mtf[mtf["timestamp"].dt.year.eq(2025)].reset_index(drop=True)
    if h1.empty or market.empty or mtf.empty:
        raise ValueError("one or more required 2025 source partitions are empty")
    for col in ("open", "high", "low", "close"):
        find_col(h1, (col,), f"H1 {col}")
    h1 = h1.rename(columns={find_col(h1, ("open",), "open"): "open",
                            find_col(h1, ("high",), "high"): "high",
                            find_col(h1, ("low",), "low"): "low",
                            find_col(h1, ("close",), "close"): "close"})
    # The Murphy file is rule evidence (timestamp/status/direction/rule id), not
    # a market-state table. Volatility is sourced from the market-state reader
    # and joined backward/as-of, never inferred from future rows.
    direction_col = find_col(mur, ("direction", "signal_direction"), "Murphy direction")
    mur["direction"] = normalized(mur[direction_col]).str.upper()
    vol_col = find_col(
        market,
        ("volatility_regime", "volatility", "volatility_state", "volatility_level", "atr_volatility_regime"),
        "market-state volatility regime",
    )

    # As-of joins only: context timestamps must never be later than the event.
    mtf = mtf.sort_values("timestamp")
    market = market.sort_values("timestamp")
    base = mur.sort_values("timestamp")
    market_vol = market[["timestamp", vol_col]].rename(columns={vol_col: "_volatility_regime"})
    base = pd.merge_asof(
        base.sort_values("timestamp"),
        market_vol.sort_values("timestamp"),
        on="timestamp",
        direction="backward",
    )
    high_mask = normalized(base["_volatility_regime"]).eq("high")
    market_clock = market[["timestamp"]].rename(columns={"timestamp": "market_timestamp"})
    merged = pd.merge_asof(
        base[["timestamp"]].sort_values("timestamp"),
        market_clock.sort_values("market_timestamp"),
        left_on="timestamp",
        right_on="market_timestamp",
        direction="backward",
    )
    # MTF conditions must be derived from the actual MTF source, not same-named Murphy fields.
    mtf_join = pd.merge_asof(base[["timestamp"]].sort_values("timestamp"), mtf.sort_values("timestamp"), on="timestamp", direction="backward")
    c1_mask = high_mask.reset_index(drop=True) & bearish_mtf_mask(mtf_join).reset_index(drop=True)
    c2_mask = high_mask.reset_index(drop=True) & h4_bearish_mask(mtf_join).reset_index(drop=True)
    c3_mask = high_mask.reset_index(drop=True) & base["direction"].isin({"SELL", "BEARISH"}).reset_index(drop=True)

    # Context is required for provenance and checked as-of; missing context is not filled forward from the future.
    if merged["market_timestamp"].isna().any() or (merged["market_timestamp"] > merged["timestamp"]).any():
        raise ValueError("market-state as-of context missing or future-dated for one or more Murphy event timestamps")
    if not {"open", "high", "low", "close"}.issubset(h1.columns):
        raise ValueError("H1 price schema invalid")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summaries, all_trades = [], []
    for candidate, mask in zip(CANDIDATES, (c1_mask, c2_mask, c3_mask)):
        sig = base.loc[mask, ["timestamp", "direction"]].copy()
        # C1/C2 are short-only frozen bearish candidates; C3 is explicit SELL+HIGH.
        sig["direction"] = "SELL"
        summary, trades = evaluate_candidate(candidate, sig, h1)
        summaries.append(summary)
        all_trades.extend(trades)

    results = pd.DataFrame(summaries)
    results.to_csv(out_dir / "oos_2025_candidate_results.csv", index=False)
    pd.DataFrame(all_trades).to_csv(out_dir / "oos_2025_candidate_trades.csv", index=False)
    manifest = {
        "window": "2025-only",
        "candidate_set_frozen": True,
        "tuning_applied": False,
        "threshold_sweep": False,
        "future_data_used": False,
        "strict_asof_context": True,
        "entry_next_h1_open": True,
        "stop_atr": STOP_ATR,
        "target_R": TARGET_R,
        "candidate_ids": list(CANDIDATES),
        "source_files": {
            "murphy": str(args.murphy),
            "h1": str(args.h1),
            "market_state": str(args.market_state),
            "mtf": str(args.mtf),
        },
        "official_profitability_claim_allowed": False,
        "note": "Evaluation-only diagnostic. Not a canonical three-book Decision Brain result; Nison/TIZ/Risk gates are not evaluated by this candidate-only gate.",
    }
    (out_dir / "oos_2025_candidate_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
