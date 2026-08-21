# Risk Boundary Test Harness Recovery — 2026-08-21

## Purpose
Resolve the open question of whether the original Knowledge Alignment → Risk Engine boundary test was only documented or whether a recoverable executable/test artifact existed in the project backups.

## Recovery result
The complete milestone backup contains the exact test-result artifact under both local and GitHub-governance paths:

- `local/KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_BOUNDARY_INTEGRATION_TEST_V1.json`
- `github/governance/KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_BOUNDARY_INTEGRATION_TEST_V1.json`

The local artifact records:

- artifact: `KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_BOUNDARY_INTEGRATION_TEST_V1`
- created UTC: `20260821T021557Z`
- status: `PASS`
- passed: `8`
- total: `8`
- live execution: `NOT_EXECUTION_READY`
- scope: boundary test only; it does not promote the recovered Risk Engine research prototype to live execution.

The governance copy records the same PASS 8/8 result and preserves historical provenance references:

- GitHub blob SHA: `aefd615398be9e39a290f72d41bdd9408ac29ab3`
- historical commit: `47ddd6a0c1637490e54fafc40a9ab14b262a9d47`

## The eight verified cases
1. `aligned_valid_research_candidate` → `PASS_RESEARCH_ONLY`
2. `missing_stop_distance` → `NOT_READY_INSUFFICIENT_INPUT`
3. `stop_below_half_atr` → `FAIL_HARD_GATE`
4. `stop_above_four_atr` → `FAIL_HARD_GATE`
5. `undefined_take_profit` → `FAIL_HARD_GATE`
6. `risk_not_fixed` → `FAIL_HARD_GATE`
7. `nison_contradiction_not_promoted` → `NOT_READY_INSUFFICIENT_INPUT`
8. `process_blocked` → `NOT_READY_INSUFFICIENT_INPUT`

## Hard boundaries explicitly verified
- No BUY/SELL output is emitted by this boundary.
- The Risk Engine does not create market direction.
- A Nison contradiction is not promoted into a trade candidate.
- Missing required data abstains.
- Research hard gates remain boundary gates only.
- Live-execution requirements remain unresolved.

## Compatibility contract recovered alongside the test
The companion `KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_COMPATIBILITY_CONTRACT_V1.md` states the boundary is `COMPATIBLE_FOR_RESEARCH_BOUNDARY_INTEGRATION_ONLY`.

Required fields are:
- `alignment_state`
- `process_gate`
- `market_context_available`
- `candidate_trade_available`
- `stop_distance`
- `atr_reference` when used
- `take_profit_defined`
- `risk_budget_fixed_before_entry`

Preserved research hard gates:
- positive stop;
- stop range of 0.5–4 ATR when ATR is used;
- defined take profit;
- risk budget fixed before entry.

Boundary outputs:
- `PASS_RESEARCH_ONLY`
- `FAIL_HARD_GATE`
- `NOT_READY_INSUFFICIENT_INPUT`
- `NOT_EXECUTION_READY`

## Important distinction
The recovered artifact is a canonical PASS-result/contract record, not the Python source code of a standalone test harness. Therefore the exact result contract is recovered, while the executable harness implementation itself is still not located as a separate source file.

If the active workspace lacks the harness, any new harness must be explicitly labeled as a reproduction of this recovered contract and must not be presented as the original implementation.

## Status update
| Item | Status |
|---|---|
| Original boundary test result artifact | RECOVERED |
| 8-case expected/actual contract | RECOVERED |
| Historical PASS 8/8 evidence | CONFIRMED |
| Research-only boundary | CONFIRMED |
| Live execution readiness | NOT EXECUTION READY |
| Standalone executable harness source | NOT YET LOCATED |
| Decision Brain → Risk runtime retest in active workspace | PENDING |

## Governance
2025 remains protected OOS and must not be used for tuning. This recovery does not authorize any parameter optimization or live trading.

## Next controlled action
Compare the current `run_knowledge_decision_brain.py` output schema with the recovered required boundary fields. First classify each field as directly present, derivable without new rules, or missing. Only then decide whether a narrow adapter is required for a research-only retest.
