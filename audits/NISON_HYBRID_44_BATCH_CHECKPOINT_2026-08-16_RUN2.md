# Nison Hybrid 44-Rule Batch — Run 2 Checkpoint

Date: 2026-08-16
Status: WORKING AUDIT — NO AUTO-FREEZE
Branch: feature/nison-hybrid-44-batch-v1

## What changed since Run 1

1. Re-inspected the feature branch tree and confirmed the Nison source archive is present and the Hybrid 44 factory contract, source-sync manifest, batch manifest, and prior proof-batch audits are present.
2. Added `nison_batch/source_map_44.py`, a source-bounded provenance scanner. It only maps registry rule IDs/names to text files inside the extracted Nison source package; it does not infer semantics, thresholds, lookbacks, scoring, direction, or freeze status.
3. Extended the Nison 44 batch workflow to run the source mapper after archive extraction and to preserve the mapping as an auditable artifact on the feature branch. Workflow trigger paths exclude generated artifacts to prevent recursive runs.
4. Re-verified the existing 0035–0038 proof batch: 0035–0037 remain blocked/not-evaluable on unresolved semantic comparators; 0038 remains a freeze candidate, not frozen.
5. Re-verified the 0026/0030/0031 checkpoint: no Nison-specific evaluator evidence was found for those rules; Murphy artifacts are explicitly not reused as Nison semantics.

## Current 44-rule status

| Status | Count | Rules / scope |
|---|---:|---|
| FROZEN | 0 | None |
| FREEZE CANDIDATE | 1 | 0038 |
| NOT_EVALUABLE / BLOCKED / IMPLEMENTATION GAP | 6 | 0026, 0030, 0031, 0035, 0036, 0037 |
| INCOMPLETE_NEEDS_DEFINITION | 37 | Remaining registry rules |
| TOTAL | 44 | Exact registry count |

## Gate interpretation

- 0038 has structural compatibility, 6/6 tests, 2016–2024 replay evidence, zero availability violations, and no lookahead in the Window geometry, but sessionization/future-window closure and formal freeze governance remain open.
- 0035–0037 have working structural evaluators/tests but required qualitative comparators remain source-unlocked; historical outcomes are not used to define them.
- 0026/0030/0031 have no Nison-specific implementation evidence in the current repository search surface; existing Murphy implementations are not accepted as substitutes.
- The remaining 37 rules stay in definition/source-mapping lane until authoritative Nison contracts and compatible primitives are evidenced.

## Safety invariants

- Nison remains confirmation-only.
- No invented Nison semantics, thresholds, tolerances, lookbacks, scoring, or direction.
- 2016–2024 is validation only after semantics/operators are closed.
- 2025 remains OOS and is excluded from tuning, calibration, selection, optimization, and operator choice.
- No automatic production freeze.
- `main` is untouched.

## Next action

Use the extracted source package in GitHub Actions to produce the rule-level source map, then use that evidence to move only independently supportable rules from `INCOMPLETE_NEEDS_DEFINITION` into compatibility/evaluator lanes. Do not reopen 0035–0037 without new authoritative evidence and do not promote 0038 without its remaining governance gates.
