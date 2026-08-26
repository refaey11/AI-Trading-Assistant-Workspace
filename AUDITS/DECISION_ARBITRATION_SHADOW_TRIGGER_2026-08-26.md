# Direction Arbitration Shadow Trigger

Date: 2026-08-26
Branch: `recovery/direction-arbitration-shadow-v1`

Purpose: trigger the existing read-only Direction Arbitration Shadow Audit after the 78-rule wiring recovery.

This checkpoint does not change Murphy, Nison, TIZ, Memory, Risk, Decision Brain, or execution semantics. It is only a CI trigger/audit marker.

Required outcome:
- quantify Brain directional coverage;
- quantify Murphy directional coverage;
- measure AGREE vs CONFLICT vs NO_DIRECTION;
- produce the shadow artifact before any production arbitration semantics are changed.

2025 remains OOS/evaluation-only and must not be used for tuning.
