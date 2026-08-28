# AI Trading Assistant — Decision Brain Handoff

Date: 2026-08-28
Branch: `backtest-only-2026-08-28`

## Current point
The previous 2016–2024 Backtest technically ran, but produced `0` executed trades because the runner did not pass the complete governed evidence/context stack into the Decision Brain. This result is diagnostic only and is NOT a profitability verdict.

## What already exists
- Authoritative GBPUSD H1 development source: 2016–2024 development window, with 2025 kept OOS-locked.
- Murphy 34-rule historical evidence.
- Nison 44-rule historical evidence.
- Market State source + contract adapter.
- Dynamic MTF binding/runtime components.
- Historical Context Memory V1.
- Historical Outcome Memory V1.
- Similarity Memory V2.
- Context-Aware Retrieval V2.
- Trading in the Zone (TIZ) process gate.
- Risk/Execution integration.
- Recovered Decision Brain V1.
- Knowledge/Decision handoff adapter.
- Compatibility tests and governance guards.

## Frozen governance
1. Murphy may provide directional market context.
2. Nison provides confirmation/contradiction; it does not independently generate direction.
3. Historical Context Memory and Historical Outcome Memory are evidence only.
4. Similarity Memory is historical evidence only and cannot generate direction.
5. Context-Aware Retrieval supplies evidence/context only.
6. TIZ is a process/psychology gate only and cannot generate direction.
7. Risk is a hard execution gate.
8. 2025 must remain OOS-locked and cannot be used for calibration/tuning.
9. Recovered Decision Brain V1 semantics must remain unchanged.

## Correct runtime map
`H1 -> Market State -> MTF -> Murphy 34 -> Nison 44 -> Historical Context Memory -> Historical Outcome Memory -> Similarity Memory -> Context-Aware Retrieval -> TIZ Gate -> Risk Gate -> Knowledge/Decision Handoff -> Decision Brain V1 -> Execution -> Backtest`

Every historical input must be joined by `timestamp/as-of` without lookahead.

## What was added before this handoff
- Integration Gate: `BACKTEST/decision_brain_integration_gate_v1.py`
- Integration map: `BACKTEST/DECISION_BRAIN_INTEGRATION_MAP_2016_2024.md`
- Backtest-only CircleCI config: `.circleci/config.yml` on this branch.
- Connection marker after the CircleCI account change: `New 8/TEST_CONNECTION_AFTER_ACCOUNT_CHANGE.txt`.

## Exact remaining work
### 1. Complete the governed runner
Replace the simplified runner path that used hardcoded `TIZ=PASS`, `risk=PASS`, and `similarity=None` with real source-backed calls to the existing adapters/boundaries.

### 2. Bind every source into one per-timestamp evidence package
For each evaluation timestamp, collect and provenance-tag:
- Market State
- MTF role bindings
- Murphy evidence
- Nison evidence
- Historical Context Memory
- Historical Outcome Memory
- Similarity Memory metadata/evidence
- Context-Aware Retrieval metadata/evidence
- TIZ process state
- Risk/Execution inputs

### 3. Enforce governance at the handoff
Use the existing handoff/compatibility boundaries so Memory/Similarity/Nison/TIZ never become independent direction generators, and Risk/TIZ/Nison contradictions can block or route to review.

### 4. Integration Gate
Do not run the full Backtest until the gate proves all required sources are actually present, time-aligned, as-of safe, and visible to the handoff.

### 5. Final development Backtest
Run only the 2016–2024 development window after the Integration Gate passes.

### 6. Validate before reading profitability
Required outputs:
- `unified_78_events_2016_2024.csv`
- `decision_events_2016_2024.csv`
- `executed_trades_2016_2024.csv`
- `execution_funnel_2016_2024.json`
- `backtest_metrics_2016_2024.json`
- `validation_manifest_2016_2024.json`

No official profitability claim is allowed unless timestamp/as-of, lookahead, MTF consumption, memory leakage, execution funnel, and frozen cost/slippage checks pass.

## Status map
- Components: COMPLETE
- Contracts/boundaries: COMPLETE
- Integration Gate: CREATED
- Integration map: CREATED
- Governed runner: INCOMPLETE — CURRENT WORK
- Final 2016–2024 Backtest: NOT YET VALID
- Profitability conclusion: NOT ALLOWED YET
- 2025 OOS: LOCKED

## What NOT to repeat
- Do not regenerate Nison 2016–2024.
- Do not regenerate Murphy historical evidence.
- Do not rerun the old `build-and-test` pipeline.
- Do not tune any rule using 2025.
- Do not treat the prior `0 trades` run as a strategy failure.

## Restart instruction for the next chat
Start here: `Complete the governed runner and integration gate. Do not rebuild existing knowledge or rerun the old pipeline. First verify real data flow through all source adapters, then run the 2016–2024 Backtest once.`
