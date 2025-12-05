# -*- coding: utf-8 -*-
"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-12-03

Purpose: Configuration keys and constants for ObsGraph Flask application.

This module defines ReadOnlyClass-based constants used for configuration
management throughout the application. Keys are immutable once defined.

License: MIT
"""

from jsktoolbox.attribtool import ReadOnlyClass


class ObsKeys(object, metaclass=ReadOnlyClass):
    """Read-only configuration keys for ObsGraph Flask application.

    This class uses ReadOnlyClass metaclass to ensure that all key values
    are immutable after class definition. Keys are used to access configuration
    values from the Config object and maintain consistency across the application.
    """

    CONF_MAIN_SECTION_NAME: str = "ObsGraphFlaskApp"
    CONF_SALT: str = "salt"
    CONF_OBSERVIUM_API_URL: str = "observium_url"
    CONF_API_LOGIN: str = "api_login"
    CONF_API_PASSWORD: str = "api_password"
    CONF_PORT_IDS: str = "port_ids"
    CONF_GRAPH_WIDTH: str = "graph_width"
    CONF_GRAPH_HEIGHT: str = "graph_height"
    CONF_FILE: str = "obsgraph.conf"


# #[EOF]#######################################################################
