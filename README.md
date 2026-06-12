# Acro TD Core

![Version](https://img.shields.io/badge/version-1.10.12-blue)

TouchDesigner project template with automated version management, external tox handling, and MCP integration for AI-assisted development.

## Features

- **Version Tracking** — Semantic versioning with build numbers and remote update checking
- **External Tox Management** — Save, load, and sync component `.tox` files
- **Component Creator** — Dialog-based scaffolding with network protocol support
- **MCP Integration** — AI tools for scene introspection via Claude Code
- **Macros** — Hierarchical macro management with signals
- **Theme Manager** — CSS-based color theming for TD's UI
- **Hotkey Manager** — Central keyboard-shortcut registration
- **Widgets** — Building blocks for custom in-TD UIs

## MCP Server

The project includes a general-purpose MCP server for TouchDesigner at `modules/acro-td-mcp/`. It provides tools for executing Python, inspecting operators, and exploring the scene hierarchy.

See [docs.derivative.ca](https://docs.derivative.ca) for TouchDesigner documentation.

## Subtree Management

This project uses git subtrees for shared modules. Each module lives under `modules/` and is mirrored to its own GitHub repo.

```bash
# Pull updates for a module (replace <module> with one of the seven below)
git subtree pull --prefix=modules/acro-td-<module> https://github.com/acronym-lol/acro-td-<module>.git main --squash

# Push changes upstream
git subtree push --prefix=modules/acro-td-<module> https://github.com/acronym-lol/acro-td-<module>.git main
```

Modules:

- `acro-td-component-creator`
- `acro-td-hotkey-manager`
- `acro-td-macros`
- `acro-td-mcp`
- `acro-td-theme-manager`
- `acro-td-version-manager`
- `acro-td-widgets`

## Documentation

Full documentation available at the [docs site](https://acronym-lol.github.io/acro-td-core/).
