# Murphy 0042-0045 Execution Backup V1

Date: 2026-08-17

## Scope
Batch implementation for Murphy Chapter 16 Capital Allocation rules 0042-0045.

## Source-derived constraints
- 0042 Capital reserve: total investment <= 50% of available capital.
- 0043 Single-market exposure: source states 10%-15% of total capital; operational adapter uses 15% as the maximum boundary while preserving the source range metadata.
- 0044 Maximum risk per market: <= 5% of total capital.
- 0045 Total margin: source states 20%-25% of total capital; operational adapter uses 25% as the maximum boundary while preserving the source range metadata.

## Architecture
These are portfolio-level NO_TRADE / risk constraints, not entry signals. They are isolated in `risk_engine/murphy_0042_0045_risk_adapter.py` and do not alter Murphy direction, confirmation, or entry logic.

## Problems and solutions
1. The rules were represented as incomplete in the generic trading-rules schema. Solution: implement them as a dedicated portfolio-risk adapter rather than forcing them into indicator/backtest semantics.
2. Murphy gives ranges for 0043 and 0045 rather than a single project execution number. Solution: preserve the source range and use only the upper boundary as the conservative operational maximum; do not claim that 15% or 25% is a universal Murphy law beyond the source wording.
3. These rules do not generate BUY/SELL signals. Solution: evaluator returns constraint pass/fail only.

## Tests
Local pytest: 5/5 PASS.
- all four boundaries pass
- 0042 breach fails
- 0043 breach fails
- 0044 breach fails
- 0045 breach fails

## Freeze boundary
Implementation and unit tests are complete. Production freeze still requires integration into the project's canonical Risk Engine and its integration/portfolio QA gate. No profitability backtest is required for the semantic constraint itself.

## 2025
No tuning or selection uses 2025.
