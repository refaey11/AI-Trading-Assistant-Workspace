# Existing MT5 Raw Capture Fixtures — V1.3 Readiness Audit

**Date:** 2026-11-18  
**Scope:** Read-only review of the existing V1 raw contract, CSV ingest adapter, tests, and GitHub Actions workflow.  
**Reviewed source branch:** `feature/mt5-raw-capture-v1`  
**Source commit:** `6b7ef616d09f77f147930f2f1d85d3597c100e63`  
**Related workflow run:** `43806113054` — GitHub Actions completed successfully.  
**Decision:** Existing tests provide a useful V1 baseline, but they do not implement or prove the proposed V1.3 timestamp-observation contract.

## 1. Files reviewed

- `RUNTIME/MT5_RAW_CAPTURE_V1/mt5_raw_capture_contract_v1.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1/mt5_csv_ingest_v1.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1/test_mt5_raw_capture_contract_v1.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1/test_mt5_csv_ingest_v1.py`
- `.github/workflows/mt5-raw-capture-v1.yml`

The workflow runs:

```bash
python -m unittest discover -s RUNTIME/MT5_RAW_CAPTURE_V1 -p "test_*.py" -v
```

The inspected GitHub Actions run completed successfully. The PR #123 description records 16 Python unit tests passed. This is evidence for the existing V1 contract tests only; it is not V1.3 acceptance evidence and does not prove MQL5 compilation or broker/terminal clock behavior.

## 2. Existing V1 coverage

The current V1 raw contract already tests:
- accepted timezone-aware `bar_time_mt5_utc` and separate host clock observation fields;
- rejection of naive bar and host clock timestamps;
- support for M5, M15, M30, H1, H4, and D1 as allowed timeframe labels;
- rejection of unsupported periods and unfinished bars;
- OHLC geometry validation;
- volume field separation;
- idempotent identical duplicates and rejection of conflicting duplicates;
- canonical payload hash mismatch rejection.

The CSV ingest tests cover:
- exact 20-column header/schema;
- row parsing and payload hash generation;
- unfinished-bar rejection;
- invalid numeric parsing;
- schema drift rejection;
- negative volume/spread rejection.

These are useful baseline fixture tests. They do not test the proposed V1.3 fields because those fields are not present in the current V1 schema.

## 3. V1.3 test requirement mapping

| Proposed requirement | Existing V1 coverage | Safe conclusion |
| --- | --- | --- |
| Timezone-aware bar label | Partial: `bar_time_mt5_utc` is required and parsed | Parser behavior covered; source-clock truth is not proven by Python |
| Naive timestamp rejection | Present for both required V1 UTC fields | Covered in V1 scope |
| Explicit clock source/domain | Not represented as structured provenance metadata | Not covered |
| Synchronization state and uncertainty | Not represented | Not covered |
| `closed_bar_observed_at_utc` | Field absent | Not covered |
| `retrieved_at_utc` | Field absent | Not covered |
| `bar_close_time_utc` | Field absent | Not covered; absence is preferable to fabricated derivation |
| No timeframe-duration close-time synthesis | No V1.3 field or derivation path exists in reviewed Python contract | Not a positive V1.3 behavior test yet |
| `timezone_policy_id` | Field absent | Not covered |
| Reject unknown policy ID | No policy-ID contract | Not covered |
| Causal/no-future availability checks | No observation-time field to compare | Not covered |
| Preserve V1/V1.2 compatibility | V1 exact CSV header is enforced | V1 header strictness covered; V1.3 cross-version compatibility not implemented |
| Six-timeframe closed-bar selection in actual MT5 | Unit test checks allowed labels; it does not call MT5 | Not proven; requires MT5-DEMO evidence |
| Boundary, stale feed, weekend, restart/replay | No controlled terminal tests in this suite | Not covered by existing tests |

## 4. Why we should not extend the V1 validator in place

The current contract has a fixed required field set and the CSV adapter enforces an exact 20-column header. Adding V1.3-only required fields to these V1 modules would change the meaning and compatibility boundary of the existing capture contract.

Therefore:
- keep `mt5_raw_capture_contract_v1.py`, `mt5_csv_ingest_v1.py`, the V1 EA, and V1.2 EA unchanged;
- do not weaken the exact V1 header check;
- do not make old V1/V1.2 rows pretend to contain observation/retrieval provenance they never recorded;
- do not backfill new timestamps from `host_gmt_estimate_utc`, `terminal_time_server`, current quote time, or server-host offsets.

## 5. Safe fixture implementation boundary

A future V1.3 implementation can add a separately named contract module and test module, for example:

- `RUNTIME/MT5_RAW_CAPTURE_V1_3/mt5_raw_capture_contract_v1_3.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1_3/test_mt5_raw_capture_contract_v1_3.py`
- `RUNTIME/MT5_RAW_CAPTURE_V1_3/mt5_csv_ingest_v1_3.py` (only after schema approval)

The first test-only increment should be limited to pure validation behavior over synthetic fixtures:
1. required provenance metadata and allowed clock domains;
2. explicit unknown/unavailable states;
3. timestamp-awareness and invalid timestamp rejection;
4. uncertainty/synchronization metadata validation;
5. causal ordering checks between bar identity, observation, and retrieval events where the approved contract defines such ordering;
6. rejection of any derived `bar_close_time_utc` created by timeframe-duration arithmetic;
7. explicit no-backfill and V1/V1.2 compatibility fixtures.

This module must not read live MT5 data, create timestamps from the machine clock, generate MTF features, or modify the existing V1/V1.2 schema.

**Important:** Until authoritative MT5 source semantics and the clock policy are approved, these tests can validate the shape and internal consistency of a proposed contract only. They cannot prove the real-world UTC accuracy of a clock or the exact time a broker made a bar available.

## 6. Recommended next step

Do not modify the existing V1/V1.2 code or EA. First review and approve the V1.3 schema and provenance vocabulary. Then implement a separate V1.3 pure-Python contract with synthetic fixtures, and add its test path to GitHub Actions without replacing or weakening the existing V1 test job.

The MT5-DEMO tests remain a separate evidence gate and must be completed for M5/M15/M30/H1/H4/D1.

## 7. Gate status

- Existing V1 fixture suite: **PASS on inspected GitHub Actions run**.
- V1.3 fixture suite: **NOT IMPLEMENTED / NOT RUN**.
- MT5-DEMO six-timeframe observation tests: **NOT RUN**.
- Stage B provenance completeness: **PARTIAL**.
- Stage C derived feature producer: **BLOCKED**.
- Stage D historical parity: **BLOCKED**.
- Legacy 2016–2024 timestamp provenance: **BLOCKED**.
- 2025 OOS: **LOCKED / NOT TOUCHED**.
- Live orders: **NOT AUTHORIZED**.

No changes to existing V1/V1.2 source, market data, frozen components, Decision Brain, or live trading behavior are made by this audit.
