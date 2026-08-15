# MURPHY_0030 — Real Resolution V1

Date: 2026-08-16
Status: RESOLUTION / PRE-FREEZE

## Problem actually blocking 0030
The Murphy source material is present in the Master KB under Chapter 11, including:
- Construction, Box Size, and Reversal Criteria
- Patterns, Trendlines, and Trading Rules

The integrated rule registry, however, currently records MURPHY_0030 as `UNATTRIBUTED` and `needs_source_review`, even though its source is Chapter 11 / Point and Figure.

Therefore the project does NOT need another Murphy source search. The real missing work is an implementation + source-to-rule contract.

## Source-supported semantics available now
From the project's Chapter 11 KB:
1. P&F uses X columns for upward movement and O columns for downward movement.
2. P&F ignores time when there is no qualifying price movement.
3. Box size controls sensitivity; the KB gives examples but does not define one GBPUSD production value.
4. Reversal requires a minimum number of boxes; 3-box and 5-box are explicitly mentioned as examples.
5. Bullish Support Line is a 45-degree line upward/right from the base of the lowest O column.
6. Bearish Resistance Line is the reciprocal 45-degree line from the highest X column.

## MURPHY_0030 scope
The existing registry description for 0030 is a structural P&F bullish-support rule:
- represent price structure through X/O columns;
- use the bullish support trendline as the structural reference;
- direction is BULLISH;
- no explicit entry trigger is currently specified.

Therefore 0030 must NOT be turned into an invented entry rule.

## Implementation decision
Build the smallest deterministic P&F implementation required for 0030–0032:
- parameterized box size;
- parameterized reversal count (default must be explicitly frozen before evaluation; do not tune from OOS);
- X/O column state machine;
- deterministic D1 High/Low construction policy;
- 45-degree bullish support line geometry;
- support-line violation defined only where the source contract explicitly supports it.

Do NOT add unrelated P&F patterns, targets, or trading signals merely to make 0030 evaluable.

## Box-size boundary
The Chapter 11 KB does not provide a GBPUSD-specific production box size. Any GBPUSD box-size operationalization must remain a separately labeled project decision and must be frozen before OOS evaluation. It must not be selected by profitability.

## Acceptance gate
0030 can move from NOT_EVALUABLE only after:
1. source mapping is corrected from UNATTRIBUTED to the exact Chapter 11 KB files;
2. the minimal P&F implementation exists;
3. deterministic/unit tests pass;
4. no-lookahead/prefix replay passes;
5. box/reversal parameters are frozen before OOS;
6. evaluator output is evidence, not an invented trade trigger.

## Important correction
Do not reopen the Murphy-source search. The source exists. The missing artifact is the deterministic implementation/contract.
