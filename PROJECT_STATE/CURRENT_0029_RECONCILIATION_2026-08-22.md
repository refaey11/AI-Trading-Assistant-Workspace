# CURRENT 0029 Reconciliation — 2026-08-22

## Source-derived status
- Rule: MURPHY_0029
- Historical QA window: 2016-2024
- Events: 5819
- PASS: 2930
- FAIL: 2889
- Duplicate events: 0
- Missing required fields: 0
- Availability-before-pivot violations: 0
- 2025 rows: 0
- Semantics: BULLISH divergence + LOW pivot

## Current governance evidence
- Continuity backup status: FREEZE_CANDIDATE
- Provenance artifact status: FREEZE_CANDIDATE_PENDING_GOVERNANCE
- The uploaded continuity backup states a later dedicated freeze record exists, but the current GitHub code-search surface does not expose that file by name.

## Runtime work already completed
- Existing shared evaluator retained; no rebuild.
- Runtime adapter added for 0029.
- Historical replay matched the preserved 2016-2024 evidence.

## Decision
Do not change the official Runtime count for 0029 until the dedicated canonical freeze record is present in the live GitHub state or an explicit newer current-state record promotes it.

## Next action
Reconcile 0029's canonical freeze record in the live repository, then run the repository-level runtime integration and update the official count if the full path passes.

## Protected boundaries
- Do not reopen or rebuild 0028.
- Do not rebuild shared divergence evaluator, RSI, Pivot Sequence V2, or bridge.
- 2025 remains OOS and is excluded from tuning/selection.
- Missing evidence remains NOT_EVALUABLE.
