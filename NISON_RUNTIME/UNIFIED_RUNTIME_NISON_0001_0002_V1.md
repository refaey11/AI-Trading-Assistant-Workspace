# Nison Unified Runtime — 0001/0002

Date: 2026-08-22

Scope:
- CANDLE_RULE_0001 — Bullish Engulfing
- CANDLE_RULE_0002 — Bearish Engulfing

Implementation state:
- Source contract: FROZEN (canonical Nison freeze)
- Evaluator: IMPLEMENTED
- Deterministic tests: PASS (6/6 in prior promotion smoke)
- Unified runtime routing: VERIFIED at adapter/dispatch level
- Full GitHub Actions CI run: NOT CLAIMED (manual dispatch unavailable through connector)

Fail-closed behavior:
- Missing or invalid candle inputs produce NOT_EVALUABLE rather than an inferred signal.
- Nison remains confirmation/evidence only and does not independently generate a final trade direction.
- No invented numeric thresholds were added.

Promotion decision:
- 0001/0002 are Runtime-Ready for unified Decision Brain integration, subject to repository CI execution when available.
