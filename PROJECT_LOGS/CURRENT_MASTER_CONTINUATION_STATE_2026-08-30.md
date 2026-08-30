# AI Trading Assistant — Current Master Continuation State
Date: 2026-08-30

## Purpose
Single source for continuing the project without losing state or reopening already-settled architecture.

## Current objective
Finish Gate 3C, then run the governed 2016–2024 Profit Test, then freeze the corrected integration path and proceed toward demo. 2025 remains OOS and locked for tuning/calibration.

## Frozen architecture / roles
- Murphy 34: technical context / market structure / directional context.
- Nison 44: confirmation or contradiction only; never an independent direction generator.
- Trading in the Zone (TIZ): process/psychology layer only; not an execution blocker in the current evaluator; it does not generate direction.
- Historical Context Memory + Historical Outcome Memory + Similarity + Context-Aware Retrieval: historical evidence/context only; never the sole decision maker and never a direction generator.
- Decision Brain V1: existing recovered runtime; do not rebuild or replace.
- Risk/Execution: hard gate; use authoritative existing inputs/contracts; do not hardcode PASS.
- 2025: OOS/evaluation-only; no tuning or calibration.

## Work sequence — do not deviate
1. Freeze/verify one baseline snapshot.
2. Run a final Gate 3C dependency audit before expensive execution.
3. Resolve only concrete integration blockers, without changing settled rule semantics.
4. Build one canonical single-event E2E test using real source-backed evidence.
5. Prove: MTF → Murphy 34 → Nison 44 → Memory/Retrieval → Handoff → Decision Brain V1 → TIZ status → Risk → Execution.
6. Only after the single-event proof passes, run the governed 2016–2024 Profit Test once.
7. Do not use 2025 for tuning.

## Known current issues / facts
- The latest CI failure visible during this phase stopped in MTF source normalization at `D1_trend_regime`; this is an integration/schema issue, not evidence that MTF itself is missing.
- The current Dynamic MTF adapter defines the allowed six timeframes: M5, M15, M30, H1, H4, D1.
- The current Three-Book evaluator treats TIZ as audit/process context and explicitly disables it as an execution gate.
- The current Risk integration preserves the canonical 3.0R minimum and only tolerates the exact floating-point boundary; materially sub-3R values still fail.
- A narrow PR exists for the `pandas` import required by MTF normalization; do not confuse that code fix with proof of Gate 3C completion.
- A narrow Risk/Execution reconciliation PR exists; do not treat it as a replacement Risk model.
- The canonical E2E plan says the CI runner is only an execution wrapper and that evidence compilation plus event-by-event decision/execution are the architecture.

## Anti-loop rules
- Do not reopen Murphy 34, Nison 44, TIZ semantics, MTF six-timeframe definition, Decision Brain V1, or 2025 governance unless direct evidence shows a regression.
- Do not launch another expensive/full CircleCI run while the small contract/single-event proof is unresolved.
- Do not fabricate missing evidence, zero-fill directional fields, or synthesize MTF values merely to make a test pass.
- Do not claim a blocker is "the last blocker" until the complete Gate 3C dependency chain has been audited.
- Every PASS must be backed by a specific test/artifact, not by assumption.

## Current status
- Gate 1: complete.
- Gate 2: complete.
- Gate 3B: complete.
- Gate 3C: in progress; the remaining work is integration proof, not rebuilding the system.
- Profit Test 2016–2024: not yet accepted; must wait for Gate 3C single-event proof.
- Demo: later, after the governed profit test and freeze.

## Resource protection
With limited CI credits remaining, prefer local/static/contract checks and single-event tests. Do not consume credits on speculative backtests.
