#!/usr/bin/python3
##################################################################
# File               : tests/end_to_end/word_wrap_test.py
# Description        : Apply the hook to a file in desperate
#                      need of word wrapping (with no
#                      other issues present)
# Maintainer(s)      : richardgarryparker@gmail.com
# Created            : 2025-03-22
# Last updated       : 2025-03-22
# Change Log :
#   2025-03-22       : First release.
##################################################################
"""word_wrap_test.py
Apply the hook to a file in desperate need of word wrapping
(with no other issues present)

Note:
    Functions in this file make use of Pytest fixtures. Importing
    of fixtures is handled by conftest.py, situated within the same
    directory as this .py file
"""

# Metadata attributes
# __version__ and __date__ refer to the pipeline
# as a whole, not this individual file. Datestamps
# for this file can be found in the header comment
# block
__version__ = "0.0.0"
__date__ = "1970-01-01"
__author__ = "richardgarryparker@gmail.com"

#################################
# Imports
#################################
# 3rd party
import pytest

#################################
# Tests
#################################


@pytest.mark.end_to_end
def test_wrapping_with_no_other_issues(setup_and_teardown):
    test_input = setup_and_teardown
    # Ensure the input file is copied correctly
    assert test_input.exists()
    print("Done!")

    # Perform formatting operation and assertions
