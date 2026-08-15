# Murphy 0030 P&F Signal Reconciliation V2

Date: 2026-08-15
Status: AUDIT CLOSED / RULE STILL BLOCKED

## Finding

Murphy Chapter 11 explicitly identifies S-7 as a downside breakout below a Bullish Support Line. Murphy also describes the broader P&F requirement that complex line-break patterns combine a prior basic buy/sell signal with clearance/penetration of the relevant trendline.

This does NOT prove that MURPHY_0030 itself equals S-7. The project's MURPHY_0030 identity is recorded as `P&F bullish support`, not `downside breakout below bullish support line`.

Therefore:
- Bullish Support Line geometry is source-supported.
- S-7 is a source-supported P&F sell pattern involving a Bullish Support Line.
- The mapping `0030 -> S-7` is NOT source-proven and must not be silently adopted.
- 0030 must remain separate from S-7 unless the authoritative rule record explicitly binds them.

## Source/project boundary

Project rule records and closure artifacts must determine the exact rule operator. External P&F educational material may corroborate terminology but cannot rewrite the project's rule identity.

## Current operator implications

A future shared P&F evidence module may expose at least:
- X/O column state
- Bullish Support Line state
- price relative to Bullish Support Line
- line penetration/break event
- P&F basic/complex signal state where the engine supports it
- availability timestamp

But MURPHY_0030's exact PASS condition remains unresolved until the authoritative rule record binds the required signal/condition.

## Governance

Do not:
- equate 0030 with S-7 without provenance;
- choose Box Size from backtest performance;
- invent a timeframe;
- use 2025 for tuning/selection;
- create a duplicate P&F engine when a shared feature is approved.

## Next gate

Recover the authoritative MURPHY_0030 record from the Master Rule Database/Rule Registry and determine whether `P&F bullish support` means:
1. structural state above Bullish Support Line;
2. a Bullish Support Line event/penetration;
3. a specific P&F signal; or
4. another source-defined condition.

Only after that mapping is explicit should the shared P&F feature contract be frozen and the 0030 evaluator implemented.
