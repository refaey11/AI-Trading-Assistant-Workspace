# Murphy 0030 — Book-Wide Box-Size Reconciliation V1

Date: 2026-08-15
Status: DEEP SOURCE REVIEW COMPLETE / OPERATOR STILL OPEN

## Purpose
Resolve whether Murphy's book supplies a source-faithful, deterministic Box Size / scaling rule that can be bound to Murphy 0030 (P&F bullish support) for GBPUSD without inventing parameters or tuning.

## Source findings
Murphy Chapter 11 establishes:
- Three-box reversal is intended for intermediate trend analysis.
- Three-box reversal construction uses daily High/Low rather than intraday prices.
- A P&F chart must be scaled by assigning a value to each box.
- Box size is adjustable and changes chart sensitivity.
- Murphy gives arithmetic examples such as 3, 5, and 10 point boxes, but these are examples tied to instruments/purposes, not a universal GBPUSD rule.
- Murphy also describes a logarithmic/percentage method attributed to Kenneth Tower: a screening process measuring volatility over the prior 3 years determines a percentage box size for each stock; examples include 3.6% and 3.2%.
- The book does not provide Tower's exact volatility formula/selection algorithm in the relevant passage.

## 0030 source identity
Master Rule Database identifies 0030 as P&F bullish support and maps it to the Bullish Support Trendline / X-O P&F structure. The source semantics therefore require a valid P&F chart representation before the 45-degree Bullish Support Line can be evaluated.

## Compatibility conclusion
A P&F implementation candidate exists externally, but the project cannot yet bind a deterministic GBPUSD Box Size from Murphy without an additional governed operationalization.

The following are NOT authorized as an inferred 0030 parameter:
- 3 points
- 5 points
- 10 points
- 3.6%
- 3.2%
- any ATR/pip/percentage value selected from replay performance
- any backtest-selected Box Size

The book supports a family of methods and examples, but it does not specify one universal GBPUSD Box Size or the exact formula for Tower's volatility screen.

## Important distinction
This is NOT evidence that 0030 is impossible. It means the remaining blocker is now precisely identified:

**A source-faithful, deterministic, non-tuned Box Size / scaling policy for GBPUSD must be explicitly governed before production evaluation.**

## Allowed next solutions
1. Recover an existing project-approved P&F configuration/contract from Workspace/GitHub that predates this audit and is source-compatible.
2. Recover the exact external methodology/formula used by an authoritative P&F implementation and explicitly govern it as project operationalization, without using 2025 or performance tuning.
3. If neither exists, create a separately approved operational contract that clearly states it is project operationalization rather than verbatim Murphy semantics.

## Not allowed
Do not jump to 0031.
Do not tune Box Size against 2016-2024 to maximize rule counts/performance.
Do not use 2025 for Box Size selection.
Do not claim 0030 frozen until the Box Size/scaling contract, evaluator, tests, historical QA, availability/no-lookahead, and freeze gates pass.

## Evidence references
Murphy Chapter 11 external source review: computerized P&F section and 3-box reversal construction.
Workspace source/closure records: MURPHY_0030_0051_CLOSURE_MATRIX_V1; MURPHY_0030_0051_FORWARD_GATE_V1; Master Rule Database record for MURPHY_0030.

## Current status
0030 remains the active rule.
Status: IN PROGRESS — BOX-SIZE / SCALING GOVERNANCE BLOCKER.
Next action: search for an existing authoritative project P&F configuration or recover the exact external methodology before proposing any new operational contract.
