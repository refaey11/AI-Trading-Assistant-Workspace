# Nison 0042-0044 External Source Contract V1

Date: 2026-08-17
Status: CONTRACT CLOSED / E2E PENDING

## 0042 — Support / Resistance
Nison's Rule of Multiple Technical Techniques treats support/resistance as a Western structural location and uses candlesticks as confirmation. A support/resistance area may be a zone rather than an exact price. The canonical binding is therefore:
1. upstream structural S/R zone exists;
2. price tests/enters the zone;
3. a source-supported candlestick confirmation occurs at the zone;
4. confirmation is observed without using future candles beyond the confirmation event.
No new zone width, ATR, pip, percentage, or lookback is introduced by this adapter.

External source evidence: Nison describes support/resistance areas as zones and repeatedly uses candlestick patterns to confirm those areas. Search evidence also shows his examples combining a bearish engulfing with a resistance line and a change-of-polarity resistance area.

## 0043 — False Breakouts / Springs / Upthrusts
The Nison source chapter explicitly covers Springs and Upthrusts. The operational sequence is source-first:
- establish the relevant trading range / support-resistance context;
- price penetrates the boundary;
- the penetration fails and price returns back into the prior range;
- candlestick evidence can provide confirmation of the failure.
No arbitrary percentage/pip penetration threshold is added. If the canonical upstream range/boundary producer does not provide the event, the Rule remains NOT_EVALUABLE.

## 0044 — Change of Polarity Principle
Nison defines change of polarity as old support becoming new resistance and old resistance becoming new support. The principle can operate on a zone, not necessarily one exact price. Nison also states that potency is related to how often the old support/resistance was tested and to volume/open interest on those tests. The operational sequence is:
1. established support/resistance zone;
2. decisive penetration/break of that zone;
3. former support/resistance becomes the opposite role;
4. subsequent test/retest demonstrates the new role;
5. candlestick confirmation may confirm the new support/resistance role.
No arbitrary distance/tolerance is introduced. The number of prior tests is evidence/context, not a fabricated minimum unless an authoritative rule explicitly specifies one.

## Governance
These contracts use external research only to recover source semantics. They do not authorize thresholds, tuning, or optimization. 2025 remains OOS. Nison remains confirmation/evidence only and cannot generate standalone direction.

## Current integration verdict
0042 source semantics: PASS
0043 source semantics: PASS
0044 source semantics: PASS
Canonical upstream producers: PENDING
Historical E2E: PENDING
Production freeze: NOT YET
