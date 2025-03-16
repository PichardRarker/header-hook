#!/usr/bin/bash
##################################################################
# File          : utils/bumpy-my-version_config_setter.sh
# Description   : Create bump-my-version configs for all Python
#                 files that make up a code project
# Usage         : bumpy-my-version_config_setter.sh [-h|--help] 
# Maintainer(s) : richardgarryparker@gmail.com
# Created       : 2025-03-16
# Last updated  : 2025-03-16
# Change Log :
#   2025-03-16  : First release.
##################################################################

# Metadata attributes
# VERSION and DATE refer to the pipeline
# as a whole, not this individual file. Datestamps
# for this file can be found in the header comment
# block
readonly VERSION="0.1.0"
readonly DATE="2025-02-06"
readonly AUTHOR="richardgarryparker@gmail.com"

#################################
# Helper functions
#################################
help() {
	# Prints script usage information
	echo -e "Usage: bumpy-my-version_config_setter.sh [-h|--help]\n"
	echo -e "Build a suitable config file for the bump-my-version Python module\n"
	echo -e 'Script assumes that all source code is located within $ROOT/src, where '
	echo -e '$ROOT might be the /app folder, or the working directory of a container.'
	echo "--------------------"
	echo -e "None"
	echo ""
	echo "Options"
	echo "-------"
	echo -e "-h, --help\t\tDisplay this help message and exit"
	exit 1
}
#################################
# Basic setup
#################################
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
BASE_DIR=$( dirname "$SCRIPT_PATH" )

#################################
# Input parsing
#################################
# Parse arguments
while [[ $# -gt 0 ]]; do
	case $1 in
	-h | --help) help ;;
	# Break out of the loop for positional arguments
	*) break ;;
	esac
	shift
done
#################################
# Set configs
#################################
CONFIGS="$BASE_DIR"/pyproject.toml
# Current version of the project
CURR_VER='0.1.0'
[ -f "$BASE_DIR"/VERSION ] && CURR_VER=$(cat "$BASE_DIR"/VERSION)

# First, any pre-existing bump-my-version configs are removed
# from pyproject.toml
print "Removing pre-existing "$SEP"bump-my-version"$SEP" configs \
	from "$SEP""$CONFIGS""$SEP"" "info"
python3 "$BASE_DIR"/utils/bump_config_cleaner.py

# Next, add in general configs
cat <<'EOF' >>"$CONFIGS"


[tool.bumpversion]
current_version = VERSION_WILL_GO_HERE
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
search = "{current_version}"
replace = "{new_version}"
regex = false
ignore_missing_version = false
ignore_missing_files = false
tag = true
sign_tags = false
tag_name = "v{new_version}"
tag_message = "Bump version: {current_version} → {new_version}"
allow_dirty = false
commit = false
message = "Bump version: {current_version} → {new_version}"
commit_args = ""
setup_hooks = []
pre_commit_hooks = []
post_commit_hooks = []


[[tool.bumpversion.files]]
filename = "VERSION"
EOF

# Add the current version
# (done here, as allowing variable expansion/special character
# interpretation during the addition of general configs messes
# up some of the syntax)
sed -i "s/current_version = VERSION_WILL_GO_HERE/current_version = \'$CURR_VER\'/" "$CONFIGS"

# Recursively find all .py files in the ./src directory
find "$SRC_DIR" -name "*.py" | while read -r file; do
	# Remove the root directory from the filepath, simplifying switching between
	# Dev Containers and GitHub Actions when using bumpmyversion
	new_file=$(echo "$file" | sed "s|$BASE_DIR/||")
	# Append the bumpmyversion config for each .py file using echo statements
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "__date__ = \"\\d{{4}}-\\d{{2}}-\\d{{2}}\""' >>"$CONFIGS"
	echo 'replace = "__date__ = \"{now:%Y-%m-%d}\""' >>"$CONFIGS"
	echo "regex = true" >>"$CONFIGS"
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
done

