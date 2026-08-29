# TIZ Candidate Bridge CI Validation

Status: CANDIDATE — NOT AUTHORITATIVE — NOT FROZEN

This branch now contains a dedicated GitHub Actions workflow for the candidate bridge.

Validation scope:
- run the existing candidate bridge tests only;
- do not promote the producer;
- do not change the seven source rules;
- do not generate direction;
- do not introduce psychological thresholds;
- 2025 remains OOS and is not used for tuning/selection/calibration.

Promotion remains blocked until the authoritative producer/provenance contract, deterministic evaluator, adapter validation, historical QA, OOS checks, and cross-file consistency gates pass.
