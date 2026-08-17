# Murphy 0037–0041 Compatibility Audit V1

Date: 2026-08-17
Status: FORWARD-GATE / NO NEW OPERATORS

## Source-of-truth findings
The current project closure matrix defines the following states:

- 0037 — PARTIAL: Fibonacci evidence exists conceptually, but exact rule-specific feature/operator/timeframe/gate closure is incomplete.
- 0038 — NOT_EVALUABLE: Cycle feature/operator is not currently available.
- 0039 — PARTIAL: process/system-discipline rule; exact source/operator/gate closure remains incomplete. It must not become a market-direction generator.
- 0040 — NOT_EVALUABLE: Parabolic SAR feature exists, but exact Murphy rule operator/gate is not frozen.
- 0041 — NOT_YET_EVALUABLE: DMI/ADX evidence exists, but exact trend-vs-ranging operator is not frozen.

## Existing infrastructure
The project already contains compatible feature modules for DMI/ADX and Parabolic SAR. Their existence removes the feature-availability blocker only; it does not establish a Murphy rule operator.

The project explicitly requires reuse of existing components after compatibility audit and prohibits invented thresholds, fixed timeframes, proxies, or operators.

## Decisions
### 0037
Keep PARTIAL. Reuse the existing Fibonacci evidence/feature path if and only if the exact Murphy rule mapping is recovered. Do not select a retracement percentage, timeframe, or gate from historical outcomes.

### 0038
Keep NOT_EVALUABLE. No Cycle primitive is currently available; do not proxy it with another indicator.

### 0039
Keep PARTIAL. Preserve as process/system-discipline context and do not generate market direction.

### 0040
Keep NOT_EVALUABLE. Reuse PARABOLIC_SAR_V1 only after the exact Murphy operator/gate is source-locked.

### 0041
Keep NOT_YET_EVALUABLE. Reuse DMI_ADX_V1 only after the exact Murphy trend-vs-ranging operator is source-locked. No ADX threshold or fixed timeframe is invented.

## Next implementation gate
The next valid work is rule-specific provenance/contract recovery for 0037, 0040, and 0041. Once an authoritative operator is found, implement only the smallest missing adapter/evaluator and then run deterministic tests, 2016–2024 QA, availability/no-lookahead, and provenance gates.

## Controls
- 2025 remains OOS and is excluded from tuning, selection, calibration, and implementation choice.
- No proxy substitution for unavailable Cycle evidence.
- Existing components are audited and integrated, not rebuilt.
- Evaluator existence does not equal production freeze.
