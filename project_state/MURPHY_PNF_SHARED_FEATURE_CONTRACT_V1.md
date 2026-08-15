# Murphy Shared Point & Figure Feature Contract V1

Status: DRAFT / PRE-FREEZE
Date: 2026-08-15

## Purpose
Provide one shared Point & Figure evidence layer for Murphy rules 0030-0032. This is a feature contract, not a trading rule and not a tuning artifact.

## Source-faithful semantics currently established
- MURPHY_0030 identity: P&F bullish support.
- P&F structure uses X/O columns.
- Murphy describes 3-box reversal construction using High/Low.
- Bullish Support Line is a structural 45-degree guide rising from the low of the lowest O-column; price above it represents bullish major-trend context.
- Murphy/Chapter 11 discusses multiple box-size/scaling choices. The audited source does not provide a GBPUSD-specific deterministic box-size value or a complete reproducible Kenneth Tower screening formula.

## Scaling decision boundary
- No fixed GBPUSD box value is currently claimed as Murphy source semantics.
- No ATR, pip, percentage, or other scaling method is to be silently substituted and labeled as Murphy.
- No scaling value may be selected from backtest performance.
- Any missing construction parameter must remain explicitly unresolved until either (a) an authoritative reproducible source is found, or (b) an explicitly approved project operationalization is created and frozen before historical evaluation.

## Sampling / timeframe decision boundary
- P&F is an event/price-movement representation, not a conventional time-based chart signal.
- The input sampling policy must be explicitly defined before evaluation because High/Low construction and availability depend on the source bars used.
- No future bar may affect an already emitted P&F state or event.
- Replaying a historical prefix must reproduce the same P&F state prefix.
- The sampling policy must be frozen before evaluator execution and must not be chosen by performance.

## Non-negotiable governance
1. Do not choose box size by backtest performance.
2. Do not use 2025 for parameter selection or tuning.
3. Do not silently substitute ATR, pips, percentage, or another scaling method and label it as Murphy source semantics.
4. Any construction parameter not directly supported by the source must be explicitly labeled as project operationalization and frozen before historical evaluation.
5. Availability and chronology must be testable; no future-bar information may enter a P&F state.
6. A shared P&F engine may be reused by 0030-0032, but each rule retains its own semantic/operator contract.

## Current status
- Shared P&F feature candidate: FOUND externally.
- Internal approved P&F construction contract: NOT YET FROZEN.
- MURPHY_0030: blocked at construction-contract boundary.
- Do not advance 0030 to evaluator freeze until the construction contract is approved.

## Next gate
Resolve the scaling and sampling policies through source evidence or explicit project operationalization. Then run the deterministic/no-lookahead harness before rule-specific evaluation.
