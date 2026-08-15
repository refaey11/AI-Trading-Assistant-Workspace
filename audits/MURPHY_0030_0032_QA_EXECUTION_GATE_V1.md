# Murphy 0030-0032 — QA Execution Gate V1

Date: 2026-08-16
Status: EXECUTION GATE ADDED — NOT FROZEN

Purpose: make the existing Murphy 0030-0032 tests executable in GitHub Actions before any production freeze.

Scope:
- Murphy Chapter 11 P&F construction semantics already mapped in the Rule Contract.
- Shared 3-box P&F core and logarithmic project operationalization remain on the proposal branch.
- 2025 is excluded from tuning and selection.

Required CI gate:
1. Install pytest.
2. Execute `python -m pytest -q tests/murphy_0030_0032`.
3. A successful workflow run is required before the proposal can advance.

Important boundary:
- CI success proves the committed unit tests execute successfully; it does not by itself prove the Project Box Policy is Murphy/Tower's exact method.
- Full 2019-2024 evaluator QA, availability/no-lookahead audit, and freeze remain separate gates.
- No merge to production is authorized by this artifact.
