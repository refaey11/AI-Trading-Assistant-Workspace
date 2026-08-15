# Murphy 0030 — Master KB Operator Gap Reconciliation V1

Date: 2026-08-15
Status: AUDIT FINDING / NOT PRODUCTION FROZEN

## Source-of-truth finding

The current Master Knowledge Base record for `MURPHY_0030` states:
- rule identity: `P&F bullish support`
- source: John J. Murphy, Technical Analysis of the Financial Markets, Chapter 11, Point and Figure
- X/O price structure
- bullish support trendline as structural reference
- direction: BULLISH
- decision logic: use P&F trendlines as structural guides and confirm with specific P&F signal rules

The same rule record leaves these fields empty:
- market trend/context
- timeframe
- confirmation
- entry trigger
- invalidation
- risk fields
- exact evaluator logic
- testing status is `UNTESTED`

## Chapter 11 feature facts in Master KB

- P&F is time-independent at the chart representation level.
- X represents upward price movement; O represents downward price movement.
- Larger boxes (example 5–10 points) filter noise and are described as suitable for long-term investment.
- Smaller boxes (example 1 point) are described as highly sensitive and suitable for short-term/intraday use.
- Reversal can be 3-box or 5-box in the knowledge base description.
- Bullish Support Line is a 45-degree line from the base of the lowest O column.

## Consequence

The previous working hypothesis that the only blocker was `Box Size` was incomplete.

There are at least three unresolved operator boundaries:
1. P&F construction/scaling policy (including box size and reversal choice).
2. Rule-specific confirmation/signal required by the phrase "confirm with the specific P&F signal rules".
3. Entry/evaluation semantics and any applicable timeframe/sampling role, which are blank in the canonical rule record.

## Governance

Do not invent:
- a GBPUSD box size
- a fixed timeframe
- an entry trigger
- a P&F signal threshold
- a lookback/tolerance
- a proxy for missing P&F evidence
- a value selected from historical performance

2025 remains OOS and cannot be used for tuning or operator selection.

## Correct next step

Do not build the 0030 evaluator yet.

First perform a shared P&F feature compatibility audit for 0030–0032, then separately close the rule-specific operator contracts. Reuse one compatible P&F evidence module rather than building separate engines.

0030 remains `NOT_EVALUABLE / BLOCKED` at the exact feature/operator/TF/gate boundary until these contracts are source-supported or explicitly approved as project operationalization before QA.
