from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

DIRECTIONS = {"BUY", "SELL", "BULLISH", "BEARISH"}
MTF_FIELDS = [
    "mtf_trend_score", "M5_trend_regime", "M15_trend_regime",
    "M30_trend_regime", "H1_trend_regime", "H4_trend_regime", "D1_trend_regime",
]
NISON_IDS = {f"NISON_{i:04d}" for i in range(1, 45)}


def csv_with_columns(root: Path, required: set[str], hints: tuple[str, ...]) -> Path:
    candidates = []
    for path in sorted(root.rglob("*.csv")):
        try:
            columns = set(pd.read_csv(path, nrows=0).columns)
        except Exception:
            continue
        if required.issubset(columns):
            score = sum(hint in path.name.upper() for hint in hints)
            candidates.append((score, path))
    if not candidates:
        raise FileNotFoundError(f"no CSV under {root} with columns {sorted(required)}")
    candidates.sort(key=lambda item: (-item[0], str(item[1])))
    if len(candidates) > 1 and candidates[0][0] == candidates[1][0]:
        raise ValueError(f"ambiguous source CSV selection under {root}: {candidates[0][1]}, {candidates[1][1]}")
    return candidates[0][1]


def split_ids(value: object) -> set[str]:
    return {part.strip().upper() for part in str(value or "").split("|") if part.strip()}


def _mtf_frame(root: Path, year: int) -> tuple[Path, pd.DataFrame]:
    expected = root / f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"
    matches = [path for path in root.rglob("*.csv") if path.name.upper() == expected.name.upper()]
    if len(matches) != 1:
        raise ValueError(f"BLOCKED_MTF_ANNUAL_SOURCE_CARDINALITY:year={year}:observed={len(matches)}")
    path = matches[0]
    frame = pd.read_csv(path)
    required = {"timestamp", *MTF_FIELDS}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"BLOCKED_MTF_SOURCE_SCHEMA:{path.name}:missing={sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce", format="mixed")
    return path, frame


def _mtf_valid(frame: pd.DataFrame, ts: pd.Timestamp) -> bool:
    eligible = frame.loc[frame["timestamp"].notna() & frame["timestamp"].le(ts)]
    if eligible.empty:
        return False
    latest = eligible["timestamp"].max()
    if ts - latest > pd.Timedelta(minutes=5):
        return False
    selected = eligible.loc[eligible["timestamp"].eq(latest)]
    if len(selected) != 1:
        return False
    row = selected.iloc[0]
    return all(pd.notna(row[field]) and not (isinstance(row[field], str) and not row[field].strip())
               for field in MTF_FIELDS)


def select_candidate(*, murphy_root: Path, registry_path: Path, h1_path: Path,
                     market_state_path: Path, nison_path: Path, mtf_root: Path) -> str:
    registry = pd.read_csv(registry_path, dtype=str).fillna("")
    allowed = set(registry.loc[
        registry["decision_eligible"].str.upper().str.strip().eq("YES")
        & registry["historical_status"].str.upper().str.strip().eq("SOURCE_BACKED_HISTORICAL_EVALUATION"),
        "rule_id",
    ].str.upper().str.strip())

    murphy_path = csv_with_columns(
        murphy_root,
        {"timestamp", "direction", "status", "source_rule_id", "pass_rule_id"},
        ("MURPHY", "2016_2024", "FULL", "EVIDENCE"),
    )
    murphy = pd.read_csv(murphy_path, dtype={"direction": str, "status": str, "source_rule_id": str, "pass_rule_id": str})
    murphy["timestamp"] = pd.to_datetime(murphy["timestamp"], utc=True, errors="coerce", format="mixed")
    status = murphy["status"].fillna("").str.upper().str.strip()
    direction = murphy["direction"].fillna("").str.upper().str.strip()
    pass_id = murphy["pass_rule_id"].fillna("").str.upper().str.strip()
    candidates = murphy.loc[
        murphy["timestamp"].notna()
        & murphy["timestamp"].dt.year.between(2016, 2024)
        & status.eq("PASS")
        & direction.isin(DIRECTIONS)
        & pass_id.isin(allowed)
    ].copy()
    candidates = candidates.loc[
        candidates.apply(lambda row: row["pass_rule_id"] in split_ids(row["source_rule_id"]), axis=1)
    ].sort_values("timestamp", kind="stable")

    if candidates.empty:
        raise ValueError("BLOCKED_NO_ELIGIBLE_MURPHY_DIRECTIONAL_PASS_IN_2016_2024")

    h1 = pd.read_csv(h1_path)
    market = pd.read_csv(market_state_path)
    nison = pd.read_csv(nison_path)
    for frame, label in ((h1, "H1"), (market, "MARKET_STATE"), (nison, "NISON")):
        if "timestamp" not in frame.columns:
            raise ValueError(f"BLOCKED_{label}_TIMESTAMP_COLUMN_MISSING")
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce", format="mixed")
    nison_id_col = "source_rule_id" if "source_rule_id" in nison.columns else "rule_id"
    if nison_id_col not in nison.columns:
        raise ValueError("BLOCKED_NISON_RULE_ID_COLUMN_MISSING")

    mtf_cache: dict[int, pd.DataFrame] = {}
    mtf_paths: dict[int, Path] = {}
    rejected = {"h1": 0, "market_state": 0, "nison_fanin": 0, "mtf": 0, "ambiguous_murphy": 0}

    for ts, group in candidates.groupby("timestamp", sort=True):
        if len(group) != 1:
            rejected["ambiguous_murphy"] += 1
            continue
        if len(h1.loc[h1["timestamp"].eq(ts)]) != 1:
            rejected["h1"] += 1
            continue
        if len(market.loc[market["timestamp"].eq(ts)]) != 1:
            rejected["market_state"] += 1
            continue
        nison_rows = nison.loc[nison["timestamp"].eq(ts)]
        nison_ids = set()
        for value in nison_rows[nison_id_col].dropna():
            nison_ids.update(split_ids(value))
        if nison_ids != NISON_IDS:
            rejected["nison_fanin"] += 1
            continue
        year = ts.year
        try:
            if year not in mtf_cache:
                mtf_paths[year], mtf_cache[year] = _mtf_frame(mtf_root, year)
        except (FileNotFoundError, ValueError):
            rejected["mtf"] += 1
            continue
        if not _mtf_valid(mtf_cache[year], ts):
            rejected["mtf"] += 1
            continue
        print(f"SELECTED_EVENT={ts.isoformat()}")
        print(f"MURPHY_SOURCE={murphy_path}")
        print(f"MTF_SOURCE={mtf_paths[year]}")
        print(f"REJECTED_COUNTS={rejected}")
        return ts.isoformat().replace("+00:00", "Z")

    raise ValueError(f"BLOCKED_NO_COMPLETE_EVENT_CANDIDATE:rejected={rejected}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--murphy-root", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--h1", type=Path, required=True)
    parser.add_argument("--market-state", type=Path, required=True)
    parser.add_argument("--nison", type=Path, required=True)
    parser.add_argument("--mtf-root", type=Path, required=True)
    args = parser.parse_args()
    print(select_candidate(
        murphy_root=args.murphy_root, registry_path=args.registry, h1_path=args.h1,
        market_state_path=args.market_state, nison_path=args.nison, mtf_root=args.mtf_root,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
