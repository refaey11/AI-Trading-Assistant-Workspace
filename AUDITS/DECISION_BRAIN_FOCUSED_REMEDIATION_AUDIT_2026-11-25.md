# Decision Brain Focused Remediation Audit — 2026-11-25

## Scope and safety
- Repository: `refaey11/AI-Trading-Assistant-Workspace`
- Base: `current-stack-dev-backtest-2016-2024-v3` at `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`
- Work branch: `fix/similarity-direction-isolation-2026-11-25`
- Audit/fix only. No main changes, no merges, no Dropbox access, no 2025/2026 market-data payloads.
- Commits use `[skip ci]` because repository workflows include unrelated legacy workflows and some Gate 3C workflows explicitly access Dropbox.

## Confirmed defect fixed in this branch: Similarity can influence direction in a compatibility path
Before:
- `compatibility/run_knowledge_decision_brain.py` called `assess(row, handoff["similarity"])`.
- `decision_brain.assess` explicitly turns `similarity.predicted_return` into bullish/bearish directional evidence and includes it in the directional/confidence aggregation.
- Therefore this caller violated the project invariant that Similarity is historical evidence only and cannot create or influence direction.

Change:
- The adapter now calls `assess(row, similarity=None)`.
- Similarity remains preserved in the handoff's evidence bundle for traceability; it is not passed into the directional engine.
- The frozen Decision Brain implementation itself was not modified.

Regression test:
- Extended `tests/test_knowledge_decision_brain_runtime.py` with an aligned, direction-neutral market row.
- Compares no memory, strongly bullish memory, and strongly bearish memory.
- Asserts direction and confidence remain identical while the memory payload remains retained in the evidence bundle.

Commits:
- Adapter fix: `d646a02e7448074d1aa2c9c3ac0a15f776755580`
- Regression test: `37ee03705e4a6f857ec9ebaabeaccba65fafa104`

Verification:
- Both modified files were fetched back from GitHub and their content verified.
- GitHub compare against the base branch reports exactly 2 commits ahead, 0 behind, and exactly 2 modified files.
- Tests have NOT been executed. The commits intentionally used `[skip ci]`; no successful test run is claimed.

## Additional confirmed integration risks — not changed

### 1. Canonical development bridge imports modules from OOS_2025
`RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py` dynamically imports:
- `OOS_2025/full_decision_brain_assembler_v1.py`
- the assembler imports `OOS_2025/execution_oos_compatibility_v1.py`.

This is an architectural namespace/lifecycle leak: a development runtime bridge depends on modules stored under the locked OOS namespace. It does not prove OOS data was read, but it makes the boundary difficult to govern. Recommended remediation is a compatibility-audited relocation of neutral orchestration/execution-contract code to a neutral package, preserving byte-for-byte behavior first and testing both old and new import paths. Do not move or alter OOS datasets or tuning artifacts.

### 2. Candidate 2R execution profile is still present in the assembler path
`OOS_2025/execution_oos_adapter_v1.py` hardcodes `SL_ATR = 0.75` and `TP_R = 2.0`. The full assembler test fixture supplies a risk result with `rr = 2.0` and expects an `EXECUTABLE` evaluation plan. This appears to be the frozen candidate/evaluation profile, not the canonical 3R Risk Engine contract. Keep it isolated and explicitly label it evaluation-only; never let this adapter replace canonical Risk Engine SL/TP or authorize canonical production eligibility.

### 3. Runtime bridge authority checks are asymmetric
`full_brain_runtime_bridge_v1.py` checks `authoritative` only for Risk. It checks that Murphy/Nison mappings are present, but does not itself require their `authoritative` flags. Gate 3C's current caller validates Murphy and Nison upstream, but the bridge can be called independently. Recommended: make the bridge's own public contract fail closed for required evidence authority/provenance, or make it private and callable only through the validated event runner. Add direct negative tests for non-authoritative Murphy/Nison.

### 4. Recovered Decision Brain computes direction from MTF row fields
`RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py` derives directional bias from `mtf_trend_score`, trend-regime averages, and volume fields. The three-book evaluator later compares this bias with Murphy direction. This means there are two direction-bearing inputs, not a pure Murphy direction followed by Nison confirmation. Needs a formal contract decision: either prove these row fields are the approved Murphy-derived market-structure context, with lineage and provenance, or refactor the orchestration so Murphy remains the sole directional authority. Do not change frozen Brain semantics until this is decided.

### 5. TIZ remains intentionally metadata-only under the checked-in 2026-11-12 decision
The runtime TIZ gate implementation exists but is not part of current execution eligibility. This is consistent with the current repository decision and inconsistent with the older Master Map expectation. No code changed. Reinstatement requires a superseding decision plus approved producer/evidence semantics for the deferred rules.

### 6. Canonical Risk hardening remains tied to PR #119
The development branch's canonical risk engine uses 3R but the PR #119 hardening is still a separate review item. The PR's observed tests passed previously, but its MTF source workflow failed at archive download. Do not treat the failed MTF workflow as validation of data provenance. Preserve the 3R canonical / 2R candidate distinction.

## Recommended next order
1. Run the new Similarity regression test in a trusted isolated CI run.
2. Audit every caller of `decision_brain.assess` to ensure Similarity is never passed as a directional argument.
3. Close the runtime bridge's direct authority/provenance gap with tests.
4. Separate neutral runtime orchestration from `OOS_2025` namespace after compatibility review.
5. Explicitly segregate 2R candidate execution from canonical 3R risk eligibility.
6. Resolve the directional-authority contract between Murphy and the recovered MTF row-based Brain.
7. Resolve TIZ authority only through a superseding architecture decision.

## Explicit non-actions
- `main` untouched.
- No PR merged or opened from this branch.
- No OOS 2025/2026 market data accessed.
- No Dropbox or Dropbox workflow used.
- No strategy thresholds or production runtime behavior beyond the isolated Similarity adapter call changed.
- No live trading or automatic order execution enabled.
