# Nison 44 Rule Source / Runtime Audit — 2026-08-22

## Scope
Audit the existing 44 Nison entries without rebuilding them. Preserve source contracts, treat 2025 as locked OOS, and do not invent missing semantics.

## Authoritative project inventory
- Nison execution scope: 44.
- Registry composition: 38 candlestick rules + 6 context modules.
- Development period: 2016–2024.
- 2025: LOCKED OOS.
- Current freeze state from existing governance artifacts: 0 production_frozen, 44 pre_freeze.
- Freeze review ready: 15.
- Open QA: 29.

## Key source findings
- The Nison 44 execution package explicitly requires source-backed contracts and says source-blocked rules remain blocked.
- The Nison 44 governance manifest says auto-freeze is false and no production freeze has been reached.
- The existing candle confirmation ZIP is an engineering prototype, not an exact reproduction of Steve Nison. Its deterministic pattern list contains 9 operational pattern labels; the package itself requires source-context mapping before canonical treatment.
- The existing context engine is also an operational prototype and explicitly states its thresholds are not canonical Nison thresholds.

## Important distinction
The 44 Rule work is valuable and preserved. However, the 44 entries are not currently equivalent to 44 authoritative Runtime producers. PRE_FREEZE means the rule artifacts exist and have governance records; Runtime promotion requires source-backed semantics, deterministic evaluator/adapter evidence, relevant tests, and appropriate QA.

## Current 44-rule status model
- PRE_FREEZE: 44 / 44.
- Production frozen: 0 / 44.
- Freeze review ready: 15 / 44.
- Open QA: 29 / 44.

## Immediate mapping strategy
For each rule: source rule_id/name -> formation/context contract -> directional implication (confirmation only) -> invalidation/conflict -> evidence availability/provenance -> evaluator -> adapter -> tests -> 2016–2024 QA -> no-lookahead -> freeze gate.

## Rules with known source-closure caveats from the current closure gate
The closure artifact explicitly marks some entries SOURCE_PARTIAL or MODULE_SOURCE_ONLY, including but not limited to Harami Cross, Bullish/Bearish Counterattack Lines, Three Buddha Tops/Bottoms, Fry Pan Bottom, Tower Top/Bottom, Unique Three River Bottom, Three White Soldiers, Advance Block, Separating Lines, Tasuki Gap, Gapping Play, Side-by-Side White Lines, Windows, and the six technical/context modules 39–44.

## Prototype boundary
The existing operational candlestick engine currently recognizes a smaller subset (Doji, Hammer, Shooting Star-like, Bullish/Bearish Engulfing, Bullish/Bearish Harami, Morning/Evening Star-like). This must not be interpreted as evidence that only those Nison 9 exist; it is evidence that the prototype detector is narrower than the 44-rule registry.

## Decision
Do not discard or rebuild the 44 rules. Continue with source-mapped audit and promote only when the applicable production gates are directly evidenced. Never use 2025 for tuning, calibration, threshold selection, or operator selection.
