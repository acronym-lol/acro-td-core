# Acro TD Core

![Version](https://img.shields.io/badge/version-1.10.12-blue)

A TouchDesigner project template with automated version management, external tox file handling, and component scaffolding.

## What you get

This template bundles seven modules as git subtrees and wires them together at project load:

| Module | Provides |
|--------|----------|
| `acro-td-version-manager` | `AcroToxExt` / `AcroVersionExt` mixins + central `AcroVersionManager`. External tox management, semantic versioning, remote update checks. |
| `acro-td-component-creator` | Dialog + API for scaffolding new components with extensions, callbacks, and network protocols (MQTT, OSC, TCP, UDP, WebSocket). |
| `acro-td-hotkey-manager` | Project-wide keyboard-shortcut registry with conflict resolution. |
| `acro-td-theme-manager` | CSS-based UI theming for `ui.colors`, TUIK2 widgets, and op-shortcut params. |
| `acro-td-macros` | Hierarchical macro framework with callbacks, signal routing, and on-disk persistence. |
| `acro-td-widgets` | Widget framework — `AcroWidgetContainer` primitive + reusable UI library for building custom in-TD UIs. |
| `acro-td-mcp` | MCP bridge — HTTP server in TD + Node MCP server exposing scene introspection and Python execution to Claude Code. |

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/acronym-lol/acro-td-core.git
   ```

2. From the repo root, run the setup script (registers env vars for the modules + the project):
   ```powershell
   ./setup.ps1   # Windows
   ./setup.sh    # macOS / Linux
   ```

3. Open `AcroCore.toe` in TouchDesigner.

4. On first load, the project will:
   - Initialize each module's tox + version tracking
   - Print a startup banner to the textport
   - Check for available updates (if configured)
   - Apply the configured theme

See [Getting Started](getting-started) for the full setup.

## Project-level documentation

| Page | Description |
|------|-------------|
| [Getting Started](getting-started) | Installation, first-time setup, project structure |
| [Architecture](architecture) | Class hierarchy, mixin pattern, tag discovery, lifecycle hooks |
| [Configuration Reference](configuration) | All parameters, tags, env vars, file formats |

## Module documentation

Each module ships its own Docsify site under `modules/acro-td-X/docs/`.

| Module | Doc home |
|--------|----------|
| Version Manager | [`modules/acro-td-version-manager/docs/`](modules/acro-td-version-manager/docs/) |
| Component Creator | [`modules/acro-td-component-creator/docs/`](modules/acro-td-component-creator/docs/) |
| Hotkey Manager | [`modules/acro-td-hotkey-manager/docs/`](modules/acro-td-hotkey-manager/docs/) |
| Theme Manager | [`modules/acro-td-theme-manager/docs/`](modules/acro-td-theme-manager/docs/) |
| Macros | [`modules/acro-td-macros/docs/`](modules/acro-td-macros/docs/) |
| Widgets | [`modules/acro-td-widgets/docs/`](modules/acro-td-widgets/docs/) |
| MCP | [`modules/acro-td-mcp/docs/`](modules/acro-td-mcp/docs/) |
