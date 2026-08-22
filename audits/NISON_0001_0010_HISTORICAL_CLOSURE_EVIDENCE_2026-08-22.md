# Nison 0001–0010 Historical Closure Evidence — 2026-08-22

## Basis
Canonical Nison lifecycle/QA artifacts from the uploaded 2026-08-18 full canonical backup, reconciled against the current GitHub runtime.

## Rule-level evidence
- 0001 Bullish Engulfing: 206 lifecycle rows; 115 confirmed, 91 unconfirmed. All confirmations strictly later than formation; 0 2025 rows. Dedicated no-lookahead QA PASS: 206 candidate events, 148 confirmed, 206 next-bar available.
- 0002 Bearish Engulfing: 197 lifecycle rows; 103 confirmed, 94 unconfirmed. All confirmations strictly later than formation; 0 2025 rows. Dedicated no-lookahead QA PASS: 197 candidate events, 141 confirmed, 197 next-bar available.
- 0003 Dark Cloud Cover: source-locked QA PASS; 15/15 source-core pass; development 2016–2024; 2025 unused. Dedicated no-lookahead QA PASS: 15 candidates, 8 confirmed, 15 next-bar available.
- 0004 Piercing Pattern: source-locked QA PASS; 12/12 source-core pass; development 2016–2024; 2025 unused. Dedicated no-lookahead QA PASS: 12 candidates, 10 confirmed, 12 next-bar available.
- 0005 On Neck: event-driven confirmation QA PASS; 9 formations, 8 confirmed, 1 unconfirmed; strictly later confirmation = True; 2025 unused; development 2016–2024.
- 0006 In Neck: event-driven confirmation QA PASS; 23 formations, 22 confirmed, 1 unconfirmed; strictly later confirmation = True; 2025 confirmation rows = 0; development period clean.
- 0007 Thrusting: event-driven confirmation QA PASS; 88 formations, 86 confirmed, 2 unconfirmed; strictly later confirmation = True; 2025 confirmation rows = 0; development period clean.
- 0008 Morning Star: dedicated data-integrity QA PASS (21 events, 0 duplicate timestamps, 0 missing formation timestamps, 0 2025 rows) and dedicated no-lookahead QA PASS (21 confirmed, causal context PASS, source timestamp PASS, 0 duplicate formation timestamps, 0 2025 rows).
- 0009 Evening Star: dedicated data-integrity QA PASS (20 events, 0 duplicate timestamps, 0 missing formation timestamps, 0 2025 rows) and dedicated no-lookahead QA PASS (20 confirmed, causal context PASS, source timestamp PASS, 0 duplicate formation timestamps, 0 2025 rows).
- 0010 Morning Doji Star: freeze QA PASS; 9 formations, 5 confirmed, 4 unconfirmed; strictly later = True; 2025 unused; development 2016–2024.

## Governance state
These artifacts establish substantial historical/no-lookahead evidence for all 0001–0010, but the canonical closure matrix still records the rules as NOT_FROZEN with final QA/manifest open. This report therefore records evidence closure progress, not a production freeze.

## Remaining closure action
Reconcile these artifacts against the exact current runtime/adapter contract and produce a freeze manifest only if every required gate is explicitly closed. Do not rebuild existing Nison components.

## Protected boundaries
- 2016–2024 is the development/QA period.
- 2025 remains locked OOS and was not used.
- Nison remains confirmation/context evidence only and cannot independently create direction.
- No invented thresholds or proxy operators were introduced.