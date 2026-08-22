# Decision Brain 2025 OOS Lock V1

Date: 2026-08-22

## Purpose

Establish the explicit OOS boundary for the frozen Decision Brain before any 2025 performance evaluation.

## Locked boundary

- OOS year: 2025
- Development years: pre-2025 only
- 2025 tuning: forbidden
- 2025 calibration: forbidden
- 2025 threshold selection: forbidden
- Future data: forbidden
- Similarity Memory: historical evidence only; never a direction generator
- Historical Memory: evidence only
- Trading in the Zone: process/psychology gate only; never direction
- Risk: hard gate and not overridable
- V1 automatic execution: disabled
- Legacy/alternate backtests: cannot be attributed to the frozen Decision Brain

## Rule boundary

The active Decision Brain Rule Adapter allowlist is the separately frozen 78-rule runtime allowlist: 34 Murphy + 44 Nison. Rules outside that allowlist are deny-by-default and must be rejected. MURPHY_0008 is explicitly blocked as NOT_EVALUABLE.

## Source-of-truth note

The canonical 102-rule inventory distinguishes 79 closed/frozen rules from 23 open/deferred rules, while the current runtime-verified allowlist is 78 because MURPHY_0008 is not runtime-verified. These are different counts with different meanings and are not to be conflated.

## Status

PENDING_CI_OOS_LOCK_PASS

The OOS performance run must not start until the dedicated CI lock job passes.
