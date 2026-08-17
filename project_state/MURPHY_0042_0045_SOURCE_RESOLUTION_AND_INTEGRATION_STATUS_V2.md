# Murphy 0042–0045 — Source Resolution & Integration Status V2

Status: SOURCE RESOLVED / INTEGRATION BLOCKED ON FIELD-PRODUCER BINDING

## Correction
The earlier statement that the authoritative 0042–0045 rule records were missing is superseded.
The current Master KB and independent MT5 Pro AI archive reconciliation provide the exact source semantics.

## Source-locked semantics
- 0042: total investment <= 50% of available capital; capital reserve guideline.
- 0043: total entry into a single market limited to 10%–15% of total capital.
- 0044: risk exposure in a single market limited to 5% of total capital.
- 0045: total margin limited to 20%–25% of total capital.

The ranges in 0043 and 0045 are source ranges. No single project threshold is selected here.

## Existing infrastructure
The project already contains a Risk Engine as a research component and a Rule Adapter. The adapter is currently design/initial implementation and its present risk behavior is NOT a real risk gate: textual risk-field presence may be marked as support rather than evaluating authoritative PASS/FAIL.

## Exact remaining blocker
We must identify the authoritative Risk Engine producer fields for:
- total investment / capital allocation
- single-market entry exposure
- single-market risk exposure
- total margin

Only after those producer fields are identified can the existing Rule Adapter normalize authoritative PASS/FAIL/NOT_EVALUABLE results.

## Forbidden actions
- Do not invent producer field names as if they already exist.
- Do not rebuild the Risk Engine.
- Do not select 10% or 20% as a hard ceiling merely because Murphy states ranges.
- Do not infer PASS from text presence or missing evidence.
- Do not use 2025 for tuning or threshold selection.

## Next engineering step
Trace the existing Risk Engine implementation/contract to its authoritative runtime producer, then add the smallest 0042–0045 mapping and deterministic tests. Historical QA and freeze follow only after that integration is proven.
