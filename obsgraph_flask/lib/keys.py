# -*- coding: utf-8 -*-
"""
keys.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 3.12.2025, 08:55:04

Purpose:
"""

from jsktoolbox.attribtool import ReadOnlyClass


class ObsKeys(object, metaclass=ReadOnlyClass):
    """
    ObsGraph Flask application keys
    """

    CONF_MAIN_SECTION_NAME: str = "ObsGraphFlaskApp"
    CONF_SALT: str = "salt"
    CONF_OBSERVIUM_API_URL: str = "observium_url"
    CONF_API_LOGIN: str = "api_login"
    CONF_API_PASSWORD: str = "api_password"
    CONF_FILE: str = "obsgraph.conf"


# #[EOF]#######################################################################
