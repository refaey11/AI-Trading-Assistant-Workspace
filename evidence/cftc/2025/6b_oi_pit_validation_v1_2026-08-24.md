# CFTC 6B OI 2025 — PIT Validation V1

## Scope
- Instrument: British Pound Futures
- CFTC contract market code: 096742
- Dataset: Financial Futures Only
- Report-date inventory: 51 observed report dates for 2025

## Authoritative publication rule
CFTC states COT reports are generally published Friday at 3:30 p.m. Eastern using the immediately preceding Tuesday's data. Historical exceptions and the 2025 shutdown catch-up schedule are taken from CFTC's historical special announcements. No publication timestamp is inferred outside those rules.

## 2025 exceptions incorporated
- 2025-01-07 report -> 2025-01-13 15:30 ET (National Day of Mourning delay)
- 2025-09-30 -> 2025-11-19 15:30 ET
- 2025-10-07 -> 2025-11-21 15:30 ET
- 2025-10-14 -> 2025-11-25 15:30 ET
- 2025-10-21 -> 2025-12-02 15:30 ET
- 2025-10-28 -> 2025-12-05 15:30 ET
- 2025-11-04 -> 2025-12-09 15:30 ET
- 2025-11-10 -> 2025-12-10 15:30 ET
- 2025-11-18 -> 2025-12-12 15:30 ET
- 2025-11-25 -> 2025-12-15 15:30 ET
- 2025-12-02 -> 2025-12-17 15:30 ET
- 2025-12-09 -> 2025-12-19 15:30 ET
- 2025-12-16 -> 2025-12-23 15:30 ET
- 2025-12-23 -> 2025-12-29 15:30 ET
- 2025-12-30 -> 2026-01-13 15:30 ET

## Validation results
- Expected 2025 report-date count after holiday/calendar normalization: 51
- PIT publication schedule: bound for all 51 report dates under the rule set above
- No lookahead permission: enforced by available_time
- No interpolation: enforced
- No spot-FX OI proxy: enforced
- November 11 is not treated as an independent COT report date; the affected week is represented by the CFTC 2025-11-10 report in the catch-up schedule.

## Status
PIT schedule is ready for evidence join. This artifact does NOT claim 0022/0023 are production-usable until the normalized 51-row OI inventory is joined to the PIT timestamps and the evaluator is rerun.
