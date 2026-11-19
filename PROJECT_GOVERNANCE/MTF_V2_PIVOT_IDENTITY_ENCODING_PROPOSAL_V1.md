# MTF Pivot Detector V2 — Pivot Identity Encoding Proposal V1

**Status:** ENCODING METHOD APPROVED BY USER (2026-11-19) — REFERENCE IMPLEMENTATION ONLY — NOT PRODUCTION INTEGRATED  
**Parent:** PR #141  
**Scope:** deterministic identity for one independently confirmed HIGH or LOW pivot

## 1. Purpose and boundary

The approved identity ingredients are symbol, timeframe, original source-bar identity, pivot kind, detector version, and configuration fingerprint. This proposal specifies one candidate byte-level encoding so the identity can be deterministic across languages and replay environments.

This document does not approve numeric L/R windows, source-bar identity semantics, symbol normalization, configuration contents, or event lifecycle rules. It does not implement an ID generator.

## 2. Proposed identity payload

The identity payload contains exactly these fields:

```json
{
  "config_fingerprint": "<lowercase-hex-sha256>",
  "detector_version": "MTF_PIVOT_V2",
  "pivot_kind": "HIGH",
  "source_bar_id": "<opaque-original-source-id>",
  "symbol": "<canonical-upstream-symbol>",
  "timeframe": "M5"
}
```

Allowed `pivot_kind` values: `HIGH`, `LOW`.

The payload intentionally excludes:
- price values, OHLC, timestamps, availability time, and confirmation row;
- output status, downstream structure state, BOS/CHOCH events;
- market direction, score, trade decision, and risk values.

A source bar may independently produce HIGH and LOW candidates. They receive distinct identities because `pivot_kind` differs; no intrabar ordering is implied.

## 3. Proposed canonical encoding

Proposal:
1. Validate all six required fields and reject missing, null, empty, or wrong-type values.
2. Do not silently normalize symbol, timeframe, or source_bar_id. Preserve the exact canonical values supplied by their authoritative upstream contracts. If those upstream contracts do not define canonical identity, identity generation is blocked.
3. Encode the payload using RFC 8785 JSON Canonicalization Scheme (JCS), UTF-8, with no BOM and no trailing newline.
4. Compute SHA-256 over the domain-separated byte sequence:

   `b"MTF_PIVOT_V2_ID_V1\n" + canonical_payload_utf8`

5. Render the digest as 64 lowercase hexadecimal characters.
6. Prefix the rendered digest with `mpv2_` for the externally displayed pivot ID.

The domain separator prevents accidental reuse of the same digest namespace for another object type or future identity format. Any future field or encoding change requires a new identity version and prefix; do not mutate V1 IDs in place.

## 4. Configuration fingerprint proposal

The `config_fingerprint` is SHA-256 over a separately canonicalized, versioned configuration document, using RFC 8785 JCS and UTF-8. The configuration document must include every parameter that can change candidate classification or confirmation, including per-timeframe L/R, comparison policy version, precision-policy reference, gap-policy reference, and detector build/config schema version.

The exact configuration document schema is not yet available and must be separately reviewed. Never hash only L/R while omitting other behavior-affecting settings. Never include runtime secrets or machine-specific paths.

## 5. Source identity requirements

`source_bar_id` must be an original, stable identifier from the source-data contract. It must not be synthesized from an unverified timestamp, row number, rounded price, or dataframe index. If the source has no stable bar identity, the producer must define and verify one in a separate source-lineage contract before IDs can be generated.

Symbol and timeframe must likewise come from the verified source envelope, not user-supplied free text or guessed aliases.

## 6. Collision and replay properties

- SHA-256 collision risk is treated as cryptographically negligible for this identifier use, not mathematically impossible.
- Same six identity ingredients and same identity version must yield the same ID.
- Different pivot kinds on the same bar must yield different IDs.
- Different source bars, symbols, timeframes, detector versions, or configuration fingerprints must yield different input payloads and therefore distinct IDs except for a cryptographic collision.
- Serialization must be byte-identical across implementations; test vectors are required before implementation.
- IDs identify a pivot candidate under a detector/config version. They do not encode event recross count, expiry, invalidation, supersession, or dedup lifecycle.

## 7. Required conformance tests before implementation

1. Golden canonical JSON byte vectors with expected SHA-256 and final ID.
2. Cross-language equivalence (at least Python and one independent implementation).
3. Object-key insertion-order invariance under JCS.
4. Reject missing, null, empty, wrong-type and unsupported enum fields.
5. Preserve source identity strings exactly; no silent case folding or whitespace trimming.
6. Same source bar HIGH vs LOW produces distinct IDs.
7. Each identity ingredient mutation changes canonical payload and expected digest.
8. Config fingerprint changes when any behavior-affecting setting changes.
9. Domain-separator/version changes produce a different namespace.
10. Repeated replay produces byte-identical canonical bytes and ID.

## 8. Decisions still required

User review is required for:
- RFC 8785 JCS as canonical serializer;
- SHA-256 and domain-separated prefix scheme;
- exact field names and `mpv2_` external prefix;
- exact configuration document schema and fingerprint lifecycle;
- authoritative canonical symbol/timeframe/source_bar_id upstream contracts.

No production integration is authorized by this reference implementation.

## 9. Safety

This is identity metadata only. It does not generate direction, signals, BUY/SELL, entries, SL/TP, or orders. It does not authorize Brain integration, live trading, or changes to legacy PIVOT_SEQUENCE_V2. The 2025 OOS dataset is not used.
