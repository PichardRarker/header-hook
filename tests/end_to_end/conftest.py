##################################################################
# File               : /workspaces/tests/end_to_end/conftest.py
# Description        : Common configuration for header-hook
#                      end to end tests
# Maintainer(s)      : richardgarryparker@gmail.com
# Created            : 2025-03-22
# Last updated       : 2025-03-22
# Change Log :
#   2025-03-22       : First release.
##################################################################
"""conftest.py
Common configuration for header-hook end to end tests
"""

#################################
# Imports
#################################
# 3rd party
import pytest  # nopycln: import

# Project-specific
from tests.fixtures.fixtures_end_to_end import (  # nopycln: import
    setup_and_teardown,
)
