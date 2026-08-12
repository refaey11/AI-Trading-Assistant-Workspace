# Murphy 51 Closure Matrix V1

Date: 2026-08-12

## Purpose

This matrix is a closure-control artifact, not a claim that all 51 rules are complete. The Master Handoff explicitly states that exact Feature → Operator → TF Role → Gate Logic is not frozen for all 51 and that evaluator artifacts are only partial. fileciteturn185file10

## Verified states

| Rule(s) | Current evidence-backed state | Closure action |
|---|---|---|
| 0001 | PARTIAL — existing trend_regime / structure mapping; definite-reversal operator not frozen | Source-lock operator before evaluator |
| 0002 | NOT_EVALUABLE — execution/timing/process operator not frozen | Recover/verify exact operator |
| 0003–0004 | V2 implementation/test artifacts exist, but historical provenance remains unresolved; MUST NOT be frozen | Preserve V2; recover old provenance; side-by-side reconciliation |
| 0006–0007 | Existing Trendline Geometry; working split LOW+UP/BULLISH and HIGH+DOWN/BEARISH, but operational third-touch/reaction evidence is unproven | Source-lock mapping + Geometry compatibility |
| 0021–0023 | Existing evaluator + unit-test + historical artifacts; unit-test artifact cases pass | Historical/semantic QA; then adapter integration |
| 0027 | BLOCKED / NOT_EVALUABLE — exact trend-vs-range operator missing | Source-supported operator only |
| 0028–0029 | Existing evaluator + unit-test artifacts; preserved unit-test cases pass | Source semantic + historical QA |
| 0050 | Structural evaluator exists but CURRENT_STATE_NOT_EVALUABLE; combined evidence contract incomplete | Close missing upstream evidence contracts only |

## All other Murphy rules

Rules not listed above are **NOT_YET_CLOSED in this matrix**. This is deliberately different from assigning a new semantic status to those rules. Their exact Feature → Operator → TF Role → Gate Logic must be checked from the source workspace before closure.

## Mandatory closure pipeline

For every rule:

1. Workspace/source check
2. Mapping
3. Feature
4. Dynamic MTF
5. Operator/logic
6. Existing evaluator
7. Unit tests
8. Historical/provenance evidence
9. QA
10. Freeze only after all required gates pass

The Master Handoff explicitly requires this ordering and prohibits inventing thresholds/operators/timeframes. fileciteturn185file1

## Architecture controls

- Decision Brain V1/V1.1 already exists; do not rebuild it.
- Rule Adapter is normalization only; it does not decide trades.
- Murphy = technical context.
- Nison = confirmation only.
- Trading in the Zone = process/psychology gate only.
- Similarity = historical evidence only.
- Risk = hard gate.
- 2025 = OOS and must not be used for tuning.

## Baseline gate

The Official Baseline is still NOT FROZEN. Candidate: Similarity Engine V2 + 4H. The required gate is one frozen uniform walk-forward across all five assets with 2016–2023 → OOS 2024 and 2016–2024 → OOS 2025, identical signal/k/SL-TP/ambiguity/costs, followed by leakage audit. fileciteturn182file0

## Current phase

**CLOSURE / QA — NOT IMPLEMENTATION REBUILD.**

The next work should prioritize the rules with existing evaluator artifacts and then the highest-impact blockers (0006–0007 and 0003–0004 provenance), without rebuilding existing modules.
