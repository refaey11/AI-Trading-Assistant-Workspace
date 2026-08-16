# Nison 0003–0007 Execution Gate V1

Status: STRUCTURAL GATE IMPLEMENTED — NOT PRODUCTION FROZEN

## Rules
- 0003 Dark Cloud Cover
- 0004 Piercing Pattern
- 0005 On Neck
- 0006 In Neck
- 0007 Thrusting

## Source-bounded implementation
The gate implements only source-supported hard relationships and rejects impossible structures. It deliberately returns NOT_EVALUABLE when the source uses qualitative language that has no approved project comparator.

### 0003
Hard checks: uptrend context, bullish first candle, bearish second candle, second open above prior high, second close within prior white real body. Full PASS is blocked by qualitative strength/penetration language and confirmation contract.

### 0004
Hard checks: downtrend context, bearish first candle, bullish second candle, second close above prior black-body midpoint. Full PASS remains blocked by source-described ideal gap/long-candle semantics and confirmation contract.

### 0005
Hard checks: downtrend context, black then white candle polarity, close not above prior black-body midpoint. Final PASS remains blocked by qualitative "near the low" / small-candle comparator and confirmation/invalidation.

### 0006
Hard checks: downtrend context, black then white polarity, close not above prior black-body midpoint. Final PASS remains blocked by qualitative "slightly into" / small-candle comparator and confirmation/invalidation.

### 0007
Hard checks: downtrend context, black then white polarity, close not above prior black-body midpoint. Final PASS remains blocked by qualitative "longer/stronger" comparator and confirmation/invalidation.

## Governance
- No numeric tolerance was invented for near/slightly/strong/small/longer/stronger.
- No ATR/pip/percentage/lookback/scoring was introduced.
- Nison remains confirmation-only and cannot create market direction.
- 2025 is excluded from tuning/selection.
- Unit tests are deterministic but do not grant production freeze.

## Evidence basis
The supplied Nison PDF identifies Dark Cloud Cover and Piercing as the paired two-candle reversal structures and identifies On-Neck, In-Neck and Thrusting as variants distinguished by penetration depth; the supplied project queue still lists 0003–0007 as requiring confirmation/invalidation completion. Web-accessible Nison text was used only as corroboration of the same source semantics.

## Next gate
Resolve only the remaining project-approved comparators and confirmation/invalidation contracts, then run the complete evaluator + availability/no-lookahead + 2016–2024 historical QA. Do not use 2025 to choose any comparator.
