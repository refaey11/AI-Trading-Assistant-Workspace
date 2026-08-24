# CFTC 6B OI 2025 — Verified Web Sample V1
Date: 2026-08-24
Branch: `evidence-architecture-v1`

## Purpose
Record source-verified 2025 British Pound futures Open Interest values while the annual compressed binary file is not directly ingestible by the current runtime.

## Source
CFTC Historical Compressed page states that the complete Futures Only COT file is included by year and provides a 2025 Text/Excel archive. The relevant contract is British Pound — CME, CFTC code 096742.

## Verified observations
| report_date | open_interest | source |
|---|---:|---|
| 2025-01-07 | 188770 | CFTC `deacmesf010725.htm` |
| 2025-01-14 | 200826 | CFTC `deacmesf011425.htm` |
| 2025-01-21 | 212688 | CFTC `deacmesf012125.htm` |
| 2025-01-28 | 206821 | CFTC `deacmesf012825.htm` |
| 2025-02-04 | 204644 | CFTC `deacmesf020425.htm` |
| 2025-02-11 | 208138 | CFTC `deacmesf021125.htm` |
| 2025-02-18 | 203370 | CFTC `financial_lf021825.htm` |

## Important limitation
These verified web observations are NOT yet the materialized 2025 production evidence stream. The annual 2025 archive is the authoritative acquisition target, but the current binary-download path is not available in the execution runtime. No interpolation or synthetic daily OI is introduced.

## Next
1. Materialize the full 2025 annual archive or an equivalent source-backed weekly extract.
2. Preserve report date separately from availability date.
3. Run PIT join and 0022/0023 evaluator.
4. Re-run Murphy 34 coverage.
