# PR #119 Compatibility Audit — 2026-11-16

## Scope
Focused compatibility review of the timestamp remediation branch. This record does not promote the branch to production and does not authorize a merge.

## Timestamp provenance
- The MTF-to-Brain join already rejects naive timestamps and normalizes explicit offsets to UTC.
- The Gate 3C E2E runner still had a direct `pd.Timestamp(value, tz="UTC")` path and `pd.to_datetime(..., utc=True)` row parsing. Those paths could assign UTC to naive values or bypass the explicit-source-timezone rule. They now use an aware-only parser and reject invalid, naive, and mixed source rows.
- The six-timeframe MTF source gate and its source-acquisition workflow also used `utc=True` directly. They now use one shared aware-only parser and reject unresolved source timezone provenance.
- These changes do not infer broker time, local time, DST, or candle-close semantics.

## Six-timeframe MTF compatibility
- The governed timeframe family remains M5, M15, M30, H1, H4 and D1.
- Existing 2020–2024 as-of alignment evidence reports no future mappings in the tested chain. That evidence is not equivalent to proof of source timezone provenance, exact producer encoding, or a live six-timeframe producer.
- The existing MTF provenance blocker still requires the exact serialized feature contract and source lineage. No categorical-to-numeric mapping, imputation, scaling, timeframe hierarchy, or direction is added here.
- The strict source gate will now return NOT EVALUABLE for naive timestamps rather than silently treating them as UTC.

## Canonical risk compatibility
- The canonical Risk Engine owns the 3R minimum and its exact-boundary tolerance.
- The separate frozen candidate/evaluation adapter retains its documented 0.75 ATR / 2R protocol; it is not redefined as the canonical risk contract.
- The development bridge previously accepted an executable result even when the execution adapter's generated stop/target differed from the canonical Risk result. A narrow guard now blocks that development result unless the execution levels match the canonical Risk output and its RR is at least the canonical minimum.
- No new stop/target formula is introduced. The frozen OOS candidate adapter and OOS data are not modified.

## Trading in the Zone boundary
- The project decision dated 2026-11-12 makes TIZ optional audit metadata only.
- TIZ cannot generate or influence direction, confirmation, confidence, risk, or execution eligibility. Missing, FAIL, NOT_EVALUABLE, and arbitrary TIZ states remain non-blocking metadata.
- Existing compatibility tests cover the metadata-only boundary and preserve the independent Risk hard gate. No psychological threshold or synthetic TIZ PASS is introduced.

## Validation boundaries
- Added synthetic-only tests for Gate 3C timestamp provenance, the six-timeframe source gate, and the development canonical-risk execution-level guard.
- CircleCI already runs the expanded timestamp test module in both configured jobs; GitHub Actions TIZ and risk workflows are also wired to run it.
- No 2025 data is read or used. No expensive backtest, live order, or broker execution is run.
- Compile/unit success alone does not establish producer provenance, broker timezone semantics, complete timeframe resolution, production risk authorization, or trading readiness.
