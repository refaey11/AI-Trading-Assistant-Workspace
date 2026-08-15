# Murphy 0030 P&F Percentage Engine Compatibility Findings V1

Date: 2026-08-15
Status: AUDIT / NOT FROZEN

## Finding
The candidate P&F engine supports a Percentage box-size method, but its implementation is `box = price * percentage / 100`. This is a percentage-scaled box calculation; it is not evidence that the implementation is the same as Murphy/Kenneth Tower logarithmic P&F.

## Important distinction
- Murphy source semantics: 3-box reversal, High/Low construction, X/O columns, bullish support-line structure.
- Candidate engine capability: configurable Percentage scaling and High/Low construction.
- Project decision: do NOT label the candidate Percentage implementation as "Murphy logarithmic" without source evidence.

## Construction concern requiring harness verification
The candidate engine recalculates the Percentage box from the price passed into `calculate_box_size()`. During High/Low processing, different calls can therefore use box sizes derived from different prices within the same bar (high, low, or reversal price). This must be tested for deterministic construction and historical-prefix replay before any integration.

## Governance
1. Do not select a percentage from trading performance.
2. Do not freeze a percentage as Murphy source semantics.
3. If a percentage is eventually adopted, it must be explicitly labeled as Project Operationalization and frozen before historical evaluation.
4. First prove deterministic/prefix-replay/no-lookahead behavior of the implementation.

## Current conclusion
Percentage mode remains a technical candidate only. It is NOT a validated Murphy implementation and is NOT a production P&F contract.

## Next gate
Run construction-only harness tests against canonical GBPUSD D1 2016-2024 for deterministic replay, prefix consistency, and no-lookahead. Do not score trading performance and do not tune the percentage.
