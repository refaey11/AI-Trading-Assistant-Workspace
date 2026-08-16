# Nison 0001–0015 Compatibility Gate V1

## Purpose
Advance the Nison 44-rule batch using existing project evidence without inventing missing rule semantics.

## Source-bounded evidence
The current project queue identifies Rules 0001–0015 as Steve Nison recognition rules that remain `INCOMPLETE_NEEDS_RULE_DEFINITION` and `UNTESTED`. For 0001–0013, the queue explicitly lists missing `confirmation; invalidation_rule`; 0014 lists missing `confirmation`; 0015 remains incomplete in the same queue.

## Governance
- Nison remains confirmation-only and cannot create direction alone.
- Existing components must be audited and reused; no rebuild from scratch.
- Missing source-bounded conditions remain NOT_EVALUABLE.
- No invented threshold, tolerance, lookback, proxy, scoring, or direction rule is introduced.
- 2025 remains OOS and is excluded from tuning/selection/calibration/optimization.
- Unit-test presence elsewhere does not promote these rules to production.

## Rule gate
| Rule | Pattern | Current source-backed state | Gate |
|---|---|---|---|
| 0001 | Bullish Engulfing | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0002 | Bearish Engulfing | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0003 | Dark Cloud Cover | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0004 | Piercing Pattern | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0005 | On Neck | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0006 | In Neck | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0007 | Thrusting | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0008 | Morning Star | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0009 | Evening Star | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0010 | Morning Doji Star | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0011 | Evening Doji Star | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0012 | Abandoned Baby | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0013 | Harami | Queue: incomplete; confirmation + invalidation missing | NOT_EVALUABLE |
| 0014 | Harami Cross | Queue: incomplete; confirmation missing | NOT_EVALUABLE |
| 0015 | Tweezers Top | Queue: incomplete in current queue; exact closure fields must be recovered before evaluator work | NOT_EVALUABLE |

## Important distinction
This gate does not say the candlestick formations do not exist in Nison material. It says the current project evidence does not yet provide a closed, source-bounded operational contract for the required confirmation/invalidation fields. Therefore implementation must stop at the gate rather than silently converting recognition into a production evaluator.

## Next action
Recover the authoritative Nison source/knowledge records for each rule and map:
1. canonical formation/recognition;
2. context requirement;
3. confirmation requirement;
4. invalidation/failure condition;
5. availability timestamp;
6. compatible existing primitive/adapter;
7. deterministic tests;
8. 2016–2024 historical QA;
9. availability/no-lookahead QA;
10. explicit freeze review.

No production freeze is granted by this document.