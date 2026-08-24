# CFTC 6B / British Pound Futures OI — 2025 Authoritative Acquisition V2

Status: ACQUISITION_PATH_PREPARED / MATERIALIZATION_BLOCKED
Instrument: CFTC contract market code 096742 (British Pound Futures)
Year: 2025

## Purpose
Provide the authoritative 2025 futures open-interest evidence needed by Murphy rules 0022 and 0023, while preserving point-in-time integrity.

## Required fields
- report_date
- cftc_contract_market_code
- open_interest_all
- authoritative publication/availability timestamp
- source lineage

## Gate
Do not mark 2025 OI as production evidence until the acquisition output is materialized, schema-validated, and PIT-bound.

## Source hierarchy
1. CFTC Public Reporting API dataset gpe5-46if
2. CFTC official Historical Compressed 2025 Futures-Only archive as documented fallback

## Governance
- No proxy OI.
- No interpolation.
- No backfilling from post-event information.
- report_date is not automatically available_time.
- 2025 remains OOS and must not be tuned on.
