#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wsgi.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 5.12.2025, 12:16:47

Purpose: WSGI entry point for the obsgraph_flask application.
"""

from obsgraph_flask.app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0")

# #[EOF]#######################################################################
