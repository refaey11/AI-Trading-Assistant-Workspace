# Murphy 0030 — Source Lock V2

## Source
Master KB / John Murphy / Chapter 11 — Point and Figure Charts.

## What the source explicitly supports
- P&F uses X columns for upward movement and O columns for downward movement.
- Box size is a material construction parameter; the source gives examples of larger 5–10 point boxes and a smaller 1-point box.
- Reversal requires a minimum price move; the source gives 3-box and 5-box reversal as examples.
- Trendline/risk rules use the lowest O column / highest X column as structural anchors.

## What remains source-underdetermined
- No single universal box size is selected by the source for this project.
- No single universal reversal value is selected by the source for this project.
- Bootstrap/initial-column construction is not specified in the Chapter 11 source artifact.

## Implementation rule
The evaluator MUST NOT silently choose a box size, reversal value, or bootstrap rule. These must arrive as explicit configuration/evidence. Missing configuration returns NOT_EVALUABLE.

## Freeze implication
0030 can pass governance/CI tests without being Production Frozen. Production freeze requires the missing bootstrap policy and explicit evaluator configuration, followed by QA and availability/no-lookahead evidence.
