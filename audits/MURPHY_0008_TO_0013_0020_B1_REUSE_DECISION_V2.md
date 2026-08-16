# Murphy PF-B1 — 0008 → 0013-0020 Reuse Decision V2

Status: COMPATIBILITY DECISION — NOT PRODUCTION FROZEN
Date: 2026-08-16

## Evidence reviewed
The File Library contains the 0008 handoff and PF-B1 Governance Proposal. Those artifacts explicitly state that PF-B1 is a shared Breakout Confirmation primitive intended for 0008/0009/0010 and future breakout consumers, with outputs including boundary_id, direction, breakout_timestamp, confirmation_timestamp, availability_timestamp, and status.

The same source material explicitly states that PF-B1 was still PROPOSAL / NOT PRODUCTION FROZEN and that no already-approved production-frozen decisive-break contract was found. Murphy's 3% example and two-day example were explicitly prohibited from being silently promoted to a project threshold.

## Reuse decision
REUSE the 0008 PF-B1 architecture/interface/governance boundary for 0013-0020.

DO NOT copy a numeric/operational breakout threshold from 0008 because the accessible 0008 source-era artifacts do not establish such an approved frozen policy. The latest canonical status saying 0008 is frozen is not sufficient evidence of the missing policy artifact, and the preserved source-era handoff records a status conflict.

## Result for 0013-0020
The shared PF-B1 interface is compatible as an architecture. The decisive-break operator remains NOT_EVALUABLE until a production policy is explicitly approved and provenance/freeze evidence exists.

This means no duplicate breakout engine is required.

## Required next gate
Use the shared PF-B1 interface for all eight rules. Resolve the policy once at the shared primitive level, then run one compatibility + no-lookahead + 2016-2024 QA pass across all applicable rules. 2025 remains OOS and must not be used for policy selection or tuning.

## Explicit non-goals
- No new breakout engine.
- No automatic 3% binding.
- No automatic two-day binding.
- No ATR/pip/arbitrary percentage/lookback/tolerance.
- No 2025 tuning.
- No claim that this audit itself production-freezes PF-B1.
