# Murphy 0008–0010 Verification V1

Date: 2026-08-12

## 0008

Registry condition: `A support level is decisively broken to the downside.`

Status: **PARTIAL / OPERATOR NOT CLOSED**

Existing source terminology establishes Support as an area where buyers are expected to appear. The project registry does not freeze an exact operational definition of `decisively broken`.

## 0009

Registry condition: `A resistance level is decisively broken to the upside.`

Status: **PARTIAL / OPERATOR NOT CLOSED**

Existing source terminology establishes Resistance as a level where sellers are expected. The project registry does not freeze an exact operational definition of `decisively broken`.

## 0010

Registry condition: `A price or time filter is used before accepting the break as meaningful.`

Status: **NOT_EVALUABLE / FILTER CONTRACT NOT CLOSED**

The source material supports the concept of a time filter: prices must remain above/below a level for a period before an important technical area is considered broken. However, the project artifacts inspected do not freeze the exact filter operator/parameters for this rule.

## Compatibility decision

Do not create a new evaluator for 0008–0010 yet.

Do not invent:
- ATR distance
- percentage distance
- candle-count threshold
- wick/close criterion
- lookback
- exact time duration

Keep 0008–0010 in the Revisit Queue and continue forward.

## Architectural note

0008/0009 (break event) and 0010 (meaningfulness filter) remain separate rule semantics until their authoritative contracts are verified. Existing support/resistance/time-filter components must be reused if and when their contracts match.

2025 remains OOS and cannot be used for tuning or implementation selection.
