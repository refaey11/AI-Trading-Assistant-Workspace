# Murphy 0006–0007 PR #2 Review Update
Date: 2026-08-12

## PR
Murphy 0006-0007 source contract and generic evaluator

## Review finding
PR #2 is a draft and its original source-contract text predates recovery of the authoritative `MASTER_TRADING_RULES_V2.json` rows. The original PR text said the exact 0006/0007 ID binding remained unresolved.

That statement is now stale.

## Recovered authoritative binding
- MURPHY_0006 = Confirmed uptrend line = successive reaction lows + upward slope = BULLISH.
- MURPHY_0007 = Confirmed downtrend line = successive reaction highs + downward slope = BEARISH.

The uploaded John Murphy Chapter 4 independently confirms these semantics and the third successful touch/reaction confirmation concept, including the no-break condition.

## Changes applied to PR branch
The evaluator now:
- enforces the recovered ID binding (`0006` -> `UP`, `0007` -> `DOWN`);
- requires explicit `third_touch`, `reaction_bounce`, and `no_break` upstream evidence;
- returns `NOT_EVALUABLE` when required evidence or availability timestamp is missing;
- preserves the existing no-invented-threshold rule.

Tests were extended for:
- successful UP confirmation;
- successful DOWN confirmation;
- touch without bounce;
- touch + bounce with a break;
- missing geometry evidence;
- rule-ID/direction mismatch;
- insufficient anchors.

## What remains valid
- Reuse existing Trendline Geometry V1.
- Do not invent touch tolerances, ATR thresholds, percentages, or lookbacks.
- 2025 remains OOS.

## Remaining closure gate
The actual Trendline Geometry V1 output schema still needs direct verification for explicit fields/evidence representing:
1. two valid anchors;
2. trendline family/direction;
3. third touch;
4. successful reaction/bounce;
5. no break;
6. confirmation availability timestamp with no lookahead.

The evaluator is now contract-ready for those upstream facts, but it must not be declared production/frozen until the existing Geometry V1 schema proves those facts are actually emitted.

## Merge decision
**DO NOT MERGE PR #2 YET.**
The semantic binding and evaluator-side gates are corrected; direct Trendline Geometry V1 schema verification and CI are still required before review/merge.
