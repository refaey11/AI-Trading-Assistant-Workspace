# GBPUSD 2025 Market-State / Volume Compatibility Audit — 2026-08-22

## Result
**ADAPTER_REQUIRED / NOT OOS-READY**

## Verified source finding
The uploaded `HISTDATA_COM_MT_GBPUSD_M12025.zip` contains a 7-column M1 source with the final column present but equal to `0` for all 371,091 rows. The raw file was not modified.

## Existing project contract
`compatibility/market_state_contract_adapter_v1.py` currently treats any explicitly supplied non-null `volume` as `volume_evaluable=True`. It does not define `0` as unavailable.

## Compatibility conclusion
For this 2025 source, passing the raw zero-valued field directly into the current Market-State contract would incorrectly classify the source volume as usable. Therefore the source-to-contract boundary needs an explicit provenance-aware interpretation for this dataset before the 2025 OOS stream proceeds.

## Guardrails
- Do not synthesize volume.
- Do not convert the zero field into directional evidence.
- Do not modify the raw 2025 source.
- Do not tune, calibrate, or select thresholds using 2025.
- Do not silently deduplicate timestamps.

## Required next step
Recover the existing project-approved volume source/semantics for the 2020–2025 period (if available), then implement the smallest boundary adapter needed to mark this HistData field as unavailable unless that source is explicitly mapped by an existing contract. Re-run the Market-State contract tests before allowing 2025 into the frozen 78-rule OOS path.
