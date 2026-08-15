# Murphy 0008 — PF-B1 Policy Decision Audit V1

Date: 2026-08-15
Status: GOVERNANCE GATE OPEN / NOT PRODUCTION FROZEN

## Finding
The Murphy source and project handoff support two policy families for significant support/resistance penetration:
1. PRICE_FILTER
2. TIME_FILTER / two successive closes

The source does not select one fixed project-wide value for 0008. The project must therefore explicitly approve the family, value/condition, context, confirmation timestamp rule, and availability/no-lookahead rule before PF-B1 can emit decisive-break CONFIRMED.

## Evidence reviewed
- AI_TRADING_ASSISTANT_MURPHY_0008_FULL_HANDOFF_V2
- PF_B1_GOVERNANCE_PROPOSAL_V1
- Murphy 0008 compatibility/governance records
- Existing 0006/0007 confirmation governance precedent

## Rejected shortcuts
- No automatic 3% binding.
- No automatic two-day binding.
- No ATR/pip/arbitrary percentage/lookback/tolerance.
- No backtest-based threshold selection.
- No 2025 tuning.

## Operational gate
If no explicitly approved policy is supplied, PF-B1 decisive confirmation MUST be NOT_EVALUABLE. Raw boundary crossing may be recorded separately, but it must not be promoted to decisive confirmation.

## 0008 consequence
MURPHY_0008 remains evaluator-pending until PF-B1 policy approval and PF-H1 compatibility/approval are complete.

## Next decision
Select/approve one source-faithful policy family and its exact context through project governance, without using 2025 or historical outcome optimization. Then run deterministic chronology/availability tests and 2016–2024 QA before freeze.
