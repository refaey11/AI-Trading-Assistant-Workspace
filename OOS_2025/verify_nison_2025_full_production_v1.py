from __future__ import annotations

import json
import sys
from pathlib import Path

# Authoritative 2025 production source contains 6,225 H1 rows.
# This is a data-contract value only; it does not tune or alter any rule.
EXPECTED_2025_ROWS = 6225
EXPECTED_RULES = 44
EXPECTED_EVIDENCE_ROWS = EXPECTED_2025_ROWS * EXPECTED_RULES


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_nison_2025_full_production_v1.py <manifest>", file=sys.stderr)
        return 2
    manifest_path = Path(sys.argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["input_rows_2025"] == EXPECTED_2025_ROWS, manifest["input_rows_2025"]
    assert manifest["nison_rules"] == EXPECTED_RULES, manifest["nison_rules"]
    assert manifest["evidence_rows"] == EXPECTED_EVIDENCE_ROWS, manifest["evidence_rows"]
    assert manifest["scope"].startswith("2025-01-01T00:00:00Z")
    assert manifest["lookahead_policy"] == "none"
    assert manifest["oos_policy"] == "2025 is evaluation-only; no tuning or threshold selection"

    print("FULL_2025_NISON_PRODUCTION=PASS")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
