# MURPHY 0006/0007 — FINAL FREEZE MANIFEST V1

Date: 2026-08-15
Status: EVALUATOR RULES FROZEN / LIVE RUNTIME DEPLOYMENT NOT CLAIMED

## Freeze scope
This manifest freezes the Murphy 0006/0007 evaluator contract and its Decision Brain evidence adapter at the project-evaluator layer. It does not claim that a live trading runtime is deployed or authorized to trade autonomously.

## Frozen source/lineage
`PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 -> MURPHY_CONFIRMATION_LAYER -> 0006/0007 EVALUATOR -> Decision Brain evidence adapter`

Existing upstream components are reused. No rebuild of Pivot V2 or Geometry V1 is part of this freeze.

## Frozen operational semantics
### 0006
Reaction lows -> UP trendline -> first eligible same-family third-touch candidate -> D1 range intersection -> next eligible opposite-family confirmed bullish reaction -> completed-bar lows remain on/above the line between touch and reaction -> confirmation at reaction availability.

### 0007
Reaction highs -> DOWN trendline -> first eligible same-family third-touch candidate -> D1 range intersection -> next eligible opposite-family confirmed bearish reaction -> completed-bar highs remain on/below the line between touch and reaction -> confirmation at reaction availability.

Missing required evidence remains `NOT_EVALUABLE`.

## Explicit exclusions
No ATR, pip, arbitrary percentage tolerance, arbitrary lookback, automatic 3% filter, automatic 2-day binding, or 2025 tuning/selection.

## Validation gates
- Governance/operationalization decision: PASS
- Canonical Pivot V2 lineage: PASS
- Canonical Geometry V1 lineage: PASS
- Fresh 2016–2024 production-path replay: PASS
- Replay result: 0006=8, 0007=7, total=15
- Historical row reconciliation: 15/15
- 2025 excluded: PASS
- Availability/no-lookahead safeguards: PASS
- Operator regression suite: PASS (7/7 in the reconciled project evidence)
- Current deterministic CI on HEAD `c8497ef4a761856c6138a9c34c28ccd00305e99c`: PASS
- Audit #14 deterministic CI: PASS, `4 passed in 0.03s`
- Audit #14 artifact: `0006-0007-deterministic-audit-14`
- Local SHA-256 of uploaded Audit #14 ZIP: `2dd1fab08a5094f3822bebd0041d09eee3b08d40b8fe89bf748c432b8443367b`
- Decision Brain evaluator adapter integration gate: PASS / CLOSED

## Artifact evidence
Audit #14 artifact contains:
- `commit.txt` = `c8497ef4a761856c6138a9c34c28ccd00305e99c`
- `pytest.txt` = `4 passed in 0.03s`
- `evidence.txt`
- `run_utc.txt` = `2026-08-14T21:42:36Z`
- `run_cairo.txt` = `2026-08-15T00:42:36+0300`

## Freeze decision
The 0006/0007 evaluator rules and their evidence-only Decision Brain adapter are now FROZEN at the project-evaluator layer. Any future semantic or numeric change requires a new governance/source audit, new tests, and a new freeze cycle. Historical case counts must never be used as the reason to alter the operator.

## Runtime boundary
This freeze does not authorize autonomous live trading. The Decision Brain adapter emits normalized Murphy evidence only; final decision confidence, conflict resolution, process gates, risk, and any execution authority remain outside this adapter.

## Next rule
After this manifest is accepted, work may proceed to the next Murphy rule set without reopening 0006/0007 unless a new source, reproducibility defect, or integration defect is discovered.
