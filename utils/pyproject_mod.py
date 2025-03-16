#!/usr/bin/python3
##################################################################
# File               : utils/pyproject_mod.py
# Description        : Change a value within a
#                      pyproject.toml file
# Command-line usage : pyproject_mod.py --key KEY --new_val VALUE
# Maintainer(s)      : richardgarryparker@gmail.com
# Created            : 2025-03-16
# Last updated       : 2025-03-16
# Change Log :
#   2025-03-16       : First release.
##################################################################
"""pyproject_mod.py
Change a value within a pyproject.toml file
"""
# Metadata attributes
# __version__ and __date__ refer to the pipeline
# as a whole, not this individual file. Datestamps
# for this file can be found in the header comment
# block
# In addition, as this file originates from a template
# codebase, these variables reflect versioning of the template
# (`eng-toolkit-python`), and not the downstream project
__version__ = "0.1.0"
__date__ = "2025-02-06"
__author__ = "richardgarryparker@gmail.com"

#################################
# Imports
#################################
# Standard
import os
import sys
from typing import Tuple

# 3rd party
import tomlkit
from tomlkit.exceptions import NonExistentKey

#################################
# Helper functions
#################################


def mod_help() -> None:
    """Print help for lumberjack.py to ``STDOUT``.

    Args:
        None

    Returns:
        None
    """
    msg = """
    -----------------------------------------------------
    pyproject_mod.py : change a value within a
                       pyproject.toml file
    -----------------------------------------------------
    Parameters
    ----------
    --key
        The key to modify. Use '.' to distinguish
        subheadings. For example:
        'project.configs.general.docker_name'
    --new_val
        New value for this key
    -----------------------------------------------------
    """
    print(msg)


def arg_parse() -> Tuple[str, str, str, str, str]:
    """Parse command-line arguments and perform basic error checks.

    Args:
        None

    Raises:
        ValueError: if `--key` and `--new_val` are not both provided

    Returns:
        tuple: a tuple containing:
            - key: the key to modify.
            - new_val: the new value for the given key
    """
    # Initialize a dictionary to store arguments
    args = {
        "key": None,
        "new_val": None,
    }
    # Iterate over the command line arguments
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--key" and i + 1 < len(sys.argv):
            args["key"] = sys.argv[i + 1]
        elif sys.argv[i] == "--new_val" and i + 1 < len(sys.argv):
            args["new_val"] = sys.argv[i + 1]

    # Inputs specified properly?
    if args["key"] is None or args["new_val"] is None:
        mod_help()
        raise ValueError("Both --key and --new_val need to be provided")
    else:
        return (
            args["key"],
            args["new_val"],
        )


#################################
# Main
#################################
# If invoked from command-line, large arguments
# and execute main function
if __name__ == "__main__":
    # Argument parsing
    key, new_val = arg_parse()

    # Load config file
    src_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
    root_dir = os.path.dirname(src_dir)
    config_file = os.path.join(root_dir, "pyproject.toml")
    with open(config_file, "rb") as f:
        configs = tomlkit.parse(f.read())

    # Find key of interest
    # Split the key into its components
    keys = key.split(".")
    # Navigate through the TOML structure
    current_section = configs
    for part in keys[:-1]:
        current_section = current_section[part]

    # Check the key exists
    try:
        old_Val = current_section[keys[-1]]
    except NonExistentKey:
        print(f"Key {key} not found in pyproject.toml file")
        sys.exit(1)

    # Update the final key with the new value
    current_section[keys[-1]] = new_val

    # Save the modified TOML file, preserving
    # ordering and comments
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(configs))
