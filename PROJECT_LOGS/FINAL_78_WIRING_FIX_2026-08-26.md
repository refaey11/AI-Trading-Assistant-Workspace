# FINAL 78 Wiring Repair Checkpoint — 2026-08-26

- Previous governed 2025 run: 6225 events, 0 executable, 3534 MURPHY_CONTEXT_NOT_PASS, 2691 MURPHY_BRAIN_DIRECTION_CONFLICT.
- Root cause: downstream compatibility decision consumed a lossy legacy Murphy candidate while the full 34-rule evidence was preserved separately.
- Repair: full-rule path now derives the compatibility Murphy status/direction from the complete 34-rule evidence set.
- Conflict policy: bullish+bearish PASS remains explicit CONFLICT; no synthetic direction is created.
- Added regression tests covering full PASS vs legacy FAIL, conflicting directions, and all-fail behavior.
- No changes to rule thresholds, Nison role, TIZ role, risk formula, frozen P&L, or 2025 tuning.
- Current PR head after repair: 3c8145224795e50fcfc24309785c6ad4068c3ca1.
- Next gate: CircleCI must validate the new wiring and produce a new governed 2025 artifact set before profitability is judged.
