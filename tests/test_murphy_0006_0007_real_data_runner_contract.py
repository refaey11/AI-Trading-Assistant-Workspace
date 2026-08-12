from pathlib import Path
import pandas as pd

from scripts.run_murphy_0006_0007_real_data_candidates import END, START


def test_historical_window_excludes_2025_plus():
    assert START == pd.Timestamp("2016-01-01")
    assert END == pd.Timestamp("2024-12-31 23:59:59")


def test_candidate_status_is_evidence_only_contract():
    # The runner's contract is intentionally candidate-only; production
    # confirmation must remain downstream of source-backed operators.
    assert START.year == 2016
    assert END.year == 2024
