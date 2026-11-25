# Branch-Aware MTF Lineage and Gate 3C Caller Audit — 2026-11-25

## Scope and method
Inspected the exact review-branch Git tree at commit `cd18ef52bbf86f794eea33a00f32190aed56732b` using GitHub's recursive Git tree endpoint, then fetched the source files named below from that branch. This was source inspection only: no CSV/data payloads, 2025/2026 market data, or Dropbox content were opened. No runtime source was changed and no tests were run.

## 1. MTF source existence is established; numeric field semantics are not fully closed

### Existing source evidence
- `docs/MTF_ALIGNMENT_RUNTIME_CONFIRMED_V1.md` records the six-timeframe MTF artifact family and the fields `mtf_trend_score`, timeframe trend-regime fields, and related context.
- `audits/evidence/MTF_ALIGNMENT_6_TIMEFRAME_SOURCE_CLOSURE_2026-08-21.md` and `audits/evidence/MTF_ALIGNMENT_GBPUSD_V1_EVIDENCE_2026-08-21.md` identify the recovered `MTF_ALIGNMENT_GBPUSD_V1` artifact family and six-timeframe schema.
- `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py` performs a backward as-of join of the seven Brain MTF fields. It performs numeric validation and explicitly does not generate direction or transform values.
- `BACKTEST/mtf_source_contract_gate_v1.py` checks numeric presence and timestamps, but it does not establish the original producer's numeric encoding or lineage.
- `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md` explicitly leaves raw-to-feature semantics, encoding, missing-value policy, scaling, producer lineage, and timestamp semantics unresolved, noting that the V5.4 inline categorical-to-numeric mapping is not proven canonical.

### Conclusion
The MTF source family and six-timeframe field family exist. This corrects any blanket statement that the source itself is unknown. However, source-backed numeric semantics and exact field-level lineage into Brain remain NOT CLOSED. Do not infer Murphy derivation from MTF source existence.

## 2. Gate 3C builds the Brain row by merging market state and MTF fields
File: `tools/gate3c_build_single_event_bundle_v1.py`

The builder:
- selects an MTF CSV containing the seven expected fields;
- selects the latest MTF row at or before the event timestamp;
- selects market-state context at or before the event timestamp;
- creates `brain_row = {**market, **mtf}`;
- returns both `mtf` and `brain_row`.

This establishes the immediate data path into the Brain row for the Gate 3C event builder. It does not independently prove the original semantics/encoding of those MTF values or that they are Murphy-rule-derived.

## 3. Gate 3C validates Murphy authority before invoking the bridge
File: `RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py`

The inspected caller:
- requires a non-empty Murphy event rule set;
- requires `murphy.authoritative is True` and `murphy.status == PASS`;
- requires the complete 44-rule Nison envelope;
- validates authoritative Risk and the Murphy/Risk direction and provenance match;
- constructs bridge evidence with Murphy and Nison marked authoritative;
- invokes `bridge.run_full_brain_cycle(...)` using `event["brain_row"]`.

Therefore the canonical Gate 3C caller applies stronger upstream checks than the bridge itself. This does not remove the bridge's direct-call contract gap: `full_brain_runtime_bridge_v1.py` remains callable without the Gate 3C wrapper and currently checks authority only for Risk.

## 4. Important independent path: legacy integration gate creates MTF values
File: `BACKTEST/decision_brain_integration_gate_v1.py`

This path contains an explicit `trend_map` mapping:
- `BULL_TREND -> 1.0`
- `BEAR_TREND -> -1.0`
- `TRANSITION/UNKNOWN -> 0.0`

It uses that mapping to set `mtf_trend_score`, `H4_trend_regime`, and `H1_trend_regime` when those values are absent. It then calls the recovered Brain directly with `similarity=None`.

This is a concrete example of generated numeric MTF values in a legacy integration path, not proof that this is the canonical producer encoding. The code also uses MTF context to produce Brain directional bias. It therefore cannot be treated as Murphy-only direction authority.

## 5. Volume lineage remains a separate unresolved compatibility gap
- The recovered Brain reads `volume_available` and six `*_volume_regime` fields and can add bullish evidence when the mean volume regime is positive.
- `BACKTEST/mtf_source_contract_gate_v1.py` does not require or validate any volume-regime fields.
- `audits/evidence/MARKET_STATE_VOLUME_LINEAGE_COMPATIBILITY_2026-08-21.md` identifies an existing 2020–2024 M1-derived volume source but records the compatibility and propagation mapping into Market State as open.
- The six-timeframe MTF alignment evidence pack documents trend-regime fields; it does not by itself close the producer/encoding/availability contract for the Brain's six volume-regime fields.

Conclusion: volume-derived direction in the recovered Brain is not source-lineage-closed.

## 6. Caller enumeration status
The exact branch tree identifies the following distinct inspected paths:
- Gate 3C event builder -> `brain_row` -> `gate3c_single_event_e2e_v1.py` -> `full_brain_runtime_bridge_v1.py` -> assembler -> governed adapter -> recovered Brain.
- Legacy `BACKTEST/decision_brain_integration_gate_v1.py` -> recovered Brain directly with Similarity disabled.
- Historical `OOS_2025/full_decision_brain_historical_event_producer_v1.py` -> assembler directly with a market-context row, not the public runtime bridge.
- `OOS_2025/full_brain_input_producer_v1.py` normalizes separate context/Murphy/Nison/Risk/execution streams; it does not itself establish MTF-to-Murphy lineage.

This is a branch-aware path inspection, not an exhaustive whole-repository call graph. GitHub code search available through the connector is default-branch indexed; no claim is made that all indirect/dynamic callers across every file have been enumerated.

## 7. Current authority disposition
- Similarity directional isolation on the two governed adapters: code change present; tests not run.
- Murphy authority in Gate 3C wrapper: enforced before bridge call.
- Murphy authority in bridge itself: not enforced.
- MTF six-timeframe source existence: established.
- MTF numeric encoding/producer semantics: unresolved.
- MTF fields' derivation from Murphy: not proven.
- Volume-regime producer and encoding into Brain: unresolved.
- Brain direction remains generated from MTF/volume fields and then checked against Murphy; this is not a Murphy-only direction architecture.

## Next safe action
Do not modify frozen Brain semantics or the bridge yet. First close the field-level contract for:
1. the seven numeric MTF fields consumed by Brain, including producer, encoding, timestamp/as-of and missing-value semantics;
2. the six volume-regime fields plus `volume_available`, including source availability and propagation;
3. the approved authority model: either prove these fields are Murphy-derived with immutable provenance, or formally designate Murphy as sole directional authority and make Brain's directional output non-authoritative at the decision boundary.

Only after that decision should bridge-level negative tests be added against the exact approved Murphy/Nison evidence schemas.

## Guardrails
No source/runtime code modified. No PR or merge. No main changes. No workflow dispatch or CI run. No Dropbox. No 2025/2026 market-data payload access. No tuning. 2025 remains locked OOS. No live trading or automatic orders enabled.
