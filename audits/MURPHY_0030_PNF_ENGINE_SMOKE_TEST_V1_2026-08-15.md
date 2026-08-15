# Murphy 0030 P&F Engine Smoke Test V1

Date: 2026-08-15
Status: ENGINE-COMPATIBILITY SMOKE TEST ONLY / NOT EVALUATOR-FROZEN

## Inputs
- Canonical local GBPUSD D1 OHLC: `/mnt/data/ws2/D1.csv`
- Coverage: 2016-01-03 through 2024-12-31
- Rows: 2,544
- Candidate engine: `gregorian-09/pnf-chart-system` v0.2.0

## Source/engine compatibility observed
The candidate engine exposes HighLow construction, Traditional/Percentage/Fixed/Points box-size methods, and configurable reversal. Its documented example uses HighLow + Traditional + reversal=3. The implementation's HighLow path processes high/low sequentially and maintains X/O columns.

## Smoke-test execution
A local reference implementation was used only to reproduce the inspected engine's documented Traditional box-size mapping and HighLow 3-box mechanics for a construction smoke test. This is NOT an assertion that the engine is Murphy-faithful in every detail and is NOT a production implementation.

With Traditional scaling and reversal=3, GBPUSD prices in the observed range initially map to a 0.25 price-unit box under the candidate engine's Traditional ladder. On the full 2016-2024 D1 dataset, this construction produced a single X column with three boxes and no 3-box reversal. This result is a construction observation only; it is NOT a performance comparison and must NOT be used to choose parameters.

## Governance interpretation
- The smoke test confirms the candidate engine can represent the required HighLow/X-O/3-box construction shape.
- The Traditional scaling result is not automatically acceptable as Murphy's GBPUSD policy.
- No box-size parameter is promoted or frozen from this result.
- No trading performance, backtest score, or 2025 data was used for selection.
- No-lookahead and prefix-replay are still required before evaluator integration.

## Next gate
1. Obtain/validate the candidate engine locally as an executable artifact, or maintain the reference implementation strictly as a test oracle.
2. Run deterministic prefix-replay and no-lookahead tests.
3. Resolve box/scaling policy through authoritative source evidence or an explicitly approved project operationalization.
4. Only then advance Murphy 0030 to evaluator/QA.
