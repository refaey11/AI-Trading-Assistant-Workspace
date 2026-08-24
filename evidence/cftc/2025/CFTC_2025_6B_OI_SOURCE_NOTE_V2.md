# CFTC 2025 6B Open Interest — Source Note V2

## Authoritative source
CFTC Historical Compressed archive:
https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm

For Traders in Financial Futures (TFF), Futures Only, the 2025 annual archive is listed by CFTC.

The CFTC Public Reporting dataset is `gpe5-46if` (TFF - Futures Only). Relevant fields include:
- `report_date_as_yyyy_mm_dd`
- `cftc_contract_market_code`
- `open_interest_all`

Instrument:
- British Pound — Chicago Mercantile Exchange
- CFTC Contract Market Code: `096742`

## Acquisition route selected
Primary runtime route: CFTC Socrata API (`gpe5-46if`) using a restricted query for 2025 and contract `096742`.
Fallback archival route: official annual TFF Futures Only compressed archive (`fut_fin_txt_2025.zip`) resolved from the CFTC historical archive naming convention.

## Governance
- 2025 remains OOS and evaluation-only.
- `report_date` is event/report time, not `available_time`.
- Availability/PIT must come from the governed publication manifest; it must not be inferred from trade date.
- No proxy OI.
- No interpolation.
- No tuning on 2025.

## Current runtime status
The repository-side acquisition adapter has been added, but this ChatGPT runtime cannot complete the external CFTC HTTP download itself. Therefore no 2025 OI rows are promoted to authoritative project evidence by this commit.

## Validation target
Expected final artifact:
`report_date, available_time, cftc_contract_market_code, open_interest, source_id, provenance, quality`

Promotion gate for Murphy 0022/0023:
1. Complete 2025 OI inventory.
2. Complete authoritative PIT/availability binding.
3. Rerun existing Murphy 0022/0023 evaluator.
4. Publish PASS/FAIL/NOT_EVALUABLE coverage snapshot.
