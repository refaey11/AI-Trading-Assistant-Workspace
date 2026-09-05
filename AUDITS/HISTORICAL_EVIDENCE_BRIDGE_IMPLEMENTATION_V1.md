# Historical Evidence Bridge Implementation V1

## Status
SHADOW-ONLY CONTRACT — no direction or risk semantics changed.

## Purpose
Attach existing Historical Context Memory, Historical Outcome Memory, Similarity Memory, Context-Aware Retrieval, and explicit MTF evidence to the existing Decision Event without rebuilding subsystems.

## Required invariants
- Murphy remains the primary technical context.
- Nison confirms or contradicts; it cannot create direction.
- Memory can support or weaken evidence only; it cannot generate BUY/SELL.
- Memory cannot override Risk.
- `shadow_only=true` until runtime parity tests pass.
- Memory timestamps must be <= decision timestamp.
- Development validation uses 2016–2024 only.
- 2025 remains OOS-locked and cannot be used for tuning or threshold fitting.

## Envelope fields
- `historical_evidence.status`
- source availability for all four memory systems
- `candidate_count`, `matched_count`
- `lookahead_safe`
- timestamp coverage
- bounded support/confidence delta
- `can_generate_direction=false`
- `can_override_risk=false`
- `shadow_only=true`

## MTF fields
- higher timeframe: H4
- execution timeframe: H1
- alignment: aligned/mixed/opposed/unknown
- lookahead safety
- shadow-only flag

## Acceptance tests
1. Schema validation.
2. Source availability audit.
3. Timestamp/lookahead audit.
4. Candidate-count audit.
5. Decision parity before/after shadow envelope.
6. No direction generation.
7. No risk override.
8. Funnel accounting: events -> executable -> execution -> final trades.

This file is an implementation contract and audit target; it does not claim runtime integration until the actual Decision Event producer passes these tests.