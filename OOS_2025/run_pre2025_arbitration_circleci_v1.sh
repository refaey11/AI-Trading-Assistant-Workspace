#!/usr/bin/env bash
set -euo pipefail

: "${DROPBOX_ACCESS_TOKEN:?BLOCKED: configure CircleCI project secret DROPBOX_ACCESS_TOKEN.}"
H1_INPUT="${H1_CSV:-${H1:?H1 source path is required.}}"
M1_INPUT="${M1_CSV:-${M1:?M1 source path is required.}}"
MTF_ZIP="${MTF_ZIP:-/tmp/pre2025/mtf/source.zip}"

ROOT=/tmp/pre2025_arbitration
BASE='https://content.dropboxapi.com/2/files/download'
AUTH=(-H "Authorization: Bearer ${DROPBOX_ACCESS_TOKEN}" -H 'Content-Type: application/octet-stream')
MARKET_ZIP="$ROOT/market/source.zip"
MARKET_UNPACK="$ROOT/market/unpack"
OUT="artifacts/pre2025_arbitration"

rm -rf "$ROOT"
mkdir -p "$MARKET_UNPACK" "$OUT"

curl -L --fail --silent --show-error "$BASE" "${AUTH[@]}" \
  -H 'Dropbox-API-Arg: {"path":"/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MARKET_STATE_READER_V1.zip"}' \
  -o "$MARKET_ZIP"

unzip -q "$MARKET_ZIP" -d "$MARKET_UNPACK"
MARKET=$(find "$MARKET_UNPACK" -type f -name 'GBPUSD_MARKET_STATE.csv' | head -1)
test -n "$MARKET"
test -f "$H1_INPUT"
test -f "$M1_INPUT"
test -f "$MTF_ZIP"

echo "Using market=$MARKET"
echo "Using h1=$H1_INPUT"
echo "Using m1=$M1_INPUT"
echo "Using mtf=$MTF_ZIP"

for year in 2016 2017 2018 2019 2020 2021 2022 2023 2024; do
  YEAR_OUT="$OUT/$year"
  mkdir -p "$YEAR_OUT"
  python OOS_2025/pre2025_realdata_arbitration_shadow_v1.py \
    --market-state "$MARKET" \
    --mtf "$MTF_ZIP" \
    --h1 "$H1_INPUT" \
    --m1 "$M1_INPUT" \
    --year "$year" \
    --output "$YEAR_OUT/ARBITRATION_SHADOW.csv"
done

python - <<'PY'
import json
from pathlib import Path

root = Path('artifacts/pre2025_arbitration')
rows = [
    json.loads(p.read_text(encoding='utf-8'))
    for p in sorted(root.glob('*/ARBITRATION_SHADOW.json'))
]
summary = {
    'status': 'PASS_SHADOW_ONLY',
    'years': rows,
    'oos_2025_locked': True,
    'replacement_pnl': False,
    'policy_changed': False,
    'new_rule_semantics': False,
    'purpose': 'Measure real-data Brain-vs-Murphy topology before any arbitration policy change.'
}
(root / 'PRE2025_ARBITRATION_SHADOW_SUMMARY.json').write_text(
    json.dumps(summary, indent=2, sort_keys=True), encoding='utf-8'
)
print(json.dumps(summary, indent=2, sort_keys=True))
PY