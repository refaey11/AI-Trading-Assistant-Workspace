# Integration Map V1

The runtime is an orchestration boundary, not a replacement for existing modules.

## Existing source-of-truth components

| Capability | Existing project component | Runtime role |
|---|---|---|
| Market context | MARKET_STATE / MARKET_READER / MTF | input snapshot |
| Direction | Murphy evaluators/evidence | primary directional evidence |
| Confirmation | Nison evaluators/evidence | confirmation / contradiction |
| Process | TIZ runtime boundary | process gate |
| Historical memory | Similarity + Historical Context/Outcome | supporting evidence only |
| Decision synthesis | recovered Decision Brain + governed evaluator | final decision boundary |
| Risk | frozen risk runtime/contracts | hard gate |
| Execution levels | existing execution adapter | trade-plan generation |
| Broker execution | not yet canonical | next implementation boundary |

## Integration rule

No module is reimplemented here. The runtime consumes existing outputs and emits exactly one canonical DecisionEvent per market snapshot.

## Completion criteria for V1

1. One deterministic GBPUSD replay path.
2. One canonical DecisionEvent schema.
3. Fail-closed behavior on missing/conflicting evidence.
4. Backtest/Paper/Demo/Live mode separation.
5. No 2025 tuning.
6. No changes to book-rule semantics.
