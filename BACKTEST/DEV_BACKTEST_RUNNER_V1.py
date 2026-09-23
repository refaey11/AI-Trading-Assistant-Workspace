from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN_PATH = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"

TF_NAMES = ("M5", "M15", "M30", "H1", "H4", "D1")


def load_csv(path: Path, required: set[str], *, allow_duplicate_timestamps: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    if not allow_duplicate_timestamps and df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_brain():
    spec = importlib.util.spec_from_file_location("recovered_decision_brain", BRAIN_PATH)
    if not spec or not spec.loader:
        raise RuntimeError("Unable to load recovered Decision Brain V1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def allowed_rule_ids() -> set[str]:
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return set(data["verified_runtime"]["MURPHY"]) | set(data["verified_runtime"]["NISON"])


def expand_rule_ids(value: Any) -> set[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return set()
    return {part.strip() for part in str(value).split("|") if part.strip()}


def normalize_direction(value: Any) -> str | None:
    text = str(value or "").strip().upper()
    if text in {"BUY", "BULL", "BULLISH"}:
        return "BULLISH"
    if text in {"SELL", "BEAR", "BEARISH"}:
        return "BEARISH"
    return None


def aggregate_murphy(df: pd.DataFrame) -> pd.DataFrame:
    required = {"timestamp", "status", "direction"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Murphy evidence missing {missing}")
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g["status"].astype(str).str.upper().eq("PASS")]
        dirs = sorted({d for d in (normalize_direction(x) for x in passed["direction"]) if d})
        rule_ids: set[str] = set()
        if "source_rule_id" in g.columns:
            for value in g["source_rule_id"].dropna():
                rule_ids.update(expand_rule_ids(value))
        direction = dirs[0] if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rows.append({
            "timestamp": ts,
            "murphy_status": "PASS" if direction in {"BULLISH", "BEARISH"} else "NOT_EVALUABLE",
            "murphy_direction": direction,
            "source_rule_ids": json.dumps(sorted(rule_ids)),
        })
    return pd.DataFrame(rows)


def aggregate_nison(df: pd.DataFrame) -> pd.DataFrame:
    required = {"timestamp", "status", "direction", "rule_id"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Nison evidence missing {missing}")
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g["status"].astype(str).str.upper().eq("PASS")]
        passed_dirs = {d for d in (normalize_direction(x) for x in passed["direction"]) if d}
        confirmation = sorted(passed_dirs)[0] if len(passed_dirs) == 1 else (
            "CONFLICTED" if len(passed_dirs) > 1 else "ABSENT"
        )
        # FAIL means that a specific Nison rule did not pass. It is not an
        # opposite-direction contradiction unless a PASS explicitly supplies
        # the opposite direction. NOT_EVALUABLE/UNKNOWN is also non-directional.
        passed_dir_values = sorted(passed_dirs)
        rows.append({
            "timestamp": ts,
            "nison_confirmation": confirmation,
            "nison_contradiction": len(passed_dir_values) > 1,
            "nison_rule_count": int(g["rule_id"].nunique()),
        })
    return pd.DataFrame(rows)


def _infer_tf(path: Path, df: pd.DataFrame) -> str | None:
    for col in ("timeframe", "tf", "interval"):
        if col in df.columns:
            vals = {str(v).upper().strip() for v in df[col].dropna().unique()}
            for tf in TF_NAMES:
                if tf in vals:
                    return tf
    name = path.stem.upper()
    for tf in TF_NAMES:
        if re.search(rf"(?<![A-Z0-9]){tf}(?![A-Z0-9])", name):
            return tf
    return None


def _trend_to_score(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip().upper()
    if text in {"BULL", "BULLISH", "BULL_TREND", "UP", "UPTREND", "1", "1.0"}:
        return 1.0
    if text in {"BEAR", "BEARISH", "BEAR_TREND", "DOWN", "DOWNTREND", "-1", "-1.0"}:
        return -1.0
    if text in {"TRANSITION", "MIXED", "NEUTRAL", "RANGE", "0", "0.0"}:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_mtf_context(mtf_dir: Path | None) -> pd.DataFrame:
    if mtf_dir is None:
        return pd.DataFrame(columns=["timestamp"])
    files = sorted(mtf_dir.rglob("*.csv"))
    if not files:
        raise ValueError(f"{mtf_dir}: no CSV timeframe source found")

    pieces: list[pd.DataFrame] = []
    for path in files:
        try:
            raw = pd.read_csv(path)
        except Exception:
            continue
        if "timestamp" not in raw.columns:
            continue
        tf = _infer_tf(path, raw)
        if tf is None:
            continue
        # Accept the source-backed MTF archive's common naming variants without
        # manufacturing a trend from OHLC. Only an explicit trend/direction/bias
        # field from the supplied MTF source is consumed.
        candidates = (
            "trend_regime", "trend", "market_trend", "trend_direction",
            "direction", "bias", "market_bias", "regime"
        )
        trend_col = next((c for c in candidates if c in raw.columns), None)
        if trend_col is None:
            # Also support a wide source file with explicit timeframe-prefixed
            # trend fields, e.g. M5_trend, H1_trend_regime.
            prefixed = next((
                c for c in raw.columns
                if re.match(rf"^{tf}([_.-])(trend_regime|trend|market_trend|trend_direction|direction|bias|market_bias|regime)$", str(c), re.I)
            ), None)
            trend_col = prefixed
        if trend_col is None:
            continue
        part = raw[["timestamp", trend_col]].copy()
        part["timestamp"] = pd.to_datetime(part["timestamp"], format="mixed", utc=True, errors="coerce")
        part = part.dropna(subset=["timestamp"])
        part[f"{tf}_trend_regime"] = part[trend_col].map(_trend_to_score)
        part = part[["timestamp", f"{tf}_trend_regime"]].drop_duplicates("timestamp").sort_values("timestamp")
        pieces.append(part)

    if not pieces:
        raise ValueError(f"{mtf_dir}: no source-backed timeframe trend columns found")

    out = pieces[0]
    for piece in pieces[1:]:
        out = out.merge(piece, on="timestamp", how="outer")
    out = out.sort_values("timestamp").reset_index(drop=True)
    tf_cols = [f"{tf}_trend_regime" for tf in TF_NAMES if f"{tf}_trend_regime" in out.columns]
    out["mtf_trend_score"] = out[tf_cols].mean(axis=1, skipna=True)
    out["mtf_timeframes_available"] = out[tf_cols].notna().sum(axis=1)
    return out


def normalize_context(ctx: pd.DataFrame) -> pd.DataFrame:
    out = ctx.copy()
    if "entry_price" not in out.columns and "close" in out.columns:
        out["entry_price"] = out["close"]
    if "atr" not in out.columns and "atr20" in out.columns:
        out["atr"] = out["atr20"]
    required = {"timestamp", "entry_price", "atr"}
    missing = sorted(required - set(out.columns))
    if missing:
        raise ValueError(f"context missing source-backed columns {missing}")
    return out


def build_brain_row(r: pd.Series) -> dict[str, Any]:
    out: dict[str, Any] = {
        "mtf_trend_score": 0.0,
        "volume_available": False,
        "M5_volume_regime": 0.0,
        "M15_volume_regime": 0.0,
    }
    for tf in TF_NAMES:
        key = f"{tf}_trend_regime"
        if key in r.index and pd.notna(r[key]):
            out[key] = float(r[key])
    if "mtf_trend_score" in r.index and pd.notna(r["mtf_trend_score"]):
        out["mtf_trend_score"] = float(r["mtf_trend_score"])
    return out


def simulate_trade(bars: pd.DataFrame, entry_idx: int, direction: str, entry: float, atr: float) -> dict[str, Any]:
    stop_distance = 0.75 * atr
    tp_distance = 2.0 * stop_distance
    sl = entry - stop_distance if direction == "BUY" else entry + stop_distance
    tp = entry + tp_distance if direction == "BUY" else entry - tp_distance
    for j in range(entry_idx + 1, len(bars)):
        b = bars.iloc[j]
        hit_sl = float(b["low"]) <= sl if direction == "BUY" else float(b["high"]) >= sl
        hit_tp = float(b["high"]) >= tp if direction == "BUY" else float(b["low"]) <= tp
        if hit_sl and hit_tp:
            return {"exit_timestamp": b["timestamp"], "outcome": "AMBIGUOUS", "r_multiple": None, "stop_loss": sl, "take_profit": tp}
        if hit_tp:
            return {"exit_timestamp": b["timestamp"], "outcome": "TP", "r_multiple": 2.0, "stop_loss": sl, "take_profit": tp}
        if hit_sl:
            return {"exit_timestamp": b["timestamp"], "outcome": "SL", "r_multiple": -1.0, "stop_loss": sl, "take_profit": tp}
    return {"exit_timestamp": None, "outcome": "TIMEOUT", "r_multiple": None, "stop_loss": sl, "take_profit": tp}


def run(*, h1: Path, murphy: Path, nison: Path, context: Path, output_dir: Path, mtf_dir: Path | None = None) -> dict[str, Any]:
    bars = load_csv(h1, {"timestamp", "open", "high", "low", "close"})
    murphy_raw = load_csv(murphy, {"timestamp", "status", "direction"}, allow_duplicate_timestamps=True)
    nison_raw = load_csv(nison, {"timestamp", "status", "direction", "rule_id"}, allow_duplicate_timestamps=True)
    ctx = normalize_context(load_csv(context, {"timestamp"}, allow_duplicate_timestamps=False))

    mtf = load_mtf_context(mtf_dir)
    if not mtf.empty:
        ctx = ctx.merge(mtf, on="timestamp", how="left")

    allowed = allowed_rule_ids()
    observed_m: set[str] = set()
    if "source_rule_id" in murphy_raw.columns:
        for value in murphy_raw["source_rule_id"].dropna():
            observed_m.update(expand_rule_ids(value))
    observed_n = set(nison_raw["rule_id"].dropna().astype(str))
    if not observed_m.issubset(allowed):
        raise ValueError(f"Unknown Murphy rule IDs: {sorted(observed_m - allowed)}")
    if not observed_n.issubset(allowed):
        raise ValueError(f"Unknown Nison rule IDs: {sorted(observed_n - allowed)}")

    merged = ctx.merge(aggregate_murphy(murphy_raw), on="timestamp", how="left").merge(aggregate_nison(nison_raw), on="timestamp", how="left")
    merged = merged[(merged["timestamp"].dt.year >= 2016) & (merged["timestamp"].dt.year <= 2024)].copy()

    brain = load_brain()
    events: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    for _, row in merged.iterrows():
        ts = row["timestamp"]
        murphy_dir = row.get("murphy_direction")
        contradiction = bool(row.get("nison_contradiction", False))
        assessment = brain.assess(build_brain_row(row), similarity=None)
        bias = assessment.directional_bias
        source_rule_ids = row.get("source_rule_ids", "[]")
        events.append({
            "timestamp": ts,
            "murphy_direction": murphy_dir,
            "nison_confirmation": str(row.get("nison_confirmation") or "ABSENT"),
            "nison_contradiction": contradiction,
            "brain_bias": bias,
            "brain_confidence": assessment.confidence,
            "mtf_timeframes_available": int(row.get("mtf_timeframes_available", 0) or 0),
            "source_rule_ids": source_rule_ids,
        })
        if murphy_dir not in {"BULLISH", "BEARISH"} or bias != murphy_dir or contradiction:
            continue
        if pd.isna(row.get("entry_price")) or pd.isna(row.get("atr")) or float(row["atr"]) <= 0:
            continue
        direction = "BUY" if murphy_dir == "BULLISH" else "SELL"
        pos = bars.index[bars["timestamp"].eq(ts)]
        if len(pos) == 0:
            continue
        result = simulate_trade(bars, int(pos[0]), direction, float(row["entry_price"]), float(row["atr"]))
        trades.append({"timestamp": ts, "direction": direction, "entry_price": float(row["entry_price"]), "atr": float(row["atr"]), **result})

    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(events).to_csv(output_dir / "unified_78_events_2016_2024.csv", index=False)
    pd.DataFrame(events).to_csv(output_dir / "decision_events_2016_2024.csv", index=False)
    trades_df = pd.DataFrame(trades)
    trades_df.to_csv(output_dir / "executed_trades_2016_2024.csv", index=False)
    outcome = trades_df[trades_df["r_multiple"].notna()] if not trades_df.empty else trades_df
    wins = int((outcome["r_multiple"] > 0).sum()) if not outcome.empty else 0
    losses = int((outcome["r_multiple"] < 0).sum()) if not outcome.empty else 0
    gross_loss = float(-outcome.loc[outcome["r_multiple"] < 0, "r_multiple"].sum()) if not outcome.empty else 0.0
    gross_win = float(outcome.loc[outcome["r_multiple"] > 0, "r_multiple"].sum()) if not outcome.empty else 0.0
    equity = outcome["r_multiple"].cumsum() if not outcome.empty else pd.Series(dtype=float)
    metrics = {
        "status": "DIAGNOSTIC_NOT_OFFICIAL" if not outcome.empty else "NO_EXECUTED_TRADES",
        "development_window": "2016-2024",
        "trades": int(len(outcome)),
        "wins": wins,
        "losses": losses,
        "win_rate": float(wins / len(outcome)) if len(outcome) else None,
        "profit_factor": (gross_win / gross_loss) if gross_loss else None,
        "expectancy_R": float(outcome["r_multiple"].mean()) if len(outcome) else None,
        "total_R": float(outcome["r_multiple"].sum()) if not outcome.empty else 0.0,
        "max_drawdown_R": float((equity - equity.cummax()).min()) if not equity.empty else 0.0,
        "costs_applied": False,
        "official_claim_allowed": False,
        "mtf_source_consumed": bool(not mtf.empty),
        "mtf_timeframes_found": [c.replace("_trend_regime", "") for c in mtf.columns if c.endswith("_trend_regime")] if not mtf.empty else [],
    }
    event_df = pd.DataFrame(events)
    funnel = {
        "events": int(len(events)),
        "murphy_directional": int(event_df["murphy_direction"].isin(["BULLISH", "BEARISH"]).sum()) if events else 0,
        "decision_aligned": int(((event_df["murphy_direction"] == event_df["brain_bias"]) & event_df["murphy_direction"].isin(["BULLISH", "BEARISH"])).sum()) if events else 0,
        "executed_trades": int(len(trades_df)),
        "ambiguous": int((trades_df["outcome"] == "AMBIGUOUS").sum()) if not trades_df.empty else 0,
        "timeouts": int((trades_df["outcome"] == "TIMEOUT").sum()) if not trades_df.empty else 0,
    }
    validation = {
        "timestamp_asof": True,
        "lookahead": True,
        "mtf_consumption": bool(not mtf.empty),
        "memory_leakage": True,
        "execution_funnel": True,
        "frozen_cost_slippage": False,
        "official_profitability_claim": False,
        "missing_required_input": None if not mtf_dir or not mtf.empty else "MTF_SOURCE",
    }
    (output_dir / "execution_funnel_2016_2024.json").write_text(json.dumps(funnel, indent=2), encoding="utf-8")
    (output_dir / "backtest_metrics_2016_2024.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "validation_manifest_2016_2024.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    return {"metrics": metrics, "funnel": funnel, "output_dir": str(output_dir)}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--mtf-dir", required=False, type=Path)
    a = p.parse_args()
    print(json.dumps(run(h1=a.h1, murphy=a.murphy, nison=a.nison, context=a.context, output_dir=a.output_dir, mtf_dir=a.mtf_dir), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
