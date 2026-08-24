# CFTC 6B Open Interest 2025 Acquisition Manifest V2

Date: 2026-08-24
Branch: `evidence-architecture-v1`

## Authoritative source
CFTC Historical Compressed / Futures Only reports, using the CME British Pound contract code `096742`.

CFTC's Historical Compressed page states that the complete Commitments of Traders Futures Only file is available by year, including 2025.

Source index:
https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm

2025 legacy Futures Only archive:
https://www.cftc.gov/files/dea/history/deacot2025.zip

## Scope
- Report year: 2025
- Contract: British Pound — Chicago Mercantile Exchange
- CFTC code: 096742
- Feature: Open Interest
- Frequency: weekly report date
- Output: normalized Evidence V1 records

## Point-in-time policy
`report_date` is the market-state/as-of date. It is NOT the availability date.

The parser refuses to invent an availability timestamp. A record becomes `AVAILABLE` only when a verified publication/update timestamp is attached by the acquisition layer. Until then it remains `NOT_EVALUABLE`.

This deliberately supersedes the earlier manifest's blanket next-calendar-day assumption; that assumption is not authoritative enough for the project.

## 2025 publication anomaly
CFTC's special announcements document delayed publication affecting October 1 through November 12, 2025. The acquisition therefore must use the source's actual publication/update metadata rather than assuming a fixed weekly release cadence.

## Non-negotiable controls
- No spot-FX OI proxy.
- No tick-volume-to-OI conversion.
- No fabricated daily interpolation.
- Missing report pages remain acquisition gaps.
- OI direction is computed only between observed source reports.
- 2025 is OOS and is never used for tuning.

## Integration target
CFTC 096742 -> 2025 OI normalized evidence -> Point-in-Time Evidence V1 -> Murphy 0022/0023 existing evaluator/Rule Adapter.

This manifest does not alter Murphy rule semantics.

## Independent verification samples
CFTC 2025 report pages independently expose 096742 and Open Interest, e.g. 2025-01-14, 2025-05-27, 2025-07-15, and 2025-08-12. These are source checks only and do not replace the annual archive.
