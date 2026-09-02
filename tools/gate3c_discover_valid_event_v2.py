"""Discover a real Gate 3C source-backed event using the canonical as-of semantics.

This tool does not generate evidence. It only finds a timestamp that already has:
- a non-conflicting Murphy directional fan-in event,
- all 44 Nison rule IDs at that timestamp,
- H1 and Market State available as-of the event,
- complete canonical six-TF MTF evidence as-of the event.

It deliberately mirrors the builder's exact/as-of semantics instead of imposing
an artificial exact timestamp requirement on H1 or Market State.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

EXPECTED_NISON = {f"NISON_{i:04d}" for i in range(1, 45)}
REQUIRED_MTF = [
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
]


def parse_ts(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True, errors="coerce", format="mixed")


def exact_murphy_candidates(murphy: pd.DataFrame) -> pd.DataFrame:
    m = murphy.copy()
    m["timestamp"] = parse_ts(m["timestamp"])
    m = m[(m["timestamp"].dt.year >= 2016) & (m["timestamp"].dt.year <= 2024)].dropna(subset=["timestamp"])
    m["status_norm"] = m.get("status", "").astype(str).str.upper().str.strip()
    m["direction_norm"] = (
        m.get("direction", "").astype(str).str.upper().str.strip()
        .replace({"BULLISH": "BUY", "BEARISH": "SELL"})
    )
    m = m[(m["status_norm"] == "PASS") & (m["direction_norm"].isin({"BUY", "SELL"}))]
    rows = []
    for ts, grp in m.groupby("timestamp", sort=True):
        dirs = set(grp["direction_norm"])
        if len(dirs) == 1:
            rows.append((ts, next(iter(dirs)), len(grp)))
    return pd.DataFrame(rows, columns=["timestamp", "murphy_direction", "murphy_rows"])


def nison_candidates(nison: pd.DataFrame) -> pd.DataFrame:
    n = nison.copy()
    n["timestamp"] = parse_ts(n["timestamp"])
    if "source_rule_id" not in n.columns:
        if "rule_id" in n.columns:
            n = n.rename(columns={"rule_id": "source_rule_id"})
        else:
            raise SystemExit("DISCOVERY_NISON_SCHEMA_NO_RULE_ID")
    n = n.dropna(subset=["timestamp"])
    grouped = n.groupby("timestamp", sort=True)
    rows = []
    for ts, grp in grouped:
        ids = {str(x).strip() for x in grp["source_rule_id"].tolist()}
        if ids == EXPECTED_NISON:
            rows.append((ts, len(grp), len(ids)))
    return pd.DataFrame(rows, columns=["timestamp", "nison_rows", "nison_distinct_ids"])


def latest_asof(df: pd.DataFrame, ts: pd.Timestamp) -> pd.Series | None:
    rows = df.loc[df["timestamp"].le(ts)]
    if rows.empty:
        return None
    return rows.iloc[-1]


def discover(murphy_path: Path, nison_path: Path, h1_path: Path, market_path: Path, mtf_path: Path) -> tuple[pd.Timestamp, str, dict]:
    murphy = pd.read_csv(murphy_path, low_memory=False)
    nison = pd.read_csv(nison_path, low_memory=False)
    h1 = pd.read_csv(h1_path, low_memory=False)
    market = pd.read_csv(market_path, low_memory=False)
    mtf = pd.read_csv(mtf_path, low_memory=False)

    for df, name in [(murphy, "murphy"), (nison, "nison"), (h1, "h1"), (market, "market"), (mtf, "mtf")]:
        if "timestamp" not in df.columns:
            raise SystemExit(f"DISCOVERY_MISSING_TIMESTAMP:{name}")
        df["timestamp"] = parse_ts(df["timestamp"])
        df.sort_values("timestamp", inplace=True, kind="stable")

    missing_mtf = [c for c in REQUIRED_MTF if c not in mtf.columns]
    if missing_mtf:
        raise SystemExit(f"DISCOVERY_MTF_FIELD_MISSING:{missing_mtf}")

    mc = exact_murphy_candidates(murphy)
    nc = nison_candidates(nison)
    if mc.empty:
        raise SystemExit("DISCOVERY_NO_MURPHY_DIRECTIONAL_EVENTS")
    if nc.empty:
        raise SystemExit("DISCOVERY_NO_NISON_COMPLETE_44_TIMESTAMPS")

    # Merge the two exact-event clocks first; then validate all context sources as-of.
    candidates = mc.merge(nc, on="timestamp", how="inner").sort_values("timestamp")
    diagnostics = {
        "murphy_directional_timestamps": int(len(mc)),
        "nison_complete_timestamps": int(len(nc)),
        "exact_murphy_nison_overlap_timestamps": int(len(candidates)),
        "h1_asof_pass": 0,
        "market_asof_pass": 0,
        "mtf_asof_pass": 0,
    }
    for row in candidates.itertuples(index=False):
        ts = pd.Timestamp(row.timestamp).tz_convert("UTC")
        h = latest_asof(h1, ts)
        c = latest_asof(market, ts)
        mt = latest_asof(mtf, ts)
        if h is not None:
            diagnostics["h1_asof_pass"] += 1
        if c is not None:
            diagnostics["market_asof_pass"] += 1
        if mt is not None and all(pd.notna(mt.get(col)) for col in REQUIRED_MTF):
            diagnostics["mtf_asof_pass"] += 1
        if h is None or c is None or mt is None:
            continue
        if not all(pd.notna(mt.get(col)) for col in REQUIRED_MTF):
            continue
        return ts, str(row.murphy_direction), diagnostics

    diagnostics["result"] = "NO_VALID_SOURCE_BACKED_EVENT"
    raise SystemExit("DISCOVERY_NO_VALID_SOURCE_BACKED_EVENT:" + str(diagnostics))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--murphy", type=Path, required=True)
    p.add_argument("--nison", type=Path, required=True)
    p.add_argument("--h1", type=Path, required=True)
    p.add_argument("--market", type=Path, required=True)
    p.add_argument("--mtf", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    ts, direction, diagnostics = discover(args.murphy, args.nison, args.h1, args.market, args.mtf)
    lines = [
        f"EVENT_TS={ts.isoformat()}",
        f"MURPHY_DIRECTION={direction}",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("DISCOVERED_EVENT_TS", ts.isoformat())
    print("DISCOVERED_MURPHY_DIRECTION", direction)
    print("DISCOVERY_DIAGNOSTICS", diagnostics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
