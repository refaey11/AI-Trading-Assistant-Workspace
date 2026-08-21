# Rule Adapter Compatibility Audit — 2026-08-21

## Scope
Compatibility audit only. No source-rule rewrite, no threshold invention, no new trading logic, no TIZ promotion.

## Sources audited
- `rule_adapter_contract_v1.json` (local project artifact)
- `THREE_BOOK_DECISION_CONTRACT_V1.json`
- `DECISION_SCHEMA_V1.json`
- `THREE_BOOK_INTEGRATION.json`
- `PROJECT_INDEX/MASTER_PROJECT_STATE_2026-08-19.md`

## Compatibility findings

### PASS — architecture roles
The adapter contract preserves the required boundaries:
- Murphy = primary technical context.
- Nison = confirmation only.
- TIZ = process/psychology gate only.
- Similarity = historical evidence only, never sole decision maker.
- Risk = hard gate.
- Adapter = normalization, not source-rule duplication.

### PASS — precedence
The adapter precedence is compatible with the Three-Book Decision Contract:
- process failure blocks execution;
- risk failure blocks execution;
- Murphy invalidation blocks directional setup;
- Nison can confirm or contradict but cannot create direction alone;
- similarity cannot override hard gates.

### GAP — runtime status
`rule_adapter_contract_v1.json` explicitly reports `status: DESIGN_ONLY`.
Therefore the contract itself is not proof of an authoritative runtime implementation.

### GAP — unavailable evidence representation
The adapter contract has `available`, but `DECISION_SCHEMA_V1.json` contains several boolean defaults for TIZ fields. A compatibility implementation must not silently interpret an unavailable source as `false` or `true`.
`NOT_EVALUABLE` / unavailable semantics must remain distinguishable from an evaluated failure.

### GAP — TIZ parking
TIZ remains deferred/parked for current closure work. Open candidate TIZ pull requests are not promotion evidence and must not be merged or used to reopen the TIZ closure track without an explicit decision.

### GOVERNANCE — 2025
2025 remains OOS and must not be used for tuning, calibration, selection, or optimization.

## Result
**Rule Adapter contract compatibility: PASS at design/contract level.**
**Authoritative Rule Adapter runtime: NOT PROVEN by this audit.**

## Next work
Do not rebuild the adapter. Locate and validate any existing runtime implementation first. If none exists, define the smallest bridge required to execute the existing contract while preserving unavailable evidence and hard-gate precedence.
