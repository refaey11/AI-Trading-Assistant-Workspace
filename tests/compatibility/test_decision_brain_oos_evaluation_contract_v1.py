from compatibility.decision_brain_oos_evaluation_contract_v1 import OOSContract


def test_2025_is_locked_out_of_development():
    c = OOSContract()
    for year in (2025, 2026):
        try:
            c.validate_partition(year, "development")
        except ValueError:
            continue
        raise AssertionError("OOS year was accepted in development")


def test_2024_is_valid_development_year():
    c = OOSContract()
    c.validate_partition(2024, "development")


def test_oos_mode_is_pinned_to_2025():
    c = OOSContract()
    c.validate_partition(2025, "oos_evaluation")
    try:
        c.validate_partition(2024, "oos_evaluation")
    except ValueError:
        pass
    else:
        raise AssertionError("Non-2025 data was accepted as OOS evaluation")


def test_legacy_backtest_cannot_be_attributed():
    c = OOSContract()
    try:
        c.validate_legacy_backtest_attribution(
            is_frozen_brain_path=False,
            costs_applied=False,
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("Legacy backtest was incorrectly accepted")


def test_unconfigured_or_unknown_mode_fails_closed():
    c = OOSContract()
    try:
        c.validate_partition(2025, "unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown evaluation mode did not fail closed")
