# Time and Multi-Timeframe Context Recovery Audit — 2026-08-21

## Scope
Recover evidence for the market pipeline's time/timeframe context before claiming a full end-to-end Decision Brain chain.

## Source evidence reviewed
- `AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip`
  - `CONTRACT.json`
  - `README.md`
- `AI_Trading_Assistant_MARKET_READER_V1.zip`
  - `MARKET_READER_SCHEMA.md`
  - `MARKET_READING_OUTPUT_TEMPLATE.json`
- Active GitHub tree search for `time context`, `dynamic timeframe`, `session`, and the six runtime fields.

## Findings
1. Multi-Timeframe Reader V1 is explicitly evidenced as a real module.
2. Its original V1 contract is H4 higher-timeframe context plus H1 local structure.
3. The contract explicitly says M15 was not implemented from H1 and must not be fabricated.
4. The current `decision_brain.py` recovered from Dropbox accepts six timeframe fields: M5, M15, M30, H1, H4, D1.
5. Therefore the six-timeframe runtime is newer/different from the original MTF Reader V1 contract and must not be retroactively attributed to that V1 contract without provenance.
6. Market Reader V1 carries a `timeframe` field, but this alone does not prove a separate session/time-of-day or dynamic-timeframe runtime context.
7. Active GitHub search did not recover a distinct `Time Context`, `Session Context`, or `Dynamic Timeframe Context` runtime/contract.

## Governance decision
- Six-timeframe evidence in `decision_brain.py`: AVAILABLE, but provenance-to-source-pipeline requires explicit contract recovery.
- Original MTF Reader V1: AVAILABLE and evidenced for H4/H1 only.
- M15 fabrication prohibition: HARD COMPATIBILITY CONSTRAINT.
- Separate Time/Session Context: NOT YET RECOVERED.
- Dynamic Timeframe Context: NOT YET RECOVERED.
- No synthetic session/dynamic-timeframe rules may be invented to close this gap.

## Next required action
Recover the exact newer six-timeframe source contract/data pipeline, or mark the Decision Brain six-timeframe fields as externally supplied inputs with provenance metadata before a full end-to-end PASS is declared.

## OOS constraint
2025 remains out-of-sample and must not be used for tuning this recovery or compatibility work.
