# MURPHY 0006/0007 — PRODUCTION PATH VALIDATION V1

Date: 2026-08-14
Status: PASS for fresh replay execution; integration gate evidence recorded

## Scope
- Period: 2016–2024 only
- 2025: excluded
- Canonical Pivot V2 reused
- Canonical Geometry V1 reused
- D1 rebuilt from the supplied M1 master by calendar date
- Corrected deterministic `src/murphy_0006_0007/murphy_event_operator.py` at commit `4932035bf0227d100e81e1d1b593ce3aed969460`
- No reference-result artifact was read by the replay logic

## Inputs
- Pivot V2: `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
- Geometry V1: `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`
- M1: `GBPUSD_M1_MASTER_2016_2026.csv`
- Rebuilt D1 rows: 2,544

## Input hashes
- Pivot V2 SHA-256: `bd9df3ec9fea3e180628daf9d4a079b5d030edbb4a3bd659c4a7baf9de6033f8`
- Geometry V1 SHA-256: `9394b594a15a9e0e33a3fda14364b9158fda13ff074a325df24997c92295b1b3`
- M1 SHA-256: `e0383c003fdb08e8776e68a4e8d1cc30529c0be55799295c0ffbdd52a80e1bb8`
- Rebuilt D1 SHA-256: `467d6a08ee59721e4a6048b7888b4d19b6da8d2fa46a89f6af47249b27cd31cb`
- Replay result SHA-256: `0709dce08ed37072be40db6fccc6a7c72481c7db4700842b8f0cd7a4abcff360`

## Result
- MURPHY_0006: 8
- MURPHY_0007: 7
- Total: 15

The corrected operator reproduced the historical 8 + 7 result using the canonical Pivot V2 and Geometry V1 inputs and a freshly rebuilt 2016–2024 D1 series. No reference-result artifact was used to select confirmations.

## Confirmation IDs
15/15 expected historical confirmation rows were reproduced by the fresh replay. The line IDs and third-touch/reaction dates are recorded in the replay result artifact associated with this audit.

## Safety checks
- 2025 excluded: PASS
- First eligible same-family candidate cannot be skipped: enforced by operator and regression test
- Reaction must be strictly after touch by event timestamp: enforced
- Availability is used as a no-lookahead eligibility gate: enforced
- No ATR/pip/percentage/2-day/3%/2025 tuning: PASS

## Important distinction
This artifact proves the fresh replay behavior of the corrected operator with canonical inputs. It does not by itself prove that the evaluator has been merged into an external Decision Brain production runtime. That remaining integration claim must be recorded separately and must not be inferred from replay success.
