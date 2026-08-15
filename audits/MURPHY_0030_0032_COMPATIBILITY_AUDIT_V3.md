# Murphy 0030–0032 Compatibility Audit V3

Date: 2026-08-16
Status: BLOCKED — compatibility corrected; historical gates still open

## Source-of-truth findings
The project contract defines:
- 0030 = bullish P&F support, structural context only, originating from the base of the lowest O column and represented as a bullish 45-degree support reference.
- 0031 = long-stop reference below the previous O column in valid P&F uptrend context.
- 0032 = short-stop reference above the previous X column in valid P&F downtrend context.

The contract explicitly prohibits autonomous BUY/SELL decisions, invented stop offsets, future data, profitability-based box selection, and 2025 tuning.

## Compatibility correction
The evaluator now distinguishes:
- `PNF_BULLISH_SUPPORT_ORIGIN` + `role=STRUCTURAL_REFERENCE` for 0030;
- `PNF_LONG_STOP_REFERENCE` + `role=RISK_REFERENCE` for 0031;
- `PNF_SHORT_STOP_REFERENCE` + `role=RISK_REFERENCE` for 0032.

All three expose `entry_trigger=None`.

0030 intentionally records the lowest-O origin required by the source contract without inventing a separate trendline projection, break operator, touch operator, or entry trigger that is not source-locked.

## External technical verification
Independent P&F references corroborate the operational High/Low and 3-box mechanics. StockCharts specifies High-first continuation for X columns and Low-first continuation for O columns, with the opposite price used for a 3-box reversal. Jeremy du Plessis' material independently documents daily High/Low 3-box construction and the fact that the High/Low method needs a deterministic sequence because daily high and low order is not known.

These sources support construction mechanics only. They do not establish an exact Kenneth Tower volatility-to-box conversion formula for this project.

## Box policy
The project proposal remains `0.6257356643%`, calculated from the pre-declared 2016–2018 daily log-return standard deviation. It remains explicitly a project operationalization, not a Murphy/Tower exact value.

## Bootstrap
The first-column bootstrap remains a separate external deterministic operational policy. It is not represented as verbatim Murphy.

## Tests / execution state
The current proposal branch contains focused evaluator tests covering structural/risk roles, entry-trigger prohibition, malformed input, and prefix replay. The repository's GitHub Actions workflow exists, but the latest proposal commits still have no associated workflow run/status; CI is therefore unproven.

The canonical D1 file is available in File Library and is documented as 2,544 rows from 2016-01-03 through 2024-12-31 in the project's historical QA artifacts. The full bytes are not mounted into the current runtime, so a fresh 2019–2024 evaluator replay cannot honestly be claimed as executed here.

## Decision
**BLOCKED**

The semantic compatibility issue is corrected. The remaining blockers are execution/provenance gates:
1. CI run must actually execute and pass.
2. Fresh 2019–2024 evaluator replay on canonical D1 must execute.
3. Dataset-level availability/no-lookahead must be proven.
4. Pre-declared structural sensitivity/robustness must be rerun against the corrected evaluator.
5. Only then can freeze/merge be considered.

2025 remains OOS and must not be used for tuning or selection.
