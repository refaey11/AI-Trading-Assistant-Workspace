# Rule Factory × Murphy Batch Pilot V1

## Execution
Local batch run against the project's `MASTER_TRADING_RULES_V2.json` Murphy entries (51 rules).

## Result
- Total Murphy rules: 51
- Source status: `READY_FOR_BACKTEST` = 16
- Source status: `INCOMPLETE_NEEDS_RULE_DEFINITION` = 35
- Factory mapping with canonical status preservation:
  - `INCOMPLETE_NEEDS_RULE_DEFINITION` -> `BLOCKED`
  - `READY_FOR_BACKTEST` must NOT be promoted to `FROZEN` merely because generic gates return true; it remains a research/backtest candidate until its historical QA/promotion gate is explicitly satisfied.

## Important finding
The first adapter used `historical_qa=True` for every rule and therefore produced `FROZEN` for the 16 `READY_FOR_BACKTEST` rules. This was rejected as an unsafe adapter configuration. It would have confused `READY_FOR_BACKTEST` with production-frozen status.

This is exactly the type of governance error the factory is intended to expose before integration.

## Correct boundary
The factory may orchestrate and test existing rule contracts, but it must not infer promotion eligibility from the source status alone. `FROZEN` requires an explicit promotion/historical-QA gate.

## Decision
- Rule Factory architecture: **PASS as an isolated orchestration pilot**.
- Current Murphy integration: **NOT YET READY**.
- No production merge.
- No Murphy semantics changed.
- 2025 remains excluded from tuning/selection.

## Next step
Build the real adapter against the existing canonical evaluators/regression controls, with explicit promotion eligibility, then compare factory outputs to the existing rule status/output contract before any Murphy batch is promoted.
