# AI Trading Assistant — Chat Handoff / Project Continuation Backup
**Date:** 2026-08-22
**Purpose:** Complete handoff for a new ChatGPT chat.

## Project and source of truth
- Project: AI Trading Assistant — Decision Brain, not a trading indicator.
- Murphy = technical context / market structure.
- Nison = candlestick confirmation / confluence only; never an independent direction generator.
- Trading in the Zone = psychology/process gate; never generates direction.
- Similarity Engine = historical evidence only; never sole decision maker.
- Decision Brain combines current evidence, book knowledge, historical memory, and risk.
- Do not rebuild existing project knowledge from scratch.
- Before any new integration, perform compatibility audit.
- 2025 is locked OOS and must never be used for tuning.
- Never invent source semantics or numeric thresholds; use fail-closed / NOT_EVALUABLE when evidence is insufficient.

## Nison canonical freeze
The canonical Nison state is **44 frozen source-contract entries**:
- 38 candlestick pattern scopes.
- 6 methodology/context entries: 039–044.
- 039–044 are not six extra candlestick patterns.

Important distinction:
- SOURCE CONTRACT FROZEN = source definition is frozen.
- RUNTIME/CI VERIFIED = implementation, tests, router, and CI are verified.
- PRODUCTION RUNTIME FROZEN = higher lifecycle state; do not infer it from CI alone.

## Execution agreement
We agreed to work in batches of 10 runtime rules.
- Batch 1: 0001–0010 ✅
- Batch 2: 0011–0020 ✅
- Batch 3: 0021–0030 ✅
- Remaining: 0031–0044 = 14 entries, agreed to process together as one Super-Batch.

## Completed runtime batches
### 0001–0010
- Runtime/evaluators implemented.
- Unit tests implemented and passing.
- Unified router implemented/verified.
- CircleCI passed.
- Regression stayed green after later batches.
- Status: **Runtime/CI Verified**.

Recorded Dropbox artifact:
`NISON_0001_0010_RUNTIME_CI_VERIFIED_2026-08-22.md`

### 0011–0020
- Runtime/evaluators implemented.
- Tests implemented and passing.
- Unified router extended.
- CircleCI passed.
- Regression 0001–0010 passed.
- Status: **Runtime/CI Verified**.

Implementation rule: qualitative phrases like “nearly equal” / “approximately equal” are represented as upstream categorical facts; no numeric tolerance was invented.

Recorded Dropbox artifact:
`NISON_0011_0020_RUNTIME_CI_VERIFIED_2026-08-22.md`

### 0021–0030
- Runtime/evaluators implemented.
- Tests implemented and passing.
- Unified router extended.
- CircleCI passed.
- Regression 0001–0010 passed.
- Regression 0011–0020 passed.
- Status: **Runtime/CI Verified**.

Rules 0021–0029 are fail-closed: they do not invent formation geometry. They require source-backed upstream formation facts; missing evidence -> `NOT_EVALUABLE`; missing required confirmation -> `FAIL`.

Rule 0030 uses source-backed structural facts: existing Uptrend, completed formation, final bullish strong candle fact, and required confirmation.

Known verified commit:
`484f1a138fb3b52a1513b243f713b3fc8b699b28`

Latest observed verified CircleCI run for this batch: **#35**.

## Current numerical state
**30 / 44 Runtime/CI Verified ✅**
- 0001–0010 ✅
- 0011–0020 ✅
- 0021–0030 ✅

**14 remaining / not yet Runtime-verified:**
- 0031–0038
- 0039–0044

Do NOT say 44/44 Runtime Verified. That has not been established.

## Last discussion / exact next step
User asked to finish the last 14 together. We agreed to process **0031–0044 as one Super-Batch**.

Earlier discussion/attempts around the final 14 did not result in a successful verified CI result. Treat 0031–0044 as pending until fresh implementation + CI evidence proves otherwise.

### Next exact workflow
1. Audit canonical contracts for 0031–0044.
2. Inspect existing runtime/source artifacts first.
3. Do not rewrite frozen source contracts.
4. Implement runtime only where deterministic evidence is supported.
5. For qualitative relationships, use source-backed categorical facts; do not invent numeric tolerances.
6. Add positive, negative, missing-confirmation, and fail-closed tests.
7. Extend unified router through 0044 with correct dispatch.
8. Add CircleCI coverage for the Super-Batch.
9. Run regression for all already-verified batches 0001–0030.
10. After CI, assign each remaining entry precisely: `Runtime/CI Verified`, `NOT_EVALUABLE`, or `BLOCKED`.

### Special handling for 0039–0044
Treat these as methodology/context contracts, not candlestick-pattern evaluators. Use their own source contracts and do not force them into the same evaluator model as 0001–0038.

## Governance rules to preserve
- Nison remains confirmation/context evidence only.
- 2025 remains locked OOS.
- Do not invent numeric thresholds or undocumented geometry.
- Do not rebuild old project knowledge from scratch.
- Keep provenance and fail-closed behavior.
- Regression-test earlier verified batches whenever new batches are added.
- Record every verified checkpoint in GitHub and Dropbox.

## Repository / backup locations
GitHub:
`https://github.com/refaey11/AI-Trading-Assistant-Workspace`

Dropbox backup root:
`/AI_Trading_Assistant_BACKUP_2026-08-22/`

## One-paragraph handoff
We are building the AI Trading Assistant Decision Brain. Nison source contracts are already frozen: 38 candlestick pattern scopes plus 6 methodology/context entries (039–044), with 2025 locked OOS. We agreed to implement Nison runtime in batches. Batches 0001–0010, 0011–0020, and 0021–0030 are complete and passed runtime tests, router smoke tests, CircleCI, and regression checks, so **30/44 are Runtime/CI Verified**. Nison remains confirmation/context evidence only; no invented numeric thresholds; insufficient deterministic evidence must produce `NOT_EVALUABLE` rather than fabricated geometry. The remaining work is exactly **0031–0044 (14 entries)**, agreed to be handled as one Super-Batch. Start by auditing canonical contracts, then implement runtime/tests/router/CI and finish with full regression for the first 30.
