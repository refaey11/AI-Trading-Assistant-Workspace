# Nison 44 — Compiled Contract Status V1

Date: 2026-08-17
Branch: nison-batch-v1
Source: Master Trading Rules V2 + Master KB Formation_Rules

## Result
All 44 Nison rule IDs have now passed through the normalized contract compiler.

| IDs | Count | Compiler state |
|---|---:|---|
| 0001–0007, 0008–0020, 0022, 0025–0033, 0037 | 29 | PARTIAL_NOT_EVALUABLE — structural contract extracted; one or more source-defined qualitative terms remain unresolved |
| 0021, 0023, 0024, 0034, 0036 | 5 | STRUCTURAL_CANDIDATE — source formation is structurally expressible; confirmation/context/QA still required |
| 0035, 0038 | 2 | EXISTING_REPLAY_ARTIFACT_REUSE — reuse existing evaluator/replay evidence; do not rebuild |
| 0039–0044 | 6 | CONTEXT_GATE — methodology/context rules, not standalone candle recognizers |

## Important source findings
- 38 rules have Formation_Rules source artifacts in the Nison pattern KB.
- 0039–0044 do not have standalone Formation_Rules files; they are technique/context entries.
- Qualitative source language is preserved rather than converted into invented thresholds.
- Examples include `long`, `small`, `near`, `strong`, `similar`, `approximately`, `ideally`, and related wording.
- A qualitative blocker does not invalidate the deterministic structural portion; it prevents a full PASS/FREEZE claim.

## Reuse policy
0035 Tasuki Gap and 0038 Windows retain their existing evaluator/replay artifacts. Existing evidence is reconciled; no replacement implementation is created.

## Output contract
Each compiled rule is expected to expose:
- source_reference
- formation contract
- required context
- confirmation contract or unresolved state
- invalidation contract or unresolved state
- availability/no-lookahead requirements
- output state: MATCH / NO_MATCH / NOT_EVALUABLE
- direction: NEUTRAL

## Freeze gate
No rule is marked Frozen by compilation alone. Freeze requires source lock, complete operators, passing tests, historical QA, and no-lookahead verification. 2025 remains OOS and cannot be used for tuning.

## Next execution step
Run the compiled contracts against the real Market Reader/OHLCV runtime for 2016–2024, reusing existing 0035/0038 replay evidence, and produce per-rule PASS/FAIL/NOT_EVALUABLE results. Compilation itself is not historical QA.