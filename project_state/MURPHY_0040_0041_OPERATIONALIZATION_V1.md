# Murphy 0040-0041 Operationalization V1

Status: CANDIDATE / NOT FROZEN
Date: 2026-08-17

## 0040 — Parabolic SAR
- Source-supported semantic: Parabolic SAR is trend-following context; SAR points below price represent bullish state and above price represent bearish state.
- Existing primitive: `PARABOLIC_SAR_V1`.
- Canonical operator status: PENDING explicit rule-to-primitive binding.
- No new SAR parameter, threshold, timeframe, or whipsaw tolerance is introduced here.
- Unsupported clauses remain `NOT_EVALUABLE`.

## 0041 — DMI / ADX
- Source-supported semantic: DMI directional relationship and ADX trend-strength/ranging context are used as market-condition evidence.
- Existing primitive: `DMI_ADX_V1`.
- Canonical operator status: PENDING explicit rule-to-primitive binding.
- No new ADX threshold or timeframe is introduced here.
- External thresholds may only be recorded as `EXTERNAL_CANDIDATE`; they cannot become Murphy semantics without explicit approval.

## Decision
This document converts no candidate into a Production Rule. It establishes the safe operationalization boundary and prevents repeated ad-hoc threshold invention.

## Next gates
1. Verify exact source wording for the rule-specific operator.
2. Compatibility audit against existing primitive outputs.
3. Build evaluator only for source-bounded clauses.
4. Unit tests.
5. Historical QA on 2016-2024.
6. Availability/no-lookahead checks.
7. Explicit freeze decision.

2025 remains OOS and is not used for tuning, selection, calibration, or optimization.
