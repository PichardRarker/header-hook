#!/usr/bin/python3
##################################################################
# File               : /workspaces/utils/common/header_hook.py
# Description        : Formatting and error checking of
#                      header blocks within code files
# Command-line usage : header_hook.py INP_FILE
# Maintainer(s)      : richard.parker@lifearc.org
# Created            : 2025-02-08
# Last updated       : 2025-02-08
# Change Log :
#   2025-02-08       : First release.
##################################################################
"""header_hook.py
Formatting and error checking of
header blocks within code files
"""

# Metadata attributes
# __version__ and __date__ refer to the pipeline
# as a whole, not this individual file. Datestamps
# for this file can be found in the header comment
# block
__version__ = "0.0.0"
__date__ = "1970-01-01"
__author__ = "richad.parker@lifearc.org"

#################################
# Imports
#################################
# Standard
import copy
import fnmatch
import os
import re
import subprocess
import sys
from datetime import datetime
from typing import Any, Tuple

#################################
# Settings
#################################

# Valid programming languages when deciding if a Shebang is valid or not
# TODO: extend support beyond Python and Shell
VALID_LANG = [
    "python",
    "python?",
    "python?.?",
    "python?.??",
    "sh",
    "ksh",
    "zsh",
    "dash",
    "bash",
    "ksh",
]

# Allowed section keys within the metadata block
# Match searches are case-insensitive. In addition,
# date strings of the format `YYYY-MM-DD`
# are considered valid keys.
# The ordering of keys within this list is used
# to create the formatted header block (with dates
# added last, in reverse chronological order)
ALLOWED_KEYS = [
    "file",
    "description",
    "command-line usage",
    "maintainer(s)",
    "created",
    "last updated",
    "change log",
]
# List of keys that do not have a large indent added
# before the associated value
# TODO: is indent the right word here?
NO_KEYVAL_INDENT = ["change log"]
# Fields for which values must start with a capital letter
# In addition to this list, all change log entries will be
# capitalised)
TO_CAP = ["description"]
# Divider used to denote stand and end of header block (and also
# defines the limit for word wrapping)
SEP = "##################################################################"
WRAP_LIMIT = len(SEP)
# The spacing that defines the gap between the key and the value
# is defined by the lengthiest key in the header block
FIRST_KEYVAL_INDENT_N = max([len(x) for x in ALLOWED_KEYS]) + 1
# Changelog dates are indented compared to the other keys
# in the header block
DATE_INDENT_N = 2
DATE_INDENT = " " * DATE_INDENT_N
# .. and so a custom key/value spacing is needed to ensure
# alignment with the rest of the keys
SECOND_KEYVAL_INDENT_N = FIRST_KEYVAL_INDENT_N - DATE_INDENT_N
# Max number of lines the change log can be before entries get cut
# (oldest cut first)
LOG_LINE_LENGTH = 20
# Define the regex pattern for ANSI escape codes
ANSI_ESCAPE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
# Date variables
TODAY = datetime.today().strftime("%Y-%m-%d")
DEFAULT_DATE = "Thu 1 Jan 1970 00:00:00 +0000"


#################################
# Exceptions
#################################


class MissingHeaderBlockError(Exception):
    def __init__(
        self, message="Header block is missing at the top of the file"
    ):
        self.message = message
        super().__init__(self.message)


class BlankLineError(Exception):
    def __init__(self, message="Line of text is entirely blank"):
        self.message = message
        super().__init__(self.message)


class InvalidHeaderBlockError(Exception):
    def __init__(self, message="Header block is formatted improperly"):
        self.message = message
        super().__init__(self.message)


class InvalidKeyError(Exception):
    def __init__(self, message="Text contains an illegal key"):
        self.message = message
        super().__init__(self.message)


class GitError(Exception):
    def __init__(
        self, message="Problem encountered when interacting with Git"
    ):
        self.message = message
        super().__init__(self.message)


class MultipleResultsFound(Exception):
    def __init__(self, message="Expected one match. Found multiple"):
        self.message = message
        super().__init__(self.message)


#################################
# Helpers
#################################


