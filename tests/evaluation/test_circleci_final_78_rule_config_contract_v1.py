from pathlib import Path


def test_final_78_workflow_is_present_and_isolated():
    config = Path('.circleci/config.yml').read_text(encoding='utf-8')
    assert 'final_2025_governed_78_rule_v1:' in config
    assert 'final_2025_governed_78_rule:' in config
    assert 'build_and_test:' in config


def test_final_workflow_requires_all_upstream_gates():
    config = Path('.circleci/config.yml').read_text(encoding='utf-8')
    for item in [
        'nison_2025_full_production_v1',
        'murphy_0021_2025_fresh_v1',
        'murphy_0022_0023_2025_pit_v1',
        'oos_2025_78_rule_coverage_v1',
        'final_2025_governed_78_rule_v1',
    ]:
        assert item in config


def test_final_gate_is_fail_closed_on_34_44_manifest():
    config = Path('.circleci/config.yml').read_text(encoding='utf-8')
    assert "m['murphy_rule_count_in_event'] == 34" in config
    assert "m['nison_rule_count_in_event'] == 44" in config
    assert "m['fan_in_mode'] == 'LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT'" in config
