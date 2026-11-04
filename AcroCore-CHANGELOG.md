# Changelog

All notable changes to this project will be documented in this file.

## [1.11.1] - 2026-11-04
- New projects' .gitignore ignores .env files and alpacka.local.yml again. The template had been replacing ALPACKA's baseline file without them. Projects created earlier need the lines added by hand

## [1.11.0] - 2026-11-03
- AcroMCP only answers local requests that carry the per-session token from the instance registry. The MCP server sends it automatically (AcroMCP 1.1.0)
- The Macros REST API requires an API key from the variable named in Apikeyenv, and adds Allowremote and Alloworigins (AcroMacros 2.5.0)
- Version checking reads its token from the environment variable named in Tokenenv. The saved Token parameter is removed (AcroVersionManager 1.2.0)
- The MCP server ships prebuilt, and .mcp.json points at ${ACRO_TD_MCP}/dist/index.js. Re-run setup.ps1 / setup.sh after updating
- Several TouchDesigner instances can run at once without taking each other's port (AcroMCP 1.2.0)
- Setup no longer writes TouchDesigner's pref.txt. Python packages come from the project venv
- Updated the MCP server's dependencies (npm audit is clean) and shipped their licenses in dist/THIRD_PARTY_LICENSES.txt (AcroMCP 1.2.1)
- New projects' .gitignore also ignores numbered saves

## [1.10.15] - 2026-10-27
- Added macro API

## [1.10.14] - 2026-10-27
- Fixed Widget and Components updating

## [1.10.13] - 2026-10-27
- Fixed widgets modifier keys

## [1.10.12] - 2026-06-09
- Fixed changelog and version naming scheme
