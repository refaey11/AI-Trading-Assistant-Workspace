# Integration Progress — 2026-08-22

## Purpose
Checkpoint for runtime recovery and Decision Brain integration. This record does not modify frozen Murphy or Nison rule definitions.

## Verified recovery
- Reconstructed the multi-part GBPUSD Rule Evaluator workspace successfully.
- Archive integrity test passed.
- 241 files extracted/read.
- 16/16 direct evaluator tests passed for the evaluator artifacts exercised during recovery.
- Pivot V2 artifacts inspected: 33 files contained `CONFIRMED_AFTER_2_BARS` and `availability_timestamp` data required for the verified pivot path.

## Murphy runtime status confirmed in this checkpoint
- 0003: runtime verified.
- 0004: runtime verified.
- 0006: NOT_EVALUABLE pending approved successful third-touch/reaction definition.
- 0007: NOT_EVALUABLE pending approved successful third-touch/reaction definition.
- 0018: partial; approved derived wedge geometry still required.
- 0019: partial; approved derived wedge geometry still required.

## Adapter integration completed in this checkpoint
A runtime adapter path was exercised for available Murphy outputs and normalized evidence.
Covered rule IDs:
- 0003
- 0004
- 0021
- 0022
- 0023
- 0028
- 0029
- 0050

Integration test result: 9/9 PASS.

Verified safety behavior:
- NOT_EVALUABLE does not become a trade signal.
- Adapter does not independently create BUY/SELL.
- Rule 0050 remains non-directional/process-gate behavior.
- Unknown rule IDs are rejected.
- Fail-closed behavior is preserved for invalid/unsupported inputs.

## Runtime execution result — Breakout / Role-Reversal Family
### 0008 — Role reversal: support to resistance
Cross-source recovery completed against the reconstructed workspace, source registry, GitHub, and Dropbox metadata.

Findings:
- GitHub code search: no direct `MURPHY_0008` evaluator artifact found in the current repository index.
- Reconstructed workspace: `MURPHY_51_RULE_TO_MTF_FUNCTION_MAP_V1.csv` lists MURPHY_0008 as `setup_or_confirmation`, using `risk,support_resistance,trend`; its timeframe resolution is `UNRESOLVED_BY_RULE` and requires an explicit MTF policy/contract.
- Reconstructed workspace: `MURPHY_51_EXACT_CONDITION_PREP_V1.csv` lists MURPHY_0008 as `PARTIALLY_EVALUABLE`, with condition families `trend;support_resistance;risk_process`; missing feature family `risk_process`; timeframe policy `DYNAMIC_MTF_POLICY_V1_DRAFT`; note: do not mark PASS/FAIL until exact rule conditions are mapped.
- Reconstructed workspace compatibility audit: MURPHY_0008 is `SUPPORTED_PRIMITIVE` because support/resistance primitives exist (`support_20`, `support_50`, `support_100`, `resistance_20`, `resistance_50`, `resistance_100`).
- Reconstructed source rule registry: the frozen/source rule requires a support level to be decisively broken downward and later rallied toward, with broken support acting as resistance. The source rule does not itself supply the missing runtime definition needed to operationalize `decisively broken` or the exact MTF policy.
- Dropbox: newer workspace parts dated 2026-08-20 were found, but the available Dropbox text extractor cannot read the ~199 MB archive part directly; this does not override the already reconstructed readable workspace evidence.

Final current status: PARTIAL / NOT FINAL-PASS.
Reason: primitives exist, but the exact runtime binding for decisive break, risk/process dependency, and explicit MTF policy is not yet frozen/bound. No PASS/FAIL trade outcome is assigned.
No frozen rule definition was changed.

## Current next work
Continue remaining Murphy rules by shared dependency family, then bind the recovered runtime outputs into the broader path:

Murphy Runtime -> Rule Adapter -> Normalized Evidence -> Decision Brain -> Risk Hard Gate -> Final Output

Nison remains confirmation/context evidence only. Similarity remains historical evidence only. Trading in the Zone remains a process/psychology gate and cannot create direction.

## GitHub logging policy
All material recovery, integration, test, gap, and status checkpoints should be committed here going forward. Frozen source-of-truth rule definitions must not be altered during integration work.
