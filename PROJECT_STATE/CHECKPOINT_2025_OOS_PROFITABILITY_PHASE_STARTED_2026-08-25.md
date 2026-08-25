# AI Trading Assistant — Decision Brain

## Checkpoint: 2025 OOS PROFITABILITY PHASE STARTED

Date: 2026-08-25
Branch: `recovery/final-78-runtime-wiring`

## Entry Gate

The Canonical Runtime Reconciliation and Final 78-rule validation have passed in CircleCI before entering this phase.

Validated checks include:
- Murphy 0021 fresh 2025 — PASS
- Murphy 0022/0023 PIT — PASS
- 78-rule coverage — PASS
- Nison full production — PASS
- Three-Book decision evaluator — PASS
- Decision Brain integration — PASS
- 78-rule adapter allowlist gate — PASS
- Final E2E readiness — PASS

The validated runtime path has demonstrated 34 Murphy + 44 Nison rule counts in the final decision event stream.

## Phase 2 — 2025 OOS Profitability

The same 2025 source data and validated final runtime are now executed without `--validation-only` to calculate profitability.

No Rule IDs, thresholds, weights, or decision semantics may be changed because of 2025 results.

The profitability run is rejected as non-canonical unless `final_brain_provenance` confirms:
- Murphy rule count = 34
- Nison rule count = 44
- fan-in mode = `LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT`
- OOS tuning = false
- new rule semantics = false

## Required Outputs

- trades
- win rate
- profit factor
- expectancy
- total R
- total P&L
- max drawdown
- best/worst/core breakdown only when already supported by frozen contracts

## Governance

2025 is OOS/evaluation-only. The output is for measurement, not tuning. Any later strategic change must be made without using 2025 outcome information for calibration.
