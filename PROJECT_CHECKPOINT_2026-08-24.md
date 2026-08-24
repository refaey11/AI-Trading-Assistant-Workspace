# AI Trading Assistant — Project Checkpoint
## 2026-08-24

## Mainline status
- PR #53 merged: PIT OI / Murphy 0021-0023 preparation.
- PR #55 merged: full Decision Brain OOS assembler and historical-year Nison compatibility rebased onto current main.
- PR #56 merged: rebased historical Full Decision Brain producer/input/risk builder layer.
- Nison 2025 Producer CI: PASS.
- Decision Brain Progressive Gate 01 CI: PASS.

## Frozen Decision Brain boundaries
- 78 runtime rules: 34 Murphy + 44 Nison.
- Murphy provides technical direction/context.
- Nison provides candlestick confirmation/context only and cannot generate direction.
- Trading in the Zone remains process/psychology gate and cannot generate direction.
- Similarity/historical memory is evidence-only and cannot be the sole decision maker.
- Risk remains a hard gate.
- 2025 is evaluation-only: no tuning or threshold selection from 2025 results.

## Nison 2025 coverage finding
The prior production coverage audit showed 44 Nison rules with 18 zero-coverage rules and additional low-coverage rules. These remain fail-closed `NOT_EVALUABLE` where upstream evidence is unavailable. No evidence is invented to improve coverage.

A recent CI failure was due to a stale compatibility test expecting context fields at the payload root. The runtime contract places explicit context under `payload.context`. The test was aligned with the existing contract; the Nison producer then passed both source-adapter contract tests and producer tests.

## Official OOS / profitability status
The full authoritative 2025 Decision Brain profitability run has NOT yet been completed. The historical event producer and orchestration boundary are now integrated on `main`, but the official 2025 result still requires the authoritative 2025 streams and the governed evaluation path.

The previously observed `+166R` result is diagnostic only and must not be treated as the official Decision Brain profitability result.

## Remaining sequence
1. Run authoritative 2025 OOS streams.
2. Validate 78-rule coverage and point-in-time/timestamp alignment.
3. Produce governed Decision Brain historical events.
4. Run official profitability evaluation with frozen execution/risk protocol and costs.
5. Perform final E2E readiness audit and freeze Decision Brain V1.

## Compute constraint
CircleCI credits are exhausted. Kaggle is the practical external-compute fallback for the final 2025 OOS run. Integration and code audit can continue without waiting for CircleCI credits.

## Integrity rule
Do not rebuild existing Murphy, Nison, TIZ, Similarity, or project knowledge from scratch. Audit and integrate existing sources first; preserve frozen contracts; 2025 cannot be used for tuning.
