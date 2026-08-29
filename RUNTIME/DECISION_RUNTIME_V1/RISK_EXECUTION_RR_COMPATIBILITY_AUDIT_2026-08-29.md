# Risk / Execution Compatibility Audit — 2026-08-29

## Finding
The existing execution adapter and the frozen risk integration contract currently disagree on the minimum reward:risk requirement.

## Existing execution adapter
`RUNTIME/DECISION_RUNTIME_V1/execution_runtime_adapter_v2.py` currently constructs a mechanical plan with:
- `SL_ATR = 0.75`
- `TP_R = 2.0`

So an approved direction produces a 2R target.

## Existing risk integration
`RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py` currently enforces:
- `CURRENT_CANONICAL_MIN_RR = 3.0`
- Risk fails with `RR_BELOW_CURRENT_CANONICAL_MINIMUM` when RR < 3.0.

## Consequence
A trade plan produced by the current execution adapter at 2R cannot honestly receive a `RISK_GATE_PASS` from the current risk integration. This is a real contract incompatibility, not a missing-data issue.

## Required handling
Do not silently change either contract during Gate 3C.
Do not invent a new SL/TP method.
Resolve which existing project contract is authoritative, with evidence from the existing governance/readiness artifacts, then make the minimum wiring-only change.

## Gate status
- MTF source provenance: PASS / CLOSED
- Six timeframe set: PASS / CONFIRMED
- MTF -> Brain strict join adapter: IMPLEMENTED / NOT YET PROVEN ON REAL SOURCE ROW
- TIZ boundary: AUTHORITATIVE process-only interface; unavailable remains NOT_EVALUABLE
- Risk / Execution RR compatibility: BLOCKED (2R execution plan vs 3R risk minimum)
- Gate 3C: PENDING

## Next action
Audit the existing frozen decision/execution/risk governance artifacts to determine the authoritative RR contract before any full replay. Keep 2025 locked and do not tune on OOS data.