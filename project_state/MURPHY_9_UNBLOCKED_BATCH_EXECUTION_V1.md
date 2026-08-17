# Murphy 9-Rule Unblocked Batch Execution V1

Status: EXECUTION BATCH DEFINED — NOT FROZEN

## Scope
Run the nine rules currently marked UNBLOCKED as one batch. No new semantics are invented. Existing project primitives are reused where actually present; missing implementation remains blocked.

## Rules
- MURPHY_0005 — Pivot audit; producer: PIVOT_SEQUENCE_V2; gate: source contract + evaluator.
- MURPHY_0014 — Ascending Triangle; producer: PIVOT_SEQUENCE_V2; gate: point qualification contract.
- MURPHY_0015 — Descending Triangle; producer: PIVOT_SEQUENCE_V2; gate: point qualification contract.
- MURPHY_0016 — Flag continuation; producer: SHARED_EVIDENCE; gate: flagpole detector contract.
- MURPHY_0017 — Pennant/flag continuation; producer: SHARED_EVIDENCE; gate: flagpole detector contract.
- MURPHY_0018 — Converging geometry; producer: SHARED_EVIDENCE; gate: converging two-line contract.
- MURPHY_0019 — Converging geometry; producer: SHARED_EVIDENCE; gate: converging two-line contract.
- MURPHY_0040 — Parabolic SAR; producer: EXISTING_SAR_MODULE; gate: exact SAR operator.
- MURPHY_0041 — DMI/ADX; producer: EXISTING_DMI_ADX_MODULE; gate: exact DMI/ADX operator.

## Source-locked Murphy semantics available in Master KB
### Triangles
- Triangle requires two converging trendlines and at least four reversal points (two highs, two lows) for initial boundaries.
- Ascending triangle: horizontal upper resistance + higher lows / ascending lower trendline; expected bullish continuation, with occasional bottom-reversal behavior.
- Descending triangle: horizontal lower support + lower highs / descending upper trendline; expected bearish continuation.
- Symmetrical triangle: descending upper + ascending lower trendlines converging at apex; breakout typically occurs between 2/3 and 3/4 of horizontal width; base height is projected from breakout; volume contracts inside and breakout confirmation requires a sharp volume spike.

### Flags / Pennants
- They are short continuation pauses after a sharp rapid move (flagpole).
- Flag: parallelogram sloping slightly against preceding move.
- Pennant: very small horizontal symmetrical triangle.
- Typical completion: 1–3 weeks.
- Target uses flagpole length projected from breakout price.

### Parabolic SAR / DMI / ADX
- SAR dots below price in uptrend and above price in downtrend; SAR stops/reverses when hit; acceleration factor increases trailing speed.
- +DI crossing above -DI is a buy signal; +DI crossing below -DI is a sell signal.
- Rising ADX above 20 indicates strengthening trend; falling ADX below 40/dropping indicates weakening/range conditions in the Master KB wording.
- DMI/ADX is a filter for Parabolic SAR to reduce sideways-market whipsaws.

## Execution policy
1. Source-lock each rule against the Master KB.
2. Bind only to the named existing producer.
3. If the producer/entrypoint is absent, status = NOT_EVALUABLE; do not synthesize it.
4. Tests must include unavailable/future evidence rejection.
5. 2025 remains OOS and cannot be used for tuning.
6. No rule is marked FROZEN from this manifest alone.

## Expected next artifacts
- shared point-qualification contract for 0014/0015
- shared flagpole detector contract for 0016/0017
- converging-two-line contract for 0018/0019
- exact SAR operator binding for 0040
- exact DMI/ADX operator binding for 0041
- evaluator/test results for 0005
