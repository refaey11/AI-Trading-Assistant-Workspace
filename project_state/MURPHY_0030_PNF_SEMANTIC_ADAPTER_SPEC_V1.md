# Murphy 0030 P&F Semantic Adapter Specification V1

Status: DRAFT / PRE-FREEZE
Date: 2026-08-15

## Purpose
Define the smallest semantic boundary required to reuse a candidate P&F engine for Murphy rule 0030 without inheriting engine-specific trendline or signal semantics.

## Engine responsibilities
- Consume canonical GBPUSD D1 OHLC in chronological order.
- Construct X/O columns using the approved P&F construction parameters.
- Apply the approved 3-box reversal behavior.
- Expose column/box chronology and prices.
- Preserve deterministic state across replay.

## Adapter responsibilities
- Treat engine output as raw P&F construction evidence only.
- Derive Murphy 0030 bullish-support evidence from the raw X/O structure according to the approved Murphy contract.
- Do not use the engine's proprietary significant-low heuristic, lookback rule, touch tolerance, or break buffer as Murphy semantics unless independently approved by source evidence.
- Do not generate trade direction, entry, stop, target, or risk decisions.
- Emit explicit availability/unknown states when required construction inputs are unresolved.

## Murphy 0030 evidence contract
The adapter must expose, at minimum:
1. P&F construction available/not available.
2. Current column type and chronology.
3. Bullish-support candidate availability.
4. Support-line definition inputs used to construct the candidate.
5. Current price relative to the approved Murphy support line.
6. Evidence timestamp / source-bar boundary.
7. Reason code when evidence is unavailable or unresolved.

## Anti-lookahead requirements
- A state emitted at source timestamp T may depend only on source data at or before T.
- Prefix replay through T must reproduce the same adapter state at T when the later suffix is removed.
- Adding future bars must never rewrite a previously emitted state.
- Any line that requires a future-confirmed pivot must remain unavailable until that confirmation is legitimately available.

## Box-size boundary
- Box size remains unresolved at this stage.
- No value is inferred from backtest performance.
- No ATR/pip/percentage value is labeled as Murphy source semantics without explicit source support.
- Once an operationalization is selected, it must be frozen before historical evaluation.

## Acceptance gate
The adapter is not production-ready until:
- engine construction passes deterministic replay tests;
- no-lookahead tests pass;
- Murphy semantic mapping is independently verified;
- unresolved Box Size is resolved through source evidence or explicitly frozen project operationalization;
- 0030 evaluator consumes only the adapter contract.
