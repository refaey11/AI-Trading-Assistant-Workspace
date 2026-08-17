# Source-Bounded Operationalization Layer V1

Status: DESIGN_ONLY / NO_AUTO_FREEZE
Date: 2026-08-17

## Purpose
Provide a controlled translation layer from source-derived qualitative rule statements to measurable evaluator contracts without changing the source semantics.

## Governance
- The source rule remains authoritative.
- Existing approved primitives may be reused only after compatibility audit.
- External research may provide candidate operationalizations, but cannot silently become canonical semantics.
- No invented thresholds, tolerances, lookbacks, timeframes, proxies, scores, or direction.
- Unknown or unsupported clauses remain `NOT_EVALUABLE`.
- Historical outcomes/backtest results cannot define semantics or select among candidate meanings.
- 2025 remains OOS and excluded from tuning, selection, calibration, and optimization.
- No auto-freeze: every rule still requires source, compatibility, evidence, availability/no-lookahead, QA, and explicit freeze gates.

## Clause classes
1. HARD_CANONICAL: directly stated and objectively executable from the approved source.
2. SOURCE_BOUNDED_OPERATOR: an explicit operator/threshold/timeframe is stated by the approved source and can be mapped to an approved primitive.
3. EXTERNAL_CANDIDATE: external literature/research proposes an operationalization not stated by the source. Candidate only; never canonical by default.
4. QUALITATIVE_UNRESOLVED: source meaning is known but no defensible source-bounded operator exists. Emit `NOT_EVALUABLE`.
5. EVIDENCE_ONLY: preserve context without creating direction or a score.

## Required contract fields
- rule_id
- source_statement
- source_reference
- clause_class
- feature_id
- operator
- threshold
- timeframe
- direction
- availability_requirements
- fallback_state
- provenance
- notes

Any unsupported field must remain `UNKNOWN`/null rather than being inferred.

## Evaluation flow
source -> semantic clauses -> compatibility audit -> clause classification -> operational contract -> existing primitive -> evaluator -> unit tests -> historical QA (2016-2024) -> availability/no-lookahead -> explicit freeze decision

## Candidate handling
External candidates must be stored separately from canonical contracts. A candidate can be promoted only through an explicit compatibility/governance decision. Performance on historical data must not be used to manufacture or tune the candidate semantics.

## Initial application target
Murphy 0040-0041 are the first candidate rules for this layer. Their existing Parabolic SAR and DMI/ADX primitives must be reused; this layer does not create new indicators or thresholds.
