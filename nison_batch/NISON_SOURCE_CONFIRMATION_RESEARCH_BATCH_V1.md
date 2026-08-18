# Nison Source Confirmation Research Batch V1
Date: 2026-08-18

## Scope
Source/contract research for the 44 Nison rules. This artifact separates source-backed confirmation semantics from project operationalization. It does not freeze rules.

## Authoritative project boundary
- Master KB / project files remain the source of truth.
- Nison is confirmation only and cannot create direction.
- Unknown qualitative language remains NOT_EVALUABLE; no threshold is selected from historical outcomes.
- 2025 remains OOS and is excluded from tuning/selection.

## Source-backed confirmation findings

### 0021 Three Mountains
Nison source states that the final/high point of the three-mountain top is ideally confirmed by a bearish candlestick indicator (examples include doji or tri-star). Therefore confirmation can be represented as: final mountain peak + subsequent/source-specified bearish candle indicator. Exact bearish-indicator set and timing must remain source-bound.

### 0022 Three Rivers
The Nison glossary/source describes the intervening valley being exceeded by a white candlestick or gap as confirmation that a bottom has formed. Operational confirmation: break above the intervening valley by a bullish candle or rising Window. Exact level/timing must reuse the existing source-backed peak/trough/window evidence.

### 0023 Three Buddha Tops
The Three Buddha top is a variant of Three Mountains with the middle peak higher than the outer peaks. Confirmation therefore inherits the Three Mountains final-peak bearish-candle confirmation. No new numeric tolerance is introduced.

### 0024 Three Buddha Bottoms
Mirror of Three Buddha Tops / Three Rivers: middle trough lower than outer troughs; bullish confirmation inherits the Three Rivers bottom-confirmation concept. No new numeric tolerance is introduced.

### 0025 Dumpling Top
Nison explicitly states that confirmation occurs when the market gaps down (falling Window). This is a deterministic confirmation primitive already represented by NISON_WINDOW_EVIDENCE_V1, subject to sessionization.

### 0026 Frypan Bottom
Nison explicitly states that the required upside gap/rising Window confirms the frypan bottom. This can reuse NISON_WINDOW_EVIDENCE_V1, subject to sessionization.

### 0027 Tower Top
Nison describes the tower top as completed by one or more large black candles after the congestion/lull. The completion candle(s) are part of the formation itself; no separate post-pattern confirmation rule was source-locked in the reviewed material. Keep separate confirmation gate NOT_EVALUABLE unless a canonical project contract is found.

### 0028 Tower Bottom
Nison describes the tower bottom as completed by one or more large white candles after the lull. This is formation completion rather than a separate post-pattern confirmation. Keep separate confirmation gate NOT_EVALUABLE unless a canonical project contract is found.

### 0019 Bullish Counterattack / 0020 Bearish Counterattack
Nison's examples emphasize the counterattack as evidence confirming significant support/resistance; the two closes are allowed some flexibility. The project must not convert 'close enough' into a numeric tolerance. Where a source-backed support/resistance context is available, expose it as confirmation evidence; otherwise keep canonical confirmation NOT_EVALUABLE.

### 0015 Tweezers Top / 0016 Tweezers Bottom
Nison describes Tweezers as minor reversal signals that gain extra importance when the two candles also form another candlestick indicator. No universal numeric post-pattern confirmation operator was found in the reviewed source set. Keep separate confirmation NOT_EVALUABLE unless an approved project comparator/context contract is found.

### 0018 Three Black Crows / 0032 Three White Soldiers
The source describes these as completed multi-candle formations and discusses contextual importance (e.g. mature/high area or low/stable area). The reviewed material did not yield a single deterministic post-pattern confirmation operator. Keep separate confirmation/context gate source-dependent and NOT_EVALUABLE when the required context is unavailable.

### 0001–0014 and 0017
The source research confirms that Nison frequently uses subsequent candles, support/resistance, and broader trend context as confirmation, but the exact confirmation/invalidation contract is pattern-specific. Do not apply a generic 'next candle' rule to all patterns.

### 0035–0038
Existing project artifacts remain authoritative for the current engineering state. 0035/0037/0036 retain their qualitative comparator blockers; 0038 retains its sessionization/freeze-manifest gates. Do not rebuild.

## Web corroboration used (not canonical source)
- Nison's book text states that candlestick signals should be interpreted with surrounding market context and that more signals confirming support/resistance increase reversal significance.
- Nison's text explicitly documents the Three Mountains bearish-candle confirmation, Dumpling Top downside-window confirmation, and Frypan Bottom upside-window confirmation.
- Nison's text documents the Counterattack examples as confirming significant support/resistance while allowing flexibility in exact close equality.

## Implementation decision
Create/reuse only these shared confirmation primitives:
1. NISON_WINDOW_EVIDENCE_V1 for rising/falling Window confirmation.
2. NISON_SR_CONFIRMATION_V1 for source-backed support/resistance confirmation where the existing context engine exposes the level.
3. NISON_BEARISH_CANDLE_CONFIRMATION_V1 for Three Mountains / Three Buddha Tops.
4. NISON_BULLISH_CANDLE_CONFIRMATION_V1 for Three Rivers / Three Buddha Bottoms.

Every primitive must emit NOT_EVALUABLE when its required source-backed input is absent. No ADX substitution is authorized for Nison trend context; the existing comparator audit explicitly rejects that substitution.

## Current outcome
This batch closes several missing *source semantics* fields, but it does not by itself freeze the 44 rules. Historical QA and the remaining context/comparator gates still have to pass.
