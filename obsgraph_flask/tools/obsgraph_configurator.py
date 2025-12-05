#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsgraph_configurator.py
Author : Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 17.10.2025, 12:30:19

Purpose: ObsGraph configuration tool
License: MIT
"""

from inspect import currentframe
import os
from pathlib import Path
import sys
from typing import Optional

from jsktoolbox.configtool import Config
from jsktoolbox.basetool import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.systemtool import CommandLineParser
from jsktoolbox.stringtool import SimpleCrypto

# Add project root to Python path
project_root: Path = Path(__file__).parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from lib.keys import ObsKeys


class _Keys(object, metaclass=ReadOnlyClass):
    """Configuration keys for ObsGraphConfigurator."""

    CONF: str = "__config__"
    CLI: str = "__cli__"

    SHORT_URL: str = "u"
    LONG_URL: str = "url"
    SHORT_LOGIN: str = "l"
    LONG_LOGIN: str = "login"
    SHORT_PASSWORD: str = "p"
    LONG_PASSWORD: str = "password"
    SHORT_HELP: str = "h"
    LONG_HELP: str = "help"
    SHORT_IDS: str = "i"
    LONG_IDS: str = "ids"


class ObsGraphConfigurator(BData):
    """ObsGraph configuration tool."""

    def __init__(self) -> None:
        """Initialize the configurator with the given config file path."""
        # current dynamic project directory
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        config_file_path: str = os.path.join(
            f"{current_dir}/../../etc/", ObsKeys.CONF_FILE
        )
        print(f"Using configuration file: {config_file_path}")

        # Set up configuration
        self._set_data(
            key=_Keys.CONF,
            value=Config(
                filename=config_file_path,
                main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
            ),
            set_default_type=Config,
        )

        # Set up command line parser
        self._set_data(
            key=_Keys.CLI,
            value=CommandLineParser(),
            set_default_type=CommandLineParser,
        )

        # Configure CLI Parser
        self.__cli_configure()

        # Create default config if it does not exist
        if not self.__config.file_exists:
            self.__create_config()

    def run(self) -> None:
        """Run the configurator."""
        cli: CommandLineParser = self.__cli
        conf: Config = self.__config
        salt = 0
        update = False

        # try to load existing configuration
        if not conf.load():
            raise Raise.error(
                f"Failed to load configuration file",
                RuntimeError,
                self._c_name,
                currentframe(),
            )

        # Parse command line arguments
        cli.parse()

        # If help option is set, show help and exit
        if cli.has_option(_Keys.LONG_HELP):
            cli.help()
            sys.exit(0)

        # Get existing salt value
        if conf.has_section(ObsKeys.CONF_MAIN_SECTION_NAME) and conf.has_varname(
            ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_SALT
        ):
            salt: int = conf.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_SALT)
        else:
            raise Raise.error(
                f"Configuration file is missing required salt value",
                RuntimeError,
                self._c_name,
                currentframe(),
            )

        # Update configuration based on CLI options
        if cli.has_option(_Keys.LONG_URL):
            url_value: Optional[str] = cli.get_option(_Keys.LONG_URL)
            if url_value is not None:
                conf.set(
                    section=ObsKeys.CONF_MAIN_SECTION_NAME,
                    varname=ObsKeys.CONF_OBSERVIUM_API_URL,
                    value=url_value,
                )
                update = True
        if cli.has_option(_Keys.LONG_LOGIN):
            login_value: Optional[str] = cli.get_option(_Keys.LONG_LOGIN)
            if login_value is not None:
                conf.set(
                    section=ObsKeys.CONF_MAIN_SECTION_NAME,
                    varname=ObsKeys.CONF_API_LOGIN,
                    value=login_value,
                )
                update = True
        if cli.has_option(_Keys.LONG_PASSWORD):
            password_value: Optional[str] = cli.get_option(_Keys.LONG_PASSWORD)
            if password_value is not None:
                encrypted_password: str = SimpleCrypto.multiple_encrypt(
                    salt, password_value
                )
                conf.set(
                    section=ObsKeys.CONF_MAIN_SECTION_NAME,
                    varname=ObsKeys.CONF_API_PASSWORD,
                    value=encrypted_password,
                )
                update = True
        if cli.has_option(_Keys.LONG_IDS):
            ids_value: Optional[str] = cli.get_option(_Keys.LONG_IDS)
            if ids_value is not None:
                conf.set(
                    section=ObsKeys.CONF_MAIN_SECTION_NAME,
                    varname=ObsKeys.CONF_PORT_IDS,
                    value=ids_value,
                )
                update = True

        # Save updated configuration if any changes were made
        if update:
            print("Updating configuration file...")
            conf.save()

    def __cli_configure(self) -> None:
        """Configure command line parser."""
        cli: CommandLineParser = self.__cli

        # Help option
        cli.configure_option(
            short_arg=_Keys.SHORT_HELP,
            long_arg=_Keys.LONG_HELP,
            desc_arg="Show this help message and exit",
        )

        # Observium API URL
        cli.configure_option(
            short_arg=_Keys.SHORT_URL,
            long_arg=_Keys.LONG_URL,
            desc_arg="Observium API URL",
            has_value=True,
            example_value="http://observium.local/",
        )

        # API Login
        cli.configure_option(
            short_arg=_Keys.SHORT_LOGIN,
            long_arg=_Keys.LONG_LOGIN,
            desc_arg="Observium API login",
            has_value=True,
            example_value="api_user",
        )

        # API Password
        cli.configure_option(
            short_arg=_Keys.SHORT_PASSWORD,
            long_arg=_Keys.LONG_PASSWORD,
            desc_arg="Observium API password",
            has_value=True,
            example_value="api_password",
        )

        # Port IDs
        cli.configure_option(
            short_arg=_Keys.SHORT_IDS,
            long_arg=_Keys.LONG_IDS,
            desc_arg="Comma-separated port IDs for multi-port graphs",
            has_value=True,
            example_value="496,508",
        )

    def __create_config(self) -> None:
        """Create a default configuration file if it does not exist."""
        conf: Config = self.__config

        if not conf.file_exists:
            salt: int = SimpleCrypto.salt_generator(16)

            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                desc="Main configuration for ObsGraph Flask application",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_SALT,
                value=salt,
                desc="Application salt value",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_OBSERVIUM_API_URL,
                value="",
                desc="Observium API URL",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_API_LOGIN,
                value="",
                desc="Observium API login",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_API_PASSWORD,
                value="",
                desc="Observium API password (encrypted)",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_PORT_IDS,
                value="",
                desc="Comma-separated port IDs for multi-port graphs",
            )
            conf.save()

    @property
    def __config(self) -> Config:
        """Get the configuration object."""
        conf = self._get_data(key=_Keys.CONF)
        if not conf or not isinstance(conf, Config):
            raise Raise.error(
                f"Configuration not set or invalid type: {type(conf)}",
                RuntimeError,
                self._c_name,
                currentframe(),
            )

        return conf

    @property
    def __cli(self) -> CommandLineParser:
        """Get the command line parser object."""
        cli = self._get_data(key=_Keys.CLI)
        if not cli or not isinstance(cli, CommandLineParser):
            raise Raise.error(
                f"CLI parser not set or invalid type: {type(cli)}",
                RuntimeError,
                self._c_name,
                currentframe(),
            )

        return cli


if __name__ == "__main__":
    print("ObsGraph Configurator")
    print("=====================")
    configurator = ObsGraphConfigurator()
    configurator.run()

    sys.exit(0)

# #[EOF]#######################################################################
