# Nison 0001-0038 D1 Structural Replay V1

Date: 2026-08-18
Dataset: uploaded D1(3).csv
Rows: 2,544
Period: 2016-01-03 through 2024-12-31
2025: excluded

## Runtime result
| Rule | Structural candidates | Status gate |
|---|---:|---|
| 0001 Bullish Engulfing | 206 | Context/qualitative gates unresolved |
| 0002 Bearish Engulfing | 197 | Context/qualitative gates unresolved |
| 0003 Dark Cloud Cover | 1 | Qualitative long-body gate unresolved |
| 0004 Piercing Pattern | 2 | Qualitative long-body gate unresolved |
| 0005 On Neck | 25 | Context + long/near gates unresolved |
| 0006 In Neck | 8 | Context + long/slightly gates unresolved |
| 0007 Thrusting | 8 | Context + long/well-into gates unresolved |
| 0008 Morning Star | 84 | Context + long/small gates unresolved |
| 0009 Evening Star | 101 | Context + long/small gates unresolved |
| 0010 Morning Doji Star | 0 | Context/strength/gap gates unresolved |
| 0011 Evening Doji Star | 0 | Context/strength/gap gates unresolved |
| 0012 Abandoned Baby | 0 | Qualitative/isolated-gap gates unresolved |
| 0013 Harami | 428 | Context + size gates unresolved |
| 0014 Harami Cross | 0 | Context + size gates unresolved |
| 0015 Tweezers Top | 1 | Nearly-equal/context/confirmation unresolved |
| 0016 Tweezers Bottom | 3 | Nearly-equal/context/confirmation unresolved |
| 0017 Upside Gap Two Crows | 0 | Context/qualitative gates unresolved |
| 0018 Three Black Crows | 109 | Context/shape gates unresolved |
| 0019 Bullish Counterattack | 0 | Context/qualitative gates unresolved |
| 0020 Bearish Counterattack | 0 | Context/qualitative gates unresolved |
| 0021 Three Mountains | 0 | Context/resistance/confirmation unresolved |
| 0022 Three Rivers | 0 | Context/support/confirmation unresolved |
| 0023 Three Buddha Tops | 86 | Context unresolved |
| 0024 Three Buddha Bottoms | 94 | Context unresolved |
| 0025 Dumpling Top | 16 | Context/rounded-shape qualitative gates unresolved |
| 0026 Fry Pan Bottom | 1 | Context/rounded-shape qualitative gates unresolved |
| 0027 Tower Top | 205 | Context/long/consolidation gates unresolved |
| 0028 Tower Bottom | 218 | Context/long/consolidation gates unresolved |
| 0029 Unique Three River Bottom | 3 | Context/size gates unresolved |
| 0030 Three Rising Methods | 4 | Context/size gates unresolved |
| 0031 Three Falling Methods | 3 | Context/size gates unresolved |
| 0032 Three White Soldiers | 172 | Stabilization/shape gates unresolved |
| 0033 Advance Block | 113 | Context/long-body gates unresolved |
| 0034 Separating Lines | 0 | Exact structural contract: NO_MATCH |
| 0035 Tasuki Gap | reuse existing evaluator/replay | Existing evidence; do not rebuild |
| 0036 Gapping Play | reuse existing evaluator/replay | Existing evidence; do not rebuild |
| 0037 Side-by-Side White Lines | reuse existing evaluator/replay | Existing evidence; do not rebuild |
| 0038 Windows | reuse existing evaluator/replay | Existing evidence; do not rebuild |

## Governance
This is a structural replay using the existing project runtime logic against the newly supplied D1 dataset. Structural candidates are not PASS/FREEZE claims. No qualitative source term was converted into an invented numeric threshold. 2025 remains OOS and is excluded. Existing 0035-0038 evaluator/replay artifacts are reused rather than replaced.

## Important implementation note
The current structural script is an existing project artifact and is being treated as a structural scan, not as final Nison canonicalization. Confirmation, invalidation, context, availability, and no-lookahead gates must still be evaluated before any rule can be Frozen.