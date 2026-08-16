"""Fail-closed inventory of real Murphy accelerator implementations.

This scanner does not infer compatibility from filenames or prose. An accelerator is
considered IMPLEMENTED only when the registry points to an existing executable
entrypoint (pytest directory/file or importable Python module). Everything else is
reported as NOT_EVALUABLE and remains eligible for later source/compatibility work.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "project_state" / "MURPHY_39_ACCELERATOR_REGISTRY_V1.csv"
OUT = ROOT / "project_state" / "MURPHY_39_ACCELERATOR_IMPLEMENTATION_INVENTORY_V1.json"


def main() -> int:
    rows = []
    with REGISTRY.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            entry = (row.get("entrypoint") or "").strip()
            exists = bool(entry) and any((ROOT / entry).exists() for _ in [0])
            kind = row.get("entrypoint_type", "")
            executable = exists and kind in {"PYTEST_DIRECTORY", "PYTEST_OR_MODULE"}
            rows.append(
                {
                    "accelerator": row["accelerator"],
                    "entrypoint": entry or None,
                    "entrypoint_type": kind,
                    "entrypoint_exists": exists,
                    "executable_entrypoint": executable,
                    "status": "IMPLEMENTED_ENTRYPOINT" if executable else "NOT_EVALUABLE",
                    "reason": None if executable else "No verified executable entrypoint in workspace registry",
                }
            )

    payload = {
        "version": "V1",
        "policy": "fail_closed_no_invention",
        "accelerators": rows,
        "counts": {
            "total": len(rows),
            "implemented_entrypoints": sum(r["executable_entrypoint"] for r in rows),
            "not_evaluable": sum(not r["executable_entrypoint"] for r in rows),
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
