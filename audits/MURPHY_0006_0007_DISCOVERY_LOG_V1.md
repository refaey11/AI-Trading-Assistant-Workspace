# MURPHY 0006/0007 — DISCOVERY LOG V1

Purpose: append-only record of material discoveries, corrections, decisions, and evidence so the project does not repeat investigations or rely on conversation memory.

## Entry 001 — D1 lineage verification
Date: 2026-08-14
Finding: The existing machine-readable fresh replay claim is supported. Calendar-date aggregation of `GBPUSD_M1_MASTER_2016_2026_V1.zip` reproduces `d1_ref.csv` exactly across 2,544 common 2016–2024 dates.
Evidence: `MURPHY_0006_0007_D1_LINEAGE_RECONCILIATION_V1.md`.
Result: D1/M1 lineage gate CLOSED/PASS for the available artifacts.

## Entry 002 — Invalid blocker corrected
Date: 2026-08-14
Finding: The earlier blocker compared Pivot V2 event price 1.43519 with D1 low 1.40792. This was a category error because a pivot event price is not the D1 bar low.
Evidence: superseded `MURPHY_0006_0007_CANONICAL_INPUT_REPLAY_BLOCKER_V1.md`.
Result: The blocker is explicitly marked SUPERSEDED.

## Entry 003 — Fresh replay evidence preserved
Date: 2026-08-14
Finding: `murphy_0006_0007_FRESH_REPLAY_2016_2024_V1.json` records `FRESH_REPLAY_PASS`, canonical Pivot V2 and Geometry V1 reuse, 2016–2024 scope, 2025 excluded, 0006=8, 0007=7, total=15, and no-lookahead/availability checks.
Result: Replay result is evidence, but production freeze remains blocked by governance/integration gates.

## Entry 004 — Freeze pack state
Date: 2026-08-14
Finding: `MURPHY_0006_0007_FINAL_FREEZE_REVIEW_PACK_V1.zip` states QA PASS but production freeze false; open gates are formal evaluator integration, governance approval, and explicit freeze manifest/decision.
Result: Do not declare Production Frozen yet.

## Entry 005 — Anti-regression rule
Date: 2026-08-14
Finding: Conversational claims are not sufficient evidence.
Decision: Every material discovery must be written to this log and/or a dedicated evidence artifact with inputs, hashes, method, result, and governance impact.

## Next required discovery
Determine whether the current operational no-break predicate can be formally approved as the project contract and confirm production-path evaluator integration without changing rule semantics.
