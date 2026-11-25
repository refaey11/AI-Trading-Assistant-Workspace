# Decision Brain Caller and Authority Audit — 2026-11-25

## Scope
- Repository: `refaey11/AI-Trading-Assistant-Workspace`
- Review branch: `fix/similarity-direction-isolation-2026-11-25`
- Comparison base: `current-stack-dev-backtest-2016-2024-v3` at `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`
- GitHub-only inspection. No Dropbox, no data payloads, no main changes, no merge.
- No 2025/2026 market-data access or tuning.

## Verified caller path: Similarity is inert in the two inspected governed paths
1. `compatibility/run_knowledge_decision_brain.py` now calls `assess(..., similarity=None)`; Similarity is retained in the handoff evidence bundle.
2. `OOS_2025/full_decision_brain_assembler_v1.py` calls `assess_with_governance(... historical_evidence=historical_evidence)`.
3. `compatibility/decision_brain_v1_handoff_adapter.py` calls `decision_brain_module.assess(row_copy, similarity=None)`.
4. Its `_sanitize_historical` function preserves historical evidence fields and explicitly marks `predicted_return_used_as_direction=False`; the sanitized history is returned for audit metadata, not passed to the Decision Brain assessment.
5. The recovered `decision_brain.assess` implementation still contains an optional Similarity-to-direction path when a caller supplies a non-null similarity object. Therefore the global invariant depends on every caller continuing to pass `None`.

### Search limitation
The connected GitHub code-search operation searches the repository default branch, not an arbitrary review branch, and returned no usable indexed results for the caller queries. This audit therefore verifies the explicit call paths above but does NOT certify that every caller across every branch has been exhaustively enumerated.

## Confirmed directional-authority ambiguity
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py` creates bullish/bearish evidence from `mtf_trend_score`, six timeframe trend-regime fields, and available volume-regime fields.
- `evaluation/three_book_decision_evaluator_v1.py` then compares the resulting Brain directional bias against `murphy_evidence.direction` / `candidate_direction`.
- Thus the current path has two direction-bearing sources: the MTF/volume-derived Brain assessment and Murphy evidence. The evaluator can reject disagreement, but it does not establish that the Brain's MTF fields are themselves Murphy-authenticated.
- No frozen Brain semantics were changed. Required decision: either document and prove field-level Murphy lineage for all direction-bearing row fields, or formally redesign the boundary so Murphy is the sole directional authority and the Brain is non-directional context/evidence.

## Confirmed public bridge authority gap
In `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`:
- The bridge rejects missing Murphy/Nison/Risk mappings.
- It checks `authoritative=True` only for Risk.
- It does not itself require Murphy's authoritative/provenance fields.
- It does not itself require Nison's authoritative/provenance fields.
- The assembler/evaluator later checks Murphy `status == PASS`, but that is not equivalent to source authority or provenance validation.
- The evaluator treats Nison contradiction as a rejection, but absent/unconfirmed Nison is not itself rejected by the inspected logic; strength falls back to medium unless confirmation is `CONFIRMED`.

This bridge is callable directly, so relying exclusively on one upstream Gate 3C caller is not a sufficient public contract. Recommended next remediation: inspect all direct bridge callers and the existing evidence schemas, then add fail-closed negative tests for non-authoritative Murphy and malformed/absent Nison according to the approved Nison contract. Do not invent new confirmation semantics.

## Existing architectural issue remains
The bridge dynamically imports `OOS_2025/full_decision_brain_assembler_v1.py`; that assembler imports `OOS_2025.execution_oos_compatibility_v1`. This is a namespace/lifecycle coupling, not proof that OOS data was read. Do not move OOS datasets or tune against them. Relocation requires a compatibility audit and import-path regression tests.

## Verification state
- Review branch compare: 3 commits ahead, 0 behind the development base.
- Exactly 3 files changed in the branch at the time of this audit (2 code/test files plus the first audit report).
- Similarity regression test is present but has NOT been executed.
- No PR exists for this branch; no CI run was observed for the remediation commit.
- No changes made in this audit to application code, strategy, Risk, TIZ, Murphy, Nison, Similarity semantics, or OOS assets.

## Next safe sequence
1. Enumerate direct bridge callers using branch-aware repository tree/source inspection (not default-branch-only code search).
2. Inspect their upstream Murphy/Nison evidence schemas and tests.
3. Add focused negative tests and a fail-closed bridge contract only after the approved authority requirements are explicit.
4. Run the Similarity regression plus bridge tests in an isolated CI path that cannot invoke legacy Dropbox workflows. If that cannot be guaranteed, keep tests marked not run.
5. Resolve Murphy-vs-MTF direction authority formally before changing the frozen Brain.
