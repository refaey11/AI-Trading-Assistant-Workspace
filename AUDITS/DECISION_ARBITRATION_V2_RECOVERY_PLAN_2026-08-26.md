# Decision Brain Direction Arbitration V2 — Recovery Plan

Date: 2026-08-26
Branch: `recovery/final-78-runtime-wiring`
Status: DIAGNOSTIC / NO-TRADE SEMANTICS UNCHANGED

## Finding

The current integration has a structural separation between the recovered Decision Brain assessment and Murphy evidence.

`compatibility/decision_brain_v1_handoff_adapter.py` calls the recovered Brain with `assessment = decision_brain_module.assess(row_copy, similarity=None)` and does not pass Murphy or Nison into that assessment call. Murphy/Nison are then checked downstream by the Three-Book evaluator.

This means the current path is effectively:

`market-state -> Brain direction`
`Murphy -> downstream directional veto`
`Nison -> confirmation/contradiction gate`

rather than a single governed directional arbitration boundary consuming Murphy technical context as an input to the directional assessment.

## Observed OOS symptom

The 2025 governed run produced 6,225 events and 0 executable trades:

- 3,534 `MURPHY_CONTEXT_NOT_PASS`
- 2,691 `MURPHY_BRAIN_DIRECTION_CONFLICT`

The 2025 result is kept frozen and is not used for tuning.

## Why this is a plausible architectural failure mode

A multi-signal decision architecture normally separates signal production from a decision/aggregation stage. The current implementation has the Brain independently produce a directional bias from market-state features, then asks Murphy to agree after the fact. That creates a veto topology where two independent directional views can disagree even when each source is internally valid.

For this project, the intended role hierarchy is stronger than generic voting:

1. Murphy = technical context / setup / directional technical evidence.
2. Nison = confirmation or contradiction only; never direction generation.
3. TIZ = process gate only; never direction generation.
4. Similarity/Memory = historical evidence only; never sole decision maker.
5. Risk = hard execution gate.
6. Decision Brain = governed arbitration/decision layer, not an independent direction generator that later vetoes Murphy.

## Proposed V2 architecture

Do not rewrite the recovered Brain source. Add a governed arbitration layer around it.

### Stage A — Direction candidates

Produce explicit, timestamped candidates:

- `MURPHY_DIRECTION`: derived only from authoritative Murphy directional PASS evidence.
- `BRAIN_CONTEXT_BIAS`: the recovered Brain's existing market-state assessment.
- `NISON`: confirmation/contradiction only.
- `TIZ`: READY / BLOCK / NOT_EVALUABLE.
- `RISK`: PASS / FAIL / NOT_EVALUABLE.

### Stage B — Arbitration

The arbitration layer must classify each event into one of:

- `AGREE`
- `MURPHY_ONLY`
- `BRAIN_ONLY`
- `CONFLICT`
- `NO_DIRECTION`

It must not silently convert disagreement into a trade.

### Stage C — Decision policy

The development candidate should be tested in shadow mode first. The first candidate policy is:

- Murphy provides the technical direction when a valid directional PASS exists.
- Brain is treated as contextual agreement/disagreement, not an automatic direction veto.
- Nison may strengthen or block; it cannot create direction.
- TIZ may block; it cannot create direction.
- Risk may block; it cannot create direction.
- Any ambiguity/conflict without an explicit frozen policy remains `NO_TRADE`.

No threshold, rule meaning, or 2025 parameter may be changed in this recovery step.

## Validation protocol

1. Run the arbitration audit in read-only shadow mode on 2025 only to measure the disagreement topology. Do not compute replacement P&L from it.
2. Run the same shadow audit on development years 2016-2024.
3. Compare:
   - direction coverage,
   - Murphy/Brain agreement rate,
   - conflict rate,
   - neutral/abstain rate,
   - regime dependence.
4. Only after the shadow evidence is understood, implement a V2 governed arbitration adapter for development validation.
5. Validate V2 with chronological walk-forward on pre-2025 data.
6. Freeze the chosen V2 policy before touching the locked 2025 OOS again.
7. Re-run 2025 exactly once as the final OOS acceptance test.

## Research-backed design constraints

External research reviewed on 2026-08-26 supports:

- modular signal/decision/risk separation in algorithmic trading architectures;
- explicit abstention/reject options with coverage/risk-coverage reporting rather than assuming every observation must trade;
- walk-forward / chronological validation and strict OOS locks to reduce overfitting;
- research-to-live parity through a shared deterministic execution core.

References reviewed include NautilusTrader architecture and backtesting documentation, selective-classification trading research, the Probability of Backtest Overfitting paper, recent 2026 work on anti-overfitting validation, and multi-signal decision-engine patterns.

## Acceptance criteria

This recovery is accepted only if:

- no existing Murphy/Nison/TIZ/Memory knowledge base is rebuilt;
- 2025 is not tuned;
- V2 does not allow Nison, TIZ, or Memory to generate direction;
- every decision is traceable to explicit source evidence;
- shadow coverage/conflict diagnostics are produced before any semantic change;
- the final profitability run uses the exact frozen V2 contract.

## Decision

Do not delete the project. Do not modify the recovered Brain or Murphy rule semantics to force trades.

The immediate next engineering task is **Direction Arbitration Shadow Audit**. The objective is to prove whether the current 0-trade result is caused by a structurally over-vetoing boundary rather than by the underlying Murphy evidence itself.
