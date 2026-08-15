# Murphy 0030–0032 — Project Box Policy V1

Status: PROPOSAL / NOT PRODUCTION FROZEN
Date: 2026-08-16

## Purpose
Provide a deterministic, no-lookahead project operationalization for the Point & Figure box size while keeping it explicitly separate from Murphy's source semantics.

## Source boundary
Murphy Chapter 11 states that Kenneth Tower uses a logarithmic P&F method in which a screening process measures volatility over the prior three years to determine the appropriate percentage box size for each stock. Murphy gives examples of 3.6% for AOL and 3.2% for Intel. The supplied source does not publish the exact volatility-to-box conversion formula.

Therefore this artifact does NOT claim to reproduce Tower's exact proprietary/unstated conversion formula.

## Proposed project policy
Use a fixed percentage box size derived from a pre-declared calibration window:

`box_pct = standard_deviation(daily_log_returns) * 100`

Calibration window for the first historical QA block:
- 2016-01-03 through 2018-12-31
- 3 calendar years
- 2016–2018 is calibration/warm-up only
- evaluation begins 2019-01-01
- 2025 remains completely OOS

Observed calibration result on the canonical GBPUSD D1 file:
- daily log-return standard deviation = 0.006257356643053343
- proposed box_pct = 0.6257356643053343%

This value is a PROJECT OPERATIONALIZATION, not a claim that Murphy/Tower prescribed 0.6257356643% for GBPUSD.

## Why this policy is acceptable as a proposal
1. It is deterministic.
2. It uses only information available before the evaluation block.
3. It directly uses the source-described concept of volatility over three years.
4. It does not use trading outcomes, profitability, or 2025 to select the value.
5. It produces one reproducible GBPUSD percentage box for the historical QA block.
6. It leaves the source/operationalization boundary explicit.

## Required validation before approval
- Run P&F 3-box construction using the proposed 0.6257356643% box policy.
- Verify X/O construction and reversal tests.
- Verify prefix replay / future-suffix invariance.
- Run 2019–2024 historical QA for 0030–0032.
- Treat 2016–2018 as warm-up/calibration and do not score it as rule evaluation.
- Run an OOS-only 2025 evaluation only after the policy is frozen; never use 2025 to modify the policy.
- Compare structural stability against a pre-declared sensitivity set as a robustness diagnostic only; do not select the value by performance.

## Explicit prohibitions
Do not:
- call 0.6257356643% a verbatim Murphy/Tower value;
- tune the box percentage on 2019–2024 outcomes;
- tune on 2025;
- choose the box because it maximizes trade profitability;
- introduce ATR, pips, hidden lookbacks, or arbitrary tolerance bands;
- alter Murphy's 3-box reversal semantics to accommodate the box policy.

## Decision gate
Until the validation gates above pass, 0030–0032 remain NOT_EVALUABLE / PROPOSAL_PENDING and this policy must not be merged into production.