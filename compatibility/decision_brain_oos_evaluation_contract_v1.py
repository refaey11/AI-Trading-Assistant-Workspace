"""Governed OOS evaluation contract for the frozen Decision Brain.

This module is intentionally a guard/contract, not a trading strategy.
It prevents accidental attribution of legacy backtests to the frozen V1 brain.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class OOSContract:
    oos_year: int = 2025
    development_end_year: int = 2024
    tuning_allowed_on_oos: bool = False
    calibration_allowed_on_oos: bool = False
    threshold_selection_allowed_on_oos: bool = False
    future_data_allowed: bool = False
    memory_direction_allowed: bool = False
    automatic_execution_in_v1: bool = False

    def validate_partition(self, year: int, mode: str) -> None:
        if mode == "development" and year >= self.oos_year:
            raise ValueError("2025+ is OOS and must not enter development.")
        if mode == "oos_evaluation" and year != self.oos_year:
            raise ValueError("OOS evaluation is pinned to 2025 in this contract.")
        if mode not in {"development", "oos_evaluation"}:
            raise ValueError("Unsupported evaluation mode.")

    def validate_frozen_decision_brain(self, *, produces_trade: bool) -> None:
        if produces_trade and self.automatic_execution_in_v1:
            raise AssertionError("V1 execution must remain disabled.")

    def validate_legacy_backtest_attribution(self, *, is_frozen_brain_path: bool, costs_applied: bool) -> None:
        if not is_frozen_brain_path:
            raise AssertionError("Legacy/alternate backtests cannot be attributed to frozen Decision Brain V1.")
        if not costs_applied:
            raise AssertionError("Performance attribution requires execution costs to be explicitly applied.")
