# Hybrid Evidence Murphy Pilot V1

## Scope
Isolated engineering pilot. No production merge and no change to canonical Murphy semantics.

## Design under test
1. Canonical hard gate remains authoritative.
2. Relative engineering measurements are converted to a bounded evidence grade.
3. Engineering evidence is explicitly versioned as `ENG-HYBRID-V1`.
4. Engineering evidence cannot generate direction and cannot rescue a failed canonical gate.

## Initial pilot cases
Use three qualitative Murphy concepts from the existing rule queue where the source meaning is known but the operational measurement is not fully specified:
- horizontalness / level quality
- convergence / parallelism
- breakout significance

## Required acceptance gates
- Source compatibility audit for each pilot rule.
- No new Murphy semantics.
- Parameters declared before evaluation.
- Calibration limited to 2016–2018.
- Evaluation 2019–2024.
- 2025 excluded from tuning/selection.
- Prefix replay and future-suffix mutation tests.
- Evidence provenance distinguishes canonical from engineering fields.
- Compare baseline blocked/evaluable status against hybrid status; do not optimize trading profitability.

## Promotion rule
The pilot is successful only if it makes previously non-evaluable qualitative conditions operationally testable **without** changing canonical meaning, introducing lookahead, or using evaluation/OOS outcomes for parameter selection.

If these conditions are not met, reject or revise the pilot. Do not generalize it to the full rule registry.
