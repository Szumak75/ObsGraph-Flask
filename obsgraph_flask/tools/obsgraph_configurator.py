#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsgraph_configurator.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 17.10.2025, 12:30:19

Purpose:
"""

import os
import sys

from jsktoolbox.configtool import Config

# current dynamic project directory
current_dir: str = os.path.dirname(os.path.abspath(__file__))
config_file_path: str = os.path.join(current_dir, "obsgraph.conf")

if __name__ == "__main__":
    print("ObsGraph Configurator")
    print("======================\n")
    print(f"Loading configuration file: {config_file_path}\n")

    sys.exit(0)

# #[EOF]#######################################################################
