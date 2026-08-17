# Murphy 0042–0045 — Implementation Blocker Audit V1

Status: BLOCKED / NOT PRODUCTION FROZEN

## Evidence reconciliation
The project source-of-truth artifacts establish that a Risk Engine exists as a research component and that the Rule Adapter exists as a normalization layer. However, the current adapter implementation is explicitly not a real risk gate: it does not evaluate the Risk Engine contract and can treat textual risk fields as support rather than evaluating `risk_pass=true/false`.

Therefore the following are NOT claimed:
- production Risk Engine integration;
- rule-level PASS for 0042–0045;
- historical QA closure;
- production freeze.

## Required smallest missing implementation
1. Locate the authoritative Risk Engine runtime producer.
2. Expose its rule-specific result as PASS / FAIL / NOT_EVALUABLE with source metadata and availability timestamp.
3. Connect that result to the existing Rule Adapter contract only.
4. Preserve hard precedence: Risk FAIL blocks execution; missing evidence becomes needs_review; Similarity and Murphy/Nison evidence cannot override the hard gate.
5. Add deterministic adapter tests and availability/no-lookahead tests.

## Explicit non-actions
- Do not rebuild the Risk Engine.
- Do not infer PASS from textual risk fields.
- Do not choose among source ranges as a tuning exercise.
- Do not use 2025 to select thresholds/operators.
- Do not freeze 0042–0045 until the runtime producer and tests are evidenced.

## Source alignment
This audit is consistent with the existing 0042–0045 Risk Gate Adapter Contract and the project compatibility audit, which identifies the current adapter risk logic as not equivalent to a real risk gate.
