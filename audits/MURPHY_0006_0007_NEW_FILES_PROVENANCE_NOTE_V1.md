# Murphy 0006–0007 — New Workspace Files Provenance Note V1

Date: 2026-08-13
Status: PROVENANCE RECORDED / OPERATOR GATE STILL OPEN

## Purpose
Record the material findings from the newly supplied workspace files so future work resumes from verified project state without rebuilding or relying on chat memory.

## Source files reviewed
- MURPHY_EVALUATORS_V1(2).zip
- MURPHY_RULE_WORKSPACE_STATUS_V1(1).csv
- MURPHY_REFRESH_V1(2).zip
- WORKSPACE_TRANSFER_MANIFEST variants
- UNIFORM_OOS_AGGREGATION_V1.json
- UNIFORM_OOS_PNL_2025.zip
- DECISION_BRAIN_V1_SPEC(1).json

## Verified findings relevant to 0006/0007
1. MURPHY_0006 and MURPHY_0007 remain NOT_YET_EVALUABLE.
2. The existing qualitative operator is explicitly recorded as: `third touch followed by reaction away from line` / `A third successful touch and reaction confirms the trendline`.
3. The supplied evaluator bundle does not provide a dedicated production evaluator that closes 0006/0007.
4. Existing project evidence/adapter/gate infrastructure is reusable; it must not be rebuilt.
5. The existing evidence gate accepts upstream `third_touch_detected`, `reaction_detected`, `no_break_valid`, and `confirmation_timestamp`; it intentionally does not infer touch tolerance, reaction magnitude, or break thresholds.
6. Existing `break_structure_up/down` material remains generic evidence and is not proven as a 0006/0007-specific no-break operator.
7. The new files therefore do NOT close the 0006/0007 operational gate.

## Still open
- deterministic successful third-touch predicate
- deterministic reaction-away-from-line predicate
- deterministic 0006/0007 no-break/line-hold binding
- confirmation timestamp semantics
- production evaluator execution
- 2016–2024 historical QA
- final freeze

## Prohibited inference remains in force
Do not add ATR, pip, percentage, fixed lookback, fixed reaction magnitude/duration, automatic 2-day binding, automatic 3% binding, or any other threshold/operator unless supported by an authoritative source/approved project contract.

2025 remains OOS and must not be used for tuning or implementation/operator selection.

## Architectural decision
Preserve and reuse PIVOT_SEQUENCE_V2, TRENDLINE_GEOMETRY_V1, Evidence Adapter, Evidence Gate, and evaluator infrastructure. The next investigation remains provenance-first: recover an authoritative source/project contract that operationalizes successful third touch, reaction away from line, and no-break.

## Important distinction
These files strengthen provenance and confirm the exact missing layer; they do not authorize a PASS/FAIL evaluator for 0006/0007.
