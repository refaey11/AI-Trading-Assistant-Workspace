# Murphy 0030 P&F Execution Smoke Test V1

Status: BLOCKED / ENGINE-INTEGRATION GATE
Date: 2026-08-15

## Local execution evidence
Canonical local file: D1.csv
Rows: 2544
Date range: 2016-01-03 through 2024-12-31
Duplicate timestamps: 0
Chronological order: PASS
Missing OHLC values: 0
OHLC consistency (High >= Open/Close >= Low): PASS

## Box-policy diagnostics
Fold 2024: calibration 2016-2023; trailing 2021-2023 sample std of daily log returns = 0.5880466175%
Fold 2025: calibration 2016-2024; trailing 2022-2024 sample std of daily log returns = 0.5839896630%
These are diagnostics only; candidate remains NOT FROZEN.

## Reference execution of inspected engine semantics
A local reference harness was used to reproduce the relevant behavior visible in sources/pnf/chart.cpp: percentage box = price * pct / 100, 3-box reversal, High/Low dispatch, and the observed high/low reversal branch behavior.

Determinism: PASS for repeated identical inputs.
Prefix replay: PASS at tested cutoffs; state emitted at each cutoff matched a fresh replay truncated at that cutoff.

## Blocking finding
The inspected engine's High/Low path has an intrabar ambiguity on D1. In the tested data, both High and Low triggered reversal conditions on 8 bars per fold under the candidate percentage policy. The engine evaluates both and, when either triggers, selects the high-trigger path while the reversal type variable can be overwritten by the low test. D1 OHLC does not provide the true within-bar order.

Therefore these smoke tests do NOT constitute Murphy 0030 PASS. They only show that the arithmetic/replay harness is deterministic under the inspected engine semantics.

## Decision
- T1 Determinism: PASS (reference semantics)
- T2 Prefix replay: PASS (reference semantics)
- T3 Future-suffix invariance: not yet accepted as production gate because semantic construction remains unresolved
- T4 Fold isolation: PASS for candidate box calculation
- T5 Intrabar ordering: BLOCKED
- T6 Adapter isolation: BLOCKED until production adapter is implemented

0030 remains PRE-FREEZE / NOT_EVALUABLE.

## Next action
Resolve an approved D1 High/Low construction policy independently of OOS performance, then rerun the production harness against the exact approved policy. Do not tune box size or use 2025 to resolve this ambiguity.
