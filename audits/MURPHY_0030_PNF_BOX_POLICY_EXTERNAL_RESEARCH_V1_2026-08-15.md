# MURPHY 0030 — P&F Box Policy External Research V1
Date: 2026-08-15
Status: RESEARCH COMPLETE / POLICY NOT FROZEN

## Finding
A deep external search did not recover the exact Kenneth Tower screening formula that maps the 3-year volatility measure to a percentage box size.

## Source-supported facts
- Murphy states that Tower uses a logarithmic P&F method.
- Murphy states that a screening process measuring a stock's volatility over the prior 3 years determines the percentage box size.
- Murphy gives examples: AOL 3.6%, Intel 3.2%, and Royal Dutch Petroleum 2.7% in the cited charts.
- Murphy explains that P&F can be constructed from real-time/intraday or end-of-day data and that changing box size changes sensitivity/time horizon.
- Tower's own chapter in *New Thinking in Technical Analysis* confirms P&F is price-change based and does not use time as the chart's horizontal axis.

## External implementation evidence
- Multiple P&F implementations support percentage/logarithmic box sizing and High/Low construction.
- Some third-party sources provide fixed percentage examples or forex-specific fixed-pip practices, but none found in this audit establishes the missing Tower formula for GBPUSD.
- Vendor defaults are not acceptable as Murphy semantics.

## Governance decision
Do NOT freeze a GBPUSD box size as Murphy/Tower semantics.
Do NOT select a value using backtest performance.
Do NOT use 2025 for selection/tuning.

## Operationalization boundary
If the project elects to make 0030 executable despite the missing Tower formula, the chosen box policy must be labeled explicitly as PROJECT OPERATIONALIZATION, include provenance, be frozen before evaluation, and remain distinct from Murphy source facts.

## Current status
0030 remains BLOCKED at the P&F box-policy contract boundary. No evaluator result may be treated as a Murphy result until this boundary is resolved.

## Next action
Prepare a bounded operationalization proposal with explicit alternatives and a no-tuning rule; obtain project approval/freeze before historical evaluation.
