# MURPHY 0030 — P&F BOX METHOD COMPARISON V1
Date: 2026-08-15
Status: RESEARCH / NO PARAMETER SELECTION

## Objective
Compare candidate box-size methodologies for implementing Murphy 0030 without tuning on trading outcomes.

## Source-backed Murphy constraints
- Murphy describes 3-box reversal P&F and explains that box size controls sensitivity.
- Murphy shows smaller boxes producing more signals and being more suitable for shorter-term analysis, while larger boxes are less sensitive and more suitable for longer-term analysis.
- Murphy describes Kenneth Tower's logarithmic P&F: a screening process measuring stock volatility over the prior 3 years determines the percentage box size for each stock. The published text gives examples (AOL 3.6%, Intel 3.2%) but does not publish the screening formula.
- Murphy does not provide a GBPUSD-specific fixed box value in the reviewed material.

## Candidate methods reviewed
### A. Fixed traditional box
Examples exist in classic P&F software and literature. Simple and deterministic once selected. However, selecting the GBPUSD absolute value would be a project choice; Murphy's stock examples do not establish a GBPUSD value.

### B. Percentage / logarithmic box
This is directionally closest to Murphy's description of Tower. A percentage box normalizes box size to price level. However, the exact GBPUSD percentage cannot be derived from Murphy without Tower's unpublished screening formula.

### C. ATR-derived box
Modern platforms support ATR box sizing. This is deterministic but is not the same as Murphy's described Tower volatility screening and would therefore be an explicit project operationalization.

### D. Quantile/percentile volatility-derived box
A deterministic percentile rule can be constructed from OHLC data, but this is also a project operationalization and must not be selected by trading performance. It must also have a fixed lookback and information cutoff.

## Governance conclusion
No candidate should be selected by backtest profitability, Sharpe, win rate, drawdown, or any 2025 outcome.

B is the closest semantic family to Murphy/Tower, but it is NOT yet a complete reproducible method because the Tower screening formula is not published in the reviewed source.

A, C, and D are technically implementable but are not source-faithful Murphy rules. They may only be considered under an explicitly labeled Project Operationalization decision.

## Recommended gate
Do not freeze a GBPUSD box value yet. First attempt to recover any project-local historical configuration that already specifies P&F scaling. If none exists, create a separate operationalization decision with:
1. fixed formula,
2. fixed lookback,
3. fixed data cutoff,
4. no optimization on outcomes,
5. explicit provenance as project policy,
6. frozen configuration before evaluation.

## Current status of 0030
- Murphy semantics: CLOSED
- Box methodology family: B is directionally preferred, NOT frozen
- Exact GBPUSD box value: OPEN
- Evaluator: BLOCKED pending construction contract
- 2025: OOS and excluded from selection
