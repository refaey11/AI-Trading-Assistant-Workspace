"""CFTC TFF Futures-Only acquisition for British Pound Futures (096742).

This module is an acquisition boundary only. It does not change Murphy rule
semantics and never manufactures missing observations or publication times.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import requests

BASE_URL = "https://publicreporting.cftc.gov/api/v3/views/gpe5-46if/query.json"
CONTRACT_CODE = "096742"


@dataclass(frozen=True)
class OIObservation:
    report_date: date
    open_interest: int
    cftc_contract_market_code: str
    market_and_exchange_names: str


def fetch_2025_096742_oi(*, timeout: int = 30, session: requests.Session | None = None) -> list[OIObservation]:
    """Fetch the authoritative 2025 TFF Futures-Only 096742 observations.

    Availability is deliberately NOT synthesized here. The caller must join
    these report dates to an authoritative publication calendar before PIT use.
    """
    client = session or requests.Session()
    query = (
        "SELECT report_date_as_yyyy_mm_dd,open_interest_all,"
        "cftc_contract_market_code,market_and_exchange_names "
        "WHERE cftc_contract_market_code='096742' "
        "AND report_date_as_yyyy_mm_dd >= '2025-01-01T00:00:00' "
        "AND report_date_as_yyyy_mm_dd < '2026-01-01T00:00:00' "
        "ORDER BY report_date_as_yyyy_mm_dd ASC"
    )
    response = client.get(
        BASE_URL,
        params={"pageNumber": 1, "pageSize": 1000, "query": query},
        timeout=timeout,
    )
    response.raise_for_status()
    payload: Any = response.json()
    rows = payload if isinstance(payload, list) else payload.get("data", [])

    out: list[OIObservation] = []
    for row in rows:
        report_raw = row["report_date_as_yyyy_mm_dd"]
        report_date = date.fromisoformat(str(report_raw)[:10])
        out.append(
            OIObservation(
                report_date=report_date,
                open_interest=int(row["open_interest_all"]),
                cftc_contract_market_code=str(row["cftc_contract_market_code"]),
                market_and_exchange_names=str(row["market_and_exchange_names"]),
            )
        )
    return out


def compute_observed_direction(previous_oi: int | None, current_oi: int | None) -> str | None:
    """Return direction only when two observed OI values exist; no interpolation."""
    if previous_oi is None or current_oi is None:
        return None
    if current_oi > previous_oi:
        return "UP"
    if current_oi < previous_oi:
        return "DOWN"
    return "FLAT"
