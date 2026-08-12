# Murphy 0006–0007 CI Failure Diagnosis V1

Date: 2026-08-12
Run: Murphy Evidence Adapter Tests #2
Commit under test: f45ac1867fa22fdfa3f83563ed0ba9e35276414b

## Observed result

GitHub Actions reported:
- 1 failed
- 3 passed
- exit code 1

## Root cause

The failing assertion was the 0006 fixture's `daily_range_intersects_line is True` assertion.

The test fixture used:
- anchor 1 = 2024-01-01 @ 1.20
- anchor 2 = 2024-01-03 @ 1.24
- candidate = 2024-01-08

The mathematical line value at the candidate timestamp is 1.34.
The fixture's daily range was 1.25 to 1.28, so the line is NOT inside that range.

Therefore the adapter returned `False` correctly. The implementation was not the cause of the failure; the test fixture was internally inconsistent with its assertion.

## Corrective action

Updated only the test fixture so its daily high is 1.35, making the expected intersection true while leaving the adapter implementation unchanged.

Correction commit:
`d9b89f9d6eb5fa6fe9b697d8ba150ce9df36fc44`

## Safety

No production rule, touch threshold, reaction threshold, or no-break logic was changed.
