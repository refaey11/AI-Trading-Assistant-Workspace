# Murphy PF-B1 / PF-H1 Contract Candidate V1

## Scope
Shared primitives for Murphy rules 0013–0015, 0018–0020.

## PF-B1 — Breakout Confirmation

**Candidate semantics:**
1. Consume an already approved boundary/level from the existing project geometry/SR layer.
2. A breakout event occurs only on a completed-bar close beyond that approved boundary.
3. Emit boundary identifier, direction, breakout timestamp, and availability timestamp.
4. Intrabar penetration that closes back inside does not constitute a breakout.
5. Missing/unapproved boundary returns `NOT_EVALUABLE`.
6. Availability earlier than the completed-bar close is rejected as look-ahead.

**Explicitly prohibited:** importing external ATR, percentage, pip, volume, or multi-day thresholds.

## PF-H1 — Horizontal Level

**Candidate semantics:**
1. Consume confirmed pivot-derived level candidates from the existing project layer.
2. Consume the existing support/resistance role identity.
3. Return `HORIZONTAL_AVAILABLE` only when an authoritative existing producer explicitly labels the level horizontal.
4. If horizontal classification is unavailable, return `NOT_EVALUABLE`.
5. Do not infer horizontal status using an external percentage, ATR, pip, or clustering tolerance.

## Governance status
These are **candidate contracts**, not Production-Frozen contracts. They are intended to replace the ambiguous proposal layer only after explicit project governance approval.

## Required gates after approval
- deterministic tests
- 2016–2024 historical QA
- availability/no-lookahead audit
- provenance/freeze manifest
- explicit Production Freeze approval

2025 is OOS and must not be used for tuning or selection.
