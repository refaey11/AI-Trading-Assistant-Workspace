# Murphy 0030–0032 — Policy Decision V1

Date: 2026-08-16
Status: DECISION FOR PROPOSAL / NOT PRODUCTION FROZEN

## 1. State initialization
Decision: **CALIBRATION-CARRY FORWARD**.

The P&F state used for the 2019–2024 evaluation must be built from the complete pre-evaluation history available to the declared project pipeline, including the 2016–2018 calibration/warm-up block, and then evaluated from 2019-01-01 onward without resetting the P&F state at the evaluation boundary.

Reason: resetting at 2019 changes the P&F state and produces a materially different column history (the earlier diagnostic showed 89 columns when started at 2019, versus 150 when the same deterministic engine is built from 2016). A reset is therefore a model-definition change, not a harmless evaluation-window choice.

Important: this does **not** use 2019–2024 outcomes to tune the P&F policy. 2016–2018 remains the declared calibration/warm-up block and 2019–2024 remains evaluation.

## 2. Bootstrap policy
Decision: **EXPLICIT DETERMINISTIC HIGH/LOW BOOTSTRAP WITH AMBIGUITY BLOCK**.

The current engine's bootstrap is retained as a project operational policy: first completed bar supplies the initial high/low references; later completed bars are scanned until the first upward or downward box threshold is reached. If both thresholds qualify on the same completed bar, the state is `AMBIGUOUS` / `NOT_EVALUABLE` and no direction is chosen.

This policy is explicitly not claimed as verbatim Murphy or Kenneth Tower methodology.

Reason: silently resolving a same-bar conflict using bar order, close, or a future bar would introduce an undocumented assumption or potential look-ahead.

## 3. Box-size policy
Decision: **RETAIN 0.6257356643% AS THE DECLARED PROJECT PROPOSAL**, pending final validation.

It remains a reproducible project operationalization derived from the declared 2016–2018 calibration block. It is not presented as Murphy/Tower exact methodology.

## 4. Evaluation boundary
2016–2018: calibration/warm-up only.
2019–2024: evaluation only.
2025: OOS and excluded from tuning/selection.

## 5. Consequence
The final replay must be rebuilt from 2016 through 2024 and the 2019–2024 rows/snapshots selected for evaluation. It must **not** rebuild a fresh P&F state from 2019.

## 6. Remaining gates
This decision does not grant production approval. Required next gates remain:
- fresh 2016–2024 stateful replay with 2019–2024 evaluation output;
- availability/no-lookahead audit;
- structural sensitivity using pre-declared alternatives;
- CI evidence or equivalent reproducible record;
- explicit governance acceptance of operational policies.

No merge and no freeze until all gates pass.
