##################################################################
# File               : tests/fixtures/fixtures_end_to_end.py
# Description        : Fixtures suitable for end to end testing
#                      of header-hook
# Maintainer(s)      : richardgarryparker@gmail.com
# Created            : 2025-03-22
# Last updated       : 2025-03-22
# Change Log :
#   2025-03-22       : First release.
##################################################################
"""fixtures_end_to_end.py
Fixtures suitable for end to end testing of header-hook
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
# Standard
import shutil
from pathlib import Path

# 3rd party
import pytest

#################################
# Basic setup
#################################
# Base directories for test data and temporary testing
DATA_DIR = Path(__file__).parent.parent.parent / "data/tests/end_to_end"
TMP_DIR = Path(__file__).parent.parent.parent / "tmp/testing/end_to_end"


#################################
# Fixtures
#################################
@pytest.fixture
def setup_and_teardown(request):
    """
    Pytest fixture that dynamically locates test input files based on the invoking test function's name,
    copies them to a temporary directory, and ensures cleanup afterward.
    """
    # Gets the name of the test function
    test_name = request.node.name
    # Expected source test case folder
    source_dir = DATA_DIR / test_name
    # Temporary destination directory
    temp_test_dir = TMP_DIR / test_name
    if not source_dir.exists():
        pytest.fail(f"Test data directory '{source_dir}' does not exist.")
    files = [x.name for x in source_dir.iterdir() if x.is_file()]
    if "input.py" not in files or "expected.py" not in files:
        pytest.fail(
            f"Test data directory '{source_dir}' missing `input.py` or `expected.py` (or both"
        )
    # Ensure temporary directory is clean
    if temp_test_dir.exists():
        shutil.rmtree(temp_test_dir)
    temp_test_dir.mkdir(parents=True)
    # Copy "input" file from source to temporary directory
    inp_orig = source_dir / "input.py"
    inp_new = temp_test_dir / "input.py"
    shutil.copyfile(inp_orig, inp_new)
    # Provide the temp copy of the input file to the test function
    yield inp_new

    # Cleanup after test execution
    shutil.rmtree(temp_test_dir)
    print("Done!")
