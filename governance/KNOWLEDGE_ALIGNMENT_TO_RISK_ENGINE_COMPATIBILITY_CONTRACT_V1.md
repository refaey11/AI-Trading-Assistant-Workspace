# Knowledge Alignment → Risk Engine Compatibility Contract V1

## Purpose
Define a boundary-only compatibility contract between the existing Knowledge Alignment output and the recovered `RISK_ENGINE_SPEC_V1` research prototype. This contract does not modify the original Risk Engine specification and does not promote it to live execution.

## Source Status
`RISK_ENGINE_SPEC_V1` is a research prototype. Its own warning states that costs, spread, slippage, leverage, contract size, and broker-specific pip value must be added before live execution.

## Upstream Input
Knowledge Alignment may provide only a candidate context plus governance state. The Risk Engine does not receive authority to create market direction.

Required boundary fields:
- `alignment_state`
- `process_gate`
- `market_context_available`
- `candidate_trade_available`
- `stop_distance`
- `atr_reference` when ATR-based hard-gate validation is being used
- `take_profit_defined`
- `risk_budget_fixed_before_entry`

## Risk Engine Research Hard Gates
Preserve the recovered specification exactly at the compatibility boundary:
1. positive stop distance
2. stop distance between 0.5 ATR and 4 ATR
3. defined take profit
4. risk budget fixed before entry

## Output States
- `PASS_RESEARCH_ONLY`
- `FAIL_HARD_GATE`
- `NOT_READY_INSUFFICIENT_INPUT`
- `NOT_EXECUTION_READY`

No output from this contract may emit a final BUY/SELL instruction, broker order, position size for live execution, or execution-ready SL/TP.

## Research Parameters Preserved Without Promotion
The following remain research-prototype parameters, not project-wide production constants:
- risk profiles: 0.0025, 0.005, 0.01, 0.015
- position size formula: `risk_money / stop_distance`
- stop modes: `structure`, `2x ATR`, `hybrid`
- target: `1.5R`
- drawdown: tracked, not yet a trading halt

## Authority Boundaries
- Murphy supplies technical context / market structure evidence only.
- Nison may confirm or contradict; it cannot create direction alone.
- Trading in the Zone remains process/psychology only.
- Similarity remains historical evidence only and cannot override hard gates.
- Risk remains a hard gate.
- Decision Brain remains the synthesizing layer.

## Compatibility Result
`COMPATIBLE_FOR_RESEARCH_BOUNDARY_INTEGRATION_ONLY`

## Required Next Step
Run a boundary integration test using representative inputs. Do not claim all live execution requirements are satisfied until authoritative costs, spread, slippage, leverage, contract size, and broker-specific pip value handling exist and pass their own governance review.

## Global Governance
2025 remains OOS and must not be used for tuning, calibration, selection, or optimization.
