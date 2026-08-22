# Dynamic MTF Runtime/Contract Test — 2026-08-22

## Scope
Validate the recovered Dynamic MTF binding contract and its supplied selection examples without inventing selection thresholds or treating the architecture contract as a runtime PASS.

## Source evidence inspected
- Reconstructed GBPUSD Rule Evaluator V2 workspace: 241 readable ZIP entries.
- `DYNAMIC_MTF_BINDING_CONTRACT_V1.json`
- `DYNAMIC_TIMEFRAME_SELECTION_EXAMPLES_V1.csv`
- `DYNAMIC_TIMEFRAME_SELECTION_POLICY_V1_DRAFT.json` (explicitly DRAFT; not treated as frozen numeric policy)

## Contract-level checks
The supplied examples were validated against the contract's allowed execution-timeframe families.

Checks passed:
- 15–30 minute example uses M5/M15 and records higher timeframes still read = true.
- 30–120 minute example uses M15/M30/H1 and records higher timeframes still read = true.
- Several-hours example uses M30/H1/H4 and records higher timeframes still read = true.
- No H2 execution timeframe is introduced by the examples.
- The contract explicitly requires higher timeframe evaluation before lower timeframe evaluation.
- The contract requires missing required timeframe data to return `NOT_EVALUABLE` rather than silently substitute.
- The MTF layer assigns roles and does not itself generate BUY/SELL.

## Result
CONTRACT / EXAMPLE VALIDATION: PASS

## Runtime boundary
A true runtime PASS is NOT claimed yet because the recovered Rule Evaluator V2 archive does not contain the actual six-timeframe aligned data rows needed for point-in-time execution testing. The archive recovery record separately identifies the six-timeframe source family as `M5 -> M15 -> M30 -> H1 -> H4 -> D1`, but this artifact alone does not provide the governed runtime rows required for leakage testing.

Therefore:
- Dynamic MTF contract: RECOVERED / VALIDATED at contract-example level.
- Dynamic MTF runtime execution against actual aligned rows: PENDING.
- No-lookahead proof: PENDING.
- Time/Session standalone runtime contract: NOT FOUND in this recovered archive pass; do not invent one.

## Governance
- Do not rebuild the dynamic MTF contract.
- Do not promote `DYNAMIC_TIMEFRAME_SELECTION_POLICY_V1_DRAFT.json` to authoritative frozen policy.
- Do not add numerical weights/thresholds.
- Do not use 2025 for tuning/calibration/selection.
- Do not generate BUY/SELL from MTF alone.
