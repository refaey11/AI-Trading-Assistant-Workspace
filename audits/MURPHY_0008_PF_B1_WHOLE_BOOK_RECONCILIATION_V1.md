# Murphy 0008 / PF-B1 — Whole-Book Reconciliation V1

Date: 2026-08-15
Status: AUDIT COMPLETE — PF-B1 NOT PRODUCTION FROZEN

## Scope
Whole uploaded Murphy source archive was scanned (298 archive entries), with focused review of Chapters 4, 5, 6, 7, and the checklist/review material, plus project Workspace and GitHub contracts.

## Source findings

### Chapter 4 — Support/Resistance and filters
- Support is identified from prior reaction lows; resistance from prior reaction highs.
- Support can become resistance after a decisive/significant downside penetration; resistance can become support after decisive upside penetration.
- Murphy discusses price filters and time filters.
- Murphy gives a 1–3% price-filter family and a two-successive-close time-filter family for important support/resistance breaks as well as trendlines.
- Murphy also makes clear that the significance of penetration is contextual/subjective; 3% is described as a benchmark particularly for major levels, while shorter-term levels may require less.

### Chapter 5 — Reversal patterns
- Head-and-Shoulders explicitly uses decisive close below the neckline, with 1–3% penetration or two consecutive closes as example confirmation filters.
- The return move can test the underside of the broken neckline as new resistance.
- Volume expansion on breakdown is described as supporting evidence, not an unconditional gate.
- These are pattern-specific examples and must not be promoted into a generic 0008 policy without governance.

### Chapter 6 — Continuation patterns
- Breakout is repeatedly the resolution event for continuation structures.
- Volume contraction during formation and expansion/spike on breakout is source-compatible context where specified.
- The chapter does not provide a universal numeric breakout tolerance that should automatically govern all rules.

### Chapter 7 — Volume
- Volume is confirmation/supporting evidence around breakouts in the supplied project source material.
- No universal volume threshold was found that should be made mandatory for 0008.

### Chapter 19 — Checklist/review
- Support/resistance and volume confirmation remain general checklist considerations; no new decisive-break operator is supplied.

## Governance conclusion
The whole-book review strengthens the source basis for PF-B1 policy families but does not select a single project-wide policy for 0008.

Supported policy families:
1. PRICE_FILTER — source range/context includes 1–3%; exact project value/context is not selected by Murphy as a universal software threshold.
2. TIME_FILTER — two successive closes beyond the important support/resistance level.

The following remain prohibited unless separately governed:
- choosing 1% or 3% by backtest performance;
- binding two successive closes merely because Murphy mentions it;
- ATR, pips, arbitrary lookbacks, hidden tolerances;
- using 2025 for operator selection.

## Decision
PF-B1 remains a policy-injection contract, not a frozen operator. The next governance decision is to approve the policy family and context for each consumer without using evaluation outcomes to select it.

For 0008, if no approved policy is supplied, decisive-break status remains NOT_EVALUABLE.

## Next gate
1. Finalize PF-B1 policy selection/governance for 0008 and shared consumers.
2. Audit PF-H1 compatibility.
3. Only after both gates are approved, implement 0008 evaluator.
4. Unit tests → 2016–2024 fresh QA → availability/no-lookahead → provenance/freeze.
5. 2025 remains OOS and is never used for selection/tuning.
