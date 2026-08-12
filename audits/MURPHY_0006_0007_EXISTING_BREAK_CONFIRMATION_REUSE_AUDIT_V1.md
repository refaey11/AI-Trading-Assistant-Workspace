# Murphy 0006–0007 Existing Break/Confirmation Reuse Audit V1

Date: 2026-08-12
Status: COMPLETED

## Question

Before creating any new no-break or confirmation operator, determine whether the project already contains an existing implementation that can be reused for Murphy 0006/0007.

## Findings

An existing Murphy trendline confirmation evaluator was found in the project history/branch `feature/murphy-0006-0007-source-contract`:

`audits/MURPHY_0006_0007_TRENDLINE_SOURCE_CONTRACT_V1.py`

Function:
`evaluate_trendline_confirmation(...)`

The evaluator already binds:
- MURPHY_0006 -> UP / BULLISH_STRUCTURE
- MURPHY_0007 -> DOWN / BEARISH_STRUCTURE

It consumes the following upstream facts:
- trendline type
- anchor count
- third_touch
- reaction_bounce
- no_break
- confirmation_available_timestamp

It returns `NOT_EVALUABLE` when required upstream evidence is missing, and only returns PASS/FAIL after the upstream facts are supplied.

## Important architectural finding

The evaluator does NOT itself calculate the touch/reaction/no-break semantics. It explicitly expects those to be already-derived Trendline Geometry V1 facts.

Therefore it is an existing reusable confirmation/evaluator component, but it is NOT evidence that the upstream Geometry V1 output already contains the required fields.

## Break/no-break reuse finding

No separate authoritative repository file was located through the available GitHub code search that defines a new 0006/0007-specific no-break operator or numeric break threshold.

The project contract explicitly prohibits inventing such a threshold. The existing evaluator's `no_break` input must therefore remain an upstream evidence field rather than being synthesized inside the evaluator.

## Decision

DO NOT create a replacement evaluator.
DO NOT create a new no-break operator at this stage.
REUSE the existing `evaluate_trendline_confirmation` contract if/when Geometry V1 can provide its required evidence fields.

The remaining gate is specifically upstream Geometry V1 output/schema verification:
1. third_touch
2. reaction_bounce
3. no_break
4. confirmation_available_timestamp

If those fields are absent, keep the production evaluator blocked as `NOT_EVALUABLE` rather than inventing them.

## 2025 control

2025 remains OOS and is not used for tuning, threshold selection, or implementation choice.

## Next action

Inspect the exact Geometry V1 output schema/artifacts in the full project/workspace and reconcile them against the evaluator's required fields. If the schema exposes equivalent authoritative fields, wire the adapter to them. If not, document the missing upstream contract and stop before creating a new operator.
