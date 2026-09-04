# Murphy 0028/0029 Event Binding Audit V1

## Scope
Rules: `MURPHY_0028`, `MURPHY_0029`
Evidence window: `2020-2024`
Source module: `OSCILLATOR_DIVERGENCE_V1`
Primary event artifact: `MURPHY_EVALUATORS_V1/MURPHY_0027_0029_HISTORICAL_EVALUATION_2020_2024.csv`
Underlying divergence artifact: `OSCILLATOR_DIVERGENCE_V1_OUTPUT/GBPUSD_RSI_DIVERGENCE_2020_2024.csv`

## Verified facts
- 3,236 divergence evidence rows.
- Timeframes present: H1, H4, D1.
- 1,592 confirmed bearish/high events feed rule 0028 PASS.
- 1,644 confirmed bullish/low events feed rule 0029 PASS.
- No null values in `pivot_1_timestamp`, `pivot_2_timestamp`, or `availability_timestamp`.
- `availability_timestamp` is not earlier than either pivot timestamp for any event.
- No duplicate divergence evidence rows were found.
- Availability years are exactly 2020-2024.
- No 2025 evidence is used.
- No interpolation, threshold invention, or synthetic evidence is used.

## Rule semantics in the existing evaluator
- `MURPHY_0028`: PASS only when `divergence_type=BEARISH` and `pivot_type=HIGH`; emits `BEARISH_WARNING`.
- `MURPHY_0029`: PASS only when `divergence_type=BULLISH` and `pivot_type=LOW`; emits `BULLISH_WARNING`.
- The source contract states that the module is context/confirmation evidence only and is not a standalone trade decision.

## Governance decision
`EVENT_EVIDENCE_INTEGRITY = PASS`

`STRICT_ASOF_DECISION_BRAIN_PROMOTION = NOT_YET_VERIFIED`

`CURRENT_MURPHY_FANIN_PROMOTION = FALSE`

Reason: this audit verifies the integrity and availability ordering of the existing event evidence. It does not, by itself, prove full production binding into the governed Murphy 34 fan-in or prove Decision Brain eligibility. Promotion remains blocked until the canonical fan-in contract consumes these events with the same strict as-of semantics and provenance preserved.

## Next action
Bind the existing 0028/0029 event artifact into the governed Murphy fan-in through an adapter only; do not rewrite the evaluator, invent new thresholds, or alter Decision Brain logic.
