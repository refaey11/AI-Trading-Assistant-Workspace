# MTF / Decision Brain Direction Semantics and TIZ Boundary Audit — 2026-11-25

## Scope
GitHub-only static compatibility audit on `fix/similarity-direction-isolation-2026-11-25`. This report records source behavior and contract conflicts; it does not authorize a policy change.

No runtime/source implementation changed. No tests or workflows were run. No market-data payloads were accessed. No 2025/2026 market data was accessed. No PR, merge, rebase, cherry-pick, or main-branch change occurred.

## Files inspected
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`
- `docs/MTF_ALIGNMENT_RUNTIME_CONFIRMED_V1.md`
- `audits/evidence/MTF_ARCHITECTURE_V2_TO_DECISION_BRAIN_COMPATIBILITY_AUDIT_2026-08-21.md`
- `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md`
- `CHECKPOINTS/DECISION_BRAIN_CONTRACT_AUDIT_2026-08-21.md`
- `governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`
- `compatibility/knowledge_decision_handoff.py`
- `ADAPTERS/rule_adapter_execution_bridge_v1.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `evaluation/three_book_decision_evaluator_v1.py`

## 1. MTF architecture contract vs recovered Brain behavior

The MTF runtime confirmation states that MTF supplies market context/evidence and does not independently create LONG/SHORT decisions.

The recovered Brain V1 source nevertheless creates a `directional_bias` by aggregating:
- signed `mtf_trend_score`;
- the mean of six signed trend-regime fields (M5/M15/M30/H1/H4/D1);
- volume evidence when `volume_available` is true.

It then compares total bullish and bearish evidence and assigns bullish/bearish/conflicted/neutral bias.

Therefore the implementation is not merely displaying MTF context: MTF and trend-regime fields directly contribute to the Brain's directional-bias calculation. This is a source-level semantic mismatch with the MTF contract's statement that MTF does not independently create LONG/SHORT decisions.

Important nuance: the Brain docstring calls V1 an evidence aggregator and not a trading-signal generator. The Three-Book evaluator later converts Brain bullish/bearish bias into BUY/SELL after Murphy status/conflict, Risk and Nison contradiction checks. This makes the Brain bias an upstream directional input to the final evaluator, even though Brain V1 itself does not emit BUY/SELL.

## 2. Volume evidence asymmetry

In the recovered Brain:
- positive mean volume regime contributes bullish evidence;
- zero/negative mean contributes neutral evidence;
- negative volume does not create bearish evidence.

This is asymmetric. It must not be interpreted as balanced bullish/bearish volume direction, nor silently changed. The `volume_available` flag only controls whether this evidence block is considered; source authenticity and field-level producer semantics remain separate unresolved requirements.

## 3. MTF source provenance remains independently blocked

The MTF family and six timeframe coverage are confirmed at artifact-family level. However, the MTF provenance blocker still leaves unresolved:
- exact producer/serialized encoding for the seven Brain input fields;
- missing-value/imputation policy;
- scaling/normalization;
- producer lineage;
- timestamp/as-of semantics.

Consequently, identifying the fields in code is not equivalent to authenticating the meaning of their numeric values. No profitability or production eligibility may be inferred from field presence alone.

## 4. Murphy role and current implementation

The Master Map / allowlist governance states Murphy is technical context/directional authority, Nison is confirmation/contradiction only, Similarity is historical evidence only, and Risk is a hard gate.

The current evaluator:
- requires Murphy `status == PASS`;
- compares Brain bias against Murphy direction and rejects an opposing bias;
- uses Brain bias to select BUY/SELL;
- rejects Nison contradiction, while allowing absent confirmation at medium strength;
- requires Risk pass and stop loss.

This is a Murphy agreement/conflict check, not proof that Brain direction originated from Murphy. The rule adapter normalizes Nison rule hints to neutral, consistent with Nison not creating direction.

**Finding:** the current source path is Brain/market-row-direction-led with Murphy consistency validation, not a proven Murphy-exclusive direction-authority path.

## 5. Additional TIZ boundary conflict

The assembler and evaluator describe TIZ as optional metadata only and not a decision/eligibility gate. However, the inspected `ADAPTERS/rule_adapter_execution_bridge_v1.py` marks an event executable only when `tiz.process_state == READY`, in addition to Risk and decision status.

This is a separate governance inconsistency: a downstream execution-event builder still requires TIZ READY even though the current assembler/evaluator contract says TIZ is metadata-only. The current branch also contains historical policy snapshots with differing TIZ semantics. Do not resolve this by changing code until the project owner confirms the canonical TIZ decision and the exact production path.

## 6. Canonical decisions still required

No new field names, enum values, or thresholds are proposed. Before implementation, the project owner must confirm:

1. **Direction:** Is Murphy the sole source of directional authority, as stated in the Master Map, with MTF/Volume restricted to non-directional context/confirmation? Or is the Master Map to be formally amended to authorize MTF-derived directional evidence?
2. **Brain V1:** If Murphy is sole direction authority, should Brain's existing directional bias be retained as a non-authoritative market assessment and prevented from independently selecting BUY/SELL, using only an already-existing governed Murphy direction field? This needs an explicit compatibility design; do not rewrite recovered Brain V1.
3. **Volume:** Is volume strictly participation/confirmation evidence? The present implementation is bullish-only for positive volume and neutral otherwise; no symmetric bearish interpretation is source-authorized.
4. **MTF authentication:** Resolve the exact producer encoding/lineage/as-of blocker independently of the direction policy.
5. **TIZ:** Confirm whether TIZ is metadata-only across the entire path or remains a process gate at the execution-event boundary. Current source contracts disagree.
6. **Bridge:** Once these policies are approved, enforce the shared existing evidence contract at the public bridge and audit every direct caller.

## 7. Safe implementation order
1. Record an explicit owner decision for Direction, Volume, and TIZ semantics.
2. Complete source/schema compatibility review using existing contracts only.
3. Design a test-only contract suite for direction authority, MTF provenance, volume availability/asymmetry, TIZ boundary, Nison absence/contradiction, Risk hard gate, and Similarity directional inertness.
4. Only then implement the smallest adapter/bridge change; do not modify recovered Brain V1, frozen Murphy/Nison rules, or source data.
5. Run scoped tests only after inspecting workflow triggers and data scope.

## Status
- MTF six-timeframe artifact-family support: confirmed.
- MTF not-authorized-to-create-independent-trade-decision statement: confirmed in MTF contract.
- Brain V1 directional-bias contribution from MTF/trend-regime fields: confirmed in source.
- Volume positive-only bullish contribution: confirmed in source.
- MTF numeric producer/encoding/timestamp provenance: OPEN / BLOCKED.
- Murphy-exclusive direction authority in current Brain/evaluator path: NOT PROVEN.
- TIZ metadata-only vs downstream READY requirement: contract inconsistency confirmed.
- Runtime changes/tests/workflows: none.
- 2025 OOS and 2026 market data: untouched.
