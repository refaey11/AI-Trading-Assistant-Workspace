# Murphy 0025–0026 — Problems & Solutions V1
Date: 2026-08-15

## Problems resolved
1. Feature existed but rule evaluability was not proven -> compatibility audit and exact operator lock.
2. Four weeks could be incorrectly converted to a fixed bar count -> use four completed ISO calendar weeks; current week excluded.
3. Existing H1 boolean feature flags were weekly propagation, not authoritative row-level triggers -> evaluator uses current High/Low against weekly Four-Week reference.
4. Equality boundary was ambiguous -> equality is PASS for both rules.
5. Missing reference could be inferred -> remains NOT_EVALUABLE.
6. Lookahead risk -> only preceding four completed ISO weeks are used; current week excluded.
7. 2025 contamination risk -> historical replay restricted to 2016–2024.
8. Technical QA could be mistaken for Production Freeze -> separate final freeze manifest and explicit governance decision.

## Final QA evidence
- Full historical replay: 55,192 rows.
- Rows with Four-Week reference: 54,825.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Deterministic replay: 5/5 PASS.
- Historical replay: 8/8 PASS.
- Availability/no-lookahead: 8/8 PASS.
- Future-reference violations: 0.
- 2025 historical rows: 0.

## Governance
No fixed-bar substitution, new threshold, or 2025 tuning was introduced. Any semantic change requires a new compatibility audit and re-freeze.