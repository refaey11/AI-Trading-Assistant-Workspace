"""Source-locked 2025 CFTC British Pound futures OI acquisition.

Purpose:
- Recover weekly CFTC CME futures-only Open Interest for code 096742.
- Preserve report_date separately from availability_date.
- Never synthesize OI from spot volume or another proxy.
- Handle 2025 publication delays conservatively.

This module is deliberately an acquisition/normalization layer. It does not
change Murphy 0022/0023 semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from html import unescape
from pathlib import Path
import re
from typing import Iterable, Optional
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

CFTC_CODE = "096742"
BASE_URL = "https://www.cftc.gov/files/dea/cotarchives/2025/futures/deacmesf{mmdd}25.htm"
NY_TZ = ZoneInfo("America/New_York")

@dataclass(frozen=True)
class OIObservation:
    report_date: date
    open_interest: int
    source_url: str
    source_event_id: str
    published_date: date
    available_time: datetime

    @property
    def event_time(self) -> datetime:
        # Conservative event marker: end of the report date.
        return datetime.combine(self.report_date, time(23, 59, 59), tzinfo=NY_TZ)

    def direction_from(self, previous: Optional["OIObservation"]) -> Optional[str]:
        if previous is None:
            return None
        if self.open_interest > previous.open_interest:
            return "UP"
        if self.open_interest < previous.open_interest:
            return "DOWN"
        return "FLAT"


def _fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "AI-Trading-Assistant/1.0"})
    with urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def _parse_report_date(text: str) -> date:
    m = re.search(r"FUTURES ONLY POSITIONS AS OF\s+(\d{2}/\d{2}/\d{2})", text)
    if not m:
        raise ValueError("CFTC report date not found")
    return datetime.strptime(m.group(1), "%m/%d/%y").date()


def _parse_oi(text: str) -> int:
    marker = rf"BRITISH POUND\s+-\s+CHICAGO MERCANTILE EXCHANGE\s+Code-{CFTC_CODE}.*?OPEN INTEREST:\s*([0-9,]+)"
    m = re.search(marker, unescape(text), flags=re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError(f"CFTC Open Interest not found for code {CFTC_CODE}")
    return int(m.group(1).replace(",", ""))


def _parse_updated_date(text: str) -> date:
    # Page footers commonly expose an 'Updated Month DD, YYYY' date.
    m = re.search(r"Updated\s+([A-Z][a-z]+\s+\d{1,2},\s+\d{4})", unescape(text))
    if not m:
        raise ValueError("CFTC updated/published date not found")
    return datetime.strptime(m.group(1), "%B %d, %Y").date()


def conservative_available_time(published_date: date) -> datetime:
    """Conservative point-in-time boundary: next calendar day at 00:00 ET."""
    return datetime.combine(published_date + timedelta(days=1), time(0, 0), tzinfo=NY_TZ)


def fetch_observation(report_date: date) -> OIObservation:
    url = BASE_URL.format(mmdd=report_date.strftime("%m%d"))
    text = _fetch(url)
    parsed_report_date = _parse_report_date(text)
    if parsed_report_date != report_date:
        raise ValueError(f"URL/report-date mismatch: requested {report_date}, got {parsed_report_date}")
    published_date = _parse_updated_date(text)
    return OIObservation(
        report_date=parsed_report_date,
        open_interest=_parse_oi(text),
        source_url=url,
        source_event_id=f"CFTC-096742-{parsed_report_date.isoformat()}",
        published_date=published_date,
        available_time=conservative_available_time(published_date),
    )


def iter_tuesdays(start: date, end: date) -> Iterable[date]:
    cur = start
    while cur <= end:
        if cur.weekday() == 1:
            yield cur
        cur += timedelta(days=1)


def build_series(start: date = date(2025, 1, 1), end: date = date(2025, 12, 31)) -> list[dict]:
    observations: list[OIObservation] = []
    for report_date in iter_tuesdays(start, end):
        try:
            observations.append(fetch_observation(report_date))
        except Exception:
            # Missing report pages are retained as acquisition gaps rather than synthesized.
            continue
    observations.sort(key=lambda x: x.report_date)
    rows: list[dict] = []
    previous: Optional[OIObservation] = None
    for obs in observations:
        rows.append({
            "evidence_id": obs.source_event_id,
            "event_time": obs.event_time.isoformat(),
            "available_time": obs.available_time.isoformat(),
            "source": "CFTC_096742",
            "instrument": "6B",
            "feature": "open_interest",
            "value": obs.open_interest,
            "quality": "AUTHORITATIVE",
            "status": "AVAILABLE",
            "source_event_id": obs.source_event_id,
            "lineage": [obs.source_url, f"published_date={obs.published_date.isoformat()}", f"report_date={obs.report_date.isoformat()}"],
            "notes": "Weekly CFTC futures-only OI; point-in-time use begins only after conservative availability boundary.",
            "oi_direction": obs.direction_from(previous),
        })
        previous = obs
    return rows


def write_jsonl(rows: Iterable[dict], path: str) -> None:
    import json
    Path(path).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
