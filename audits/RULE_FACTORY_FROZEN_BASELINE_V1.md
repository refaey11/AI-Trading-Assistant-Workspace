# Rule Factory V1 — Frozen Baseline Reconciliation

Date: 2026-08-16
Branch: `pilot/frozen-regression-v1`
Status: BASELINE MAPPED / EXECUTION PENDING

## Purpose
Protect the 12 project-designated Murphy frozen rules from semantic or status changes when passed through Rule Factory V1.

## Frozen baseline
0003, 0004, 0006, 0007, 0008, 0021, 0022, 0023, 0025, 0026, 0028, 0029.

## Authoritative source principle
Workspace/project artifacts are the source of truth; GitHub is the development/provenance mirror. The continuity backup explicitly records these 12 as the current closed/frozen set and says not to reopen them without contradictory evidence or an approved semantic change.

## Baseline mapping recovered from Workspace artifacts

| Rule | Frozen status | Canonical semantics / evidence | Regression readiness |
|---|---|---|---|
| 0003 | PRODUCTION FROZEN | Higher successive reaction peaks AND troughs | READY — authoritative freeze backup recovered |
| 0004 | PRODUCTION FROZEN | Lower successive reaction peaks AND troughs | READY — authoritative freeze backup recovered |
| 0006 | EVALUATOR/EVIDENCE FROZEN | LOW reaction family → UP trendline → third successful touch/reaction without confirmed break → BULLISH | READY — freeze/evidence backup recovered |
| 0007 | EVALUATOR/EVIDENCE FROZEN | HIGH reaction family → DOWN trendline → third successful touch/reaction without confirmed break → BEARISH | READY — freeze/evidence backup recovered |
| 0008 | PRODUCTION FROZEN | Support → decisive downside break → rally/retest → resistance role reversal | BLOCKED FOR EXACT EXECUTION COMPARISON — preserved source-status conflict |
| 0021 | PRODUCTION FROZEN | Price UP + volume UP → bullish; Price DOWN + volume UP → bearish | READY — frozen package recovered |
| 0022 | PRODUCTION FROZEN | Price UP + volume UP + CME British Pound futures OI UP → bullish | READY — frozen package recovered |
| 0023 | PRODUCTION FROZEN | Price DOWN + volume UP + CME British Pound futures OI UP → bearish | READY — frozen package recovered |
| 0025 | PRODUCTION FROZEN per latest canonical status | New 4-week high → bullish | BLOCKED FOR EXACT EXECUTION COMPARISON — dedicated later freeze artifact not recovered |
| 0026 | PRODUCTION FROZEN per latest canonical status | New 4-week low → bearish | BLOCKED FOR EXACT EXECUTION COMPARISON — dedicated later freeze artifact not recovered |
| 0028 | PRODUCTION FROZEN | Confirmed bearish divergence at HIGH pivot | READY — continuity/recovery evidence recovered |
| 0029 | PRODUCTION FROZEN by dedicated freeze record | Confirmed bullish divergence at LOW pivot | READY — dedicated freeze evidence recovered |

## Regression contract
For every READY rule, compare original evaluator output with Rule Factory output without changing the source contract.

Required equality dimensions:
- status
- canonical evidence fields
- direction / relation
- availability timestamp
- chronology / eligibility
- NOT_EVALUABLE behavior
- provenance/source_rule_id

A frozen rule must never be downgraded by the Factory merely because an engineering layer is unavailable.

## Stop conditions
- Any frozen rule changes semantic output → FAIL.
- Any availability/no-lookahead regression → FAIL.
- Any invented threshold/operator → FAIL.
- Any 2025-based tuning/selection → FAIL.
- Any missing authoritative contract → BLOCKED, not PASS.

## Important status conflicts
0008 has a preserved historical conflict: the latest continuity package lists it as frozen while an older PF-B1 proposal says its decisive-break operator was not frozen. This conflict must be preserved, not silently reconciled by changing the rule.

0025/0026 are listed as frozen by the later canonical status, but the dedicated later freeze artifacts were not recovered in the current File Library search. Therefore they are protected as frozen but are not claimed to have passed an executable Factory regression until their authoritative evaluator contracts are recovered.

## Current conclusion
The 12-rule Frozen baseline is now explicitly mapped. This artifact does NOT claim a 12/12 regression PASS. Execution must use the recovered authoritative evaluator contracts only.

2025 remains OOS and is excluded from tuning, selection, and implementation choice.
