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

# Python packages (requirements.txt) are installed by TouchDesigner's tdPyEnvManager into the
# project's own venv the first time the .toe is opened (see TDPyEnvManagerContext.yaml)

# The MCP server ships prebuilt (modules/acro-td-mcp/dist/index.js); it only needs Node
if ! command -v node >/dev/null 2>&1; then
    echo "WARNING: Node.js was not found on PATH. Install it to use the acro-td-mcp MCP server."
fi
