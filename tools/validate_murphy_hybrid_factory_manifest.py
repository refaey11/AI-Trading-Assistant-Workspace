"""Integrity gate for the Murphy hybrid 39-rule factory manifest.

This validates architecture metadata only. It does not approve rule semantics,
create thresholds, or freeze rules.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "project_state" / "MURPHY_HYBRID_39_FACTORY_MANIFEST_V1.csv"
FROZEN = {
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007", "MURPHY_0008",
    "MURPHY_0021", "MURPHY_0022", "MURPHY_0023", "MURPHY_0025", "MURPHY_0026",
    "MURPHY_0028", "MURPHY_0029",
}
EXPECTED = {f"MURPHY_{i:04d}" for i in range(1, 52)} - FROZEN


def main():
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    ids = [r["rule_id"] for r in rows]
    assert len(rows) == 39, f"expected 39 rows, got {len(rows)}"
    assert len(ids) == len(set(ids)), "duplicate rule IDs"
    assert set(ids) == EXPECTED, "manifest does not exactly equal 51 rules minus frozen 12"
    assert not FROZEN.intersection(ids), "frozen rule entered hybrid factory"
    assert all(r["freeze_policy"] == "NO_AUTO_FREEZE" for r in rows)
    assert all("2025" not in r.values() for r in rows)
    assert all(r["clause_strategy"].startswith("HARD_CANONICAL") for r in rows)
    print("PASS: Murphy hybrid 39-rule factory manifest integrity")
    print("Rules:", len(rows))
    print("Frozen excluded:", len(FROZEN))
    print("Auto-freeze disabled: YES")


if __name__ == "__main__":
    main()
