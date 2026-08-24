# AI Trading Assistant — Evidence Architecture V1 Checkpoint

Date: 2026-08-24
Branch: `evidence-architecture-v1`
PR: #52

## Completed
- Canonical evidence record schema with `event_time` and `available_time`.
- Source, quality, status, lineage, and `rule_id` metadata.
- Evidence adapter contract and registry.
- Point-in-time join validation.
- Fail-closed handling for missing evidence.
- Future evidence rejection.
- Proxy evidence forbidden by default.
- 2025 remains OOS and excluded from tuning.
- Rule semantics remain immutable at the evidence boundary.
- Tests added for future-evidence rejection, latest-available selection, and fail-closed behavior.
- PR #52 opened as a Draft to add the evidence boundary without changing Murphy/Nison/TIZ/Risk/Decision Brain/execution semantics.

## Preserved project paths
- PR #51 remains the historical Full Decision Brain event producer path.
- Existing Murphy/Nison/TIZ/Risk/Memory/Decision Brain contracts are not rewritten by this architecture layer.

## Dropbox mirror
Checkpoint recorded at:
`/AI_Trading_Assistant/AI_TRADING_ASSISTANT_EVIDENCE_ARCHITECTURE_CHECKPOINT_V1_2026-08-24.md`

## Next governed steps
1. Wire authoritative adapters, including CME 6B Open Interest where a Murphy rule explicitly requires futures OI.
2. Run Murphy 34-rule historical coverage through the evidence layer.
3. Produce unified Full Decision Brain event streams for 2024 and 2025.
4. Run Final OOS profitability evaluation without tuning 2025.
5. Replay the same event contracts in shadow/paper live mode.
6. Build MT5/broker execution adapter and operational safety controls before micro-live.

## Integrity rules
- No synthetic evidence.
- No lookahead.
- No 2025 tuning.
- No profitability-readiness claim until authoritative evidence streams pass point-in-time gates.
