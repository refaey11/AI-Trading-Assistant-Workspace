# AI Trading Assistant — Decision Arbitration Recovery Checkpoint

Date: 2026-08-26
Branch: `recovery/final-78-runtime-wiring`

## Baseline preserved before new work
- Project is NOT being deleted or rebuilt.
- 2025 remains locked OOS/evaluation-only and is not used for tuning.
- Existing Murphy knowledge/rules are preserved.
- Existing Nison knowledge/rules are preserved.
- Trading in the Zone remains process-only.
- Similarity/Historical Memory remains evidence-only and cannot be the sole decision maker.
- Risk remains a hard execution gate.
- Recovered Decision Brain V1 source is not rewritten in this recovery step.

## Verified 2025 finding
The governed 2025 run produced 6,225 events and zero executable trades.
Primary reasons:
- 3,534 `MURPHY_CONTEXT_NOT_PASS`
- 2,691 `MURPHY_BRAIN_DIRECTION_CONFLICT`
The run also verified 34 Murphy rules + 44 Nison rules per final event, with lossless full-evidence fan-in, no OOS tuning, and no new rule semantics.

## Architectural finding
The recovered Brain currently generates its directional assessment from market-state context independently of Murphy/Nison. The governed boundary then applies Murphy downstream as a directional compatibility/veto check. This creates a structural Brain-vs-Murphy veto topology.

## Recovery objective
Before changing any trading semantics, run a read-only Direction Arbitration Shadow Audit to measure:
- Brain directional coverage.
- Murphy directional coverage.
- Brain/Murphy agreement rate.
- Conflict rate.
- No-direction/abstain rate.
- Which Murphy rules generate directional PASS evidence.
- Regime dependence of conflicts.

## V2 candidate architecture (development-only until validated)
1. Murphy technical direction candidate.
2. Brain market-context bias candidate.
3. Explicit arbitration classification: AGREE / MURPHY_ONLY / BRAIN_ONLY / CONFLICT / NO_DIRECTION.
4. Nison confirmation/contradiction only.
5. TIZ process gate only.
6. Risk hard gate.
7. Memory remains evidence-only.

No automatic conversion of disagreement into a trade is allowed. Any ambiguity remains NO_TRADE until a frozen policy is validated.

## Validation protocol
- Shadow audit first.
- Development validation on 2016–2024.
- Chronological walk-forward on pre-2025 data.
- Freeze V2 contract.
- Re-run 2025 exactly once as final OOS acceptance.

## Evidence
The 2025 E2E log and GitHub source were reviewed before this checkpoint. The checkpoint is intentionally stored before any semantic change.
