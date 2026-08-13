# Murphy 0021–0023 Clean Artifact Status V2

Date: 2026-08-13

IMPORTANT CORRECTION:
The prior commit `52398348952394dfad06e32ad052cb1a2dfbf2fd` created the clean CSV path but GitHub stored only the CSV header in the repository file. The full 5.6 MB CSV was NOT uploaded.

Therefore:
- The local clean artifact remains the authoritative working artifact for validation.
- The GitHub path must NOT be treated as the full historical dataset.
- The validation workflow cannot be considered runnable against the complete dataset until the full artifact is transferred through an appropriate artifact/LFS mechanism.
- No Production Freeze is authorized.

Local full artifact:
`MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024_CLEAN_V1.csv`

Size: 5,626,779 bytes.

The 774-byte clean summary is complete locally.

No rule logic, thresholds, timeframe definitions, or proxies were changed.