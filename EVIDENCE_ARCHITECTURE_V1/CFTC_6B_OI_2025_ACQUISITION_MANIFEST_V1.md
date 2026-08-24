# CFTC 6B Open Interest 2025 Acquisition Manifest V1

Date: 2026-08-24

## Authoritative source
CFTC Historical Compressed / Futures Only reports, using the CME British Pound contract code `096742`.

CFTC confirms that complete Futures Only reports are available by year, including 2025. The 2025 compressed archive is the source-of-record for this acquisition path.

## Scope
- Report year: 2025
- Contract: British Pound — Chicago Mercantile Exchange
- CFTC code: 096742
- Feature: Open Interest
- Frequency: weekly report date
- Output: normalized Evidence V1 records

## Point-in-time policy
`report_date` is the market-state date. It is NOT treated as the availability date.

The acquisition parser records the page's publication/update date and uses a conservative next-calendar-day 00:00 America/New_York availability boundary. This avoids lookahead when the exact intraday publication time is not retained in the source artifact.

## 2025 publication anomaly
CFTC's historical special-announce page records a federal-appropriations interruption from October 1 through November 12, 2025, followed by delayed chronological publication. The acquisition therefore never assumes Friday release cadence for these reports; the source page's actual update date is authoritative.

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
