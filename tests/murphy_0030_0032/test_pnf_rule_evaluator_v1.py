from src.murphy_0030_0032.pnf_3box_reference import PNFBar
from src.murphy_0030_0032.pnf_rule_evaluator_v1 import evaluate_0030_0032


def bars():
    return [
        PNFBar("2024-01-01", 100, 101, 99, 101),
        PNFBar("2024-01-02", 101, 104, 100, 103),
        PNFBar("2024-01-03", 103, 104, 99, 100),
        PNFBar("2024-01-04", 100, 100, 94, 95),
        PNFBar("2024-01-05", 95, 99, 95, 98),
    ]


def test_missing_box_policy_is_fail_closed():
    result = evaluate_0030_0032(
        bars(), box_size=1.0, box_size_policy_approved=False,
        bootstrap_policy_approved=True,
    )
    assert result["status"] == "NOT_EVALUABLE"


def test_missing_bootstrap_policy_is_fail_closed():
    result = evaluate_0030_0032(
        bars(), box_size=1.0, box_size_policy_approved=True,
        bootstrap_policy_approved=False,
    )
    assert result["status"] == "NOT_EVALUABLE"


def test_2025_is_rejected():
    data = bars()
    data[-1] = PNFBar("2025-01-05", 95, 99, 95, 98)
    result = evaluate_0030_0032(
        data, box_size=1.0, box_size_policy_approved=True,
        bootstrap_policy_approved=True,
    )
    assert result["status"] == "NOT_EVALUABLE"


def test_approved_policies_allow_structural_0030_evaluation():
    result = evaluate_0030_0032(
        bars(), box_size=1.0, box_size_policy_approved=True,
        bootstrap_policy_approved=True,
    )
    assert result["status"] == "PASS"
    assert result["rule_0030"]["evidence_type"] == "PNF_BULLISH_SUPPORT_REFERENCE"


def test_0031_requires_explicit_bullish_context():
    result = evaluate_0030_0032(
        bars(), box_size=1.0, box_size_policy_approved=True,
        bootstrap_policy_approved=True,
    )
    assert result["rule_0031"]["status"] == "NOT_EVALUABLE"


def test_0032_requires_explicit_bearish_context():
    result = evaluate_0030_0032(
        bars(), box_size=1.0, box_size_policy_approved=True,
        bootstrap_policy_approved=True,
    )
    assert result["rule_0032"]["status"] == "NOT_EVALUABLE"
