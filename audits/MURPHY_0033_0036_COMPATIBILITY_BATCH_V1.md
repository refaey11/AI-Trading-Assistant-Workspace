# Murphy 0033–0036 Compatibility Batch V1

## Source-of-truth findings
The Master Knowledge Base `MASTER_CANDIDATE_RULES_V1.json` contains:
- MURPHY_0033 — Candlestick context filter (Chapter 12)
- MURPHY_0034 — Elliott Wave 2 rule
- MURPHY_0035 — Elliott Wave 3 shortest rule
- MURPHY_0036 — Elliott Wave 4 overlap rule

## 0033 — Candlestick context filter
Registry semantics are qualitative: interpret a candlestick pattern with surrounding price context and use filtering/combination rather than treating a candle in isolation.

The Chapter 12 source artifact additionally describes candlestick filtering through oscillator extreme zones and gives Stochastic %D examples (<20 / >80), while also naming RSI/Williams %R/CCI as alternatives. Therefore the registry's generic context wording does not, by itself, lock one deterministic oscillator operator for 0033.

Decision: PARTIAL / SOURCE-OPERATOR MISMATCH.
Do not silently bind 0033 to Stochastic, RSI, or fixed 20/80 thresholds without an explicit project contract. 0033 remains evidence/context only and cannot create direction.

## 0034 — Elliott Wave 2
Source-bounded condition: Wave 2 must not retrace more than 100% of Wave 1.

Compatibility finding: no existing Elliott-wave evaluator/feature contract was found in the Murphy proposal branch or searchable GitHub project artifacts. Do not create a duplicate wave engine.

Decision: NOT_EVALUABLE pending an existing canonical Elliott feature/evaluator or source-locked integration contract.

## 0035 — Elliott Wave 3 shortest rule
Source-bounded condition: Wave 3 cannot be the shortest of Waves 1, 3, and 5.

Compatibility finding: no existing canonical Elliott-wave evaluator/feature contract was found.

Decision: NOT_EVALUABLE pending canonical Elliott evidence/evaluator.

## 0036 — Elliott Wave 4 overlap rule
Source-bounded condition: in the stated stock cash-market framework, Wave 4 must not overlap Wave 1 price territory.

Compatibility finding: no existing canonical Elliott-wave evaluator/feature contract was found. The source wording is also explicitly framework-qualified, so no forex-specific reinterpretation is allowed without source/contract evidence.

Decision: NOT_EVALUABLE pending canonical Elliott evidence/evaluator and confirmation of the applicable market framework.

## Governance
- Existing components must be reused after compatibility audit; no duplicate Elliott engine is introduced.
- No thresholds/operators/lookbacks are invented.
- 2025 remains OOS and is not used for tuning or operator selection.
- Nison PR #19 is a separate workstream and is not modified.
- No rule is frozen from this audit alone.

## Batch result
0033 = PARTIAL
0034 = NOT_EVALUABLE
0035 = NOT_EVALUABLE
0036 = NOT_EVALUABLE

Concrete next action: recover/verify the canonical Elliott-wave feature/evaluator contract from Workspace/Master KB/GitHub before implementing 0034–0036; resolve 0033's source-vs-registry operator boundary separately.
