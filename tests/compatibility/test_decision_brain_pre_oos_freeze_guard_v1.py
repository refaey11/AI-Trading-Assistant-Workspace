import json
from pathlib import Path

from compatibility.decision_brain_pre_oos_freeze_guard_v1 import (
    development_timestamp_allowed,
    future_timestamp_allowed,
    oos_timestamp_allowed,
    validate_freeze_manifest,
)


def _manifest():
    path = Path(__file__).parents[2] / "FREEZE" / "DECISION_BRAIN_PRE_OOS_FREEZE_MANIFEST_V1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_governance_is_locked():
    validate_freeze_manifest(_manifest())


def test_2024_is_development_allowed():
    assert development_timestamp_allowed(2024) is True
    assert oos_timestamp_allowed(2024) is False


def test_2025_is_oos_only():
    assert development_timestamp_allowed(2025) is False
    assert oos_timestamp_allowed(2025) is True


def test_future_is_forbidden_from_oos_boundary():
    assert future_timestamp_allowed(2026) is True
    assert oos_timestamp_allowed(2026) is False
