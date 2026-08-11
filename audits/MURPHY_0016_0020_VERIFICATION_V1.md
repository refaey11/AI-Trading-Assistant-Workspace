# Murphy 0016–0020 Verification V1

Date: 2026-08-12

## Evidence status

The preserved project Rule Registry / Master Handoff identifies these rules as unresolved:
- 0016: NOT_YET_EVALUABLE / REQUIRES_DERIVED_FEATURE
- 0017: REQUIRES_DERIVED_FEATURE
- 0018: REQUIRES_DERIVED_FEATURE
- 0019: REQUIRES_DERIVED_FEATURE
- 0020: NOT_YET_EVALUABLE

The currently retrievable GitHub index does not expose the row-level conditions or exact operator contracts for these five rules.

## Verification decision

**0016–0020 = DEFERRED / OPERATOR OR DERIVED-FEATURE CONTRACT NOT VERIFIED**

No evaluator is created from status labels alone.

For 0016–0019, the missing derived-feature contract must identify the exact existing feature, inputs, availability, operator, and MTF role before evaluation can be considered.

For 0020, the exact source condition and operational operator are required before implementation.

## Controls

- Reuse existing components only after compatibility audit.
- Do not invent thresholds, indicators, lookbacks, candle counts, or derived features.
- Do not mark any of these rules Frozen.
- Keep all five in the Revisit Queue.
- Continue the forward verification with 0021–0023, where preserved evaluator artifacts are known to exist.
- 2025 remains OOS and is never used for tuning or implementation selection.
