#!/bin/bash

# Set ACRO_TD_CORE environment variable
# Resolves to the directory containing this setup script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# launchctl setenv makes it available to GUI apps (like TouchDesigner)
launchctl setenv ACRO_TD_CORE "$SCRIPT_DIR"
# .zshenv makes it available in terminal sessions
if ! grep -q 'ACRO_TD_CORE' ~/.zshenv 2>/dev/null; then
    echo "export ACRO_TD_CORE=\"$SCRIPT_DIR\"" >> ~/.zshenv
fi
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

# install MCP server dependencies and build
echo "Installing MCP server dependencies"
cd "$SCRIPT_DIR"
npm install
npm run build
