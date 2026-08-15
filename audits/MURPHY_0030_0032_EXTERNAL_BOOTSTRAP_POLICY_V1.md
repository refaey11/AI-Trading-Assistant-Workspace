# Murphy 0030–0032 — External Deterministic Bootstrap Policy V1

Status: PROPOSAL / EVALUATION-ONLY / NOT PRODUCTION FROZEN

## Purpose
Provide a deterministic initialization procedure for the project P&F engine where the Murphy source establishes the P&F construction semantics but does not provide a fully reproducible initial-column algorithm in the project source.

## Provenance boundary
This is an **EXTERNAL DETERMINISTIC PROJECT OPERATIONAL POLICY**. It is not claimed to be verbatim Murphy and is not claimed to reproduce an exact Kenneth Tower formula.

## Inputs
- Completed D1 OHLC bars only.
- Fixed project box percentage supplied by the separate Box Policy.
- Reversal amount fixed at 3 boxes.

## Initialization
1. Use the first completed D1 bar as the initial High/Low reference.
2. Quantize the initial High downward to the project logarithmic box grid and the initial Low upward to the same grid.
3. Scan subsequent completed D1 bars in chronological order.
4. Establish the first X column when the first upward box threshold above the initial High reference is reached by a bar High.
5. Establish the first O column when the first downward box threshold below the initial Low reference is reached by a bar Low.
6. If both first-direction thresholds qualify on the same completed bar, mark the bootstrap **AMBIGUOUS / NOT_EVALUABLE**. Do not silently choose a direction.
7. If neither threshold is reached by the available data, bootstrap remains **NOT_EVALUABLE**.
8. Once initialized, use the existing shared 3-box High/Low P&F engine without changing rule semantics.

## No-lookahead requirement
Only bars up to and including the current completed bar may affect initialization. A future suffix must not alter an earlier bootstrap result.

## Forbidden substitutions
- No profitability-based bootstrap selection.
- No 2025 tuning or selection.
- No invented ATR/pip/percentage thresholds beyond the separately declared box policy.
- No silent use of close-only initialization.
- No tie-breaking on ambiguous same-bar X/O qualification.

## Acceptance
This policy may be used for the 2019–2024 evaluator only after the project governance gate explicitly accepts it as an operationalization. Acceptance does not convert it into Murphy source text.
