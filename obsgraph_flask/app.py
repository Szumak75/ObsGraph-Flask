"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Main Flask application for ObsGraph.
License: MIT
"""

from datetime import datetime
from inspect import currentframe
from logging import ERROR
import os
from typing import List, Optional

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
        config_file_path: str = os.path.join(f"{current_dir}/etc/", ObsKeys.CONF_FILE)

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

        # Validate required configuration keys
        required_keys: List[str] = [
            ObsKeys.CONF_SALT,
            ObsKeys.CONF_OBSERVIUM_API_URL,
            ObsKeys.CONF_API_LOGIN,
            ObsKeys.CONF_API_PASSWORD,
        ]

        for key in required_keys:
            if not conf.has_varname(
                section_name=ObsKeys.CONF_MAIN_SECTION_NAME, varname=key
            ):
                error_message: str = f"Missing required configuration key: {key}"
                self.error_messages.append(error_message)

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

    # Errors
    error_messages: List[str] = []
    if obs_app.has_errors:
        error_messages.append(obs_app.error_messages.pop())

    return render_template(
        "index.html",
        years=years,
        months=months,
        selected_year=selected_year,
        selected_month=selected_month,
        selected_date=selected_date,
        errors=error_messages,
    )


if __name__ == "__main__":
    app.run(debug=True)
