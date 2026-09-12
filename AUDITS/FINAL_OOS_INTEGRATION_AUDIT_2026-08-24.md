# Final OOS Integration Audit — 2026-08-24

## Source-of-truth review
This audit reconciles the current GitHub `main` state with the recovered Decision Brain governance material and the latest open final-OOS work.

## Confirmed frozen boundaries
- Decision Brain V1 remains a market-state assessment layer, not an automatic BUY/SELL execution engine.
- Runtime rule allowlist: 78 = 34 Murphy + 44 Nison.
- MURPHY_0008 remains blocked/fail-closed and is not reopened here.
- Nison is confirmation/context only; it cannot create direction.
- Similarity/historical memory is evidence-only and cannot create direction.
- TIZ is process/psychology evidence only and remains direction-neutral.
- Risk is a hard gate.
- 2025 is OOS/evaluation-only; no tuning, threshold selection, calibration, or implementation selection on 2025.
- Point-in-time/future-data controls are required for authoritative evidence.

## Current main status
The current main branch already contains the Nison availability policy, non-blocking proof for absent Nison evidence, official profitability-readiness gate, and the governed 78-rule-to-profitability event adapter plus regression tests.

## Open final-OOS branches reviewed
- PR #50: full Decision Brain event orchestration boundary; branch `decision-brain-full-oos-assembler-v1`.
- PR #51: historical 2024/2025 event producer; based on PR #50 branch.
- PR #52: point-in-time Evidence Architecture; based on PR #50 branch.
- PR #53: final-test preparation with PIT-bound 2025 CFTC 6B OI, Murphy 0021/0022/0023 unified dispatch, and a one-cell Kaggle final-test runner; based directly on `main`.

## Integration decision
Do NOT blindly merge PR #50/#51/#52/#53 in arbitrary order. PR #51 and #52 depend on the PR #50 branch, while PR #53 is a separate main-based final-prep line. The correct integration sequence is:

1. Reconcile PR #50 against current `main` and resolve merge conflicts if any.
2. Validate the full Decision Brain event path on the reconciled branch.
3. Rebase/retarget PR #51 and PR #52 onto the reconciled event-path baseline and re-run compatibility tests.
4. Integrate PR #53 after the point-in-time Evidence Architecture is present, because its PIT OI producer is intended to feed the same evidence boundary.
5. Run the final 2025 Murphy/Nison/78-rule OOS producers in Kaggle using the governed historical source files.
6. Run the final Decision Brain OOS event stream and the official profitability evaluator with execution costs explicitly applied.
7. Only after those outputs pass the governance gates may the result be called the official 2025 Decision Brain profitability result.

## Current compute blocker
CircleCI is currently out of credits. Kaggle remains the practical final execution environment. PR #53 already contains a one-cell runner that clones the exact `final-test-prep-2026-08-24` branch, runs governance/runtime tests, discovers attached H1/M1 CSVs, and executes the PIT-safe Murphy 0022/0023 producer when the governed sources are attached.

## Explicit non-claims
- No official 2025 profitability result has been established yet.
- The historical +166R diagnostic is not the official Decision Brain result.
- Full 78-rule 2025 authoritative coverage has not been re-certified after the latest branch integration work.
- Nison NOT_EVALUABLE is not treated as a global blocker under the governed availability policy.
