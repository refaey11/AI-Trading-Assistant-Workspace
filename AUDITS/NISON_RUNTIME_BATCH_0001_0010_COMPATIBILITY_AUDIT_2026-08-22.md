# Nison Runtime Batch 0001-0010 — Compatibility Audit

Date: 2026-08-22
Scope: runtime/evaluator/router/test compatibility against the integrated Nison registry and decision contract.

## Executive status

CircleCI status: PASS for the configured runtime pipeline.
This is a CI execution result, not automatic proof that every rule is source-faithful and fully verified.

## Rule-by-rule

| Rule | Pattern | Runtime | CI | Compatibility | Verification status |
|---|---|---:|---:|---|---|
| 0001 | Bullish Engulfing | yes | PASS | aligns with registry: Downtrend, 2 candles, bearish->bullish, real-body engulfing, confirmation gate | RUNTIME VERIFIED (CI) / source QA acceptable |
| 0002 | Bearish Engulfing | yes | PASS | aligns with registry: Uptrend, 2 candles, bullish->bearish, real-body engulfing, confirmation gate | RUNTIME VERIFIED (CI) / source QA acceptable |
| 0003 | Dark Cloud Cover | yes | PASS | formation logic present, but runtime does not enforce required confirmation | BLOCKED pending confirmation gate |
| 0004 | Piercing Pattern | yes | PASS | formation logic present, but runtime does not enforce required confirmation | BLOCKED pending confirmation gate |
| 0005 | On Neck | yes | PASS | categorical close relation is represented, but required confirmation is not enforced | BLOCKED pending confirmation gate |
| 0006 | In Neck | yes | PASS | categorical close relation is represented, but required confirmation is not enforced | BLOCKED pending confirmation gate |
| 0007 | Thrusting | yes | PASS | categorical close relation is represented, but required confirmation is not enforced | BLOCKED pending confirmation gate |
| 0008 | Morning Star | yes | PASS | 3-candle formation represented, but required confirmation is not enforced | BLOCKED pending confirmation gate |
| 0009 | Evening Star | yes | PASS | 3-candle formation represented, but required confirmation is not enforced | BLOCKED pending confirmation gate |
| 0010 | Morning Doji Star | yes | PASS | 3-candle formation represented, but required confirmation is not enforced | BLOCKED pending confirmation gate |

## Test coverage finding

`test_nison_0003_0010_runtime.py` covers positive cases and wrong-trend rejection, but does not cover missing-confirmation rejection. Therefore a CI PASS cannot establish the source contract `confirmation_required=true` for rules 0003-0010.

## Source contract finding

The integrated registry marks all ten rules with `integration_role: confirmation`. The three-book decision contract states Nison can provide confirmation and no-trade conditions include `Pattern not confirmed`. The runtime review therefore must not treat an unconfirmed candle pattern as an independently executable direction signal.

## 2025 / tuning

No tuning or threshold selection was performed by this audit. The audit is structural/compatibility review only.

## Decision

Do NOT mark the whole batch 0001-0010 as fully frozen/production-verified.

Current accurate state:
- 0001-0002: runtime + CI verified, subject to normal integration QA.
- 0003-0010: runtime implemented + CI tested, but blocked from final verification until confirmation gating is implemented and tested.

## Next corrective action

Add explicit confirmation inputs/gates to rules 0003-0010 using only confirmation semantics already present in the source contract. Add negative tests for absent confirmation. Re-run CircleCI. Then re-audit before changing the verification status.
