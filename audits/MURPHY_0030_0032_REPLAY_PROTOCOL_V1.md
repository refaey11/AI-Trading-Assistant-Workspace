# Murphy 0030–0032 — Final Replay Protocol V1

## Purpose
Define the exact replay required after Policy Decision V1. This is a protocol, not a result.

## Data
- Instrument: GBPUSD
- Timeframe: D1
- Full state-build range: 2016-01-01 through 2024-12-31
- Evaluation range: 2019-01-01 through 2024-12-31
- 2025 excluded from tuning and selection.

## State rule
Build one deterministic P&F state from the full 2016–2024 chronological sequence. Do not reset at 2019.

## Per-bar evaluation
For each completed D1 bar in 2019–2024, emit the 0030–0032 evidence available immediately after that bar. Never use a later bar to alter an earlier emitted record.

## Rule boundaries
- 0030: structural support reference only; no entry trigger.
- 0031: long-stop risk reference only.
- 0032: short-stop risk reference only.

## Bootstrap
Use the explicit project High/Low bootstrap. Same-bar simultaneous qualification is `AMBIGUOUS` and must not select a direction.

## Required audit outputs
1. P&F column count and X/O counts.
2. First/last column timestamps.
3. 0030/0031/0032 availability counts.
4. Prefix replay invariance checks at multiple historical checkpoints.
5. No-lookahead mutation test: append arbitrary future suffix and verify all prior emitted evidence is unchanged.
6. Structural sensitivity across the pre-declared box-policy alternatives, without selecting the alternative based on 2019–2024 performance.

## Acceptance
A replay result is not a PASS merely because code executes. The full historical and governance gates must be evidenced.
