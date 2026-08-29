# PF-B1 / PF-H1 Historical QA Gate V1

## Runtime data audit

The available historical memory datasets contain timestamped market context and outcomes for historical periods beginning in 2016, but they do not expose authoritative rule-specific labels for:
- approved horizontal levels,
- approved breakout boundaries,
- completed-bar breakout events,
- Murphy pattern membership for 0013–0015/0018–0020.

Therefore a rule-specific historical replay cannot honestly be reported as PASS/FAIL from those datasets alone.

## 2025 exclusion

The TRUE_BACKTEST_V2 artifact available in the workspace contains 2025 query timestamps. It is therefore excluded from tuning/selection and cannot be used to close this gate.

## Gate result

`PF-B1 = QA BLOCKED_PENDING_RULE_EVENT_DATA`

`PF-H1 = QA BLOCKED_PENDING_RULE_EVENT_DATA`

This is a data-contract gate, not a semantic blocker. The candidate contracts and deterministic cases are already defined.

## Required dataset fields for the next run

### PF-B1
- timestamp
- approved boundary/level id
- boundary value
- completed bar close
- breakout direction
- breakout timestamp
- availability timestamp

### PF-H1
- timestamp
- confirmed pivot id
- level value
- support/resistance role
- authoritative horizontal classification
- availability timestamp

## Freeze rule

Do not mark either primitive Production Frozen until the above event fields are available and the 2016–2024 replay passes the availability/no-lookahead audit.

2025 remains OOS.
