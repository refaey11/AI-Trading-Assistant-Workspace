"""Deterministic guard for the Murphy 39-rule batch queue.

This is a queue-integrity gate, not a rule evaluator. It prevents frozen rules
from re-entering the batch and prevents 2025 from becoming a tuning/selection
input. Rule semantics are not invented here.
"""
from pathlib import Path
import csv

QUEUE = Path(__file__).resolve().parents[1] / "project_state" / "MURPHY_39_BATCH_AUDIT_QUEUE_V1.csv"
FROZEN = {
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007", "MURPHY_0008",
    "MURPHY_0021", "MURPHY_0022", "MURPHY_0023", "MURPHY_0025", "MURPHY_0026",
    "MURPHY_0028", "MURPHY_0029",
}


def load_rows():
    with QUEUE.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    rows = load_rows()
    ids = [row["rule_id"] for row in rows]
    assert len(rows) == 39, len(rows)
    assert len(ids) == len(set(ids)), "duplicate rule IDs"
    assert not FROZEN.intersection(ids), sorted(FROZEN.intersection(ids))
    assert all(row["protected"] == "NO" for row in rows)
    assert all("2025" not in row.values() for row in rows)
    expected = {f"MURPHY_{i:04d}" for i in range(1, 52)} - FROZEN
    assert set(ids) == expected, sorted(expected - set(ids))
    print("PASS: 39-rule queue integrity")
    print("Frozen excluded:", len(FROZEN))
    print("Batch rules:", len(rows))


if __name__ == "__main__":
    main()
