# Nison 44-Rule Source → Operator Batch Matrix V1

Status: WORKING BATCH MATRIX — NOT A FREEZE MANIFEST

Purpose: process all 44 Nison rules in one batch without rewriting rules or inventing operators. Source/registry fields are taken from the project queue. Missing source definitions remain explicitly unresolved.

## Governance
- Nison = confirmation only; never creates direction alone.
- Source → operator → evaluator → tests → 2016–2024 QA → availability/no-lookahead → freeze.
- No invented numeric thresholds, tolerances, lookbacks, or proxies.
- 2025 is OOS and excluded from tuning/selection/operator choice.
- Existing evaluators/components are reused; no rebuild of the Decision Brain.

## Batch rows

| Rule | Setup | Current source status | Shared operator family | Next action |
|---|---|---|---|---|
| 0001 | Bullish Engulfing | Definition incomplete in queue | CANDLE_2_BODY_ENGULF | Source reconciliation |
| 0002 | Bearish Engulfing | Definition incomplete in queue | CANDLE_2_BODY_ENGULF | Source reconciliation |
| 0003 | Dark Cloud Cover | Definition incomplete in queue | CANDLE_2_GAP_PENETRATION | Source reconciliation |
| 0004 | Piercing Pattern | Definition incomplete in queue | CANDLE_2_GAP_PENETRATION | Source reconciliation |
| 0005 | On Neck | Definition incomplete in queue | CANDLE_2_NECKLINE | Source reconciliation |
| 0006 | In Neck | Definition incomplete in queue | CANDLE_2_NECKLINE | Source reconciliation |
| 0007 | Thrusting | Definition incomplete in queue | CANDLE_2_NECKLINE | Source reconciliation |
| 0008 | Morning Star | Definition incomplete in queue | CANDLE_3_STAR | Source reconciliation |
| 0009 | Evening Star | Definition incomplete in queue | CANDLE_3_STAR | Source reconciliation |
| 0010 | Morning Doji Star | Definition incomplete in queue | CANDLE_3_DOJI_STAR | Source reconciliation |
| 0011 | Evening Doji Star | Definition incomplete in queue | CANDLE_3_DOJI_STAR | Source reconciliation |
| 0012 | Abandoned Baby | Definition incomplete in queue | CANDLE_3_GAP_STAR | Source reconciliation |
| 0013 | Harami | Definition incomplete in queue | CANDLE_2_INSIDE_BODY | Source reconciliation |
| 0014 | Harami Cross | Definition incomplete in queue | CANDLE_2_INSIDE_DOJI | Source reconciliation |
| 0015 | Tweezers Top | Definition incomplete in queue | CANDLE_2_EXTREME_MATCH | Source reconciliation |
| 0016 | Tweezers Bottom | Definition incomplete in queue | CANDLE_2_EXTREME_MATCH | Source reconciliation |
| 0017 | Upside Gap Two Crows | Definition incomplete in queue | CANDLE_3_GAP_SEQUENCE | Source reconciliation |
| 0018 | Three Black Crows | Definition incomplete in queue | CANDLE_3_SEQUENCE | Source reconciliation |
| 0019 | Bullish Counterattack Lines | Definition incomplete in queue | CANDLE_2_COUNTERATTACK | Source reconciliation |
| 0020 | Bearish Counterattack Lines | Definition incomplete in queue | CANDLE_2_COUNTERATTACK | Source reconciliation |
| 0021 | Three Mountains | Definition incomplete in queue | SWING_PATTERN_3 | Source reconciliation |
| 0022 | Three Rivers | Definition incomplete in queue | SWING_PATTERN_3 | Source reconciliation |
| 0023 | Three Buddha Tops | Definition incomplete in queue | SWING_PATTERN_3_TOP | Source reconciliation |
| 0024 | Three Buddha Bottoms | Definition incomplete in queue | SWING_PATTERN_3_BOTTOM | Source reconciliation |
| 0025 | Dumpling Top | Definition incomplete in queue | ROUNDING_TOP | Source reconciliation |
| 0026 | SOURCE RECORD NOT RETRIEVED | Queue excerpt does not expose setup name | UNKNOWN | Recover authoritative registry row; do not invent |
| 0027 | Tower Top | Definition incomplete in queue | TOWER_PATTERN | Source reconciliation |
| 0028 | Tower Bottom | Definition incomplete in queue | TOWER_PATTERN | Source reconciliation |
| 0029 | Unique Three River Bottom | Definition incomplete in queue | CANDLE_3_RIVER | Source reconciliation |
| 0030 | SOURCE RECORD NOT RETRIEVED | Queue excerpt does not expose setup name | UNKNOWN | Recover authoritative registry row; do not invent |
| 0031 | SOURCE RECORD NOT RETRIEVED | Queue excerpt does not expose setup name | UNKNOWN | Recover authoritative registry row; do not invent |
| 0032 | Three White Soldiers | Definition incomplete in queue | CANDLE_3_SEQUENCE | Source reconciliation |
| 0033 | Advance Block (Stalled Pattern) | Definition incomplete in queue | CANDLE_3_STALL | Source reconciliation |
| 0034 | Separating Lines | Definition incomplete in queue | CANDLE_2_SEPARATION | Source reconciliation |
| 0035 | Tasuki Gap | Ready for backtest; evaluator/tests exist | TASUKI_WINDOW_SEQUENCE | Reuse evaluator; resolve qualitative body-size comparator |
| 0036 | Gapping Play | Ready for backtest; structural evaluator/tests exist | WINDOW_CONGESTION_SEQUENCE | Reuse evaluator; resolve qualitative sharp/small-body/congestion contracts |
| 0037 | Side-by-Side White Lines | Ready for backtest; structural evaluator/tests exist | WINDOW_SEQUENCE | Reuse evaluator; resolve same-open/similar-body contracts |
| 0038 | Windows | Ready for backtest; evaluator/tests/replay exist | WINDOW_EVIDENCE | Compatibility sign-off + freeze manifest |
| 0039 | 06_Multiple_Technical_Techniques | Definition incomplete in queue | CONFLUENCE | Recover source definition |
| 0040 | 13_Candlestick_Clusters | Definition incomplete in queue | CLUSTER_CONTEXT | Recover source definition |
| 0041 | 14_Trend_Lines | Definition incomplete in queue | TRENDLINE_CONTEXT | Recover source definition |
| 0042 | 15_Support_Resistance | Definition incomplete in queue | SUPPORT_RESISTANCE_CONTEXT | Recover source definition |
| 0043 | 16_False_Breakouts | Definition incomplete in queue | FALSE_BREAKOUT_CONTEXT | Recover source definition |
| 0044 | 17_Polarity_Principle | Definition incomplete in queue | POLARITY_CONTEXT | Recover source definition |

