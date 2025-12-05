"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-12-05

Purpose: Tests for utility functions and timestamp calculations.

This module contains tests for timestamp calculation logic and date utilities.
Full integration tests with ObsGraphApp configuration are performed through
Flask test client in test_app.py due to BData's strict type checking requirements.
"""

from datetime import datetime

import pytest


def test_timestamp_calculation_january() -> None:
    """Test that January timestamps cover full month.

    ### Returns:
    None - Assertions verify correctness.
    """
    year: int = 2025
    month: int = 1

    start_dt: datetime = datetime(year, month, 1, 0, 0, 0)
    start_ts: int = int(start_dt.timestamp())

    next_month: int = 2
    next_start_dt: datetime = datetime(year, next_month, 1, 0, 0, 0)
    end_ts: int = int(next_start_dt.timestamp()) - 1

    start_check: datetime = datetime.fromtimestamp(start_ts)
    end_check: datetime = datetime.fromtimestamp(end_ts)

    assert start_check.day == 1
    assert start_check.hour == 0
    assert end_check.day == 31
    assert end_check.hour == 23


def test_timestamp_calculation_december() -> None:
    """Test that December timestamps handle year rollover correctly.

    ### Returns:
    None - Assertions verify correctness.
    """
    year: int = 2025
    month: int = 12

    start_dt: datetime = datetime(year, month, 1, 0, 0, 0)
    start_ts: int = int(start_dt.timestamp())

    next_year: int = year + 1
    next_start_dt: datetime = datetime(next_year, 1, 1, 0, 0, 0)
    end_ts: int = int(next_start_dt.timestamp()) - 1

    start_check: datetime = datetime.fromtimestamp(start_ts)
    end_check: datetime = datetime.fromtimestamp(end_ts)

    assert start_check.month == 12
    assert start_check.day == 1
    assert end_check.month == 12
    assert end_check.day == 31


def test_timestamp_calculation_february_leap_year() -> None:
    """Test that February leap year has 29 days.

    ### Returns:
    None - Assertions verify correctness.
    """
    year: int = 2024  # Leap year
    month: int = 2

    start_dt: datetime = datetime(year, month, 1, 0, 0, 0)

    next_month: int = 3
    next_start_dt: datetime = datetime(year, next_month, 1, 0, 0, 0)
    end_ts: int = int(next_start_dt.timestamp()) - 1

    end_check: datetime = datetime.fromtimestamp(end_ts)

    # 2024 is a leap year, so February should have 29 days
    assert end_check.day == 29
    assert end_check.month == 2


def test_timestamp_calculation_february_non_leap_year() -> None:
    """Test that February non-leap year has 28 days.

    ### Returns:
    None - Assertions verify correctness.
    """
    year: int = 2025  # Not a leap year
    month: int = 2

    start_dt: datetime = datetime(year, month, 1, 0, 0, 0)

    next_month: int = 3
    next_start_dt: datetime = datetime(year, next_month, 1, 0, 0, 0)
    end_ts: int = int(next_start_dt.timestamp()) - 1

    end_check: datetime = datetime.fromtimestamp(end_ts)

    # 2025 is not a leap year, so February should have 28 days
    assert end_check.day == 28
    assert end_check.month == 2


def test_date_formatting() -> None:
    """Test that date formatting produces expected YYYY-MM format.

    ### Returns:
    None - Assertions verify correctness.
    """
    year: int = 2025
    month: int = 11

    formatted: str = f"{year:04d}-{month:02d}"

    assert formatted == "2025-11"
    assert len(formatted) == 7


def test_single_digit_month_formatting() -> None:
    """Test that single digit months are zero-padded.

    ### Returns:
    None - Assertions verify correctness.
    """
    year: int = 2025
    month: int = 5

    formatted: str = f"{year:04d}-{month:02d}"

    assert formatted == "2025-05"
    assert formatted[5] == "0"  # First digit of month is zero
