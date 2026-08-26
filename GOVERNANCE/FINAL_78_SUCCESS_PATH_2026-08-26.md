# AI Trading Assistant — Final 78-Rule Success Path

Date: 2026-08-26
Status: Approved working plan

## Objective
Produce a trustworthy 2025 OOS profitability result from the existing AI Trading Assistant Decision Brain without changing the existing Murphy, Nison, TIZ, Similarity/Memory, Risk, or frozen P&L semantics.

## Current finding
The governed 2025 run proved that the full rule envelope reaches the decision boundary: 34 Murphy + 44 Nison. The current 2025 result is 6225 decision events and 0 executable trades. This is not yet accepted as the final strategy profitability verdict because the audit found two distinct conditions that must be separated: rule rows that are NOT_EVALUABLE because upstream evidence is unavailable, and direction conflicts/rejections at the arbitration boundary.

## Approved sequence
1. Evidence Coverage Audit for all 78 rules: PASS / FAIL / NOT_EVALUABLE, per-rule availability, upstream source, and timestamp coverage.
2. Compatibility/Wiring Audit: verify that every evaluable rule receives the intended existing upstream facts; do not invent proxies or thresholds.
3. Direction Arbitration Audit: distinguish true Brain-vs-Murphy conflicts from insufficient/neutral/conflicted Brain state and mapping/wiring errors.
4. Preserve roles:
   - Murphy = technical context / market structure / directional context.
   - Nison = confirmation or contradiction only; it does not generate direction.
   - Trading in the Zone = process/psychology gate only; it does not generate direction.
   - Similarity / Historical Memory = historical evidence only; never the sole decision maker or direction generator.
   - Risk = hard gate.
5. Test wiring and arbitration on pre-2025 / fixture data first. 2025 remains evaluation-only and is not used for tuning.
6. Freeze the corrected integration path.
7. Re-run the governed 2025 OOS final P&L using the same frozen P&L implementation.
8. Accept the 2025 result only after provenance, OOS, no-lookahead, and trade-generation gates pass.

## Non-goals
- No 2025 threshold tuning.
- No new trading rules.
- No replacement of the existing Decision Brain.
- No forced trade generation to make the backtest look profitable.
- No synthetic substitution for missing evidence.

## Success criterion
The system must correctly propagate source-backed evidence through the existing Decision Brain and arbitration layers, then produce a transparent 2025 OOS result. Profitability is an output of that governed run, not a target to be engineered.
