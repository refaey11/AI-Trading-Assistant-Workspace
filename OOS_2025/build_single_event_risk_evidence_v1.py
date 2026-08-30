from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _csv_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.csv")) if root.exists() else []


def _find_murphy(root: Path) -> Path:
    candidates: list[tuple[int, Path]] = []
    for p in _csv_files(root):
        try:
            cols = set(pd.read_csv(p, nrows=0).columns)
        except Exception:
            continue
        if {"timestamp", "direction"}.issubset(cols):
            score = sum(k in p.name.upper() for k in ("MURPHY", "HISTORICAL", "FANIN", "EVIDENCE"))
            candidates.append((score, p))
    if not candidates:
        raise FileNotFoundError(f"No Murphy CSV with timestamp+direction under {root}")
    candidates.sort(key=lambda x: (-x[0], str(x[1])))
    return candidates[0][1]


def _one_row(path: Path, ts: pd.Timestamp) -> pd.Series:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], utc=True, errors="raise", format="mixed"
    )
    part = df.loc[df["timestamp"].eq(ts)].copy()
    if len(part) != 1:
        raise ValueError(f"{path}: expected exactly one row at {ts.isoformat()}, observed={len(part)}")
    return part.iloc[0]


def _scalar(row: pd.Series, names: tuple[str, ...], label: str) -> float:
    for name in names:
        if name in row.index and pd.notna(row[name]) and str(row[name]).strip() != "":
            return float(row[name])
    raise ValueError(f"missing {label}; tried {names}")


def build(*, timestamp: str, h1: Path, market_state: Path, murphy_root: Path, output: Path,
          equity: float = 10000.0, peak_equity: float = 10000.0,
          prior_loss_streak: int = 0) -> dict:
    ts = pd.Timestamp(timestamp, tz="UTC")
    if not (2016 <= ts.year <= 2024):
        raise ValueError("Gate 3C risk evidence is restricted to 2016-2024")
    if equity <= 0 or peak_equity <= 0 or prior_loss_streak < 0:
        raise ValueError("invalid evaluation account bootstrap")

    h1_row = _one_row(h1, ts)
    market_row = _one_row(market_state, ts)
    murphy_path = _find_murphy(murphy_root)
    murphy_row = _one_row(murphy_path, ts)

    direction = str(murphy_row.get("direction") or "").upper()
    if direction in {"BULLISH"}:
        direction = "BUY"
    elif direction in {"BEARISH"}:
        direction = "SELL"
    if direction not in {"BUY", "SELL"}:
        raise ValueError(f"INVALID_DIRECTION:{direction}")

    entry = _scalar(h1_row, ("entry_price", "close"), "entry_price")
    atr = _scalar(market_row, ("atr", "atr20", "H1_atr"), "atr")

    frozen = _load(ROOT / "OOS_2025" / "frozen_candidate_risk_profile_v1.py", "frozen_candidate_risk")
    canonical = _load(ROOT / "risk_engine" / "risk_execution_runtime_v1.py", "canonical_risk")

    frozen_result = frozen.evaluate_frozen_candidate_risk(
        direction=direction,
        equity=equity,
        peak_equity=peak_equity,
        entry=entry,
        atr=atr,
        prior_loss_streak=prior_loss_streak,
    )
    if not frozen_result.risk_pass:
        raise ValueError(f"FROZEN_CANDIDATE_RISK_BLOCKED:{frozen_result.reason}")

    stop_distance = 0.75 * atr
    reward_distance = 2.0 * stop_distance
    canonical_result = canonical.evaluate_risk(
        canonical.RiskRequest(
            equity=equity,
            risk_percent=frozen_result.risk_percent,
            entry_price=entry,
            stop_distance=stop_distance,
            take_profit_distance=reward_distance,
            stop_mode="structure",
            risk_budget_locked=True,
        ),
        direction,
        atr,
    )
    if not canonical_result.risk_pass:
        raise ValueError(f"CANONICAL_RISK_ENGINE_BLOCKED:{canonical_result.reason}")

    fields = {
        "timestamp": ts.isoformat(),
        "direction": direction,
        "equity": equity,
        "peak_equity": peak_equity,
        "prior_loss_streak": prior_loss_streak,
        "entry_price": entry,
        "atr": atr,
        "risk_percent": frozen_result.risk_percent,
        "stop_loss": frozen_result.stop_loss,
        "take_profit": frozen_result.take_profit,
        "position_size": frozen_result.position_size,
        "risk_pass": True,
        "risk_money": equity * frozen_result.risk_percent,
        "rr": 2.0,
        "risk_budget_locked": True,
        "stop_mode": "structure",
        "authoritative": True,
        "authority_scope": "evaluation_single_event",
        "account_state_source": "explicit_single_event_evaluation_bootstrap",
        "risk_profile_source": "OOS_2025/frozen_candidate_risk_profile_v1.py",
        "canonical_risk_engine_source": "risk_engine/risk_execution_runtime_v1.py",
        "frozen_candidate_contract": "0.75_ATR_stop_2R_target",
    }
    if abs(float(fields["stop_loss"]) - float(canonical_result.stop_loss)) > 1e-12:
        raise ValueError("FROZEN_VS_CANONICAL_STOP_MISMATCH")
    if abs(float(fields["take_profit"]) - float(canonical_result.take_profit)) > 1e-12:
        raise ValueError("FROZEN_VS_CANONICAL_TP_MISMATCH")
    if abs(float(fields["position_size"]) - float(canonical_result.position_size)) > 1e-12:
        raise ValueError("FROZEN_VS_CANONICAL_POSITION_MISMATCH")

    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([fields]).to_csv(output, index=False)
    return {"status": "PASS", "timestamp": ts.isoformat(), "direction": direction, "risk_percent": frozen_result.risk_percent,
            "stop_loss": frozen_result.stop_loss, "take_profit": frozen_result.take_profit,
            "position_size": frozen_result.position_size, "authority_scope": "evaluation_single_event"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--timestamp", required=True)
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--murphy-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--equity", type=float, default=10000.0)
    p.add_argument("--peak-equity", type=float, default=10000.0)
    p.add_argument("--prior-loss-streak", type=int, default=0)
    a = p.parse_args()
    report = build(timestamp=a.timestamp, h1=a.h1, market_state=a.market_state,
                   murphy_root=a.murphy_root, output=a.output, equity=a.equity,
                   peak_equity=a.peak_equity, prior_loss_streak=a.prior_loss_streak)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
