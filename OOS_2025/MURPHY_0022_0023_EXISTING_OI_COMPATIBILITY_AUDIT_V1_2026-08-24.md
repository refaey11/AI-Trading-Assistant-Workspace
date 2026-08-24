# Murphy 0022/0023 — Existing OI Compatibility Audit V1

Date: 2026-08-24
Branch: `evidence-architecture-v1`

## Finding
The project already contains a source-locked Open Interest evidence path for Murphy 0022/0023. Do not acquire or rebuild a replacement OI module merely because the current 2025 coverage snapshot shows zero available OI rows.

## Existing evidence
- OI source scope: CME British Pound futures `096742` (not spot FX OI).
- Historical development population: 2020–2024.
- Availability alignment is explicitly recorded in the project handoff.
- Murphy 0022 semantics: price UP + volume UP + available futures OI UP => bullish.
- Murphy 0023 semantics: price DOWN + volume UP + available futures OI UP => bearish.
- No proxy OI; no added thresholds; dynamic MTF policy.
- Existing unit tests cover PASS, wrong-OI, wrong-price, and missing-OI cases.
- Existing historical evaluation artifacts cover 2020–2024.

## Compatibility with Evidence Architecture V1
COMPATIBLE:
- futures OI remains the required evidence source;
- availability/alignment is already part of the existing evidence path;
- missing evidence remains NOT_EVALUABLE / fail-closed;
- rule semantics remain unchanged;
- 2025 remains OOS and is not used for tuning.

## Current gap
The current 2025 coverage stream contains 6,216 rows for 0022 and 0023 but all are NOT_EVALUABLE because no 2025 OI evidence is attached. This is a producer/evidence coverage gap, not a Murphy semantics or evaluator gap.

## New CME PDF received
A CME PG01B FX Daily Bulletin PDF for Fri 2026-08-21 was supplied and confirms the correct source family and product line: `BP BRITISH POUND FUTURE`, with Open Interest shown in the FX futures summary. It is a parser/source validation sample only; it is not historical 2025 evidence.

## Decision
1. Reuse the existing 2020–2024 OI evidence for historical QA and any non-OOS evaluation where it is valid.
2. Do not replace it with spot FX OI or tick-volume proxies.
3. Do not claim 2025 0022/0023 coverage until a source-backed 2025 futures-OI stream is attached through the evidence boundary.
4. The next technical step is to bind the existing OI evidence contract into the new point-in-time evidence adapter and then separately source/attach 2025 OI evidence.

## Provenance references
- `MURPHY_0021_0023_EVALUATOR_CONTRACT_V1.json`
- `MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`
- `MURPHY_0021_0023_HISTORICAL_SUMMARY_V1.csv`
- `MURPHY_12_FROZEN_CONTINUITY_BACKUP_V1.json`

This audit does not claim the 2025 producer is complete and does not change any rule semantics.