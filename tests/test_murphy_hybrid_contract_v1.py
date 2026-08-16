from src.engineering_evidence.murphy_hybrid_contract_v1 import combine_canonical_and_engineering


def test_soft_evidence_never_overrides_canonical_fail():
    x = combine_canonical_and_engineering("PILOT", "FAIL", "HIGH")
    assert x.canonical_status == "FAIL"
    assert x.evidence_only is True


def test_soft_evidence_is_provenance_tagged():
    x = combine_canonical_and_engineering("PILOT", "PASS", "MEDIUM")
    assert x.provenance == "ENG-HYBRID-V1"


def test_not_evaluable_remains_not_evaluable():
    x = combine_canonical_and_engineering("PILOT", "NOT_EVALUABLE", "HIGH")
    assert x.canonical_status == "NOT_EVALUABLE"
