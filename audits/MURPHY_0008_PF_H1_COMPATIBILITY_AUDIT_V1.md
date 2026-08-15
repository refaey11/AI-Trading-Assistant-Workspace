# Murphy 0008 — PF-H1 Compatibility Audit V1

Status: GOVERNANCE / COMPATIBILITY AUDIT — NOT PRODUCTION FROZEN
Date: 2026-08-15

## Scope
Audit the existing horizontal Support/Resistance path for Murphy 0008. Reuse existing primitives; do not rebuild Pivot Sequence V2 or create a duplicate S/R engine.

## Source findings
Murphy Chapter 4 defines support as a price level/area identified from prior reaction troughs and resistance from prior reaction peaks. The uploaded source also describes role reversal after a decisive/significant break. The source does not provide a project-specific deterministic tolerance for deciding when nearby prices are one horizontal level.

The uploaded Chapter 4 trendline material contains explicit 3%/1% and 2-day filter examples in the trendline-filter context. The uploaded Chapter 5 Head-and-Shoulders material contains 1–3% / two-day confirmation examples for the neckline. These context-specific examples must not be silently promoted into a generic PF-H1 horizontal-level equality rule.

## Existing project evidence
- PIVOT_SEQUENCE_V2 is canonical and must be reused.
- PF-H1 is already specified as a shared proposal using confirmed pivot-derived candidates and availability metadata.
- The project explicitly prohibits inventing percentage, ATR, pip, or other horizontal tolerances.
- If no approved horizontal-level equality/cluster contract exists, PF-H1 returns NOT_EVALUABLE.

## Compatibility decision
**REUSE PIVOT_SEQUENCE_V2: COMPATIBLE.**

**REUSE an existing frozen horizontal-level equality/cluster operator: NOT FOUND.**

Therefore PF-H1 cannot be production-frozen for cases requiring level clustering/equality. It may expose confirmed pivot-derived candidate levels, but it must not claim two nearby prices are the same horizontal boundary without an approved deterministic contract.

## Required PF-H1 boundary
Inputs:
- confirmed pivot-derived candidates
- support/resistance role identity where already established
- availability metadata

Outputs:
- level_id
- level_price
- role = SUPPORT | RESISTANCE
- availability_timestamp
- status = AVAILABLE | NOT_EVALUABLE

For clustering/equality, missing approved contract => NOT_EVALUABLE.

## 0008 consequence
0008 can proceed only when its support boundary is deterministically identified. If support-level identity requires an unavailable horizontal clustering rule, 0008 must return NOT_EVALUABLE rather than manufacture a level.

## No-governance shortcuts
- No invented tolerance.
- No 3%/1% copied from trendline or H&S context.
- No ATR/pip threshold.
- No backtest-derived level clustering.
- No 2025 tuning.

## Next gate
Resolve PF-B1 policy governance and PF-H1 level-equality governance before implementing the 0008 evaluator. Production freeze requires deterministic tests, 2016–2024 QA, availability/no-lookahead audit, provenance, and explicit freeze approval.
