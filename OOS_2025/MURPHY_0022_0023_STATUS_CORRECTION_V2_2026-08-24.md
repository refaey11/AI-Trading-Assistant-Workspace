# Murphy 0022/0023 — Status Correction V2

Date: 2026-08-24
Branch: `evidence-architecture-v1`

## Correct status
MURPHY_0022 and MURPHY_0023 are NOT missing-rule implementations.

The recovered project continuity record marks both as `PRODUCTION FROZEN` using:
- CME British Pound futures `096742`
- source-locked futures OI evidence
- no spot-FX OI substitution
- no proxy OI
- no invented thresholds
- availability-safe bridge
- 2025 excluded from selection/tuning

## What is actually blocked
The blocker is specific to the **2025 OOS evidence stream**.

Current 2025 coverage rows for 0022 and 0023 exist, but their OI evidence is unavailable, so they are `NOT_EVALUABLE` in that 2025 stream.

This must not be interpreted as:
- rule incomplete;
- evaluator missing;
- OI module missing;
- need to rebuild 0022/0023;
- need to buy replacement OI for 2020–2024.

## Evidence boundary
### 2020–2024
Existing historical OI path is the canonical reusable evidence source for these rules and is already part of the frozen continuity package.

### 2025 OOS
A source-backed 2025 CME British Pound futures OI stream is still required before 0022/0023 can produce authoritative 2025 evidence.

The newly supplied CME PG01B Daily Bulletin confirms the correct FX futures source family and includes the `BP BRITISH POUND FUTURE` line with Open Interest. It is a source/parser validation sample only, not a replacement 2025 historical series.

## Decision
Do not modify rule semantics.
Do not rebuild the historical OI module.
Do not use spot OI or tick-volume proxies.
Proceed by wiring the existing frozen OI evidence into Evidence Architecture V1, then separately close the 2025 OI data gap.

## Source references
- MURPHY_12_FROZEN_CONTINUITY_BACKUP_V1.json
- MURPHY_0021_0023_EVALUATOR_CONTRACT_V1.json
- MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv
- MURPHY_0021_0023_HISTORICAL_SUMMARY_V1.csv
- Section01B_Summary_Volume_And_Open_Interest_FX_Futures_And_Options.pdf
