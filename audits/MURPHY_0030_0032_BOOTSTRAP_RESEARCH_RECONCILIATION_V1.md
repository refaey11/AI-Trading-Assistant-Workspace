# Murphy 0030–0032 — Bootstrap Research Reconciliation V1

Status: RESEARCH CLOSED / OPERATIONALIZATION PROPOSAL / NOT FROZEN

## Findings

1. The project source and Murphy Chapter 11 establish the Point & Figure semantics, but do not provide a complete software algorithm for the first column bootstrap.
2. External P&F references independently describe the missing bootstrap concept: establish the initial direction from the first significant move relative to the initial price reference, then apply the standard High/Low 3-box method.
3. Jeremy du Plessis provides an explicit High/Low example: inspect the first High/Low, then subsequent High/Low observations; start with X when the first upward threshold is reached or O when the first downward threshold is reached, ignoring observations that reach neither threshold.
4. StockCharts independently documents the post-bootstrap High/Low priority rules: X checks High for continuation first, then Low for reversal; O checks Low first, then High for reversal.
5. MQL5 independently documents the same core parameters and High/Low rounding/3-box reversal mechanics.

## Governance decision

The project may use a deterministic bootstrap as an explicit operationalization, but it must not be represented as verbatim Murphy wording.

The selected policy is recorded in `MURPHY_0030_0032_BOOTSTRAP_POLICY_V1.md`.

## Remaining validation

- Execute the new bootstrap regression tests in the actual repository environment.
- Compare the resulting first-column construction against at least one independent implementation/reference.
- Run deterministic prefix replay on the project 2016–2024 data.
- Run the 0030–0032 evaluator only after bootstrap and box policy are both reproducibly executed.
- Any discrepancy remains NOT_EVALUABLE; do not tune the bootstrap to reproduce a target historical count.

## Sources

- Murphy Chapter 11 / project Master KB: authoritative source semantics.
- Jeremy du Plessis, *The Definitive Guide to Point and Figure*: bootstrap example.
- StockCharts ChartSchool: High–Low Method and 3-box reversal mechanics.
- MQL5 P&F construction article: independent implementation mechanics.

2025 remains locked OOS and is excluded from all selection/tuning.