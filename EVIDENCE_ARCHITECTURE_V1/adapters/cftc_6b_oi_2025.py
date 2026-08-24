"""CFTC British Pound (096742) Legacy Futures-Only OI adapter.

Purpose
-------
Normalize the authoritative CFTC 2025 futures-only annual archive into
point-in-time evidence records for Murphy rules that explicitly require
British Pound futures Open Interest.

Governance
----------
- No proxy from spot-FX volume/tick volume.
- No interpolation across missing CFTC reports.
- report/as-of date is distinct from availability date.
- A report is usable only after the CFTC publication timestamp supplied by
  the acquisition manifest; otherwise it is NOT_EVALUABLE.
- 2025 is OOS and this adapter is not a tuning mechanism.

The annual archive URL is supplied by CFTC's Historical Compressed page:
https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
and the legacy 2025 Futures-Only archive is:
https://www.cftc.gov/files/dea/history/deacot2025.zip
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from io import BytesIO
from pathlib import Path
import re
import zipfile

import pandas as pd

CFTC_CODE = "096742"
MARKET = "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"

ARCHIVE_URL = "https://www.cftc.gov/files/dea/history/deacot2025.zip"

# CFTC publishes COT reports weekly. Do not hard-code a fake publication
# timestamp for OOS use; the acquisition manifest must supply the actual
# publication timestamp for each report.

@dataclass(frozen=True)
class OIRecord:
    report_date: date
    available_time: datetime | None
    open_interest: int
    source: str
    contract_code: str


def _find_column(columns, candidates):
    normalized = {re.sub(r"[^a-z0-9]+", "", str(c).lower()): c for c in columns}
    for candidate in candidates:
        key = re.sub(r"[^a-z0-9]+", "", candidate.lower())
        if key in normalized:
            return normalized[key]
    return None


def parse_legacy_futures_only(zip_bytes: bytes) -> pd.DataFrame:
    """Return the raw 096742 rows from a CFTC annual zip."""
    with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith((".txt", ".csv"))]
        if not names:
            raise ValueError("No text/CSV member found in CFTC archive")
        # Prefer the main futures-only annual file when multiple text members exist.
        name = sorted(names, key=lambda n: ("cot" not in n.lower(), len(n)))[0]
        raw = zf.read(name)

    # Legacy annual files are commonly comma-delimited text. Fall back to the
    # Python CSV engine when quoting/spacing is irregular.
    df = pd.read_csv(BytesIO(raw), low_memory=False)

    market_col = _find_column(df.columns, [
        "Market_and_Exchange_Names",
        "Market and Exchange Names",
    ])
    code_col = _find_column(df.columns, [
        "CFTC_Contract_Market_Code",
        "CFTC Contract Market Code",
    ])
    date_col = _find_column(df.columns, [
        "As_of_Date_In_Form_YYYY-MM-DD",
        "As of Date in Form YYYY-MM-DD",
        "Report_Date_as_YYYY-MM-DD",
        "As_of_Date_In_Form_YYMMDD",
    ])
    oi_col = _find_column(df.columns, [
        "Open_Interest_All",
        "Open Interest (All)",
        "Open Interest",
    ])

    missing = [name for name, col in {
        "market": market_col,
        "code": code_col,
        "date": date_col,
        "oi": oi_col,
    }.items() if col is None]
    if missing:
        raise ValueError(f"Missing required CFTC columns: {missing}")

    out = df[
        df[code_col].astype(str).str.strip().eq(CFTC_CODE)
        & df[market_col].astype(str).str.strip().str.upper().eq(MARKET)
    ].copy()
    if out.empty:
        raise ValueError("CFTC 096742 British Pound rows not found")

    out["report_date"] = pd.to_datetime(out[date_col], errors="coerce").dt.date
    out["open_interest"] = pd.to_numeric(out[oi_col], errors="coerce")
    out = out.dropna(subset=["report_date", "open_interest"])
    out["open_interest"] = out["open_interest"].astype(int)
    out = out[["report_date", "open_interest"]].drop_duplicates()
    out = out.sort_values("report_date").reset_index(drop=True)
    return out


def build_evidence(rows: pd.DataFrame, publication_times: dict[date, datetime]) -> pd.DataFrame:
    """Materialize PIT-safe evidence; missing publication times stay blocked."""
    rows = rows.copy()
    rows["available_time"] = rows["report_date"].map(publication_times)
    rows["status"] = rows["available_time"].notna().map(
        {True: "AVAILABLE", False: "NOT_EVALUABLE"}
    )
    rows["quality"] = rows["available_time"].notna().map(
        {True: "AUTHORITATIVE", False: "MISSING"}
    )
    rows["source"] = "CFTC_COT_LEGACY_FUTURES_ONLY"
    rows["instrument"] = "GBPUSD_FUTURES_096742"
    rows["feature"] = "open_interest"
    return rows[
        ["report_date", "available_time", "open_interest", "source",
         "instrument", "feature", "quality", "status"]
    ]


if __name__ == "__main__":
    raise SystemExit(
        "This module is intentionally source-only. Supply the downloaded CFTC archive "
        "and verified publication timestamps; it will not fetch or invent availability metadata."
    )
