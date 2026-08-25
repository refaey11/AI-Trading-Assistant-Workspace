from pathlib import Path

from OOS_2025.run_murphy_0021_2025_fresh_v1 import CANONICAL_M1_NAME, resolve_canonical_m1


def test_resolve_canonical_m1_prefers_named_source(tmp_path):
    root = tmp_path / "unpacked"
    root.mkdir()
    wrong = root / "other.csv"
    wrong.write_text("timestamp,open,high,low,close,volume\n", encoding="utf-8")
    canonical = root / CANONICAL_M1_NAME
    canonical.write_text("timestamp,open,high,low,close,volume\n", encoding="utf-8")
    assert resolve_canonical_m1(wrong) == canonical


def test_resolve_canonical_m1_rejects_missing_source(tmp_path):
    candidate = tmp_path / "other.csv"
    candidate.write_text("timestamp,open,high,low,close,volume\n", encoding="utf-8")
    try:
        resolve_canonical_m1(candidate)
    except ValueError as exc:
        assert CANONICAL_M1_NAME in str(exc)
    else:
        raise AssertionError("Expected missing canonical M1 source to fail closed")