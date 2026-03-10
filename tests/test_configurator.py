#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_configurator.py
Author : Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 05.12.2025

Purpose: Unit tests for ObsGraphConfigurator
"""

import os
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch, MagicMock
import pytest

from jsktoolbox.configtool import Config
from jsktoolbox.systemtool import CommandLineParser
from jsktoolbox.stringtool import SimpleCrypto

from obsgraph_flask.tools.obsgraph_configurator import (
    ObsGraphConfigurator,
    _Keys,
)
from obsgraph_flask.lib.keys import ObsKeys


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing.

    ### Returns:
    Generator yielding path to temporary configuration file
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
        config_path: str = f.name
    yield config_path
    # Cleanup
    if os.path.exists(config_path):
        os.unlink(config_path)


@pytest.fixture
def temp_config_with_salt(temp_config_file: str):
    """Create a temporary config file with salt for testing.

    ### Arguments:
    * temp_config_file: str - Path to temporary config file

    ### Returns:
    Generator yielding path to configured temporary file
    """
    config: Config = Config(
        filename=temp_config_file, main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME
    )

    salt: int = SimpleCrypto.salt_generator(16)
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME, varname=ObsKeys.CONF_SALT, value=salt
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_OBSERVIUM_API_URL,
        value="http://test.local/",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_API_LOGIN,
        value="test_user",
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_API_PASSWORD,
        value=SimpleCrypto.multiple_encrypt(salt, "test_password"),
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
        value=1024,
    )
    config.set(
        section=ObsKeys.CONF_MAIN_SECTION_NAME,
        varname=ObsKeys.CONF_GRAPH_HEIGHT,
        value=600,
    )
    config.save()

    return temp_config_file


class TestObsGraphConfiguratorInit:
    """Test ObsGraphConfigurator initialization."""

    def test_init_creates_default_config_if_not_exists(self) -> None:
        """Test that __init__ creates default config file if it does not exist."""
        import tempfile
        import shutil

        # Create temp directory
        temp_dir: str = tempfile.mkdtemp()
        temp_path: str = os.path.join(temp_dir, "test_config.conf")

        try:
            with patch(
                "obsgraph_flask.tools.obsgraph_configurator.SimpleCrypto.salt_generator"
            ) as mock_salt:
                with patch("os.path.join") as mock_join:
                    with patch("os.path.dirname") as mock_dirname:
                        with patch("os.path.abspath") as mock_abspath:
                            mock_salt.return_value = 12345
                            mock_abspath.return_value = "/fake/path"
                            mock_dirname.return_value = "/fake"
                            mock_join.return_value = temp_path

                            configurator: ObsGraphConfigurator = ObsGraphConfigurator()

                            # Verify config file was created
                            assert os.path.exists(temp_path)

                            # Read file contents to verify structure
                            with open(temp_path, "r") as f:
                                content: str = f.read()

                            # Verify key content is present
                            assert "[ObsGraphFlaskApp]" in content
                            assert "salt" in content
                            assert "12345" in content
                            assert (
                                "observium_url" in content
                                or "observium_api_url" in content
                            )
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestObsGraphConfiguratorRun:
    """Test ObsGraphConfigurator.run() method with integration tests."""

    @patch("sys.argv", ["obsgraph_configurator.py", "--help"])
    @patch("sys.exit")
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_exits_on_help_option(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        mock_exit: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() exits when help option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        mock_exit.assert_called_once_with(0)

    @patch("sys.argv", ["obsgraph_configurator.py", "--url", "http://new.local/"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_url_option(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates URL when CLI option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        # Verify config was updated
        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_OBSERVIUM_API_URL)
            == "http://new.local/"
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--login", "new_user"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_login_option(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates login when CLI option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        # Verify config was updated
        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_API_LOGIN)
            == "new_user"
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--password", "new_password"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_password_option_with_encryption(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() encrypts and updates password when CLI option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()

        # Get salt for verification
        config_pre: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config_pre.load()
        salt: int = config_pre.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_SALT)

        configurator.run()

        # Verify config was updated with encrypted password
        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        encrypted_password: str = config.get(
            ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_API_PASSWORD
        )

        # Verify it's encrypted (should be different from plain text)
        assert encrypted_password != "new_password"

        # Verify it can be decrypted back
        decrypted: str = SimpleCrypto.multiple_decrypt(salt, encrypted_password)
        assert decrypted == "new_password"

    @patch("sys.argv", ["obsgraph_configurator.py", "--ids", "123,456,789"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_port_ids1_option_with_legacy_alias(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() maps legacy --ids to port_ids1."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        # Verify config was updated
        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_PORT_IDS1)
            == "123,456,789"
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--ids2", "987"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_port_ids2_option(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates second graph port IDs when CLI option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_PORT_IDS2) == "987"
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--header1", "Nowy TASK"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_port_header1_option(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates first graph header."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_PORT_HEADER1)
            == "Nowy TASK"
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--header2", "Nowe Biuro"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_port_header2_option(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates second graph header."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_PORT_HEADER2)
            == "Nowe Biuro"
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--width", "1920"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_graph_width(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates graph width when CLI option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        # Verify config was updated
        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_GRAPH_WIDTH) == 1920
        )

    @patch("sys.argv", ["obsgraph_configurator.py", "--height", "800"])
    @patch("os.path.join")
    @patch("os.path.dirname")
    @patch("os.path.abspath")
    def test_run_updates_graph_height(
        self,
        mock_abspath: MagicMock,
        mock_dirname: MagicMock,
        mock_join: MagicMock,
        temp_config_with_salt: str,
    ) -> None:
        """Test that run() updates graph height when CLI option is provided."""
        mock_abspath.return_value = "/fake/path"
        mock_dirname.return_value = "/fake"
        mock_join.return_value = temp_config_with_salt

        configurator: ObsGraphConfigurator = ObsGraphConfigurator()
        configurator.run()

        # Verify config was updated
        config: Config = Config(
            filename=temp_config_with_salt,
            main_section_name=ObsKeys.CONF_MAIN_SECTION_NAME,
        )
        assert config.load()
        assert (
            config.get(ObsKeys.CONF_MAIN_SECTION_NAME, ObsKeys.CONF_GRAPH_HEIGHT) == 800
        )


class TestKeysClass:
    """Test _Keys configuration constants."""

    def test_keys_class_has_conf_key(self) -> None:
        """Test that _Keys has CONF constant."""
        assert hasattr(_Keys, "CONF")
        assert _Keys.CONF == "__config__"

    def test_keys_class_has_cli_key(self) -> None:
        """Test that _Keys has CLI constant."""
        assert hasattr(_Keys, "CLI")
        assert _Keys.CLI == "__cli__"

    def test_keys_class_has_all_cli_options(self) -> None:
        """Test that _Keys has all CLI option constants."""
        assert _Keys.SHORT_URL == "u"
        assert _Keys.LONG_URL == "url"
        assert _Keys.SHORT_LOGIN == "l"
        assert _Keys.LONG_LOGIN == "login"
        assert _Keys.SHORT_WIDTH == "w"
        assert _Keys.LONG_WIDTH == "width"
        assert _Keys.SHORT_HEIGHT == "g"
        assert _Keys.LONG_HEIGHT == "height"
        assert _Keys.SHORT_PASSWORD == "p"
        assert _Keys.LONG_PASSWORD == "password"
        assert _Keys.SHORT_HELP == "h"
        assert _Keys.LONG_HELP == "help"
        assert _Keys.SHORT_IDS == "i"
        assert _Keys.LONG_IDS == "ids"
        assert _Keys.LONG_IDS1 == "ids1"
        assert _Keys.LONG_IDS2 == "ids2"
        assert _Keys.LONG_HEADER1 == "header1"
        assert _Keys.LONG_HEADER2 == "header2"


# #[EOF]#######################################################################
