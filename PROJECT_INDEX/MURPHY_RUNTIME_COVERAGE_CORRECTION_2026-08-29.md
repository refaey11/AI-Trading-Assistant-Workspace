# Murphy Runtime Coverage Correction — 2026-08-29

## Purpose
Correct the prior Gate 3C coverage interpretation using authoritative repository history. This record is audit/governance only; no trading semantics are changed.

## Correction
The earlier source-archive audit listed MURPHY_0018, 0019, 0025, and 0026 as not found in the supplied Murphy archive. Repository history confirms that all four already exist as runtime implementations and therefore must not be treated as missing runtime rules.

### MURPHY_0018 / 0019
- Exact evaluators exist.
- Runtime binding exists.
- Tests exist.
- Canonical runtime entry point exists.
- Commit `05da42997104bcc9970a501150895ade5b45a85e` explicitly promoted 0018/0019 to Runtime Implemented after full-path integration PASS (6/6 test cases).
- Earlier commits include geometry/convergence binding (`19574e6f8a6b65069ba0c4104f5ac34e6e1cc1b2`) and runtime entry point (`33316a927b28efd6924a49e92da83dac8ca412f3`).

### MURPHY_0025 / 0026
- Runtime evaluators exist.
- Runtime tests exist.
- Runtime entry-point wiring exists.
- Commit `a8cc1ae3f2bd0c51204f08904fe2938976916dbe` explicitly promoted 0025/0026 to verified runtime after entry-point smoke test.

## Official boundary
The governed Decision Brain runtime boundary remains exactly:
- 34 Murphy runtime-verified rules
- 44 Nison runtime-verified rules
- total = 78 governed rules
- Murphy 0008 remains BLOCKED / NOT_EVALUABLE

## Interpretation
The supplied Murphy archive remains a source/evidence pack and does not need to contain a dedicated standalone evidence file for every runtime rule. Repository history and existing runtime producers are authoritative for runtime implementation status.

Therefore:
- Do NOT rebuild Murphy.
- Do NOT ask for another Murphy archive merely because 0018/0019/0025/0026 are absent as standalone files in the archive.
- Do NOT create synthetic evidence for these rules.
- Gate 3C must use the existing 34-rule runtime producers/evaluators through the canonical event envelope.

## Current Gate 3C target
Prove one real pre-2025 GBPUSD event through:
Market/MTF -> full governed Murphy 34 -> full governed Nison 44 -> PIT Memory -> TIZ state -> recovered Decision Brain -> Risk -> Trade Plan.

The canonical event contract requires one authoritative `as_of`, explicit missing evidence, preserved provenance, and no future evidence. Nison, Memory, and TIZ remain non-directional; Risk remains the hard execution gate.

## 2025 rule
2025 remains OOS only and must not be used for tuning, calibration, threshold selection, implementation selection, or fitting.

## Next action
Proceed with the existing Full Brain integration boundary and build the canonical Murphy evidence envelope for the selected pre-2025 Gate 3C event. Then join Nison, PIT Memory, TIZ, Risk, and Trade Plan on the same snapshot.
