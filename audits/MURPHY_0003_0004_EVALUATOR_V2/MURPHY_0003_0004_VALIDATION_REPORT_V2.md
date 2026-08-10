# Murphy 0003–0004 Validation Report V2

## Scope

Validation of the exact structural conditions using the existing Pivot Sequence artifacts. Evaluation window: 2016–2024 only. 2025 excluded completely.

## Exact logic

- MURPHY_0003 = successive reaction peak higher AND successive reaction trough higher.
- MURPHY_0004 = successive reaction peak lower AND successive reaction trough lower.

No threshold, lookback, or source-definition change was introduced.

## Historical comparison

| TF | 0003 old trough-only | 0003 exact | 0004 old trough-only | 0004 exact |
|---|---:|---:|---:|---:|
| D1 | 197 | 15 | 204 | 15 |
| H1 | 4672 | 309 | 4335 | 309 |
| H4 | 1125 | 102 | 1102 | 102 |
| M15 | 15071 | 1135 | 14155 | 1135 |
| M30 | 7676 | 548 | 7183 | 548 |
| M5 | 42898 | 2806 | 40410 | 2806 |

## Interpretation

The exact two-condition rule is materially more selective than the legacy trough-only evaluator, as expected. This is a semantic correction, not tuning.

The symmetry of the exact PASS counts for 0003 and 0004 at each timeframe is a useful QA signal, but it is not treated as evidence of profitability or predictive accuracy.

## Validation status

- Exact condition implemented: PASS
- Missing-input handling: PASS
- Historical window restricted to 2016–2024: PASS
- 2025 excluded: PASS
- No new threshold introduced: PASS
- Legacy-vs-exact comparison recorded: PASS

## Remaining gate before production freeze

The historical counts above are a validation artifact, not a production freeze by themselves. The evaluator still needs to be wired to the canonical ordered confirmed-pivot artifact through its official contract and then run through the project's existing QA/test harness. Only after that integration QA passes should 0003–0004 be marked production-evaluable.
