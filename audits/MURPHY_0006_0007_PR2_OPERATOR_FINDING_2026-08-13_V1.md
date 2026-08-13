# Murphy 0006–0007 PR #2 Operator Discovery V1
Date: 2026-08-13

## New finding
PR #2 (`Murphy 0006-0007 source contract and generic evaluator`) contains an existing source-contract primitive for the Confirmation Layer. It is a DRAFT PR and must not be treated as production/frozen.

## What the PR contract actually defines
`audits/MURPHY_0006_0007_TRENDLINE_SOURCE_CONTRACT_V1.md` defines the evaluator-side semantic gate:
1. UP/DOWN trendline evidence;
2. two valid anchors;
3. third test/touch exists;
4. third test is successful and price bounces away in the original trend direction;
5. confirmation/availability timestamp is when the successful third test + bounce is known from completed data.
Missing required upstream evidence => NOT_EVALUABLE.
No touch tolerance, ATR, percentage threshold, or lookback is invented.

## Critical distinction
This is an evaluator-side SOURCE CONTRACT / semantic interface, not proof that the existing Geometry V1 implementation emits all required upstream facts.

PR #2's changed-file list contains the source-contract/audit/test artifacts but no production `0006/0007` evaluator implementation file. Its own Geometry Compatibility Gate says the exact Geometry V1 row-level schema proving explicit `third_touch`, `successful_reaction`, `no_break`, and confirmation availability fields remains unproven.

Therefore the contract is useful and should be reused; it does NOT by itself close the operational gate.

## Important status correction
Earlier audits correctly identified the same boundary but did not surface PR #2 as the concrete existing semantic contract. This audit records it as an existing artifact to integrate/verify rather than inventing a new operator.

## Next action
1. Retrieve the canonical Geometry V1 contract/output schema from the assembled Workspace/archives.
2. Verify whether the required upstream facts can be represented exactly.
3. If yes, wire the existing PR2 contract to those facts, add/verify deterministic evaluator tests, and run 2016–2024.
4. If no, keep NOT_EVALUABLE and document the single missing upstream field/semantics.
5. Do not merge/freeze PR2 until geometry schema verification and full QA pass.
6. 2025 remains OOS.
