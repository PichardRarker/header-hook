##################################################################
# File               : tests/helpers/helpers_end_to_end.py
# Description        : Helper functions for end to end testing
#                      (distinct from test fixtures, which are
#                      executed as soon as they are referenced
#                      as a test function argument)
# Maintainer(s)      : richardgarryparker@gmail.com
# Created            : 2025-04-05
# Last updated       : 2025-04-05
# Change Log :
#   2025-04-05       : First release.
##################################################################
"""helpers_end_to_end.py
Helper functions for end to end testing (distinct from test
fixtures, which are executed as soon as they are referenced
as a test function argument)
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
import subprocess
import sys
from pathlib import Path

# 3rd party
import pytest

#################################
# Basic setup
#################################
# Base directories for test data and temporary testing
hook_file = (
    Path(__file__).parent.parent.parent / "src/header_hook/header_hook.py"
)


def run_hook(inp_file: Path) -> None:
    """Run the hook

    Args:
        inp_file (Path): Test input

    Raises:
        RuntimeError: If the hook fails
            to run to completion for any
            reason

    Returns:
        None
    """
    if not inp_file.exists():
        pytest.fail(f"Test file '{inp_file}' does not exist.")
    # Run the hook, checking for exceptions (which may be
    # expected, depending on test setup)
    try:
        _ = subprocess.run(
            [sys.executable, str(hook_file), str(inp_file)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Header hook execution failed with exit code {e.returncode}: {e.stderr.strip()}"
        )