class HeaderBlock:
    def __init__(self):
        # Dict to store the key/value pairs that make
        # up the header
        self._data = {}
        # Shebang
        self.shebang = None

    def __iter__(self):
        date_keys = [x for x in self._data if is_valid_date(x)]
        sorted_date_keys = sorted(date_keys, reverse=True)
        for key in ALLOWED_KEYS + sorted_date_keys:
            if key in self._data:
                if is_valid_date(key):
                    is_changelog = True
                else:
                    is_changelog = False
                yield key, self._data[key], is_changelog

    def add(self, key: str, value: Any) -> None:
        if key in self._data:
            raise KeyError(f"Key '{key}' already defined for this object")
        self._data[key] = value

    def get(self, key: str) -> Any:
        return self._data[key]

    def drop(self, key: str) -> None:
        """Drop a key/value pair from the header
        If non-existent keys are requested for
        dropping, an exception is not thrown

        Args:
            key (str): Key to drop
        """
        try:
            del self._data[key]
        except KeyError:
            pass

    def drop_by_val(
        self, drop_val: str, multiple: bool = False, allow_zero: bool = True
    ) -> None:
        """By default, if more than one drop candidate
        identified, an error is thrown

        Args:
            drop_val (str): Value associated with the key to drop. Glob
                matching supported
            multiple (bool): If `False`, an exception is thrown if
                multiple matches are found. Default is `False`
            allow_zero (bool): If `False`, an exception is thrown
                if no matches are found. Default is `True`
        """
        to_drop = []
        for key, val, _ in self:
            if fnmatch.fnmatch(val, drop_val):
                to_drop.append(key)
        # Too few candidates?
        if not allow_zero and len(to_drop) == 0:
            raise ValueError(
                f"No candidates found matching value `{drop_val}`"
            )
        # Too many candidates?
        if not multiple and len(to_drop) > 1:
            raise MultipleResultsFound(
                "Multiple candidates found matching value `{drop_val}` (and argument `multiple` is set to `False`)"
            )
        for matched_key in to_drop:
            del self._data[matched_key]

    def append(self, key: str, value: Any) -> None:
        self._data[key] += " " + value

    def amend(self, key: str, value: Any) -> None:
        if key not in self._data:
            raise KeyError(f"Key `{key}` missing from header")
        self._data[key] = value

    def add_shebang(self, shebang: str) -> None:
        if self.shebang is not None:
            raise InvalidHeaderBlockError(
                "Shebang defined twice in this header"
            )
        self.shebang = shebang

    def get_first_date(self) -> str:
        date_keys = [x for x in self._data if is_valid_date(x)]
        return sorted(date_keys, reverse=True)[-1]

    def get_last_date(self) -> str:
        date_keys = [x for x in self._data if is_valid_date(x)]
        return sorted(date_keys, reverse=True)[0]


def line_formatter(line: str) -> str:
    # Ensure only single spaces exist
    # (this also removes indentations)
    formatted = re.sub(r"\s+", " ", line.strip())
    # Remove unwanted characters, including
    # leading spaces
    formatted = formatted.strip()
    return formatted


def parse_comment(line: str) -> str:
    # Confirm input is a comment
    if not is_valid_comment(line):
        raise ValueError("Input is not a valid comment")
    formatted = line_formatter(line)
    # Remove comment indicators
    i = 0
    comment_indicators = True
    while comment_indicators:
        if formatted[i] == "#":
            i += 1
        else:
            comment_indicators = False
    # Remove comment indicators and trailing
    # whitespace
    return formatted[i::].strip()


def is_valid_comment(text: str) -> bool:
    """`True` if text is a code comment,
    else `False`

    Args:
        text (str): Text (single line) to scrutinise

    Returns:
        bool: `True` if text is a code comment,
    else `False`
    """
    formatted = line_formatter(text)
    return formatted[0] == "#"


def is_blank(text: str) -> bool:
    formatted = line_formatter(text)
    return formatted.strip() == ""


def is_valid_shebang(text: str) -> bool:
    formatted = line_formatter(text)
    if formatted[0:2] != "#!":
        return False
    path = formatted[2::]
    if not os.path.isfile(path):
        return False
    executable = os.path.basename(path)
    if not any([fnmatch.fnmatch(executable, x) for x in VALID_LANG]):
        return False
    return True


