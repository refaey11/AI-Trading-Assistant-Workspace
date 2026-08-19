# Murphy 0013–0020 — Implementation & Test Specification V1

## Scope
Implement the four shared primitives as source-safe wrappers around existing project components, then evaluate Rules 0013–0020 as one batch.

## Primitive contracts
- PF-H1: consume confirmed Pivot Sequence V2 / existing S/R evidence. If horizontal qualification requires an unapproved numeric tolerance, return `NOT_EVALUABLE`.
- PF-G1: consume TRENDLINE_GEOMETRY_V1 outputs. Return only classifications supported by the existing geometry contract; no imported external tolerance.
- PF-B1: require a completed-bar boundary cross/close and a valid availability timestamp. Do not add ATR, percentage, volume, or two-bar significance thresholds unless an authoritative Murphy contract supplies them.
- PF-F1: consume existing flagpole/structure evidence. If “sharp” cannot be established by an existing authoritative deterministic field, return `NOT_EVALUABLE`.

## Determinism requirements
1. Same inputs -> same output.
2. No future bars may influence a decision timestamp.
3. Availability timestamp must be <= decision timestamp.
4. Missing/ambiguous evidence -> `NOT_EVALUABLE`, never guessed.
5. No parameter selection from 2025 or from outcome optimization.

## Unit-test matrix
### PF-H1
- confirmed horizontal evidence -> deterministic qualified result
- missing level evidence -> NOT_EVALUABLE
- ambiguous tolerance -> NOT_EVALUABLE

### PF-G1
- authoritative converging geometry -> CONVERGING
- authoritative parallel geometry -> PARALLEL
- insufficient/ambiguous geometry -> NOT_EVALUABLE

### PF-B1
- completed-bar close beyond boundary + valid availability -> confirmed breakout
- wick-only intrusion -> not confirmed
- availability after decision timestamp -> reject / NOT_EVALUABLE
- missing boundary -> NOT_EVALUABLE

### PF-F1
- authoritative flagpole relation -> qualified result
- missing pole -> NOT_EVALUABLE
- ambiguous “sharp” -> NOT_EVALUABLE

## Rule batch dependencies
0013 G1+B1; 0014 H1+B1; 0015 H1+B1; 0016 F1+G1+B1; 0017 F1+G1+B1; 0018 G1+B1; 0019 G1+B1; 0020 H1+B1.

## Historical gate
Run only on 2016–2024 after unit and availability tests pass. 2025 is OOS and must not be used for tuning/operator selection.

## Freeze gate
A rule may be marked Production Frozen only after compatibility, deterministic tests, availability/no-lookahead, 2016–2024 QA, provenance reconciliation, and explicit freeze evidence all pass.

## Safety boundary
This specification does not create a Murphy threshold. External projects are corroboration only. The 33 existing frozen Murphy rules are out of scope and must not be modified.
