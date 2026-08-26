# FINAL 2025 Governed 78-Rule P&L Audit — 2026-08-26

## Scope
This note records the current audited state of the governed 2025 OOS run before any direction-arbitration fix or tuning.

## Source artifacts audited
- FINAL_2025_DECISION_EVENTS_MANIFEST.json
- FINAL_2025_GOVERNED_78_RULE_MANIFEST.json
- FINAL_2025_PNL_MANIFEST.json
- MURPHY_2025_FULL_EVIDENCE_MANIFEST.json
- MURPHY_0021_MANIFEST.json
- MURPHY_0022_0023_2025_MANIFEST.json
- NISON_2025_FULL_EVIDENCE_MANIFEST 2.json
- RISK_2025_EVIDENCE_MANIFEST.json
- NISON_2025_CANDIDATE_STREAM.csv
- FINAL_2025_TRADES 2.csv

## Verified facts
- Evaluation year: 2025 (OOS / evaluation-only).
- Murphy rules present at the governed decision boundary: 34.
- Nison rules present at the governed decision boundary: 44.
- Total governed rule evidence: 78 rules per event.
- Events: 6,225.
- Event status: 6,225 NO_TRADE.
- Executable events: 0.
- Not evaluable events: 0.
- Trades: 0.
- Starting equity: 10,000.
- Final equity: 10,000.
- Core P&L: 0.0.
- Max drawdown: 0.0.
- This zero P&L is NOT a profitability conclusion because no trades were executable.

## Primary no-trade reasons
- MURPHY_CONTEXT_NOT_PASS: 3,534 events.
- MURPHY_BRAIN_DIRECTION_CONFLICT: 2,691 events.

## Key correlation observed
MURPHY_0021 has 2,691 PASS rows in 2025, matching the 2,691 MURPHY_BRAIN_DIRECTION_CONFLICT events in the final decision-event manifest.
This is a diagnostic correlation only; it is not yet proof of a defect.

## Governance status
- 2025 tuning: false.
- New rule semantics: false.
- Synthetic evidence: false.
- Full 34 Murphy + 44 Nison evidence preserved at the decision boundary.
- TIZ remains process-only and does not generate direction.
- Nison does not generate direction.
- Murphy is the directional confirmation source in the current governed contract.

## Important conclusion
The current run is operationally successful but is NOT a valid profitability result because the Decision Brain produced zero executable trades. The next action is a direction-arbitration / integration audit using the actual 2025 evidence. No rule thresholds or 2025 tuning should be changed before that audit.

## Next audit
1. Compare Decision Brain directional bias with Murphy 0021/0022/0023 directional confirmations event-by-event.
2. Determine whether the 2,691 conflicts are expected semantic conflicts or an integration/direction-mapping defect.
3. Verify that legacy candidate-row selection is not incorrectly suppressing valid full-envelope evidence.
4. Only after the cause is established, make the smallest compatibility fix (if needed), add regression coverage, and rerun the governed 2025 OOS P&L.
