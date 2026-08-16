# Nison 0035–0038 Hybrid Batch Gate V1

Status: BATCH EXECUTED — NOT FROZEN
Date: 2026-08-16

## Purpose

Apply the Nison Hybrid 44-Rule Batch Factory contract to the existing 0035–0038 artifacts without rebuilding evaluators or inventing semantic thresholds.

## Evidence reviewed

- NISON_0035_0038_BATCH_CLOSURE_REPORT_V1
- NISON_COMPARATOR_SEARCH_V1
- NISON_0035_SOURCE_RECONCILIATION_V3
- NISON_0035_QA_GATE_REPORT_V1
- NISON_0038_COMPATIBILITY_SIGNOFF_V1
- NISON_0038_FREEZE_GATE_REPORT_V1
- NISON_0035_0038_FINAL_QA_REPORT_V1
- NISON_0036_0037_ENGINEERING_BATCH_REPORT_V1

## Gate matrix

| Rule | Existing implementation | Unit tests | Compatibility | Historical QA | Availability / no-lookahead | Final state |
|---|---|---:|---|---|---|---|
| 0035 Tasuki Gap | V3 evaluator | 7/7 | BLOCKED by unresolved source-locked body-size comparator and explicit trend-context contract | Structural replay only; canonical PASS not claimed | Preliminary event-time check passed for candidate scan | NOT_EVALUABLE / BLOCKED |
| 0036 Gapping Play | Structural evaluator | 4/4 | PARTIAL; qualitative sharpness, small-body, congestion and near-high/low semantics unresolved | Structural replay executed; canonical PASS not claimed | Preliminary event-time audit performed | NOT_EVALUABLE / BLOCKED |
| 0037 Side-by-Side White Lines | Structural evaluator | 4/4 | BLOCKED by unresolved same-open and similar-body comparators and source-backed trend context | Structural candidates found; canonical PASS not claimed | Preliminary event-time audit performed | NOT_EVALUABLE / BLOCKED |
| 0038 Windows | Structural evaluator | 6/6 | PASS for structural Window operator | 2016–2024 replay: 2544 rows, 6 Windows (2 bullish, 4 bearish) | 0 availability violations; no lookahead in Window geometry | FREEZE CANDIDATE / NOT FROZEN |

## Data boundary

Historical replay evidence covers 2016–2024. 2025 rows used for tuning/selection: 0.

## Governance decisions

1. No ATR/pip/percentage/body-size/gap tolerance was invented.
2. Exploratory engineering thresholds from prior experiments are not promoted to Nison Canonical.
3. Unit-test success does not imply freeze.
4. A missing required comparator is a contract/evidence gap, not permission to optimize one from historical outcomes.
5. Nison remains confirmation-only and cannot create direction independently.
6. 0038 structural compatibility passes, but the official freeze manifest and upstream sessionization/future-closure boundaries must still be closed before FROZEN.

## Batch verdict

**BATCH = EXECUTED CORRECTLY / NOT YET FREEZABLE**

The batch machinery is behaving fail-closed: rules with unresolved semantic contracts remain NOT_EVALUABLE/BLOCKED while 0038 advances independently to freeze-candidate status.

## Next gate

Use the same batch factory on the remaining READY_FOR_BACKTEST Nison rules (0026, 0030, 0031) after their existing artifacts are inventoried. Do not reopen 0035–0037 unless new authoritative evidence changes their unresolved contracts.
