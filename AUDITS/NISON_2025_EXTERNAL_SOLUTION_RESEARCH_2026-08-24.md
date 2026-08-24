# Nison 2025 External Solution Research — 2026-08-24

## Objective
Find an external or existing tool that can reduce the current Nison 2025 upstream-evidence gap without replacing the canonical Nison runtime, changing rule semantics, inventing thresholds, or using 2025 for tuning.

## Findings

### 1. Nison Candle Scanner (CandleCharts / Steve Nison)
CandleCharts states that Nison Candle Scanner was designed by Steve Nison to identify his candlestick patterns and offers scanning/alerts with standard and strict criteria. The TradingView version advertises 28 candle patterns and an Intraday/FX/Crypto module. Sources:
- https://specials.candlecharts.com/ncs-tv/
- https://specials.candlecharts.com/ncs-ninjatrader/
- https://candlecharts.com/product-details/nison-candle-scanner/

Potential value: strongest external candidate for pattern-formation candidate evidence because it is explicitly a Nison-branded scanner.

Hard limitation: the public material reviewed does not establish a machine-readable API/export contract for all required project facts (formation_complete, formation_confirmed, previous_session/current_session, role, methodology evidence, or categorical qualitative facts). Therefore it cannot be promoted to authoritative Decision Brain evidence without an explicit compatibility audit and reproducible export mapping.

### 2. CandleKit / py-candlekit
CandleKit advertises 20+ classic patterns, including Rising/Falling Three Methods and Mat Hold, with pandas integration and Nison as one of its academic sources. However, it is a third-party implementation and does not establish equivalence with the project's frozen source contracts.
Sources:
- https://github.com/zhirodadkhah/CandleKit
- https://pypi.org/project/py-candlekit/

Potential value: candidate cross-check / diagnostic oracle only.

Hard limitation: not authoritative Nison evidence and not sufficient for context/methodology facts.

### 3. CandleScanner (third-party)
CandleScanner reports 104 patterns and allows intraday data import, but its public documentation says its scanning logic was influenced by multiple authors including Nison, Bulkowski, Morris and Shimizu.
Source:
- https://www.candlescanner.com/candlestick-patterns/patterns-supported-by-candlescanner/

Potential value: broad pattern coverage comparison.

Hard limitation: mixed-source semantics make it unsuitable as canonical Nison evidence without rule-by-rule reconciliation.

### 4. Other open-source detectors
Open-source JavaScript/Python libraries provide subsets of Nison-style patterns, but generally operate on OHLC shape and do not supply the project-specific context/methodology evidence required by NISON_0021..0031 and NISON_0038..0044.
Examples:
- https://github.com/cm45t3r/candlestick
- https://pypi.org/project/japanese-candlestick/

## Architectural decision
Do NOT replace the existing Nison runtime with an external detector.

Use external tools only in one of two ways:
1. Candidate upstream evidence producer for a narrow, explicitly mapped rule contract, followed by compatibility QA.
2. Independent diagnostic/cross-check oracle that can identify where the current upstream evidence path is missing.

The canonical Nison runtime remains authoritative. NOT_EVALUABLE remains fail-closed when authoritative evidence is absent.

## Best external lead
The Nison Candle Scanner is the highest-priority external lead because it is explicitly designed by Steve Nison and provides strict/intraday/FX pattern scanning. However, it is a commercial platform product and public documentation does not establish an export/API contract suitable for direct automated integration. Therefore the next step is not purchase or integration; it is to determine whether an accessible export/API exists and whether its pattern outputs can be mapped to the project's frozen rule IDs.

## Project impact
This research does not change any runtime behavior. 2025 remains evaluation-only. No thresholds or semantics were modified.

## Sources
Web research performed 2026-08-24:
- Steve Nison / CandleCharts Nison Candle Scanner pages: see URLs above.
- CandleKit / third-party pattern libraries: see URLs above.
