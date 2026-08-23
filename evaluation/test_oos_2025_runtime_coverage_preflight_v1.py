from pathlib import Path

from oos_2025_runtime_coverage_preflight_v1 import assess_runtime_coverage


def test_allowlist_is_currently_78_rules():
    root = Path(__file__).parents[1]
    report = assess_runtime_coverage(root)
    assert report["scope"] == {"murphy": 34, "nison": 44, "total": 78}


def test_nison_runtime_surface_is_present():
    root = Path(__file__).parents[1]
    report = assess_runtime_coverage(root)
    assert report["runtime_surface"]["nison_surface"]["entrypoint_available"] is True


def test_preflight_does_not_authorize_fresh_2025_stream():
    root = Path(__file__).parents[1]
    report = assess_runtime_coverage(root, ["MURPHY_0003", "NISON_0001"])
    assert report["observed_2025"]["observed_count"] == 2
    assert report["authorization"]["fresh_2025_decision_event_stream"] is False
