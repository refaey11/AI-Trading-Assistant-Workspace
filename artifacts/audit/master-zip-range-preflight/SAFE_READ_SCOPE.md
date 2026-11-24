# Safe read scope

The next preflight allowlists only `README.md` and `VALIDATION_SUMMARY.json` from the ZIP. It reads their exact local headers and compressed payloads after validating central-directory metadata, then verifies uncompressed sizes and CRC32. The large `GBPUSD_M1_MASTER_2016_2026.csv` member is explicitly not read in this stage. No 2025/2026 market-data rows are accessed.
