##################################################################
# File          : docs/source/conf.py
# Description   : Configuration file for the Sphinx documentation
#                 builder.
# Maintainer(s) : richardgarryparker@gmail.com
# Created       : 2025-03-16
# Last updated  : 2025-03-16
# Change Log :
#   2025-03-16  : First release
##################################################################
"""conf.py
Configuration file for Sphinx
"""

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

#################################
# Imports
#################################
# Standard
import os
import sys

# 3rd party
from sphinx_pyproject import SphinxConfig

# Add source code dir to path (requirement for
# autodoc extension to work)
root_dir = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
sys.path.insert(0, root_dir)


#################################
# Pull configs from pyproject.toml
#################################

pyproj = os.path.join(root_dir, "pyproject.toml")
config = SphinxConfig(pyproj, globalns=globals())

# Basic metadata
project = name  # These variables *look* to be undefined, but they aren't.  # pylint: disable=undefined-variable  # noqa: F821
copyright  # pylint: disable=redefined-builtin
author  # pylint: disable=undefined-variable  # noqa: F821
release = version  # pylint: disable=undefined-variable  # noqa: F821

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions  # pylint: disable=undefined-variable  # noqa: F821
templates_path  # pylint: disable=undefined-variable  # noqa: F821
exclude_patterns  # pylint: disable=undefined-variable  # noqa: F821

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme  # pylint: disable=undefined-variable  # noqa: F821
html_static_path  # pylint: disable=undefined-variable  # noqa: F821

# Extension options
# Set to True to include todos in the output

todo_include_todos  # pylint: disable=invalid-name  # pylint: disable=undefined-variable  # noqa: F821

# Mock imports for autodoc
autodoc_mock_imports  # pylint: disable=undefined-variable  # noqa: F821
