# Decision Brain MTF / Volume Authority Follow-up — 2026-11-25

## Scope
Read-only GitHub inspection on branch `fix/similarity-direction-isolation-2026-11-25` at parent HEAD `5725b52593678c7c0df14aca6548c8b07c7d7962`.

No market-data payloads were opened. No 2025/2026 data was accessed. No runtime/source code or tests were changed or executed.

## 1. Volume producer and Market State boundary

### Repository evidence
The recursive Git tree contains volume-related audit records, but no committed `VOLUME_CONFIRMATION_V2` producer source or six-timeframe `*_volume_regime` producer/adapter implementation was found in the inspected branch tree.

The existing volume audit records describe prior inspection of local/archived artifacts labelled `M1_TitanFX_2020_2024`, including derived volume for M5/M15/M30/H1/H4 and D1. Those records are historical evidence only; the producer code and exact serialization contract are not present in the inspected GitHub branch.

### Market State adapter
`compatibility/market_state_contract_adapter_v1.py`:
- requires `volume` as an explicitly supplied optional source value for availability;
- sets `volume_evaluable = (volume is not None)`;
- maps unavailable volume to `volume_state = UNKNOWN`;
- does not emit `volume_available` or any of the six `*_volume_regime` fields;
- does not distinguish numeric zero from unavailable when a non-null zero is supplied.

Its tests cover non-null volume, missing volume, missing required fields, and invalid trend tokens, but do not test zero-as-unavailable provenance or production of Brain's six volume-regime fields.

### Brain contract
`RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py` reads volume only when `row["volume_available"]` is truthy, then averages any present `M5/M15/M30/H1/H4/D1_volume_regime` values. No inspected canonical adapter establishes the producer, encoding, scaling, missing policy, or timeframe alignment for those fields.

**Conclusion:** 2020–2024 upstream volume artifacts are documented as existing, but the GitHub branch does not establish a source-backed path from those artifacts through Market State into the Brain's six volume-regime fields. Volume-to-Brain lineage remains OPEN / NOT EVALUABLE. Do not infer that the Brain is receiving valid volume confirmation.

## 2. MTF source and encoding

The six-timeframe MTF Alignment source family is confirmed by existing evidence records and exposes M5/M15/M30/H1/H4/D1 trend-regime features plus `mtf_trend_score`. The MTF join adapter performs backward as-of selection and numeric validation only. The source contract gate explicitly does not translate categories, impute, scale, or generate direction.

However, the inspected GitHub evidence does not close the exact numeric semantics/encoding contract for all seven Brain fields. `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md` explicitly records unresolved raw-to-feature semantics, categorical encoding, missing-value policy, scaling, producer lineage, and timestamp semantics. The older `BACKTEST/decision_brain_integration_gate_v1.py` contains an inline mapping from `BULL_TREND/BEAR_TREND/TRANSITION/UNKNOWN` to numeric values, but this is a legacy caller mapping and is not proof of the canonical MTF producer encoding.

**Conclusion:** MTF source-family existence is CONFIRMED; exact producer numeric semantics and field-level Murphy lineage remain OPEN.

## 3. Canonical Gate 3C row construction

`tools/gate3c_build_single_event_bundle_v1.py` selects an as-of Market State row and an as-of MTF row, then constructs:

```python
brain_row = {**market, **mtf}
```

This preserves all fields from both rows, with MTF keys taking precedence on collisions. It does not whitelist the Brain's directional fields or attach field-level Murphy provenance to them. Therefore any matching fields present in either source row could flow into the Brain input without this builder proving their semantic authority.

The builder separately creates Murphy evidence and a Risk direction/pass-rule linkage. That linkage proves the Risk/Murphy direction contract at the event-envelope level; it does not prove that the MTF or volume fields used inside Brain were themselves derived from that same Murphy evidence.

## 4. Decision Brain directional authority

The recovered Brain's directional bias/confidence can be influenced by:
- `mtf_trend_score`;
- the six trend-regime fields;
- the six volume-regime fields when `volume_available` is true;
- optional Similarity when a caller passes a non-null argument (the aligned knowledge handoff was remediated to pass `None`, but the recovered Brain still contains the optional path).

The canonical Gate 3C caller checks Murphy authority/status, Nison's 44-rule envelope, and Murphy/Risk direction/provenance agreement before invoking the bridge. The bridge itself only checks presence of evidence and Risk authority; it does not independently enforce Murphy/Nison authority/provenance. Gate 3C's upstream validation is therefore a caller-specific protection, not a complete direct-call contract inside the bridge.

Inspected bridge call-site paths show Gate 3C as the runtime bridge caller. The historical OOS producer and assembler call the assembler/governed handoff directly rather than the runtime bridge. This is a focused caller review, not a claim that every dynamic/indirect repository call path has been exhaustively enumerated.

## 5. Required decision before code changes

Do not change the frozen Brain, bridge, or MTF producer until the project formally chooses and documents one authority model:

A. **Murphy-lineage proof:** every Brain directional MTF/volume field must have a source-backed, point-in-time mapping to the exact governed Murphy direction evidence, with producer, encoding, availability, and timestamp contracts; or

B. **Murphy sole direction authority:** Brain's MTF/volume outputs become non-authoritative context/evidence and cannot generate or alter the final directional bias; Murphy alone supplies direction, with Nison confirmation/contradiction and Risk hard gate.

No architecture choice is made by this audit.

## Status
- Similarity directional isolation in the aligned knowledge handoff: code change recorded; regression test not yet executed.
- Six-timeframe MTF artifact existence: CONFIRMED.
- MTF numeric producer semantics/encoding: OPEN.
- Volume source artifact history: documented; GitHub producer-to-Brain contract: OPEN.
- Gate 3C event-level Murphy/Risk linkage: implemented and inspected.
- Brain direction demonstrably Murphy-only: NOT PROVEN.
- Bridge standalone authority enforcement: GAP.
- Runtime tests/workflows: NOT RUN in this continuation.
- 2025 OOS: untouched and remains locked.

## Next safe step
Complete a field-level contract matrix for the seven MTF fields and six volume fields from GitHub-tracked producer/adapter code only. Where producer source is absent, record the field as NOT EVALUABLE rather than reconstructing or guessing its encoding. Then obtain an explicit architecture decision (A or B) before any runtime change.
