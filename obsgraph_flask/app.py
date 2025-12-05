"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Main Flask application for ObsGraph network monitoring visualization.

This module provides a Flask-based web application that fetches and displays
network traffic graphs from Observium API. It includes configuration management,
error handling, and a responsive user interface for date-based chart selection.

License: MIT
"""

import base64
from datetime import datetime
from inspect import currentframe
import os
from typing import List, Optional, Tuple

import requests
from flask import Flask, render_template, request

from obsgraph_flask.lib.keys import ObsKeys

from jsktoolbox.configtool import Config
from jsktoolbox.stringtool import SimpleCrypto
from jsktoolbox.basetool import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import ReadOnlyClass


# Classes and functions for the Flask application can be defined here.


class _AppKeys(object, metaclass=ReadOnlyClass):
    """Internal keys for ObsGraphApp BData storage.

    This class defines the keys used for storing configuration and error messages
    in the ObsGraphApp instance using BData's key-value storage mechanism.
    """

    CONFIG: str = "__config__"
    ERROR_MESSAGE: str = "__error_message__"


class ObsGraphApp(BData):
    """Main application class for ObsGraph Flask application.

    This class manages the application configuration, communicates with Observium API
    to fetch network traffic graphs, and handles error messages. It inherits from
    BData to utilize type-safe data storage for configuration and error management.

    The application loads configuration from etc/obsgraph.conf and validates required
    parameters including API credentials, URL, and port IDs.
    """

    def __init__(self) -> None:
        """Initialize the application with configuration file.

        Sets up BData storage for configuration and error messages, locates the
        configuration file in etc/ directory, and loads application settings.

        ### Raises:
        * RuntimeError: If configuration initialization fails.
        """
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
        """Load and validate configuration from the config file.

        Attempts to load the configuration file and validates the presence of all
        required configuration keys. If any required key is missing, an error
        message is added to the error_messages list.

        ### Returns:
        None - Errors are stored in error_messages property.
        """
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
        """Fetch Observium network traffic chart for the specified month.

        Constructs an API request to Observium for multi-port traffic graphs,
        retrieves the image data, and encodes it as base64 data URI for HTML embedding.
        Handles authentication, timeout, and various error conditions.

        ### Arguments:
        * year: int - The year for which to retrieve the chart (e.g., 2025).
        * month: int - The month for which to retrieve the chart (1-12).

        ### Returns:
        Optional[str] - Base64 encoded data URI (data:image/png;base64,...) for HTML <img> tag,
                       or None if configuration errors exist or request fails.

        ### Raises:
        Does not raise exceptions; errors are added to error_messages list.

        ### Examples:
        ```python
        chart = obs_app.get_observium_charts(2025, 11)
        if chart:
            # Use in HTML: <img src="{chart}">
            pass
        ```

        Equivalent curl command:
        ```bash
        curl -u api_user:api_pass "https://observium.example.com/graph.php?type=multi-port_bits&id=496,508&from=1698796800&to=1701388799&height=600&width=1024"
        ```
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
            f"height={self.conf_graph_height}&"
            f"width={self.conf_graph_width}"
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
        """Calculate Unix timestamp range for the specified month.

        Computes the start timestamp (00:00:00 on the 1st) and end timestamp
        (23:59:59 on the last day) for the given month and year.

        ### Arguments:
        * year: int - The year (e.g., 2025).
        * month: int - The month (1-12).

        ### Returns:
        Tuple[int, int] - A tuple of (start_timestamp, end_timestamp) in Unix epoch seconds.

        ### Examples:
        ```python
        start, end = self.__get_month_timestamp_range(2025, 11)
        # start: 1730419200 (2025-11-01 00:00:00)
        # end: 1733011199 (2025-11-30 23:59:59)
        ```
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
        """Get the configuration object from BData storage.

        ### Returns:
        Config - The JskToolBox Config instance containing application settings.

        ### Raises:
        * RuntimeError: If configuration object is not initialized in BData storage.
        """
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
        """Get the mutable list of error messages.

        This property provides direct access to the error messages list stored
        in BData. Errors can be added using list.append() or removed using list.pop().

        ### Returns:
        List[str] - Mutable list of error message strings.

        ### Raises:
        * RuntimeError: If error messages list is not initialized in BData storage.
        """
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
        """Check if any error messages are present.

        ### Returns:
        bool - True if error_messages list contains one or more errors, False otherwise.
        """
        return len(self.error_messages) > 0

    @property
    def conf_salt(self) -> int:
        """Get the salt value used for password encryption/decryption.

        ### Returns:
        int - Salt value for SimpleCrypto operations, or -1 if not found in configuration.
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_SALT
        )
        if value is None:
            self.error_messages.append("Salt value not found in configuration.")
            return -1
        return value

    @property
    def conf_observium_url(self) -> str:
        """Get the base URL of the Observium instance.

        ### Returns:
        str - Base URL (e.g., 'https://observium.example.com/'), or empty string if not found.
        """
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
        """Get the Observium API username.

        ### Returns:
        str - API username for HTTP Basic authentication, or empty string if not found.
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_API_LOGIN
        )
        if value is None:
            self.error_messages.append("API login not found in configuration.")
            return ""
        return value

    @property
    def conf_api_password(self) -> str:
        """Get the decrypted Observium API password.

        Retrieves the encrypted password from configuration and decrypts it
        using SimpleCrypto with the configured salt value.

        ### Returns:
        str - Decrypted API password for HTTP Basic authentication, or empty string if not found.
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_API_PASSWORD
        )
        if value is None:
            self.error_messages.append("API password not found in configuration.")
            return ""
        return SimpleCrypto.multiple_decrypt(self.conf_salt, value)

    @property
    def conf_port_ids(self) -> str:
        """Get the comma-separated port IDs for multi-port graphs.

        These IDs are used in the Observium API request to specify which network
        ports should be included in the traffic graph.

        ### Returns:
        str - Comma-separated port IDs (e.g., '496,508'), or empty string if not found.
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_PORT_IDS
        )
        if value is None:
            self.error_messages.append("Port IDs not found in configuration.")
            return ""
        return value

    @property
    def conf_graph_width(self) -> int:
        """Get graph width from configuration.

        ### Returns:
        int - Width of the graph in pixels (default: 1024).
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_GRAPH_WIDTH
        )
        if value is None:
            return 1024
        return int(value)

    @property
    def conf_graph_height(self) -> int:
        """Get graph height from configuration.

        ### Returns:
        int - Height of the graph in pixels (default: 600).
        """
        value = self.__config.get(
            section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_GRAPH_HEIGHT
        )
        if value is None:
            return 600
        return int(value)


# Initialize Flask application
app: Flask = Flask(__name__)
obs_app: ObsGraphApp = ObsGraphApp()


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    """Render the main page with date selection and Observium chart display.

    Handles both GET (initial page load) and POST (form submission) requests.
    On GET, displays current month's chart. On POST, displays chart for selected
    year and month. Collects and displays any errors in the page footer.

    ### Returns:
    str - Rendered HTML template with form controls, chart image, and error messages.
    """
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month

    # Generate year list (current year + 1 years back)
    years: List[int] = list(range(current_year, current_year - 2, -1))

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
