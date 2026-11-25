# Gate 3C Direction Authority and Execution Boundary Follow-up — 2026-11-25

## Scope
Branch-pinned static inspection on `fix/similarity-direction-isolation-2026-11-25`. This report supplements, and does not replace, the prior MTF/Brain/TIZ and execution-path audits.

No runtime/source implementation changed. No tests or workflows were run. No market-data payloads were accessed. 2025 OOS and 2026 market data were not accessed. No PR, merge, rebase, cherry-pick, or main-branch change occurred.

## 1. Exact Gate 3C direction chain

Inspected:
- `RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`

Observed chain:
1. Gate 3C requires seven MTF fields in the event.
2. It requires Murphy evidence to be authoritative and PASS, and checks the event's Murphy rule IDs against its governed ID set.
3. It requires the complete Nison 44-rule envelope.
4. It requires authoritative Risk evidence.
5. Its Murphy/Risk contract requires both directions to be BUY/SELL and equal, requires Murphy and Risk pass_rule_id equality, and requires matching directional source-rule ID sets.
6. It then passes the event's separate `brain_row` into the runtime bridge.
7. The bridge only checks evidence mappings are non-empty and Risk is authoritative; it does not independently enforce Murphy authority/status or Murphy/Risk linkage for direct callers.
8. The assembler runs the recovered Brain over `brain_row`.
9. The evaluator chooses BUY/SELL from Brain `directional_bias`; it only rejects an opposing Murphy direction.

## 2. What Gate 3C proves — and does not prove

Gate 3C's Risk direction is explicitly linked to the Murphy event evidence. This is a meaningful upstream control.

However, the final BUY/SELL selection is still made from Brain directional bias. Gate 3C does not establish that the Brain's signed MTF/trend-regime inputs are sourced from Murphy or that those fields are merely non-directional confirmation. The evaluator checks that Brain and Murphy do not oppose each other, not that the selected side is sourced from Murphy.

Therefore:
- Murphy/Risk directional linkage: checked by Gate 3C.
- Brain/Murphy non-conflict: checked by evaluator.
- Brain direction derived exclusively from Murphy: NOT PROVEN.
- MTF numeric producer encoding, missing-value policy, scale, producer lineage, and timestamp semantics: OPEN / BLOCKED by the existing MTF provenance audit.

The Gate 3C output's governance label `murphy_primary_context: true` does not, by itself, prove exclusive direction authority.

## 3. Direct bridge boundary

`run_full_brain_cycle` is callable without Gate 3C. Its own boundary:
- rejects missing evidence mappings;
- requires Risk `authoritative=True`;
- does not require Murphy `authoritative=True`;
- does not require Murphy PASS or canonical BUY/SELL;
- does not bind Risk direction/pass_rule/source IDs to Murphy;
- does not validate MTF provenance.

Thus direct bridge callers can bypass the stronger Gate 3C-specific checks. Do not assume every invocation of the bridge is Gate 3C-authenticated.

## 4. TIZ and legacy event builder

The inspected Gate 3C -> bridge -> assembler -> evaluator -> execution-plan path treats TIZ as optional metadata. The evaluator's existing tests assert that absent or NOT_READY TIZ does not block BUY when other conditions pass.

The separate `ADAPTERS/rule_adapter_execution_bridge_v1.py::build_execution_event` still requires `trading_zone.process_state == READY`. This remains a separate legacy helper boundary. Its active caller inventory is not established by the files inspected here. The policy conflict is real at source level; whether it affects the active Gate 3C route is NOT PROVEN.

## 5. Risk ratio separation

The Gate 3C single-event risk builder produces a frozen evaluation candidate using 0.75 ATR stop / 2R target and labels authority scope `evaluation_single_event`. The frozen profile says it must not redefine canonical Risk or canonical three-book mode.

The canonical Risk Engine inspected validates stop distance 0.5–4 ATR and positive take-profit distance but does not itself enforce minimum RR=3. Therefore the canonical 3R rule must be enforced by the correct higher-level canonical contract; it must not be inferred from this risk-engine function or replaced by this evaluation-only 2R path.

## 6. Tests and verification state

Inspected existing tests:
- `tests/evaluation/test_gate3c_murphy_direction_contract_v1.py`: covers Murphy/Risk direction conflict, pass-rule mismatch, source evidence membership, and registry-eligible directional PASS selection.
- `tests/evaluation/test_three_book_decision_evaluator_v1.py`: covers Brain-to-Murphy conflict, Brain neutral rejection, Nison contradiction, Nison absent as medium strength, Risk failure, missing SL, and TIZ absent/NOT_READY as audit-only.
- `tests/test_knowledge_decision_brain_runtime.py`: includes Similarity directional-inertness regression test.

These files were inspected, not executed. No CI success is claimed.

## 7. Next safe work
1. Obtain a formal owner decision: Murphy-exclusive direction vs explicit MTF-authorized direction.
2. Independently resolve MTF field provenance and volume semantics.
3. Decide whether the legacy event builder remains supported; if yes, align its TIZ behavior with the approved canonical policy, only after branch-pinned caller enumeration.
4. Add direct-bridge tests proving untrusted/missing Murphy and mismatched Risk cannot bypass Gate 3C contracts.
5. Add a direction-authority test that demonstrates whether BUY/SELL can change when MTF direction changes while Murphy direction is held fixed. This is a contract test, not permission to alter Brain V1.
6. Verify the canonical 3R gate at the actual production-eligible boundary, keeping the 2R evaluation candidate isolated.
7. Inspect workflow triggers and exact data scope before running any tests.

## Status
- Gate 3C Murphy/Risk direction and rule provenance linkage: PRESENT at Gate 3C input boundary.
- Gate 3C final direction exclusively Murphy-derived: NOT PROVEN.
- Public bridge standalone Murphy/Risk validation: GAP.
- TIZ policy consistency across all helpers: OPEN / INCONSISTENT.
- Canonical 3R enforcement at production-eligible boundary: NOT PROVEN by the inspected Risk Engine alone.
- Implementation edits/tests/workflows: none.
