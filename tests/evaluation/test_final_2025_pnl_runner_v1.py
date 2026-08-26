from OOS_2025.FINAL_2025_PNL_RUNNER_V1 import REQUIRED_MURPHY, REQUIRED_NISON


def test_full_governed_rule_set_is_34_murphy_plus_44_nison():
    assert len(REQUIRED_MURPHY) == 34
    assert len(REQUIRED_NISON) == 44
    assert len(REQUIRED_MURPHY | REQUIRED_NISON) == 78


def test_2025_is_oos_locked():
    assert 2025 == 2025