## Immediate batch execution order

### Batch A — already operational artifacts
0035–0038 are processed first because evaluators/tests already exist. Do not rebuild them. Current evidence says 0038 is a freeze candidate; 0035–0037 remain partially/qualitatively blocked. Historical QA is blocked until canonical D1 bytes are available to the runtime.

### Batch B — shared two-candle primitives
0001–0007, 0013–0016, 0019–0020, 0034. Reconcile source semantics first, then implement/reuse shared primitives rather than separate engines.

### Batch C — three-candle sequence primitives
0008–0012, 0017–0018, 0029, 0032–0033. Reconcile exact sequence, gap, body, and context semantics before evaluation.

### Batch D — swing/shape/context patterns
0021–0025, 0027–0028, 0039–0044. These require source definition before deterministic evaluation.

### Batch E — unresolved registry rows
0026, 0030, 0031. Recover authoritative rule records before assigning names or operators.

## Current hard blockers
1. Canonical D1 runtime bytes for full 2016–2024 replay.
2. Source definitions for the incomplete queue rules.
3. Qualitative comparator contracts for 0035–0037.
4. Canonical compatibility sign-off/freeze manifest for 0038.

## No false completion rule
A rule is not Frozen merely because an evaluator file or unit test exists. Historical QA and availability/no-lookahead gates remain required.
