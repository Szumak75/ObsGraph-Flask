"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-12-05

Purpose: Tests for utility functions and timestamp calculations.

This module contains tests for timestamp calculation logic and date utilities.
Full integration tests with ObsGraphApp configuration are performed through
Flask test client in test_app.py due to BData's strict type checking requirements.
"""

from datetime import datetime
import os
import tempfile
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from jsktoolbox.configtool import Config
from jsktoolbox.stringtool import SimpleCrypto

from obsgraph_flask.app import ObsGraphApp
from obsgraph_flask.lib.keys import ObsKeys


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


@pytest.fixture
def temp_config_with_dual_ports() -> str:
    """Create a temporary configuration file for dual-port graph tests.

    ### Returns:
    str - Path to temporary configuration file.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as file:
        config_path: str = file.name

    config: Config = Config(
        filename=config_path,
        main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
    )
    salt: int = SimpleCrypto.salt_generator(16)

    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_SALT,
        value=salt,
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_OBSERVIUM_API_URL,
        value="https://observium.example.com/",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_API_LOGIN,
        value="api_user",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_API_PASSWORD,
        value=SimpleCrypto.multiple_encrypt(salt, "api_password"),
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_PORT_HEADER1,
        value="TASK",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_PORT_HEADER2,
        value="Biuro",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_PORT_IDS1,
        value="496,508",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_PORT_IDS2,
        value="677",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_GRAPH_WIDTH,
        value=1200,
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_GRAPH_HEIGHT,
        value=500,
    )
    config.save()

    yield config_path
    os.unlink(config_path)


class TestObsGraphDualCharts:
    """Test suite for dual chart generation based on new configuration keys."""

    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_load_config_accepts_dual_port_keys(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_dual_ports: str,
    ) -> None:
        """Test that configuration validation accepts port_ids1/2 and headers."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_dual_ports

        obs_app: ObsGraphApp = ObsGraphApp()

        assert obs_app.has_errors is False
        assert obs_app.conf_port_header1 == "TASK"
        assert obs_app.conf_port_header2 == "Biuro"
        assert obs_app.conf_port_ids1 == "496,508"
        assert obs_app.conf_port_ids2 == "677"

    @patch("obsgraph_flask.app.requests.get")
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_get_observium_charts_generates_multi_and_single_port_requests(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        mock_get: MagicMock,
        temp_config_with_dual_ports: str,
    ) -> None:
        """Test that chart type depends on whether IDs contain one or many ports."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_dual_ports

        response: MagicMock = MagicMock()
        response.status_code = 200
        response.headers = {"Content-Type": "image/png"}
        response.content = b"fake-image"
        mock_get.return_value = response

        obs_app: ObsGraphApp = ObsGraphApp()

        charts: Any = obs_app.get_observium_charts(2025, 10)

        assert isinstance(charts, list)
        assert len(charts) == 2
        assert charts[0]["header"] == "TASK"
        assert charts[1]["header"] == "Biuro"
        assert "data:image/png;base64," in charts[0]["image"]
        assert "data:image/png;base64," in charts[1]["image"]

        first_url: str = mock_get.call_args_list[0].args[0]
        second_url: str = mock_get.call_args_list[1].args[0]

        assert "type=multi-port_bits" in first_url
        assert "id=496,508" in first_url
        assert "type=port_bits" in second_url
        assert "id=677" in second_url
