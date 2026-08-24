import json
from datetime import datetime
from pathlib import Path


OI_PATH = Path("evidence/cftc/2025/6b_oi_pit_bound_v1.json")


def _load():
    return json.loads(OI_PATH.read_text(encoding="utf-8"))


def test_pit_bound_inventory_has_52_canonical_observations():
    data = _load()
    observations = data["observations"]
    assert data["observation_count"] == 52
    assert len(observations) == 52
    assert len({row["report_date"] for row in observations}) == 52


def test_pit_binding_is_monotonic_and_not_before_report_date():
    data = _load()
    for row in data["observations"]:
        report_date = datetime.fromisoformat(row["report_date"] + "T00:00:00+00:00")
        available_time = datetime.fromisoformat(row["available_time"].replace("Z", "+00:00"))
        assert available_time >= report_date


def test_shutdown_catchup_and_missing_1111_are_explicit():
    data = _load()
    dates = {row["report_date"] for row in data["observations"]}
    by_date = {row["report_date"]: row for row in data["observations"]}

    assert "2025-11-10" in dates
    assert "2025-11-11" not in dates
    assert by_date["2025-11-10"]["available_time"] == "2025-12-10T20:30:00Z"
    assert by_date["2025-12-30"]["available_time"] == "2026-01-13T20:30:00Z"


def test_primary_oi_values_used_for_key_reconciliation_dates():
    data = _load()
    by_date = {row["report_date"]: row["open_interest"] for row in data["observations"]}
    assert by_date["2025-03-25"] == 191212
    assert by_date["2025-11-10"] == 272612
    assert by_date["2025-12-30"] == 196003
