# Murphy 0008 — PF-H1 Singleton Pivot Boundary Proposal V1

Status: GOVERNANCE PROPOSAL — NOT PRODUCTION FROZEN

## Question
Can 0008 establish its Support boundary from one confirmed Pivot LOW without inventing horizontal-level clustering?

## Source-backed finding
Murphy describes Support as a price level/area identified from prior reaction lows. The project already has canonical PIVOT_SEQUENCE_V2 producing confirmed pivot-derived candidates with availability metadata. Therefore a single confirmed Pivot LOW can be represented as a candidate Support boundary without requiring a separate nearby-level clustering operation, provided the project's Support identity is explicitly established for that candidate.

## Important limitation
This does NOT prove that every Pivot LOW is automatically an "important" Support level, and it does NOT create a generic horizontal equality rule. It only provides a candidate boundary for 0008. Any requirement that multiple pivots be merged into one horizontal zone remains NOT_EVALUABLE until a separate approved equality/cluster contract exists.

## Proposed 0008 consumption path
1. PIVOT_SEQUENCE_V2 emits a confirmed LOW candidate.
2. Candidate is assigned SUPPORT role only where the existing rule/source mapping establishes Support identity.
3. PF-H1 exposes that singleton level with level_id, level_price, role, and availability_timestamp.
4. PF-B1 consumes that exact boundary; no clustering or tolerance is required for the boundary itself.
5. Decisive-break confirmation is handled only by the separately approved PF-B1 policy.
6. Later rally/retest is evaluated against the same boundary identity; no nearby-level substitution is permitted.

## What this proposal does NOT do
- No ATR/pip/percentage tolerance.
- No clustering of nearby pivot prices.
- No invented horizontal zone width.
- No assertion that Pivot LOW equals Important Support.
- No backtest-based boundary selection.
- No 2025 tuning.

## Decision gate
If Governance accepts singleton pivot-derived Support as sufficient boundary identity for 0008, PF-H1 can be used for 0008 without solving a generic horizontal-level clustering problem. If Governance requires a multi-touch/cluster definition of horizontal Support, the 0008 boundary step remains NOT_EVALUABLE until that contract is approved.

## Current recommendation
For 0008, prefer the minimal singleton-boundary path because the rule semantics require a Support level, not a generic multi-level clustering engine. Preserve all candidate provenance and availability metadata. Do not generalize this exception automatically to other rules such as rectangles/triangles that explicitly require horizontal ranges or multiple boundaries.
