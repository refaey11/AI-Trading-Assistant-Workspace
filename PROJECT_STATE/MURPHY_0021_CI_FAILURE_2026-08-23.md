# Murphy 0021 Fresh 2025 CI Failure — 2026-08-23

## Status
PR #45 (`oos-2025-murphy-0021-fresh-v1`) was created and all existing project gates reached success, but the new CircleCI job `murphy_0021_2025_fresh_v1` failed.

## Confirmed facts
- PR #44 was merged before starting this work: merge commit `2d3f58bbc9eb7c57de36591a5f9dab8b34092ab5`.
- Fresh Murphy 0021 integration is isolated in PR #45.
- New producer job URL: https://circleci.com/gh/refaey11/AI-Trading-Assistant-Workspace/4740
- CI status at diagnosis: `murphy_0021_2025_fresh_v1 = failure`; baseline jobs were green; Nison full production and combined coverage were still pending at the same check snapshot.
- The CircleCI failure log is not accessible through the current GitHub connector/web surface, so the exact root-cause line is not being guessed.

## Governance
- No 2025 tuning or threshold changes were made.
- Existing Murphy 0021 evaluator semantics were reused unchanged.
- No futures-OI proxy was introduced.
- Missing evidence remains NOT_EVALUABLE.

## Next action
Read the red failure step from CircleCI job 4740, fix only the actual CI/producer defect, rerun PR #45, and record the result before any next Murphy rule group.
