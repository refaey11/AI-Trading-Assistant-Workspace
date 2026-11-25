from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd

TARGETS = {
    "mtf_trend_score": ["mtf_trend_score", "MTF_trend_score", "mtf_score", "MTF_SCORE"],
    "M5_trend_regime": ["M5_trend_regime", "M5_trend", "M5_regime"],
    "M15_trend_regime": ["M15_trend_regime", "M15_trend", "M15_regime"],
    "M30_trend_regime": ["M30_trend_regime", "M30_trend", "M30_regime"],
    "H1_trend_regime": ["H1_trend_regime", "H1_trend", "H1_regime"],
    "H4_trend_regime": ["H4_trend_regime", "H4_trend", "H4_regime"],
    "D1_trend_regime": ["D1_trend_regime", "D1_trend", "D1_regime"],
    "volume_available": ["volume_available", "has_volume", "volume_present"],
    "M5_volume_regime": ["M5_volume_regime", "M5_volume", "M5_vol_regime"],
    "M15_volume_regime": ["M15_volume_regime", "M15_volume", "M15_vol_regime"],
    "M30_volume_regime": ["M30_volume_regime", "M30_volume", "M30_vol_regime"],
    "H1_volume_regime": ["H1_volume_regime", "H1_volume", "H1_vol_regime"],
    "H4_volume_regime": ["H4_volume_regime", "H4_volume", "H4_vol_regime"],
    "D1_volume_regime": ["D1_volume_regime", "D1_volume", "D1_vol_regime"],
}

def main(path: Path):
    df = pd.read_csv(path, nrows=5, low_memory=False)
    cols = list(df.columns)
    mapping = {}
    for target, aliases in TARGETS.items():
        hits = [c for c in cols if c in aliases]
        mapping[target] = hits
    related = [c for c in cols if any(x in c.lower() for x in ("trend", "regime", "volume", "mtf", "structure", "bias", "direction"))]
    print(json.dumps({
        "columns_total": len(cols),
        "rows_sampled": len(df),
        "exact_target_mapping": mapping,
        "related_columns": related,
        "first_80_columns": cols[:80],
    }, indent=2))

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--context", type=Path, required=True); main(p.parse_args().context)
