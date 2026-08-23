# AI Trading Assistant — 2025 Baseline Before Fresh Murphy Coverage

Date: 2026-08-23
Purpose: Freeze a factual project baseline before any fresh Murphy 2025 producer work. This document is reporting/governance only; it does not modify rule semantics or tune 2025.

## Current verified state
- Nison runtime: 44/44 rule runtimes are wired and CI-verified.
- Nison 2025 producer: CI-verified on current governed source path.
- Risk execution runtime: CI-verified.
- TIZ: process/evidence boundary resolved; in 2025 OOS, missing TIZ evidence is recorded as UNVERIFIED/NOT_EVALUABLE rather than invented. TIZ does not generate or alter direction.
- Frozen 78-rule allowlist: 34 Murphy + 44 Nison; Murphy 0008 remains excluded by the frozen allowlist contract.
- PR #43 established the governed full 78-rule event-stream boundary and passed its CI gate.
- PR #44 established the executable current 78-rule coverage report and passed the CircleCI coverage job after the heredoc parser fix.

## Current 2025 coverage result
Source: uploaded FULL_78_RULE_2025_COVERAGE_CURRENT.json.

- Rule rows reported: 52 (8 Murphy snapshot rules + 44 Nison rules).
- Observed 2025 output rules: 52.
- Rules with any available evidence: 27.
- Rules with full available rate: 1.
- Nison: 44/44 have emitted 2025 producer rows, but only a subset has available evidence across the 2025 sample.
- Murphy: the current report uses a frozen reporting snapshot, not a fresh Murphy 2025 producer run.
- Therefore this report is OOS_COVERAGE_ONLY, not a final profitability result.

## Explicit Murphy baseline
Fresh Murphy 2025 producer coverage is NOT yet complete.
The currently observed Murphy snapshot contains 8 rules:
MURPHY_0003, 0004, 0021, 0022, 0023, 0028, 0029, 0050.
Among these, MURPHY_0021 is the only one with available evidence across all 6,216 rows (2,772 PASS, 3,408 FAIL, 36 NOT_EVALUABLE). The other observed Murphy snapshot rules are not currently available for decision evidence.

## Governance locks
- 2025 remains strictly OOS and is never used for tuning/calibration/threshold selection.
- Similarity memory remains evidence-only and cannot be the sole decision maker.
- TIZ remains process-only and cannot generate direction.
- Missing evidence remains NOT_EVALUABLE; no invented facts or semantics.
- Do not call the next profitability run a complete 78-rule Final OOS until fresh Murphy coverage is established or an explicit contract authorizes a partial evaluation.

## Next milestone
Fresh Murphy 2025 Coverage Audit/Producer completion using existing project knowledge first. No rebuilding of Murphy knowledge from scratch. After that: fresh combined coverage report, checkpoint record, then final OOS decision-event stream evaluation if the contracts permit it.

## Important prior evidence retained
- The earlier full 78-rule coverage boundary reported 8 Murphy observed and 44 Nison rows, with 70 rules lacking observed output before the current producer wiring. That report was explicitly not a final evidence claim.
- The current Nison coverage report is more recent and is the authoritative baseline for Nison as of this date.
