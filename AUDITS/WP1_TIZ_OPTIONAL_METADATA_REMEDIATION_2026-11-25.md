# WP1 — TIZ Optional Metadata Remediation Record — 2026-11-25

## Status
Implemented on an isolated remediation branch; static verification completed; automated tests NOT RUN. This is not an integration-ready PR and does not authorize merge or live execution.

## Branch and ancestry
- Branch: `fix/pr120-tiz-optional-metadata-wp1-2026-11-25`
- Base: PR #120 head `d1df29b0d3526378402e47959a55a73b13bd1889`
- The branch is intentionally based on PR #120 to isolate the TIZ behavior change. It is NOT based on the latest PR #119 head and is NOT the final integration branch.
- No retarget, rebase, merge, cherry-pick, PR creation, or main change.

## Runtime changes
File: `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py`
- Removed the `evaluate_tiz_gate` import and invocation.
- Removed TIZ from the mandatory evidence-envelope validation loop.
- Missing TIZ is recorded as `NOT_EVALUABLE_METADATA_ONLY`.
- A non-mapping TIZ payload is recorded as `UNPARSEABLE_METADATA_ONLY`.
- A supplied mapping is preserved as metadata and explicitly labeled `OPTIONAL_AUDIT_METADATA_ONLY`.
- TIZ metadata is passed to the existing Three-Book evaluator with `decision_authority=False`; the evaluator already documents TIZ as optional audit metadata only.
- Removed all runtime checks that required TIZ `READY` or returned a TIZ process-gate block.
- TIZ metadata is retained in the runtime response.

## Test changes
File: `RUNTIME/DECISION_RUNTIME_V1/test_live_decision_runtime_v1.py`
Replaced the old test that expected TIZ failure to block with four tests:
1. Missing TIZ does not change status, decision, Brain confidence, or Risk result.
2. Failed TIZ process flags do not change status, decision, Brain confidence, or Risk result.
3. Malformed TIZ payload does not change authorization outcome.
4. TIZ cannot authorize a signal when canonical Risk rejects the 2R case.

## Static verification
- Fetched both changed files from the remediation branch after writes.
- Confirmed the runtime no longer contains `evaluate_tiz_gate`, `tiz_result`, or `TIZ_PROCESS_GATE`.
- Confirmed all four new test names are present and the old blocking test is absent.
- Compared branch against its PR #120 base: exactly two files changed (runtime and its tests); 3 commits ahead, 0 behind.
- The connected commit-workflow lookup returned no pull-request-triggered workflow runs for the latest commit. This is not a test pass.

## Not yet verified
- No Python test suite was executed in this session.
- No GitHub Actions run was dispatched or observed for this branch.
- Workflow triggers were not verified, so no PR was opened to trigger tests.
- No compatibility test against PR #119's latest head was performed.
- No whole-repository caller-path audit was repeated after this isolated change.

## Safety and remaining work
- PR #119 and PR #120 remain draft/open/unmerged.
- This isolated patch must be reconciled onto a new integration branch based on the explicitly approved latest PR #119 head after its current SHA is re-verified.
- Before integration, inspect the live-runtime workflow path/trigger and run the focused tests on the exact combined head.
- Murphy-exclusive direction, no-trade-reason enforcement, source authentication, event freshness, MTF/volume lineage, and canonical 3R boundary remain separate work packages.
- 2025 remains locked OOS. No market-data payloads were read. No Dropbox or CircleCI was used.
- Runtime output remains SIGNAL_ONLY; orders_enabled remains false; no MT5/broker order path was enabled.
