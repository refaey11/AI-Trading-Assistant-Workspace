# Nison Hybrid 44 Batch — Run 3 Checkpoint

Date: 2026-08-16
Branch: `feature/nison-hybrid-44-batch-v1`
Status: SOURCE-VERIFIED / COMPATIBILITY GATES CONTINUE / NOT FROZEN

## What changed since Run 2

1. The Nison source-verification workflow previously failed because it required archive directory paths that were not present at those exact locations.
2. The extraction gate was corrected to validate the authoritative Registry root plus discovered context/candlestick/adapter roots rather than hard-code archive paths.
3. GitHub Actions Run #3 (`31960161199`) completed SUCCESS on commit `f4ccfbe0a9d648c7b42ca7f2a19f410996df951e`.
4. The source-bounded mapper completed successfully and produced `nison_44_source_map.json`.
5. Local inspection of the Run #3 artifact confirms **44/44 rules have at least one authoritative source-reference file**; none has zero source references.
6. This is a source-provenance result only. It does not promote any rule to evaluator-ready, QA-passed, or frozen status.

## Current known 44-rule status

| State | Count | Notes |
|---|---:|---|
| FROZEN | 0 | No automatic or premature freeze |
| FREEZE CANDIDATE | 1 | 0038 — structural compatibility pass; freeze/sessionization/future-closure gates remain open |
| BLOCKED / EVIDENCE GAP | 6 | 0026, 0030, 0031, 0035, 0036, 0037 |
| INCOMPLETE_NEEDS_DEFINITION | 37 | Source-referenced but evaluator/semantic contract remains incomplete |
| TOTAL | 44 | Registry count preserved |

## Rule-specific evidence

### 0035–0037
Existing Nison-specific evaluators/tests exist, but the batch gate records unresolved source-locked qualitative comparator contracts. They remain NOT_EVALUABLE/BLOCKED.

### 0038
Existing Nison-specific structural evaluator: 6/6 unit tests; 2016–2024 replay covered 2,544 rows and found 6 structural Windows; availability violations = 0. Freeze remains blocked by sessionization/future-closure and final governance gates.

### 0026 / 0030 / 0031
Repository audit found no Nison-specific evaluator/adapter for these rules. Murphy artifacts are not reused as Nison semantics. They remain implementation/evidence gaps until an authoritative Nison-specific contract/evaluator is located.

## Governance

- Nison remains confirmation/evidence only.
- No invented thresholds, tolerances, lookbacks, scoring, or direction.
- Historical outcomes are not used to define semantics or choose operators.
- 2025 remains OOS and is excluded from tuning, calibration, selection, and optimization.
- `main` is untouched by this batch.
- Auto-freeze is prohibited.

## Next action

Continue the batch over the remaining 37 incomplete rules by locating authoritative Nison-specific contracts and existing compatible primitives. For any rule with a complete source + contract + compatible primitive chain, run deterministic evaluator tests, then availability/no-lookahead and 2016–2024 QA. Do not reopen 0035–0037 without new authoritative evidence. Keep 0038 in FREEZE CANDIDATE until all remaining gates close.

## Verdict

**Run 3 = PASS for source verification and provenance mapping. Overall Nison 44 batch remains NOT FROZEN.**