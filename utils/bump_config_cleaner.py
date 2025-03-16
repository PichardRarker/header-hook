#!/usr/bin/python3
##################################################################
# File               : utils/bump_config_cleaner.py
# Description        : Removes bump-my-version configs from
#                      a pyproject.toml file, so that
#                      utils/bump-my-version_config_setter.sh
#                      can add new configs
# Command-line usage : bump_config_cleaner.py
# Maintainer(s)      : richardgarryparkr@gmail.com
# Created            : 2025-03-16
# Last updated       : 2025-03-16
# Change Log :
#   2025-03-16       : First release
##################################################################
"""bump_config_cleaner.py
Removes bump-my-version configs from a pyproject.toml file, so
that ``utils/bump-my-version_config_setter.sh`` can add
new configs
"""

# Metadata attributes
# __version__ and __date__ refer to the pipeline
# as a whole, not this individual file. Datestamps
# for this file can be found in the header comment
# block
__version__ = "0.1.0"
__date__ = "2025-02-06"
__author__ = "richardgarryparker@gmail.com"

#################################
# Imports
#################################
# Standard
import os

# 3rd party
import tomlkit
from tomlkit.exceptions import NonExistentKey

#################################
# Main
#################################

# Load config file
src_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
root_dir = os.path.dirname(src_dir)
config_file = os.path.join(root_dir, "pyproject.toml")
with open(config_file, "rb") as f:
    configs = tomlkit.parse(f.read())


# Remove pre-existing bump-my-version configs,
# should they exist
try:
    configs["tool"].pop("bumpversion")
except NonExistentKey:
    pass


# Save the modified TOML file, preserving
# ordering and comments
with open(config_file, "w", encoding="utf-8") as f:
    f.write(tomlkit.dumps(configs))
