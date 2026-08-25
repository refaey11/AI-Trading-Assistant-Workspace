from pathlib import Path


def test_runner_uses_full_evidence_arguments_and_fail_closed_manifest():
    text = Path("OOS_2025/run_final_2025_governed_78_rule_v2.py").read_text(encoding="utf-8")
    assert '"--murphy-full-evidence"' in text
    assert '"--nison-full-evidence"' in text
    assert 'murphy_rule_count' in text
    assert 'nison_rule_count' in text
    assert 'LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT' in text
    assert 'oos_tuning' in text
    assert 'new_rule_semantics' in text


def test_runner_keeps_legacy_rows_only_for_compatibility():
    text = Path("OOS_2025/run_final_2025_governed_78_rule_v2.py").read_text(encoding="utf-8")
    assert 'MURPHY_2025_CANDIDATE_STREAM.csv' in text
    assert 'NISON_2025_CANDIDATE_STREAM.csv' in text
    assert 'full evidence boundary' in text
