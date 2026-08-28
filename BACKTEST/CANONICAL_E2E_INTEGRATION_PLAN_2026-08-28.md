# AI Trading Assistant — Canonical E2E Integration Plan
Date: 2026-08-28
Branch: backtest-only-2026-08-28

## Decision
Stop repeated CI/runner patching. Build one canonical end-to-end integration path and prove it with contract tests before consuming another full CircleCI backtest run.

## Canonical runtime
H1 → Market State → MTF → Murphy 34 → Nison 44 → Historical Context Memory → Historical Outcome Memory → Similarity V2 → Context-Aware Retrieval V2 → Knowledge/Decision Handoff → Decision Brain V1 → TIZ status → Risk/Execution → execution/backtest contract.

## Non-negotiable invariants
- Do not rebuild Murphy or Nison knowledge.
- Decision Brain V1 source remains unchanged.
- Murphy provides directional context.
- Nison provides confirmation/contradiction only; it cannot independently generate direction.
- Historical Context/Outcome, Similarity V2 and Retrieval are evidence/context only; they cannot generate direction or tuning parameters.
- TIZ is process/psychology only. Current development runtime remains unresolved/optional; never manufacture PASS.
- Risk/Execution is a real hard gate; never hardcode PASS.
- All evidence must be point-in-time/as-of bounded.
- 2025 remains locked/OOS and cannot be used for tuning/calibration.

## Architecture
Two explicit phases:
1. Evidence Compilation: prepare a canonical timestamp-keyed evidence table using sorted point-in-time joins (for example merge_asof), with provenance for every layer.
2. Decision/Execution: consume one event envelope at a time through Handoff → Decision Brain V1 → TIZ gate status → Risk/Execution.

The CI runner is only an execution wrapper. It is not the integration architecture.

## Pre-flight validation before another expensive run
1. Contract test on a small sample proving every layer reaches the Handoff.
2. Assert Similarity/Retrieval/Memory never produce direction.
3. Assert TIZ is not PASS unless independently proven by runtime evidence.
4. Assert Risk can PASS and FAIL according to its actual contract; no bypass.
5. Assert 2025 is blocked from the development path.
6. Assert recovered Decision Brain V1 executes unchanged.
7. Assert all timestamps are as-of bounded with no future leakage.

## Only after pre-flight passes
Run the governed 2016–2024 backtest once. Produce decision events, execution funnel, metrics, and provenance/validation manifest. Treat profitability as diagnostic/non-official until existing governance/readiness requirements are satisfied.

## Known implementation issues to remove before full backtest
- Existing runner still has partial/shadow consumption for Similarity and Context-Aware Retrieval.
- Existing runner calls Decision Brain V1 with similarity=None; memory must remain evidence-only but should be carried through the governed handoff path.
- Existing runner invents an SL/TP construction (0.75 ATR / 3R); replace this with the project's existing upstream execution/risk contract rather than inventing a new Risk method.
- Historical Outcome currently needs real as-of outcome evidence, not merely a boolean that an older row exists.
- The Handoff must be the actual boundary carrying the complete evidence envelope into Decision Brain assessment.

## Execution rule
Do not spend another full CI run until the contract/integration test passes locally or deterministically in a small test environment. Then run one governed 2016–2024 execution. 2025 stays locked.
