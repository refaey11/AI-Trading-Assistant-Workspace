# New Uploaded Artifacts — Provenance Audit V1
Date: 2026-08-13

## Scope
Reviewed newly uploaded Murphy/evaluator/baseline/parameter/similarity/strategy/data artifacts. Existing components were not modified or rebuilt.

## Murphy 0006/0007 finding
- MURPHY_REFRESH_V1 confirms 0006 and 0007 remain `NOT_YET_EVALUABLE`.
- 0006 condition: third successful touch and reaction confirms the trendline; feature: pivot_low sequence + touch/reaction; operator wording: third touch followed by reaction away from line.
- 0007 condition: same qualitative rule with pivot_high sequence + touch/reaction; operator wording: third touch followed by reaction away from line.
- Refresh explicitly says successful touch/reaction still needs an approved operational definition.
- No dedicated 0006/0007 production evaluator was found in MURPHY_EVALUATORS_V1; that package contains 0021–0023 only.
- Therefore the new uploads do NOT close the 0006/0007 operator gate.

## Baseline / parameter artifacts
- BASELINE_BACKTEST_V1 is a research artifact, not a true bar-level execution backtest. Its config explicitly states aggregate neighbor outcomes are used and exact entry/SL/TP path is not available.
- PARAMETER_VALIDATION_V1 is explicitly `2025-only sensitivity` and warns `no final promotion yet`. It must not be used for implementation/parameter selection because 2025 is OOS.
- Existing OFFICIAL_BASELINE_AUDIT remains authoritative: V2+4H is candidate-only until one uniform frozen walk-forward protocol is completed.

## Similarity Engine V3
- Similarity V3 uses past-only years 2016–2023 to query 2024, k=20, with `future_outcomes_used_as_features=false`.
- This is useful historical evidence / leakage-compatible research infrastructure, but it does not define Murphy semantics, generate direction for 0006/0007, or close their operator gate.

## Strategy V3
- Strategy V3 is explicitly a `RESEARCH_CANDIDATE` with fixed-rule research tests and no live execution.
- It is unrelated to the current 0006/0007 blocker and must not be substituted for Murphy semantics.

## Raw EURUSD uploads
- The two uploaded EURUSD 5-minute CSVs contain headers only and no OHLCV rows. They are not usable data artifacts as uploaded.
- One filename is for 2026-08-22, which is future relative to the project date 2026-08-13; it must not be used as current/OOS evidence without clarification.

## Other data
- GBPUSD 2016–2018 validated and USDCAD M1 master data are evidence/data assets, but they do not by themselves define the missing 0006/0007 operators.

## Project decision
Current 0006/0007 status remains:
- Source semantics: CLOSED
- Mapping: working/source-locked status per current project handoff
- Pivot V2: CLOSED
- Geometry V1: CLOSED
- Candidate Evidence: CLOSED
- Evidence Adapter/tests: CLOSED
- Generic Evaluator architecture: READY
- Third-touch operator: OPEN
- Reaction operator: OPEN
- No-break contract: OPEN
- Confirmation timing: OPEN
- Production evaluator: BLOCKED
- Historical QA: BLOCKED
- Freeze: BLOCKED

## Controls preserved
- No invented ATR/pip/%/lookback/tolerance thresholds.
- No automatic 2-day or 3% binding.
- No 2025 tuning/selection.
- Historical Memory/Similarity remains evidence-only.
- Existing Pivot/Geometry/Adapter/Evaluator components remain reusable and were not rebuilt.

## Next action
Continue the final deep provenance/compatibility audit specifically against the authoritative Master Rule Database/source records and any existing break/no-break contract. Only integrate an operator if an authoritative project/source contract is found.