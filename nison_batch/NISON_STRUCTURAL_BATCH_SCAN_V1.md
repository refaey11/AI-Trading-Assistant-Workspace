# Nison Structural Batch Scan V1

Date: 2026-08-18
Dataset: GBPUSD D1, 2016-2024, 2,544 rows. 2025 excluded.
Source: MASTER_CANDIDATE_RULES_V1 + Nison Formation_Rules in MASTER_KB.

## Purpose
Run one source-grounded structural scan across Nison Rules 0001-0038 using the existing OHLC runtime data. This is NOT a full PASS/FREEZE evaluation.

## Results
| Rule | Structural candidates | Canonical state | Remaining gates |
|---|---:|---|---|
| 0001 Bullish Engulfing | 206 | NOT_EVALUABLE | downtrend/context + confirmation |
| 0002 Bearish Engulfing | 197 | NOT_EVALUABLE | uptrend/context + confirmation |
| 0003 Dark Cloud Cover | 1 | NOT_EVALUABLE | long-body comparator + trend/context |
| 0004 Piercing Pattern | 2 | NOT_EVALUABLE | long-body comparator + trend/context |
| 0005 On Neck | 25 | NOT_EVALUABLE | long/near qualitative + trend |
| 0006 In Neck | 8 | NOT_EVALUABLE | long/slightly qualitative + trend |
| 0007 Thrusting | 8 | NOT_EVALUABLE | long/well-into qualitative + trend |
| 0008 Morning Star | 84 | NOT_EVALUABLE | long/small + trend |
| 0009 Evening Star | 101 | NOT_EVALUABLE | long/small + trend |
| 0010 Morning Doji Star | 0 | NO_MATCH structural scan | confirmation/strength still source-dependent |
| 0011 Evening Doji Star | 0 | NO_MATCH structural scan | confirmation/strength still source-dependent |
| 0012 Abandoned Baby | 0 | NO_MATCH structural scan | gap/session semantics |
| 0013 Harami | 428 | NOT_EVALUABLE | long/small + trend |
| 0014 Harami Cross | 0 | NO_MATCH structural scan | trend/long-body gate |
| 0015 Tweezers Top | 1 | NOT_EVALUABLE | nearly-equal comparator + trend + confirmation |
| 0016 Tweezers Bottom | 3 | NOT_EVALUABLE | nearly-equal comparator + trend + confirmation |
| 0017 Upside Gap Two Crows | 0 | NOT_EVALUABLE | trend/long/gap semantics |
| 0018 Three Black Crows | 109 | NOT_EVALUABLE | trend/near-low/shadow qualitative |
| 0019 Bullish Counterattack | 0 | NO_MATCH structural scan | long/well-below/near-equal close |
| 0020 Bearish Counterattack | 0 | NO_MATCH structural scan | long/gap/approx-equal close |
| 0021 Three Mountains | 0 exact-equal triple | NOT_EVALUABLE | approximate resistance + bearish confirmation |
| 0022 Three Rivers | 0 exact-equal triple | NOT_EVALUABLE | approximate lows + support/confirmation |
| 0023 Three Buddha Tops | 86 | NOT_EVALUABLE | trend + resistance/context |
| 0024 Three Buddha Bottoms | 94 | NOT_EVALUABLE | trend + support/context |
| 0025 Dumpling Top | 16 | NOT_EVALUABLE | weakening/rounded-top semantics + trend |
| 0026 Fry Pan Bottom | 1 | NOT_EVALUABLE | weakening/rounded-bottom semantics + trend |
| 0027 Tower Top | 205 | NOT_EVALUABLE | long bodies + consolidation semantics + trend |
| 0028 Tower Bottom | 218 | NOT_EVALUABLE | long bodies + consolidation semantics + trend |
| 0029 Unique Three River Bottom | 3 | NOT_EVALUABLE | long/very-small + trend |
| 0030 Three Rising Methods | 4 | NOT_EVALUABLE | long/small + trend |
| 0031 Three Falling Methods | 3 | NOT_EVALUABLE | long/small + trend |
| 0032 Three White Soldiers | 172 | NOT_EVALUABLE | stabilization/near-high/gradual semantics |
| 0033 Advance Block | 113 | NOT_EVALUABLE | bullish advance/long/smaller-body semantics |
| 0034 Separating Lines | 0 exact same-open | NO_MATCH structural scan | uptrend context |
| 0035 Tasuki Gap | existing replay/evaluator reused | REUSE | sessionization + qualitative body comparator |
| 0036 Gapping Play | existing evaluator/replay reused | REUSE | sharp/small/congestion/context gates |
| 0037 Side-by-Side White Lines | existing evaluator/replay reused | REUSE | same-open/similar-body + sessionization |
| 0038 Windows | existing replay/evaluator reused | REUSE | sessionization/freeze manifest |

## Important interpretation
- Candidate counts are structural scan counts, not trade signals and not PASS results.
- Trend/context gates were not converted into arbitrary numeric thresholds.
- Qualitative source terms such as long, small, near, similar, approximately, strong, gradually and ideally remain unresolved unless a source-locked comparator exists.
- 0035-0038 reuse their existing artifacts; they are not rebuilt here.
- Nison output remains confirmation-only with neutral direction.
- No 2025 data is used for tuning.

## Next execution target
Add source-locked context comparators where the existing project already defines them; otherwise retain NOT_EVALUABLE. Then run confirmation/invalidation/no-lookahead QA on the surviving structural candidates. Do not convert structural candidate counts into PASS/FREEZE automatically.