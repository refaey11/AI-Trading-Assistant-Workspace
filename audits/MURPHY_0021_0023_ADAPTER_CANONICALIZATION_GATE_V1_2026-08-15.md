# Murphy 0021–0023 — Adapter Canonicalization Gate V1

Date: 2026-08-15
Status: BLOCKED — SOURCE IMPLEMENTATION NOT VERIFIED IN CANONICAL GITHUB MAIN

## What was verified
1. The canonical clean historical artifact exists and is approved:
   - 122,934 rows
   - 2020–2024 only
   - 2025 rows = 0
2. PR #4 contains a lossless evaluator-result boundary for Murphy 0021–0023.
3. PR #4 is validation-only and is not merged.
4. The project adapter contract file available in the workspace is `rule_adapter_contract_v1.json` and is explicitly marked `DESIGN_ONLY`.

## Critical finding
A production `rule_adapter.py` / `NormalizedEvidence` implementation could not be verified in the canonical GitHub `main` branch at the expected path, and repository search did not return a canonical implementation.

Therefore this gate MUST NOT copy, recreate, or invent a Rule Adapter implementation merely to unblock 0021–0023.

## Required canonicalization procedure
A real adapter implementation must first be recovered from the authoritative project workspace/source package and reconciled against `rule_adapter_contract_v1.json`.

Required checks:
- exact source artifact identity and provenance;
- implementation ↔ contract field compatibility;
- no duplicated registry rules;
- no decision-making inside adapter;
- correct gate/conflict/decision_hint/confidence_delta semantics;
- 2025 remains excluded from tuning/selection;
- no new thresholds, timeframes, lookbacks, OI proxies, or inferred strength/confidence.

Only after this audit passes may the implementation be committed to canonical GitHub and used for 0021–0023 integration.

## Current status
Historical gate: PASS.
Evaluator: PASS.
Lossless boundary: PASS.
Canonical adapter implementation: NOT VERIFIED.
Evaluator→canonical adapter integration: BLOCKED.
Production Freeze: NOT GRANTED.

## Correction to prior project notes
The project must not treat an unverified Workspace claim that `024/rule_adapter.py` exists as proof of a canonical implementation. The current evidence available to this audit does not establish that file in GitHub `main`.
