# Murphy 0042–0045 — Source-to-Risk-Gate Reconciliation V1

Status: INTEGRATION READY / NOT PRODUCTION FROZEN

## Source-locked rule semantics

| Rule | Murphy Chapter | Source condition | Operational boundary |
|---|---|---|---|
| 0042 | Ch.16 Capital Allocation | Total investment must not exceed 50% of available capital | Breach of 50% = risk FAIL; missing evidence = needs_review |
| 0043 | Ch.16 Capital Allocation | Entry into a single market limited to 10%–15% of total capital | Preserve source range; do not silently collapse it to one project threshold |
| 0044 | Ch.16 Capital Allocation | Risk exposure in a single market limited to 5% of total capital | Breach of 5% = risk FAIL; missing evidence = needs_review |
| 0045 | Ch.16 Capital Allocation | Total margin limited to 20%–25% of total capital | Preserve source range; do not silently collapse it to one project threshold |

## Adapter behavior

- Reuse the existing Risk Engine; do not rebuild it.
- PASS -> `gate=pass`, `available=true`.
- FAIL -> `gate=fail`, `available=true`; execution is blocked.
- Missing/unsupported evidence -> `gate=needs_review`, `available=false`; no execution.
- The adapter does not infer PASS from textual presence or missing data.
- The adapter does not create direction or scoring.
- Similarity cannot override a risk FAIL.
- 2025 remains OOS and is excluded from tuning/operator selection.

## Range governance

Murphy states ranges for 0043 and 0045. This artifact intentionally does not select a lower or midpoint threshold. A later governance decision must specify how the project treats the stated range before a production evaluator can be frozen.

## Required remaining gates

1. Map each rule to actual Risk Engine fields already present in the workspace.
2. Add deterministic adapter tests for PASS / FAIL / missing / unsupported evidence.
3. Run availability and no-lookahead checks.
4. Run 2016–2024 historical QA where applicable.
5. Create provenance/freeze manifest and obtain explicit freeze approval.

This reconciliation resolves the prior provenance blocker but does not claim production freeze.
