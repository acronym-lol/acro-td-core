#!/bin/bash

# Set ACRO_TD_CORE environment variable
# Resolves to the directory containing this setup script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# launchctl setenv makes it available to GUI apps (like TouchDesigner)
launchctl setenv ACRO_TD_CORE "$SCRIPT_DIR"
# .zshenv makes it available in terminal sessions
# Drop any earlier line (e.g. from before the repo moved), then add the current path
if [ -f ~/.zshenv ]; then sed -i.bak '/^export ACRO_TD_CORE=/d' ~/.zshenv && rm -f ~/.zshenv.bak; fi
echo "export ACRO_TD_CORE=\"$SCRIPT_DIR\"" >> ~/.zshenv
export ACRO_TD_CORE="$SCRIPT_DIR"
echo "ACRO_TD_CORE set to $SCRIPT_DIR"

# Run all module setup scripts
for module_setup in "$SCRIPT_DIR"/modules/*/setup.sh; do
    if [ -f "$module_setup" ]; then
        echo "Running $(basename $(dirname "$module_setup"))/setup.sh"
        source "$module_setup"
    fi
done

echo "Creating TD pref.txt file"

# Construct the file path for macOS
FILE_PATH="$HOME/Library/Application Support/Derivative/TouchDesigner099/pref.txt"

# Create the content with the VS Code path for macOS
CONTENT=$(cat << EOF
general.pythonpackages64	/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages
general.stopplayingwhenminimized	0
dats.texteditor	/Applications/Visual Studio Code.app
general.playbarshortcuts	0
general.startupfilemode	1
chops.graphdisplay2	6
network.zoomdelay	0.19999999
network.zoomboost	1.0000002
EOF
)

# Ensure the parent directory exists
mkdir -p "$(dirname "$FILE_PATH")"

# Write the content to the file with correct line endings
echo -e "$CONTENT" > "$FILE_PATH"

# make sure the file has the correct permissions
chmod 777 "$FILE_PATH"
echo "TD pref.txt file created at $FILE_PATH"

# The MCP server ships prebuilt (modules/acro-td-mcp/dist/index.js); it only needs Node
if ! command -v node >/dev/null 2>&1; then
    echo "WARNING: Node.js was not found on PATH. Install it to use the acro-td-mcp MCP server."
fi
