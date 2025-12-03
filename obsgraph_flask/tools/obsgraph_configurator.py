#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsgraph_configurator.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 17.10.2025, 12:30:19

Purpose: ObsGraph configuration tool
License: MIT
"""

from inspect import currentframe
import os
import sys

from jsktoolbox.configtool import Config
from jsktoolbox.basetool import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import ReadOnlyClass

from ..lib.keys import ObsKeys


class _Keys(object, metaclass=ReadOnlyClass):
    """Configuration keys for ObsGraphConfigurator."""

    CONF: str = "__config__"


class ObsGraphConfigurator(BData):
    """ObsGraph configuration tool."""

    def __init__(self) -> None:
        """Initialize the configurator with the given config file path."""
        # current dynamic project directory
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        config_file_path: str = os.path.join(current_dir, "obsgraph.conf")

        self._set_data(
            key=_Keys.CONF,
            value=Config(
                filename=config_file_path,
                main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
                auto_create=True,
            ),
            set_default_type=Config,
        )

        if not self.__config.file_exists:
            self.__create_config()

    def __create_config(self) -> None:
        """Create a default configuration file if it does not exist."""
        conf: Config = self.__config

        if not conf.file_exists:
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_SALT,
                value=0,
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_OBSERVIUM_API_URL,
                value="",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_API_LOGIN,
                value="",
            )
            conf.set(
                section=ObsKeys.CONF_MAIN_SECTION_NAME,
                varname=ObsKeys.CONF_API_PASSWORD,
                value="",
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


if __name__ == "__main__":
    print("ObsGraph Configurator")
    print("======================\n")
    configurator = ObsGraphConfigurator()

    sys.exit(0)

# #[EOF]#######################################################################
