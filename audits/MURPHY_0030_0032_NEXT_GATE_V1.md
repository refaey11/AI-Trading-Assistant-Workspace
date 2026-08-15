# Murphy 0030-0032 — Next Gate V1

The proposal branch now contains an executable GitHub Actions workflow for the existing Murphy 0030-0032 test suite.

Current required sequence:

1. CI must execute and pass the committed P&F unit tests.
2. Run the independent 2019-2024 rule evaluator using the declared project Box Policy proposal.
3. Run availability and no-lookahead checks on evaluator outputs.
4. Review provenance and bootstrap assumptions.
5. Only after all gates pass may a freeze decision be considered.

The 0.6257356643% box percentage remains a project operationalization proposal, not a claimed Murphy/Tower value.

2025 remains OOS and must not be used to tune or select the policy.
