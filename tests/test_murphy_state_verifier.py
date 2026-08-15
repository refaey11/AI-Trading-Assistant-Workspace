from tools.murphy_state_verifier import Evidence, State, verify, verify_many


def frozen_evidence():
    return Evidence(
        implementation=True,
        tests_pass=True,
        historical_qa=True,
        no_lookahead=True,
        compatibility_audit=True,
        blocker_closed=True,
        freeze_manifest=True,
        frozen_snapshot=True,
        production_freeze=True,
        merged_main=True,
        canonical_frozen=True,
        oos_2025_clean=True,
        evidence_commits=("freeze-commit", "qa-commit"),
    )


def test_0021_0023_freeze_gate_is_deterministic():
    result = verify("0021", frozen_evidence())
    assert result.state is State.FROZEN
    assert result.evidence_commits == ("freeze-commit", "qa-commit")


def test_0025_0026_stale_blocker_is_superseded_by_traceable_closure():
    evidence = Evidence(
        **{**frozen_evidence().__dict__, "blocker_open": True, "blocker_closed": True}
    )
    result = verify("0025", evidence)
    assert result.state is State.FROZEN


def test_active_blocker_prevents_freeze():
    evidence = Evidence(**{**frozen_evidence().__dict__, "blocker_open": True})
    result = verify("0026", evidence)
    assert result.state is State.BLOCKED


def test_conflicting_authoritative_states_do_not_guess():
    result = verify("0006", frozen_evidence(), conflicting_states=("FROZEN", "BLOCKED"))
    assert result.state is State.CONFLICT


def test_2025_oos_forbidden_use_is_hard_block():
    evidence = Evidence(**{**frozen_evidence().__dict__, "oos_2025_used_for_forbidden_purpose": True})
    result = verify("0022", evidence)
    assert result.state is State.BLOCKED


def test_future_data_contamination_is_hard_block():
    evidence = Evidence(**{**frozen_evidence().__dict__, "future_data_contamination": True})
    result = verify("0023", evidence)
    assert result.state is State.BLOCKED


def test_missing_evidence_is_unverified():
    result = verify("0028", Evidence())
    assert result.state is State.UNVERIFIED


def test_verify_many_is_stable_and_does_not_infer():
    results = verify_many({"0029": Evidence(), "0001": Evidence()})
    assert [r.rule_id for r in results] == ["0001", "0029"]
    assert all(r.state is State.UNVERIFIED for r in results)
