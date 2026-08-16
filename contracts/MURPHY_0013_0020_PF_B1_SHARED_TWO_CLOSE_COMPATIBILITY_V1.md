# Murphy 0013–0020 PF-B1 Shared Two-Close Compatibility Contract V1

Status: COMPATIBILITY CONTRACT / NOT PRODUCTION FROZEN
Date: 2026-08-16

## Purpose
Reuse the production-frozen 0008 PF-B1 architecture without creating a new breakout engine, while preventing automatic transfer of 0008-specific Support/Resistance semantics to the eight pattern rules.

## Reused 0008 architecture
The contract preserves the 0008 shared primitive shape:
- boundary identity;
- breakout direction;
- candidate/raw breakout timestamp;
- decisive confirmation timestamp;
- availability timestamp;
- explicit status;
- fail-closed behavior;
- no-lookahead chronology.

## Candidate shared policy
For a rule that explicitly passes the compatibility gate below:

### Upside breakout
1. A completed bar closes strictly above the canonical upper pattern boundary.
2. This first close is `BREAK_CANDIDATE`.
3. The immediately following completed bar must also close strictly above the same boundary.
4. The second close becomes `DECISIVE_BREAK_CONFIRMED`.
5. Confirmation availability is the completion/close timestamp of the second bar.

### Downside breakout
1. A completed bar closes strictly below the canonical lower pattern boundary.
2. This first close is `BREAK_CANDIDATE`.
3. The immediately following completed bar must also close strictly below the same boundary.
4. The second close becomes `DECISIVE_BREAK_CONFIRMED`.
5. Confirmation availability is the completion/close timestamp of the second bar.

The candidate policy is an operationalization derived from the frozen 0008 two-close path. It is NOT a claim that Murphy literally defines every 0013–0020 rule using two closes.

## Mandatory compatibility gates
A rule may bind this policy only if all are known from its canonical rule/primitive contracts:
1. canonical upper/lower boundary identity;
2. breakout direction;
3. evaluation timeframe;
4. completed-close breakout semantics;
5. no conflicting source-specific confirmation policy;
6. boundary availability/no-lookahead semantics.

If any item is missing, ambiguous, or incompatible, decisive breakout status MUST be `NOT_EVALUABLE`.

## Boundary immutability
The boundary used for the candidate and second confirmation bar MUST remain the same canonical boundary identity. A later pivot, line refit, or future pattern update cannot rewrite the historical boundary used for an already-observed candidate event.

## Time and provenance
- The candidate close must occur after boundary availability.
- The confirmation timestamp cannot precede the candidate timestamp.
- The second bar's information cannot be used before its close.
- No future bar may be used to confirm an earlier event.
- Any missing provenance returns `NOT_EVALUABLE`.

## Pattern-specific non-transfer
Do NOT transfer from 0008:
- D1 as a universal timeframe;
- singleton LOW pivot as a universal pattern boundary;
- downside-only direction;
- Support-to-Resistance role reversal;
- 0008 retest definition;
- any historical 0008 event counts as a tuning target.

## Rule mapping
- 0013: candidate upper/lower G1 boundaries; breakout direction is UP or DOWN.
- 0014: upper horizontal boundary; breakout direction is UP.
- 0015: lower horizontal boundary; breakout direction is DOWN.
- 0016: channel boundary plus F1 flagpole prerequisites; direction is UP or DOWN.
- 0017: converging pennant boundary plus F1 flagpole prerequisites; direction is UP or DOWN.
- 0018: upper/lower wedge boundaries; breakout direction is UP.
- 0019: upper/lower wedge boundaries; breakout direction is DOWN.
- 0020: upper/lower horizontal boundaries; breakout direction is UP or DOWN.

These mappings do not override individual rule contracts. They identify only the breakout side that would be tested if the rule's canonical geometry is valid.

## Fail-closed states
- `BREAK_CANDIDATE`: first qualifying completed close only.
- `CONFIRMED`: second successive qualifying completed close, with all gates passed.
- `NOT_CONFIRMED`: a candidate was observed but the immediately following completed bar fails the required condition.
- `NOT_EVALUABLE`: boundary, timeframe, availability, provenance, or compatibility evidence is missing/ambiguous.

## Prohibited changes
- No 1% or 3% percentage copied from another Murphy context.
- No ATR/pip threshold.
- No arbitrary lookback.
- No invented tolerance.
- No 2025 tuning or selection.
- No performance-based selection between policies.
- No duplicate breakout engine.

## Production boundary
This contract establishes the shared compatibility shape and candidate two-close operationalization. It does not freeze the policy for all eight rules. Each rule requires an explicit compatibility approval and then deterministic tests, availability/no-lookahead QA, provenance, and historical QA before production freeze.
