# Murphy 0025–0026 Validation Gate V2

Date: 2026-08-12

## Search result

Workspace/file audit confirms that the existing Four-Week Lookback infrastructure is present:
- `GBPUSD_RULE_EVALUATOR_V2/FOUR_WEEK_LOOKBACK_V1_OUTPUT/FOUR_WEEK_LOOKBACK_CONTRACT_V1.json`
- `GBPUSD_RULE_EVALUATOR_V2/FOUR_WEEK_LOOKBACK_V1_OUTPUT/FOUR_WEEK_LOOKBACK_BUILD_CONTRACT_FINAL_V1.json`
- `GBPUSD_RULE_EVALUATOR_V2/FOUR_WEEK_LOOKBACK_V1_OUTPUT/GBPUSD_H1_2016_2024_FOUR_WEEK_LOOKBACK.csv`
- `GBPUSD_RULE_EVALUATOR_V2/FOUR_WEEK_LOOKBACK_V1_OUTPUT/GBPUSD_H1_WEEKLY_FOUR_WEEK_REFERENCE.csv`
- `GBPUSD_RULE_EVALUATOR_V2/FOUR_WEEK_LOOKBACK_V1_OUTPUT/FOUR_WEEK_LOOKBACK_MANIFEST_V1.csv`

The file audit records the Four-Week module as an existing project feature and the Master Handoff explicitly lists Four-Week evidence as an existing Murphy evidence module.

## Validation finding

A dedicated Murphy 0025/0026 evaluator artifact, unit-test artifact, and dedicated historical-evaluation summary were not exposed by the current searchable file/GitHub indexes during this pass.

Therefore:
- 0025 = SOURCE/FEATURE COMPATIBLE; EVALUATOR/TEST/HISTORICAL QA PENDING
- 0026 = SOURCE/FEATURE COMPATIBLE; EVALUATOR/TEST/HISTORICAL QA PENDING

Do not mark either rule Production FROZEN yet.

## Source contract retained

0025: new four-week high → bullish.
0026: new four-week low → bearish.
The four-week period is the documented source condition; no new threshold or fixed timeframe is introduced.

## OOS control

2025 remains OOS and is not used for tuning, implementation selection, or fitting.

## Next action

Use the existing Four-Week Lookback outputs to implement/validate the missing dedicated 0025/0026 evaluator and tests, then produce historical QA from the allowed pre-OOS window. If an existing evaluator artifact is later found in the newly uploaded archives, reuse it instead of creating a duplicate.