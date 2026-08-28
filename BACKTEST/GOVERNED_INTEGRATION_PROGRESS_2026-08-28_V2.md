# Governed Integration Progress V2 — 2026-08-28

Branch: `backtest-only-2026-08-28`

## Completed in this pass
1. Added `REAL_SOURCE_E2E_SMOKE_TEST_V2_2026-08-28.md` as the source-backed smoke-test contract.
2. Added `GOVERNED_RUNNER_STATIC_LINT_V1.py` to reject synthetic SL/TP/TIZ/Risk behavior and verify governance boundaries without consuming CI credits.
3. Added `REAL_SOURCE_E2E_SMOKE_CHECK_V2.py` for the small source-backed scope/column/timestamp/2025-lock check.
4. Preserved Decision Brain V1 and all book semantics.
5. Kept 2025 locked/OOS.
6. Kept `run_governed_backtest=false` as the CircleCI default; no full backtest was triggered in this pass.

## Current blocker
The existing `CANONICAL_E2E_ORCHESTRATOR_V2.py` still requires a real-source runtime correction before a full E2E execution can be declared valid. Static inspection shows the runner still contains legacy simplifications such as passing `similarity=None` to the Brain and setting TIZ to `UNRESOLVED_OPTIONAL` inside the assembled event path. These are not being treated as PASS, but they are not yet the final governed runtime contract.

## Next execution block
Fix the existing canonical runner in-place (no rebuild of Brain/books):
- consume similarity/retrieval evidence through their existing adapters rather than `snapshot`-only metadata;
- resolve TIZ via the existing process-only boundary; when evidence is absent, preserve the governed `NOT_EVALUABLE` state;
- route Risk only from upstream execution inputs, never synthetic values;
- make the Handoff the explicit boundary immediately before Decision Brain V1;
- then execute the small real-source smoke test locally/cheaply;
- only after smoke PASS, run the Integration Gate;
- only after Gate PASS, run the 2016–2024 backtest once.

## Do not do
- Do not run the old build-and-test pipeline.
- Do not regenerate Murphy or Nison.
- Do not tune on 2025.
- Do not interpret the historical `0 trades` run as a profitability verdict.
