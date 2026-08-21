# Decision Brain → Risk Boundary Field Compatibility Audit — 2026-08-21

## Purpose
Compare the active `decision_brain.py` runtime contract with the recovered canonical Risk Boundary requirements before creating any adapter or integration code.

## Active Decision Brain output evidence
The active `assess(row, similarity=None)` function returns `MarketAssessment` with exactly these top-level fields:

- `market_state`
- `directional_bias`
- `confidence`
- `evidence`
- `contradictions`
- `no_trade_reasons`

The implementation explicitly identifies V1 as an evidence aggregator, not a trading signal generator.

## Recovered Risk Boundary required inputs
Canonical boundary evidence requires:

1. `alignment_state`
2. `process_gate`
3. `market_context_available`
4. `candidate_trade_available`
5. `stop_distance`
6. `atr_reference`
7. `take_profit_defined`
8. `risk_budget_fixed_before_entry`

## Field-by-field result

| Required field | Active Decision Brain source | Status |
|---|---|---|
| alignment_state | no direct output field | MISSING DIRECTLY |
| process_gate | no direct output field found in active runtime | MISSING DIRECTLY |
| market_context_available | may be inferable from presence of assessment/evidence, but no explicit contract field | DERIVABLE ONLY WITH EXPLICIT ADAPTER DECISION |
| candidate_trade_available | no trade candidate is produced by evidence-only runtime | MISSING BY DESIGN |
| stop_distance | outside current Brain scope | MISSING BY DESIGN |
| atr_reference | outside current Brain scope | MISSING BY DESIGN |
| take_profit_defined | outside current Brain scope | MISSING BY DESIGN |
| risk_budget_fixed_before_entry | outside current Brain scope | MISSING BY DESIGN |

## Interpretation
There is no direct one-to-one Decision Brain → Risk Engine runtime contract in the active `decision_brain.py` alone. This is not automatically a defect: the active Brain is intentionally assessment-only and must not generate a trade candidate or position-risk inputs.

Therefore the missing fields split into two categories:

### Upstream/governance handoff required
- `alignment_state`
- `process_gate`
- explicit `market_context_available`

### Candidate/execution-risk context required from outside the evidence-only Brain
- `candidate_trade_available`
- `stop_distance`
- `atr_reference`
- `take_profit_defined`
- `risk_budget_fixed_before_entry`

## Compatibility conclusion
STATUS: NOT DIRECTLY CONNECTABLE WITHOUT A GOVERNED HANDOFF CONTRACT.

A simple field-renaming adapter is not sufficient because several required fields represent information that the current Decision Brain intentionally does not create. Creating those values inside the Brain would change its responsibility and violate the recovered architecture boundary.

## Correct next action
Recover or audit the canonical handoff layer between Knowledge/Process/Contradiction governance and the Risk Boundary. Only after that contract is established can an adapter map existing fields without inventing trade or risk information.

No adapter, candidate generator, directional rule, or risk rule was created by this audit.

## Governance boundary
- 2025 remains locked Out-of-Sample.
- No tuning was performed.
- This audit is compatibility/provenance work only.