def is_valid_date(date_string: str) -> bool:
    """Check if the provided string is a valid date in the format YYYY-MM-DD.

    Args:
        date_string (str): The date string to validate.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def line_splitter(line: str) -> Tuple[str, str]:
    """Convert a metadata string into a key/value
    pair. For example., "File: /path/to/file",
    becomes ("file", "/path/to/file"). Exceptions
    thrown if the line of text does not look like
    a key/value pair, or if the key is not in the
    list of allowed keys

    Args:
        line (str): Line to parse

    Raises:
        ValueError: Line doesn't look like a key/value
            pair (no ":" character)
        InvalidKeyError: Key not within list of accepted
            keys

    Returns:
        Tuple[str, str]: _description_
    """
    # Attempt to split on a ":" (which may not exist).
    # Split done on the first ":" only - subsequent ":"s
    # are considered as part of the value
    key = line.split(":")[0]
    val = ":".join(line.split(":")[1::]).strip()
    formatted_key = parse_comment(key).lower()
    if formatted_key not in ALLOWED_KEYS and not is_valid_date(formatted_key):
        raise InvalidKeyError
    return formatted_key, val


def remove_ansi_escape_codes(text: str) -> str:
    """Remove ANSI escape codes from strings

    Args:
        text (str): Message that may or may not contain
            ANSI escape codes

    Returns:
        str: Message with any ANSI codes removed
    """
    return ANSI_ESCAPE.sub("", text)


def wrap_and_indent(proc_msg: str, max_length: int, indent: int) -> str:
    """Wrap a (potentially long) message over multiple lines.
       Indent added to lines 2 and beyond (hanging indent)

    Args:
        msg (str): Message to be formatted. Messages
            already containing newline special
            characters will not be wrapped
            (but will be indented)
        max_length (int): Max length each line can be before a
            newline character is added
        indent (int): Size of the introduced indent (for
            all lines except the first one

    Returns:
        str: A string with wrapping and indentation
            added
    """
    # Remove any existing newline characters
    proc_msg = re.sub(r"\n", "", proc_msg)
    # Start the word wrap
    indent_str = "#" + " " * indent
    split_msg = proc_msg.split(" ")
    wrapped_msg = ""
    new_line = []
    first_line = True
    empty_line = True
    for word in split_msg:
        # Current line word count (including spaces)
        # If this is the first line, then we also need to account for the message prefix
        line_len = (
            sum([len(remove_ansi_escape_codes(x)) for x in new_line])
            + len(new_line)
            + ((indent + 1) * first_line)
        )
        # Are we under the wrap limit?
        if line_len + len(word) <= max_length:
            new_line.append(word)
            empty_line = False
        else:
            if empty_line:
                new_line += [word]
            wrapped_msg += " ".join(new_line) + "\n"
            new_line = [indent_str]
            if not empty_line:
                new_line += [word]
                empty_line = False
            first_line = False
    # Final addition to the formatted string (for the last line of the message,
    # which might also be the first line, if it's short)
    wrapped_msg += " ".join(new_line)

    return wrapped_msg


def wrap_wrapper(h: HeaderBlock) -> None:
    """Wrapper around method that performs
    word wrapping/indenting

    Args:
        h (HeaderBlock): Header block loaded
            into memory
    """
    # Word wrap
    for key, val, is_changelog in h:
        if key != "file":
            # Wrap and indent text. Slight changes to the standard
            # wrap limit and indent size to account for addition of
            # "#"s, and also colons that separate keys from values.
            # Wrap and indent text.
            h.amend(
                key,
                wrap_and_indent(
                    val, WRAP_LIMIT - 1, FIRST_KEYVAL_INDENT_N + 2
                ),
            )


def load_meta(raw_text: list, break_limit: int = 3) -> Tuple[dict, list]:
    """Extract the header block from a file,
    converting to a dict.

    Args:
        raw_text (list): text loaded into memory
        break_limit (int): number of contiguous lines
            without a comment before the header block
            is considered closed

    Returns:
        dict: header block dict. Text keys are mapped
            to dict keys. e.g., "File: /path/to/file",
            becomes {"file" : "/path/to/file"}. A key
            is also created for the file shebang
        list: The rest of the file, unedited
    """
    header = HeaderBlock()
    # The header block starts when we hit the first
    # line of comments (only blank spaces are allowed
    # to precede)
    header_open = False
    i = 0
    while not header_open:
        line = raw_text[i]
        if is_blank(line):
            i += 1
            continue
        elif is_valid_comment(line):
            header_open = True
        else:
            raise MissingHeaderBlockError

    # The metadata block is considered finished if
    # i)  there are X blank lines in a row
    #     (X determined by `break_limit`)
    # ii) when we hit a line containing code
    # Start of the header = Shebang (optional) and
    # start of a section (mandatory). Header is
    # considered closed after we hit the first
    # key
    header_start = True
    strike_count = 0
    for j, line in enumerate(raw_text[i::]):
        if is_blank(line):
            strike_count += 1
            if strike_count == break_limit:
                return header, (raw_text[i + j : :])
            else:
                continue
        elif is_valid_comment(line):
            strike_count = 0
        else:
            return header, (raw_text[i + j : :])
        # If we've made it this far, we have a comment
        # line to be processed
        clean_line = line_formatter(line)
        # A second divider line indicates the end of the
        # header block
        if set(clean_line) == {"#"} and not header_start:
            return header, (raw_text[i + j + 1 : :])
        if header_start:
            # Starting divider line is ignored
            if set(clean_line) == {"#"}:
                continue
            # Shebang?
            if is_valid_shebang(clean_line):
                header.add_shebang(clean_line)
            # Does the comment block start with a key?
            else:
                try:
                    key, val_frag = line_splitter(clean_line)
                    header.add(key, val_frag)
                    header_start = False
                except:
                    raise InvalidHeaderBlockError(
                        "Header block should start with a key:value pair"
                        + "For example: 'File : /path/to/this/file'"
                    )
        else:
            # Are we dealing with a new key/value, or a
            # continuation of a previously-started key/value?
            try:
                key, val_frag = line_splitter(clean_line)
                header.add(key, val_frag)
            except:
                header.append(key, parse_comment(clean_line))


def create_new_file(
    header: HeaderBlock, non_header: list, file_path: str
) -> None:
    """Save the modified header and unaltered non-header
    to file

    Args:
        header_dict (HeaderBlock): Header information
        non_header (list): The rest of the file, unaltered

    Returns:
        None
    """
    new_file_contents = []
    # First, shebang and opening divider
    new_file_contents.append(header.shebang + "\n" + SEP + "\n")
    # Next we iterate through standard keys (in the expected order)
    # followed by dates (in reverse chronological order)
    for key, val, is_changelog in header:
        # Different formatting rules for standard keys
        # vs date keys
        if is_changelog:
            indent = DATE_INDENT
            keyval_spacing = " " * (SECOND_KEYVAL_INDENT_N - len(key))
        else:
            # For non-date, keys, we also need to consider keys
            # with special spacing rules
            indent = ""
            if key in NO_KEYVAL_INDENT:
                keyval_spacing = " "
            else:
                keyval_spacing = " " * (FIRST_KEYVAL_INDENT_N - len(key))
        # Add to file, with capitalisation of the key, and (possible)
        # capitalisation of the value
        if key in TO_CAP or is_changelog:
            val = val.capitalize()
        else:
            val = val
        new_file_contents.append(
            f"# {indent}{key.capitalize()}{keyval_spacing}: {val}\n"
        )

    # Add the final header divider, then the rest
    # of the file contents. We can then save to file
    # TODO: change file save to be in-place
    new_file_contents.append(SEP + "\n")
    new_file_contents += non_header
    file_path = file_path.split(".py")[0] + "_mod.py"
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as f:
        f.writelines(new_file_contents)


def git_date_convert(datestr: str) -> str:
    # Decide direction of conversion
    if "-" in datestr:
        date_obj = datetime.strptime(datestr, "%Y-%m-%d")
        new_datestr = date_obj.strftime("%a %b %d %H:%M:%S %Y %z")
    else:
        date_obj = datetime.strptime(datestr, "%a %b %d %H:%M:%S %Y %z")
        new_datestr = date_obj.strftime("%Y-%m-%d")
    return new_datestr


def ask_git(cmd: str) -> str:
    try:
        res = subprocess.run(
            cmd.split(" "),
            check=True,
            capture_output=True,
            text=True,
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise GitError(f"Problem communicating with Git: {e}")


def check_release_date(h: HeaderBlock, branch: str = "main") -> None:
    filepath = h.get("file")
    # Drop any pre-existing changelog fields that denote
    # the first release
    for msg in ["?irst ?release?", "?irst ?omit?", "?nitial ?release?"]:
        h.drop_by_val(msg)
    # First change log value should always be "Release date"
    # (although this entry will be deleted if the changelog is
    # too long)
    # Set release date to the first date the file
    # appeared on the main branch
    git_cmd = f"git log --diff-filter=A --follow --format=%aD -1 {branch} -- {filepath}"
    try:
        rel_date = ask_git(git_cmd)
    except GitError:
        raise GitError(f"Branch {branch} not found in project")
    # Never pushed to main?
    if rel_date == "":
        rel_date = git_date_convert(TODAY) + "+0000"
    # Format provided date
    rel_date = git_date_convert(rel_date)
    # TODO: for now, change log entries for the same day as the
    # release day are dropped, replaced instead by the
    # simple release method. In future, might want to consider
    # bumping changelog entries for the same day to a future date,
    # although this could get mess
    h.drop(rel_date)
    h.add(rel_date, "First release")


def update_last_updated(h: HeaderBlock):
    last_date = h.get_last_date()
    h.amend("last updated", last_date)


def prep_for_join(msg: str) -> str:
    if not msg.endswith("."):
        msg += "."
    return msg


def changelog_merger(h: HeaderBlock, branch: str) -> None:
    """ABC

    Note:
        Merges only occur between last commit to
        main and today. Historic entries in the
        changelog are not altered

    Args:
        h (HeaderBlock): _description_
    """
    filepath = h.get("file")
    # Establish the last time this file was committed to main.
    # If never committed, the default date is used
    git_cmd = f"git log -1 --format=%cd -- {branch} -- {filepath}"
    last_commit_date = ask_git(git_cmd)
    if last_commit_date == "":
        last_commit_date = DEFAULT_DATE
    last_commit_date = git_date_convert(last_commit_date)
    latest_log = []
    for key, val, is_changelog in h:
        if is_changelog:
            if key > last_commit_date:
                prepped = prep_for_join(val)
                latest_log.append(prepped)
                h.drop(key)
    h.add(TODAY, " ".join(latest_log[::-1]))


def changelog_trim(h: HeaderBlock) -> None:
    # Apply word wrapping to a copy of the
    # header, so we can judge how many lines
    # the header (currently) takes up
    h2 = copy.deepcopy(h)
    wrap_wrapper(h2)
    # Dates to drop
    drop_dates = []
    # Count changelog lines
    n_lines = 0
    for key, val, is_changelog in h2:
        if is_changelog:
            n_lines += val.count("\n") + 1
            if n_lines > LOG_LINE_LENGTH:
                drop_dates.append(key)
    # Drop!
    for date in drop_dates:
        h.drop(date)


def chain(file_to_proc: str) -> None:
    # Load file
    with open(file_to_proc) as f:
        file_contexts = f.readlines()
    # Attempt to convert header block
    # to dict, and split off the rest of the
    # file
    header, the_rest = load_meta(file_contexts)
    # Ensure "Last updated" date is synced with the
    # change log
    update_last_updated(header)
    # Trim changelog, if it's too long
    changelog_trim(header)
    # Merge log entries that exist between commits
    # to main
    changelog_merger(header, "main")
    # Ensure "First release" date matches first push to
    # main branch. If never pushed to main, a default
    # date is used
    check_release_date(header, "main")
    wrap_wrapper(header)
    # Save to file
    create_new_file(header, the_rest, file_to_proc)


if __name__ == "__main__":
    # Get the list of files passed to the script
    files = sys.argv[1:]
    # Process each file, in turn
    for file in files:
        # TODO: update with list of supported files
        if file.endswith(".py"):
            chain(file)
