"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Main Flask application for ObsGraph.
License: MIT
"""

import base64
from datetime import datetime
from inspect import currentframe
from logging import ERROR
import os
from typing import Any, List, Optional, Tuple

import requests
from flask import Flask, render_template, request

from lib.keys import ObsKeys

from jsktoolbox.configtool import Config
from jsktoolbox.stringtool import SimpleCrypto
from jsktoolbox.basetool import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import ReadOnlyClass


# Classes and functions for the Flask application can be defined here.


class _AppKeys(object, metaclass=ReadOnlyClass):
    """Application keys for ObsGraph Flask app."""

    CONFIG: str = "__config__"
    ERROR_MESSAGE: str = "__error_message__"


class ObsGraphApp(BData):
    """Main application class for ObsGraph Flask app."""

    def __init__(self) -> None:
        """Initialize the application with the given config file."""
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        config_file_path: str = os.path.join(
            f"{current_dir}/../etc/", ObsKeys.CONF_FILE
        )

        # Set up error message list
        self._set_data(
            key=_AppKeys.ERROR_MESSAGE,
            value=[],
            set_default_type=List[str],
        )
        # Set up configuration
        self._set_data(
            key=_AppKeys.CONFIG,
            value=Config(
                filename=config_file_path,
                main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
            ),
            set_default_type=Config,
        )

        # Load configuration
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from the config file."""
        conf: Config = self.__config

        if conf.load() is False:
            self.error_messages.append("Failed to load configuration file.")
            return

        # Validate required configuration keys
        required_keys: List[str] = [
            ObsKeys.CONF_SALT,
            ObsKeys.CONF_OBSERVIUM_API_URL,
            ObsKeys.CONF_API_LOGIN,
            ObsKeys.CONF_API_PASSWORD,
            ObsKeys.CONF_PORT_IDS,
        ]

        for key in required_keys:
            if not conf.has_varname(
                section_name=ObsKeys.CONF_MAIN_SECTION_NAME, varname=key
            ):
                error_message: str = f"Missing required configuration key: {key}"
                self.error_messages.append(error_message)

    def get_observium_charts(self, year: int, month: int) -> Optional[str]:
        """Get Observium charts for the given year and month.

        ### Arguments:
        * year: int - The year for which to retrieve the chart.
        * month: int - The month for which to retrieve the chart.

        ### Returns:
        Optional[str] - Base64 encoded image data for embedding in HTML, or None if error occurs.

        ### Examples:
        curl template:
        curl -u {self.conf_api_login}:{self.conf_api_password} "{self.conf_observium_url}/graph.php?type=multi-port_bits&id=496,508&from={self.__get_month_timestamp_range(year, month)[0]}&to={self.__get_month_timestamp_range(year, month)[1]}&height=748&width=1024"
        """
        # Check if configuration is available
        if self.has_errors:
            return None

        # Get timestamp range for the month
        start_ts, end_ts = self.__get_month_timestamp_range(year, month)

        # Build the API URL
        url: str = (
            f"{self.conf_observium_url}/graph.php?"
            f"type=multi-port_bits&"
            f"id={self.conf_port_ids}&"
            f"from={start_ts}&"
            f"to={end_ts}&"
            f"height=600&"
            f"width=1024"
        )

        try:
            # Make the API request with basic authentication
            response: requests.Response = requests.get(
                url,
                auth=(self.conf_api_login, self.conf_api_password),
                timeout=30,
            )

            # Check if request was successful
            if response.status_code != 200:
                error_msg: str = f"Failed to fetch chart: HTTP {response.status_code}"
                self.error_messages.append(error_msg)
                return None

            # Check if response contains image data
            content_type: str = response.headers.get("Content-Type", "")
            if "image" not in content_type:
                error_msg = (
                    f"Unexpected content type: {content_type}. " f"Expected image data."
                )
                self.error_messages.append(error_msg)
                return None

            # Encode image to base64 for HTML embedding
            image_base64: str = base64.b64encode(response.content).decode("utf-8")
            return f"data:{content_type};base64,{image_base64}"

        except requests.exceptions.Timeout:
            self.error_messages.append(
                "Request timeout: Observium API did not respond in time."
            )
            return None
        except requests.exceptions.ConnectionError:
            self.error_messages.append(
                "Connection error: Unable to connect to Observium API."
            )
            return None
        except requests.exceptions.RequestException as exc:
            self.error_messages.append(f"Request error: {str(exc)}")
            return None
        except Exception as exc:
            self.error_messages.append(
                f"Unexpected error while fetching chart: {str(exc)}"
            )
            return None

    def __get_month_timestamp_range(self, year: int, month: int) -> Tuple[int, int]:
        """Get the start and end timestamps for a given month and year.

        ### Args:
        year (int): The year.
        month (int): The month.

        ### Returns:
        Optional[tuple]: A tuple containing start and end timestamps, or None if invalid.
        """
        # 1. Calculate the Unix timestamp for the start of the month (00:00:00 on the 1st)
        start_dt = datetime(year, month, 1, 0, 0, 0)
        start_ts = int(start_dt.timestamp())

        # 2. Determine the next month and year
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        # 3. Calculate the Unix timestamp for the start of the next month
        next_start_dt = datetime(next_year, next_month, 1, 0, 0, 0)

        # 4. The end of the selected month (23:59:59 on the last day) is 1 second before
        # the start of the next month
        end_ts = int(next_start_dt.timestamp()) - 1

        return (start_ts, end_ts)

    @property
    def __config(self) -> Config:
        """Get the configuration object."""
        config: Optional[Config] = self._get_data(_AppKeys.CONFIG)
        if config is None:
            raise Raise.error(
                message="Configuration not initialized in ObsGraphApp",
                exception=RuntimeError,
                class_name=self._c_name,
                currentframe=currentframe(),
            )
        return config

    @property
    def error_messages(self) -> List[str]:
        """Get the list of error messages."""
        errors = self._get_data(_AppKeys.ERROR_MESSAGE)
        if errors is None:
            raise Raise.error(
                message="Error messages not initialized in ObsGraphApp",
                exception=RuntimeError,
                class_name=self._c_name,
                currentframe=currentframe(),
            )
        return errors

    @property
    def has_errors(self) -> bool:
        """Check if there are any error messages."""
        return len(self.error_messages) > 0

    @property
    def conf_salt(self) -> int:
        """Get the application salt from configuration."""
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_SALT
        )
        if value is None:
            self.error_messages.append("Salt value not found in configuration.")
            return -1
        return value

    @property
    def conf_observium_url(self) -> str:
        """Get the Observium API URL from configuration."""
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME,
            varname=ObsKeys.CONF_OBSERVIUM_API_URL,
        )
        if value is None:
            self.error_messages.append("Observium API URL not found in configuration.")
            return ""
        return value

    @property
    def conf_api_login(self) -> str:
        """Get the API login from configuration."""
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_API_LOGIN
        )
        if value is None:
            self.error_messages.append("API login not found in configuration.")
            return ""
        return value

    @property
    def conf_api_password(self) -> str:
        """Get the API password from configuration."""
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_API_PASSWORD
        )
        if value is None:
            self.error_messages.append("API password not found in configuration.")
            return ""
        return SimpleCrypto.multiple_decrypt(self.conf_salt, value)

    @property
    def conf_port_ids(self) -> str:
        """Get the port IDs from configuration.

        ### Returns:
        str - Comma-separated port IDs for the Observium API request.
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_PORT_IDS
        )
        if value is None:
            self.error_messages.append("Port IDs not found in configuration.")
            return ""
        return value


# Initialize Flask application
app: Flask = Flask(__name__)
obs_app: ObsGraphApp = ObsGraphApp()


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    """Main page with year and month selection.

    ### Returns:
    str - Rendered HTML template with date selection form.
    """
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month

    # Generate year list (current year + 3 years back)
    years: List[int] = list(range(current_year, current_year - 4, -1))

    # Generate month list (1-12)
    months: List[int] = list(range(1, 13))

    # Get selected values from form or use defaults
    selected_year: int = request.form.get("year", current_year, type=int)
    selected_month: int = request.form.get("month", current_month, type=int)

    # Format selected date
    selected_date: str = f"{selected_year:04d}-{selected_month:02d}"

    # Get chart from Observium API
    chart_image: Optional[str] = obs_app.get_observium_charts(
        selected_year, selected_month
    )

    # Collect errors
    error_messages: List[str] = []
    while obs_app.error_messages:
        line: str = obs_app.error_messages.pop()
        error_messages.append(line)

    # # Test get_month_timestamp_range
    # start_ts, end_ts = obs_app.get_month_timestamp_range(selected_year, selected_month)
    # print(f"Selected month {selected_date} has timestamps: {start_ts} - {end_ts}")

    # Render template with data
    return render_template(
        "index.html",
        years=years,
        months=months,
        selected_year=selected_year,
        selected_month=selected_month,
        selected_date=selected_date,
        chart_image=chart_image,
        errors=error_messages,
    )


if __name__ == "__main__":
    app.run(debug=True)
