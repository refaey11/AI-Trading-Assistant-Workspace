# CI Dispatch Blocker V1

## Finding
The Murphy 39 Accelerator Batch workflow contains `workflow_dispatch`, but the available GitHub connector in this session exposes no workflow-dispatch/start-workflow action.

## Current consequence
A fresh CI result cannot be claimed from this session. Historical runs may be rerun, but that does not prove the current head was executed.

## Required manual action
From GitHub Actions, select `Murphy 39 Accelerator Batch` on branch `feature/murphy-hybrid-rule-factory-v1` and choose **Run workflow**.

## After dispatch
1. Verify the run commit SHA equals the current PR head.
2. Check queue validation.
3. Check factory manifest validation.
4. Check accelerator batch.
5. Inspect PNF 0030–0032 result.
6. Only then advance the 0030 gates.

## Governance
No Freeze is implied by CI dispatch or by a successful accelerator integration check. Nison remains outside this Murphy batch.
