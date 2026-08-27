#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-artifacts/development_2016_2024/nison}"

mkdir -p "$OUT_DIR"
python DEVELOPMENT_2016_2024/run_nison_development_2016_2024_v1.py \
  --output-dir "$OUT_DIR" \
  --start-year 2016 \
  --end-year 2024

python - "$OUT_DIR" <<'PY'
from pathlib import Path
import json
import pandas as pd
import sys

out = Path(sys.argv[1])
parts = []
for year in range(2016, 2025):
    p = out / f"NISON_{year}_FULL_EVIDENCE.csv"
    if not p.exists():
        raise SystemExit(f"Missing yearly evidence: {p}")
    df = pd.read_csv(p)
    if df["rule_id"].nunique() != 44:
        raise SystemExit(f"{p}: expected 44 rule IDs")
    parts.append(df)
full = pd.concat(parts, ignore_index=True)
full_path = out / "NISON_2016_2024_FULL_EVIDENCE.csv"
full.to_csv(full_path, index=False)
manifest_path = out / "NISON_DEVELOPMENT_2016_2024_MANIFEST.json"
manifest = json.loads(manifest_path.read_text())
manifest.update({
    "combined_artifact": str(full_path),
    "combined_rows": int(len(full)),
    "combined_rules": int(full["rule_id"].nunique()),
    "years_verified": list(range(2016, 2025)),
    "2025_used": False,
})
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))
print(full_path)
PY
