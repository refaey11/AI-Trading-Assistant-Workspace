#!/usr/bin/env bash
set -euo pipefail

# CI trigger: run the governed pre-2025 context-gating shadow on 2016-2024 only.
: "${DROPBOX_ACCESS_TOKEN:?BLOCKED: configure CircleCI project secret DROPBOX_ACCESS_TOKEN.}"
H1_INPUT="${H1_CSV:-${H1:?H1 source path is required.}}"
M1_INPUT="${M1_CSV:-${M1:?M1 source path is required.}}"
MTF_INPUT="${MTF:-${MTF_ZIP:-/tmp/pre2025/mtf/unpack/GBPUSD_MTF_H4_H1.csv}}"

ROOT=/tmp/pre2025_context_gate
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
test -f "$MTF_INPUT"

echo "Using market=$MARKET"
echo "Using h1=$H1_INPUT"
echo "Using m1=$M1_INPUT"
echo "Using mtf=$MTF_INPUT"
echo "Using schema-mapped Context Gate V4 (trend=H1, h4_trend=H4, mtf_state=combined)"

for year in 2016 2017 2018 2019 2020 2021 2022 2023 2024; do
  YEAR_OUT="$OUT/$year"
  mkdir -p "$YEAR_OUT"
  python OOS_2025/pre2025_murphy_context_gate_shadow_v3.py \
    --market-state "$MARKET" \
    --mtf "$MTF_INPUT" \
    --h1 "$H1_INPUT" \
    --m1 "$M1_INPUT" \
    --year "$year" \
    --output "$YEAR_OUT/CONTEXT_GATE.csv"
  python OOS_2025/pre2025_context_quality_shadow_v1.py \
    --input "$YEAR_OUT/CONTEXT_GATE.csv" \
    --output "$YEAR_OUT/CONTEXT_QUALITY.csv" \
    --runtime-entrypoint "MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py" \
    --year "$year"
done

python - <<'PY'
import json
from pathlib import Path
root=Path('artifacts/pre2025_arbitration')
rows=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(root.glob('*/CONTEXT_GATE.json'))]
quality=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(root.glob('*/CONTEXT_QUALITY.json'))]
summary={'status':'PASS_SHADOW_ONLY','years':rows,'quality_years':quality,'oos_2025_locked':True,'oos_tuning':False,'policy_changed':False,'new_rule_semantics':False,'replacement_pnl':False,'purpose':'Measure whether existing Brain context/regime can be used as a non-veto quality flag for existing Murphy direction.','schema_mapping':{'trend':'H1','h4_trend':'H4','mtf_state':'combined'},'quality_layer':'categorical_non_parametric_shadow_only','historical_full_rule_stream_used':False}
(root/'PRE2025_MURPHY_CONTEXT_QUALITY_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf-8')
print(json.dumps(summary,indent=2,sort_keys=True))
PY