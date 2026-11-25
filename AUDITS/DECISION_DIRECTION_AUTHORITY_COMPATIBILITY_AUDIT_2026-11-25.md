# Decision Direction Authority Compatibility Audit — 2026-11-25

## Scope and safety
Static inspection only on branch `fix/similarity-direction-isolation-2026-11-25`.
No runtime/source code modified. No tests or workflows run. No market-data payloads accessed. No 2025/2026 data accessed. No merge, rebase, cherry-pick, or change to `main`.

Inspected:
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `compatibility/decision_brain_v1_handoff_adapter.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py`
- `docs/MTF_ALIGNMENT_RUNTIME_CONFIRMED_V1.md`
- `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md`
- `AUDITS/RUNTIME_BRIDGE_GOVERNANCE_BOUNDARY_AUDIT_2026-11-25.md`

## 1. Confirmed direction-generation behavior in recovered Brain
The recovered `decision_brain.assess` creates directional evidence from:
- `mtf_trend_score`
- `M5_trend_regime`, `M15_trend_regime`, `M30_trend_regime`, `H1_trend_regime`, `H4_trend_regime`, `D1_trend_regime`
- Volume fields when `volume_available` is true.

It aggregates bullish and bearish evidence to produce `directional_bias`.
Similarity can also create bullish/bearish `HistoricalMemory` evidence when passed non-null, but the aligned compatibility adapter now calls `assess(row_copy, similarity=None)`. This audit does not alter that remediation.

## 2. Murphy is currently a downstream agreement check, not the Brain's demonstrated direction source
The assembler calls the Brain assessment through the governed adapter, then the Three-Book evaluator compares the resulting Brain bias against Murphy direction and rejects a directional conflict.

That comparison is a consistency check. It does not prove that the Brain's directional bias was derived from Murphy evidence.

The inspected Gate 3C path also validates Murphy authority/status and Murphy/Risk directional linkage before calling the bridge. However, the bridge passes the Brain row to the assembler, and the recovered Brain derives directional evidence from the MTF/Volume row fields described above.

## 3. Architecture compatibility finding
The repository's MTF confirmation states that MTF supplies market context/evidence and does not independently create LONG/SHORT decisions. The project Master Map requires Murphy to own technical direction, Nison to confirm or contradict, Similarity to remain historical evidence only, and Risk to act as a hard gate.

The inspected implementation does not currently demonstrate that separation:
- MTF trend score/regime fields directly contribute bullish/bearish evidence and Brain directional bias.
- Volume can contribute bullish evidence; negative/weak volume is neutral in the inspected Brain implementation.
- Murphy is checked downstream for PASS/conflict, but is not shown as the sole direction authority for the Brain's bias.
- Nison contradiction can reject a trade, while confirmation affects evaluator strength; Nison does not create direction in the inspected evaluator.
- Similarity isolation is present in the aligned adapter path, but the recovered Brain still contains an optional Similarity directional path if another caller passes non-null Similarity.

**Status: ARCHITECTURAL COMPATIBILITY GAP — NOT RESOLVED.**
This is not a finding that the recovered Brain source should be rewritten. The project rules prohibit modifying the recovered Brain V1 source without a separately approved compatibility plan.

## 4. Separate provenance blocker remains
The six-timeframe MTF artifact family and closed-bar alignment principle are documented as confirmed. However, the exact producer encoding, missing-value policy, scaling, detailed producer lineage, and timestamp/as-of semantics for the seven Brain fields remain open in `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md`.

Therefore, even before deciding direction authority, those fields are not yet fully source-authenticated for canonical profitability evaluation. This audit does not re-open or rebuild the MTF producer.

## 5. Bridge boundary remains weaker than Gate 3C
The public bridge currently:
- requires non-empty Murphy, Nison, and Risk mappings;
- checks authority only for Risk;
- does not itself enforce Murphy authority/status/direction/provenance;
- does not itself enforce Nison authority or a complete confirmation state.

Gate 3C performs stronger upstream checks, but direct bridge callers can bypass those caller-specific checks. The prior bridge governance audit records this boundary gap.

## 6. Decisions required before implementation
No new fields or enum values are proposed here. The project owner must approve the policy using existing Master Map and governed contracts:

1. **Direction authority:** confirm whether Murphy is the sole source of directional bias, with MTF and Volume context-only, or formally amend the Master Map. Do not silently treat the current MTF-derived bias as Murphy-derived.
2. **Nison absence:** decide whether missing/unknown confirmation is a hard block or a review-only state. Current paths are not consistent: evaluator permits absent confirmation at medium strength, while Gate 3C requires the full 44-rule Nison envelope.
3. **Shared bridge contract:** after the above decisions, define one reusable fail-closed contract using existing evidence fields/enums and enforce it at the public bridge boundary, not only in Gate 3C.
4. **Compatibility audit:** map the approved contract against assembler, adapter, evaluator, Gate 3C, legacy callers, and tests before any runtime edit.
5. **Regression tests:** cover direct bridge bypass, missing Murphy authority, missing/unknown Nison state, direction mismatch, source/pass-rule mismatch, valid Gate 3C path, and Similarity directional inertness.
6. **MTF source authentication:** resolve the documented producer/encoding/timestamp blocker independently before canonical profitability claims.

## 7. Explicit non-actions
- No direction policy was changed or inferred.
- No Nison absence policy was selected.
- No new evidence schema or enum was invented.
- No Brain V1, Murphy, Nison, Risk, MTF, Volume, or execution runtime source was modified.
- No tests/workflows were run.
- No profitability, production, or live-trading readiness claim is made.
- 2025 OOS remains locked; no 2025/2026 data was accessed.
