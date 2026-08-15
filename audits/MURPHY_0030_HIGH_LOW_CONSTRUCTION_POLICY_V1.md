# Murphy 0030 High/Low Construction Policy V1

Status: PRE-FREEZE / PROPOSED
Date: 2026-08-15

## Purpose
Define a deterministic end-of-day High/Low Point & Figure construction priority without claiming to reconstruct the unknown intraday sequence of a D1 candle.

## Policy
If the current P&F column is X:
1. Check the day's High for continuation of the X-column.
2. If the High extends the X-column, accept that continuation and do not use the Low for that bar.
3. If the High does not extend the X-column, evaluate the Low for the configured reversal condition.

If the current P&F column is O:
1. Check the day's Low for continuation of the O-column.
2. If the Low extends the O-column, accept that continuation and do not use the High for that bar.
3. If the Low does not extend the O-column, evaluate the High for the configured reversal condition.

## Important boundary
This is a deterministic construction priority rule. It is NOT a claim that the High actually occurred before the Low, or vice versa, inside the D1 candle.

## Engine boundary
The external candidate engine's simultaneous-trigger behavior must not be treated as the Murphy policy. The adapter/construction wrapper must enforce this policy before Murphy evidence is emitted.

## Acceptance tests
- Same input produces same output.
- Prefix replay produces identical historical state.
- Future suffix cannot alter prior emitted state.
- No silent High-first/Low-first intrabar assumption is introduced.
- Engine-specific trendline heuristics remain excluded.

## Freeze gate
This policy is not frozen until source review and implementation tests pass. It must not be selected or changed based on historical profitability.
