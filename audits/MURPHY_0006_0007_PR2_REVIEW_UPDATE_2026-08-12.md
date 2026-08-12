# Murphy 0006–0007 PR #2 Review Update
Date: 2026-08-12

## PR
Murphy 0006-0007 source contract and generic evaluator

## Review finding
PR #2 is a draft and its current source-contract text predates recovery of the authoritative `MASTER_TRADING_RULES_V2.json` rows. The PR currently says the exact 0006/0007 ID binding remains unresolved.

That statement is now stale.

## Recovered authoritative binding
- MURPHY_0006 = Confirmed uptrend line = successive reaction lows + upward slope = BULLISH.
- MURPHY_0007 = Confirmed downtrend line = successive reaction highs + downward slope = BEARISH.

The uploaded John Murphy Chapter 4 independently confirms these semantics and the third successful touch/reaction confirmation concept.

## What remains valid in PR #2
- Reuse existing Trendline Geometry V1.
- Do not invent touch tolerances, ATR thresholds, percentages, or lookbacks.
- Generic evaluator can consume upstream geometry evidence.
- 2025 remains OOS.

## What must be updated before merge
1. Replace stale ID-binding-pending language with the recovered authoritative binding.
2. Ensure the evaluator enforces the exact rule mapping:
   - 0006 only accepts UP / LOW-family geometry and returns BULLISH structure on confirmed third touch/reaction.
   - 0007 only accepts DOWN / HIGH-family geometry and returns BEARISH structure on confirmed third touch/reaction.
3. Keep the third-touch/reaction operator dependent on explicit upstream evidence; do not manufacture tolerance.
4. Verify the actual Trendline Geometry V1 output schema for third touch, reaction/bounce, no-break, and confirmation availability timestamp.
5. Add/adjust tests for ID-direction binding and no-lookahead.
6. Re-run CI before considering the PR ready for review.

## Merge decision
**DO NOT MERGE PR #2 YET.**
It is mergeable and CI previously passed, but it requires this source-binding correction and direct geometry-schema verification first.
