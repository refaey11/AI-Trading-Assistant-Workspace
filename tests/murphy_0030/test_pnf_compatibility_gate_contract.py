"""Contract tests for the source-bounded Murphy 0030 compatibility gate.

These tests deliberately validate governance and gate behavior only. They do
not select or optimize a box size and do not certify an external implementation.
"""

from pathlib import Path


HARNESS = Path("project_state/MURPHY_0030_EXTERNAL_PNF_COMPATIBILITY_HARNESS_V1.md")


def test_harness_requires_c1_to_c4_and_box_size_neutrality():
    text = HARNESS.read_text(encoding="utf-8")
    for gate in ("C1", "C2", "C3", "C4", "C5"):
        assert f"### {gate}" in text
    assert "must never search, optimize, rank, or select box sizes" in text


def test_harness_does_not_allow_compatibility_to_become_freeze():
    text = HARNESS.read_text(encoding="utf-8")
    assert "No result may be upgraded to `FROZEN` by this harness." in text


def test_historical_boundary_excludes_2025():
    text = HARNESS.read_text(encoding="utf-8")
    assert "2016–2024" in text
    assert "2025 is OOS" in text


def test_integration_rule_requires_smallest_adapter_only():
    text = HARNESS.read_text(encoding="utf-8")
    assert "smallest project adapter" in text
    assert "Do not rebuild the P&F engine." in text
