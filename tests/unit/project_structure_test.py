#!/usr/bin/python3
##################################################################
# File               : tests/common/unit/test_project_structure.py
# Description        : Basic tests to ensure the project structure is intact
# Command-line usage : test_project_structure.py
# Maintainer(s)      : richardgarryparker@gmail.com
# Created            : 2025-03-16
# Last updated       : 2025-03-16
# Change Log :
#   2025-03-16       : First release.
##################################################################
"""project_structure_test.py

Basic tests to ensure the project structure is intact
"""
# Metadata attributes
# __version__ and __date__ refer to the pipeline
# as a whole, not this individual file. Datestamps
# for this file can be found in the header comment
# block
__version__ = "0.1.0"
__date__ = "2025-03-03"
__author__ = "richardgarryparker@gmail.com"
#################################
# Imports
#################################

# Standard
import json
import os
import unittest

# 3rd party
import tomli


#################################
# Tests
#################################
class TestProjectStructure(unittest.TestCase):
    """Confirm the template's core files/folders
    and intact

    Args:
        None

    Returns:
        None
    """

    # Start with basic directory tests
    def test_src_directory_exists(self):
        """Confirm the source code
        directory exists
        """
        self.assertTrue(os.path.isdir("src"), "Directory /src does not exist")

    def test_build_directory_exists(self):
        """Confirm the build directory
        exists
        """
        self.assertTrue(
            os.path.isdir("build"), "Directory /build does not exist"
        )

    def test_data_directory_exists(self):
        """Confirm the test data
        directory exists
        """
        self.assertTrue(
            os.path.isdir("data"), "Directory /data does not exist"
        )

    def test_utils_directory_exists(self):
        """Confirm the utility script
        directory exists
        """
        self.assertTrue(
            os.path.isdir("utils"), "Directory /utils does not exist"
        )

    def test_devcontainer_directory_exists(self):
        """Confirm the Devcontainer
        config directory exists
        """
        self.assertTrue(
            os.path.isdir(".devcontainer"),
            "Directory /.devcontainer does not exist",
        )

    # ...then test directory contents
    def test_build_dir_contents(self):
        """Confirm presence of key
        files within the build directory
        """
        self.assertTrue(
            os.path.isfile("build/Dockerfile"),
            "Dockerfile does not exist in /build directory",
        )

    def test_devcontainer_dir_contents(self):
        """Confirm presence of key
        files within the Devcontainer config directory
        """
        self.assertTrue(
            os.path.isfile(".devcontainer/devcontainer.json"),
            "devcontainer.json does not exist in /.devcontainer directory",
        )

    # ...then do some more nuanced tests of file integrity
    def test_config_file_integrity(self):
        """Ensure the config file is valid
        TOML
        """
        config_path = "pyproject.toml"
        with open(config_path, "rb") as file:
            try:
                tomli.load(file)
            except tomli.TOMLDecodeError:
                self.fail(f"{config_path} is not valid TOML")

    def test_devcontainer_config_file_integrity(self):
        """Confirm the Devcontainer config file
        is formatted properly
        """
        config_path = ".devcontainer/devcontainer.json"
        # VSCode is lenient when parsing the devcontainer.json
        # file, allowing comments (starting with `//`).
        with open(config_path, encoding="utf-8") as file:
            lines = file.readlines()
        # Remove lines that start with //
        json_content = "".join(
            line for line in lines if not line.strip().startswith("//")
        )
        try:
            json.loads(json_content)
        except json.JSONDecodeError:
            self.fail(f"{config_path} is not valid JSON")


#################################
# Execute
#################################
if __name__ == "__main__":
    unittest.main()
