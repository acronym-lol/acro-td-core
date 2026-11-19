#!/bin/bash

# Run as yourself, not with sudo: under sudo the variables are set for root,
# and the apps you open never see them
if [ "$(id -u)" -eq 0 ]; then
    echo "Run setup.sh without sudo." >&2
    exit 1
fi

# An earlier run with sudo can leave ~/.zshenv owned by root
if [ -e ~/.zshenv ] && [ ! -O ~/.zshenv ]; then
    echo "~/.zshenv belongs to another user, probably from running setup with sudo." >&2
    echo "Fix it with:  sudo chown \"\$(id -un)\" ~/.zshenv  and run setup.sh again." >&2
    exit 1
fi

IS_MACOS=0
if [ "$(uname)" = "Darwin" ]; then IS_MACOS=1; fi

# Set ACRO_TD_CORE environment variable
# Resolves to the directory containing this setup script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# launchctl setenv makes it available to GUI apps (like TouchDesigner) until logout;
# the login agent below sets it again at every login
if [ "$IS_MACOS" -eq 1 ]; then launchctl setenv ACRO_TD_CORE "$SCRIPT_DIR"; fi
# .zshenv makes it available in terminal sessions
# Drop any earlier line (e.g. from before the repo moved), then add the current path
if [ -f ~/.zshenv ]; then sed -i.bak '/^export ACRO_TD_CORE=/d' ~/.zshenv && rm -f ~/.zshenv.bak; fi
echo "export ACRO_TD_CORE=\"$SCRIPT_DIR\"" >> ~/.zshenv
export ACRO_TD_CORE="$SCRIPT_DIR"
echo "ACRO_TD_CORE set to $SCRIPT_DIR"

# Run all module setup scripts. Each one sets a variable named after its folder
# (acro-td-mcp -> ACRO_TD_MCP); the ones that end up set go into the login agent.
# The module scripts set their own SCRIPT_DIR, so don't use SCRIPT_DIR after this loop.
ENV_NAMES="ACRO_TD_CORE"
for module_setup in "$SCRIPT_DIR"/modules/*/setup.sh; do
    if [ -f "$module_setup" ]; then
        module_name="$(basename "$(dirname "$module_setup")")"
        var_name="$(printf '%s' "$module_name" | sed 'y/abcdefghijklmnopqrstuvwxyz-/ABCDEFGHIJKLMNOPQRSTUVWXYZ_/')"
        unset "$var_name"
        echo "Running $module_name/setup.sh"
        source "$module_setup"
        if [ -n "${!var_name}" ]; then ENV_NAMES="$ENV_NAMES $var_name"; fi
    fi
done

# macOS: apps opened from Finder or the Dock (TouchDesigner, ALPACKA) get their environment
# from launchd, not from ~/.zshenv, and launchctl setenv is lost at logout. This login agent
# runs launchctl setenv for every variable at each login. Rerunning setup rewrites it.
if [ "$IS_MACOS" -eq 1 ]; then
    AGENT_LABEL="lol.acronym.acro-td-core.env"
    AGENT_PLIST="$HOME/Library/LaunchAgents/$AGENT_LABEL.plist"
    GUI_DOMAIN="gui/$(id -u)"

    # Values go into XML; sed rather than ${v//&/...}, which bash 5.2 treats specially
    xml_escape() {
        printf '%s' "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
    }

    # The paths are passed as arguments, never parsed by a shell: sh -c '<loop>' $0 NAME VALUE ...
    mkdir -p "$HOME/Library/LaunchAgents"
    {
        printf '%s\n' \
            '<?xml version="1.0" encoding="UTF-8"?>' \
            '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">' \
            '<plist version="1.0">' \
            '<dict>' \
            '    <key>Label</key>' \
            "    <string>$AGENT_LABEL</string>" \
            '    <key>ProgramArguments</key>' \
            '    <array>' \
            '        <string>/bin/sh</string>' \
            '        <string>-c</string>' \
            '        <string>while [ $# -gt 1 ]; do /bin/launchctl setenv "$1" "$2"; shift 2; done</string>' \
            '        <string>acro-td-core-env</string>'
        for name in $ENV_NAMES; do
            printf '        <string>%s</string>\n' "$name" "$(xml_escape "${!name}")"
        done
        printf '%s\n' \
            '    </array>' \
            '    <key>RunAtLoad</key>' \
            '    <true/>' \
            '</dict>' \
            '</plist>'
    } > "$AGENT_PLIST"

    if ! lint_output="$(plutil -lint "$AGENT_PLIST" 2>&1)"; then
        echo "ERROR: the login agent isn't a valid plist: $lint_output" >&2
        exit 1
    fi

    # Reload it so it runs now with the current paths. A bootstrap right after a bootout
    # can fail while launchd is still removing the old job, so retry briefly.
    launchctl bootout "$GUI_DOMAIN/$AGENT_LABEL" >/dev/null 2>&1 || true
    agent_loaded=0
    for attempt in 1 2 3; do
        if load_output="$(launchctl bootstrap "$GUI_DOMAIN" "$AGENT_PLIST" 2>&1)"; then
            agent_loaded=1
            break
        fi
        sleep 1
    done
    if [ "$agent_loaded" -eq 1 ]; then
        echo "Login agent installed: $AGENT_PLIST"
        echo "Apps opened from Finder or the Dock get these variables at every login. Quit and reopen any that are already open."
    else
        echo "WARNING: couldn't load the login agent now ($load_output). It loads at your next login." >&2
    fi
fi

# Python packages (requirements.txt) are installed by TouchDesigner's tdPyEnvManager into the
# project's own venv the first time the .toe is opened (see TDPyEnvManagerContext.yaml)

# The MCP server ships prebuilt (modules/acro-td-mcp/dist/index.js); it only needs Node
if ! command -v node >/dev/null 2>&1; then
    echo "WARNING: Node.js was not found on PATH. Install it to use the acro-td-mcp MCP server."
fi
