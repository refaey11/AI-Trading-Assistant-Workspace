# Murphy 0030 P&F Engine Compatibility Audit V1

Date: 2026-08-15
Candidate: gregorian-09/pnf-chart-system

## Result
DROP-IN COMPATIBILITY: REJECTED / ADAPTER REQUIRED

The candidate supports High/Low construction and configurable 3-box reversal, but its trendline logic is not sufficiently source-faithful to treat the engine as a drop-in implementation of Murphy 0030.

## Evidence reviewed
- ChartConfig defaults to Close construction, Traditional box sizing, and reversal=3; HighLow must be explicitly selected.
- `process_high_low()` feeds high and low through `calculate_box_size()` and `is_reversal()` and can use a price-dependent box size. This must be governed explicitly by the project construction contract.
- `calculate_box_size()` supports Fixed, Points, Percentage and Traditional methods. Traditional uses price bands; for GBPUSD around 1.x this produces a 0.25 box in this implementation.
- Trendline code does not simply define Murphy's bullish support from the lowest O-column. It searches for a `significant_low` using a prior-X requirement and a lookback of up to 3 columns, then creates the support line from that selected low.
- Trendline break logic uses a one-box buffer (`price < line_price - box_size`) and touch tolerance of half a box. These are implementation-specific behaviors and are not to be silently labeled as Murphy semantics.

## Compatibility decision
1. Keep the candidate as a reusable technical implementation reference.
2. Do not integrate it unchanged as the Murphy 0030 evidence engine.
3. Build a thin project adapter/specification layer that owns the source-faithful Murphy 0030 semantics.
4. The adapter must explicitly control box/scaling policy, High/Low processing order, reversal construction, bullish-support-line construction, break semantics, and event timestamps.
5. Only after the adapter contract is deterministic and no-lookahead tested may 0030 move to evaluator status.

## Important governance
- No box-size value is selected from historical performance.
- No external scaling method is labeled as Murphy without source support.
- 2025 remains OOS and is excluded from tuning.
- If a required construction parameter remains unsupported, the rule stays NOT_EVALUABLE rather than being guessed.

## Current 0030 state
Murphy semantics: established.
Candidate engine: technically useful, but not drop-in compatible.
Adapter/faithful construction: required.
Box/scaling: unresolved.
Evaluator: blocked.
Freeze: blocked.
