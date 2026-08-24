from datetime import date

from EVIDENCE_ARCHITECTURE_V1.adapters.cftc_tff_096742_2025 import (
    CONTRACT_CODE,
    OIObservation,
    compute_observed_direction,
)


def test_direction_uses_only_observed_values():
    assert compute_observed_direction(200826, 212688) == "UP"
    assert compute_observed_direction(212688, 206821) == "DOWN"
    assert compute_observed_direction(206821, 206821) == "FLAT"


def test_missing_observation_is_fail_closed():
    assert compute_observed_direction(None, 212688) is None
    assert compute_observed_direction(212688, None) is None


def test_contract_identity():
    row = OIObservation(
        report_date=date(2025, 1, 21),
        open_interest=212688,
        cftc_contract_market_code=CONTRACT_CODE,
        market_and_exchange_names="BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
    )
    assert row.cftc_contract_market_code == "096742"
    assert row.open_interest == 212688