# Repeat for .py files in the tests directory
find "$TESTS_DIR" -name "*.py" | while read -r file; do
	# Remove the root directory from the filepath, simplifying switching between
	# Dev Containers and GitHub Actions when using bumpmyversion
	new_file=$(echo "$file" | sed "s|$BASE_DIR/||")
	# Append the bumpmyversion config for each .py file using echo statements
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "__date__ = \"\\d{{4}}-\\d{{2}}-\\d{{2}}\""' >>"$CONFIGS"
	echo 'replace = "__date__ = \"{now:%Y-%m-%d}\""' >>"$CONFIGS"
	echo "regex = true" >>"$CONFIGS"
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
done

# Repeat for .sh scripts in the the utilities directory
find "$UTILS_DIR" -name "*.sh" | while read -r file; do
	# Remove the root directory from the filepath, simplifying switching between
	# Dev Containers and GitHub Actions when using bumpmyversion
	new_file=$(echo "$file" | sed "s|$BASE_DIR/||")
	# Append the bumpmyversion config for each .py file using echo statements
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "readonly DATE=\"\\d{{4}}-\\d{{2}}-\\d{{2}}\""' >>"$CONFIGS"
	echo 'replace = "readonly DATE=\"{now:%Y-%m-%d}\""' >>"$CONFIGS"
	echo "regex = true" >>"$CONFIGS"
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "readonly VERSION=\"{current_version}\""' >>"$CONFIGS"
	echo 'replace = "readonly VERSION=\"{new_version}\""' >>"$CONFIGS"
done

# Repeat for .py scripts in the the utilities directory
find "$UTILS_DIR" -name "*.py" | while read -r file; do
	# Remove the root directory from the filepath, simplifying switching between
	# Dev Containers and GitHub Actions when using bumpmyversion
	new_file=$(echo "$file" | sed "s|$BASE_DIR/||")
	# Append the bumpmyversion config for each .py file using echo statements
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "__date__ = \"\\d{{4}}-\\d{{2}}-\\d{{2}}\""' >>"$CONFIGS"
	echo 'replace = "__date__ = \"{now:%Y-%m-%d}\""' >>"$CONFIGS"
	echo "regex = true" >>"$CONFIGS"
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
done

# Repeat for .sh scripts in the the build directory
find "$BUILD_DIR" -name "*.sh" | while read -r file; do
	# Remove the root directory from the filepath, simplifying switching between
	# Dev Containers and GitHub Actions when using bumpmyversion
	new_file=$(echo "$file" | sed "s|$BASE_DIR/||")
	# Append the bumpmyversion config for each .py file using echo statements
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "readonly DATE=\"\\d{{4}}-\\d{{2}}-\\d{{2}}\""' >>"$CONFIGS"
	echo 'replace = "readonly DATE=\"{now:%Y-%m-%d}\""' >>"$CONFIGS"
	echo "regex = true" >>"$CONFIGS"
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "readonly VERSION=\"{current_version}\""' >>"$CONFIGS"
	echo 'replace = "readonly VERSION=\"{new_version}\""' >>"$CONFIGS"
done

# Repeat for .py scripts in the the build directory
find "$BUILD_DIR" -name "*.py" | while read -r file; do
	# Remove the root directory from the filepath, simplifying switching between
	# Dev Containers and GitHub Actions when using bumpmyversion
	new_file=$(echo "$file" | sed "s|$BASE_DIR/||")
	# Append the bumpmyversion config for each .py file using echo statements
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
	echo 'search = "__date__ = \"\\d{{4}}-\\d{{2}}-\\d{{2}}\""' >>"$CONFIGS"
	echo 'replace = "__date__ = \"{now:%Y-%m-%d}\""' >>"$CONFIGS"
	echo "regex = true" >>"$CONFIGS"
	echo -e "\n\n" >>"$CONFIGS"
	echo "[[tool.bumpversion.files]]" >>"$CONFIGS"
	echo "filename = '$new_file'" >>"$CONFIGS"
done

echo "Configurations have been appended to $CONFIGS"
