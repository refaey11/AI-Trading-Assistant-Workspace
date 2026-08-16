# Murphy 0013-0020 — PF-B1 Transfer Audit V1

Status: GOVERNANCE / TRANSFER AUDIT — NOT PRODUCTION FROZEN
Date: 2026-08-16

## Finding
An approved PF-B1 two-day operationalization exists for Murphy Rule 0008 in the project history. That approval is explicitly rule-specific and therefore cannot be silently transferred to Murphy 0013-0020.

## What can be reused
The PF-B1 architecture can be reused: policy injection, explicit confirmation state, raw-break versus decisive-confirmation separation, availability timestamps, and no-lookahead governance.

## What cannot be reused without approval
The specific two-day policy for 0008 cannot be treated as approved for 0013-0020 merely because it exists for 0008. These pattern rules have different source semantics and evidence contracts.

## Current decision
PF-B1 remains an open governance gate for 0013-0020. The Factory may record an observable boundary-cross event, but it must not label that event a Murphy decisive breakout unless a policy is approved for the relevant rules.

No 3%, 2-day, ATR, pip, arbitrary percentage, arbitrary lookback, or hidden tolerance is introduced by this audit.

## Consequence for 0013-0020
- 0013: G1 may establish exact convergence; decisive breakout remains gated.
- 0014: H1 may establish an exact horizontal boundary; decisive breakout remains gated.
- 0015: F1/G1 may provide prerequisites where contracts exist; breakout remains gated.
- 0016: F1/G1 prerequisites; breakout remains gated.
- 0017: F1/G1 prerequisites; breakout remains gated.
- 0018: G1 may establish exact convergence; breakout remains gated.
- 0019: G1 may establish exact convergence; breakout remains gated.
- 0020: H1/G1 may establish exact horizontal parallel boundaries; breakout remains gated.

2025 remains OOS and cannot be used to select or tune the missing breakout policy.
