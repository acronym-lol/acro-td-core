---
last_reviewed: 2026-08-27
---

# Getting Started

## Prerequisites

- **TouchDesigner** 2025+ (tested with build 2025.32280)
- **Git** (for version checking and subtree management)
- **Python 3** (bundled with TouchDesigner)

## Installation

Clone the repository to your machine:

```bash
git clone https://github.com/acronym-lol/acro-td-core.git
```

Then run the parent setup script, which loops over each module's `setup.ps1` / `setup.sh` and also registers the project-level `ACRO_TD_CORE` env var:

**Windows (PowerShell):**

```powershell
./setup.ps1
```

**macOS / Linux:**

```bash
./setup.sh
```

Each per-module setup script registers a per-module variable (`ACRO_TD_VERSION_MANAGER`, `ACRO_TD_COMPONENT_CREATOR`, `ACRO_TD_HOTKEY_MANAGER`, `ACRO_TD_MACROS`, `ACRO_TD_MCP`, `ACRO_TD_THEME_MANAGER`, `ACRO_TD_WIDGETS`) pointing at the absolute path of the module on disk. See [Configuration Reference → Per-Module Environment Variables](configuration#per-module-environment-variables) for the full list.

Open the `.toe` file in TouchDesigner once the variables are set.

## First-Time Setup

When the project loads for the first time, the extensions automatically:

1. **Initialize version tracking** — Each component creates its `*-version.json` if missing.
2. **Tag themselves** — Components inheriting from `AcroVersionExt` get the `tox_managed` and `version_tracking` tags so the manager can find them.
3. **Print the startup banner** to the textport.
4. **Refresh `alpacka.yml`** — AcroCore writes the launcher's project metadata file alongside the `.toe` on every save.

## Project Structure

```
acro-td-core/
├── scripts/                              ← Project-level Python
│   ├── AcroCore.py                       ← Main project extension
│   └── AcroColors.py                     ← UI color theming
├── modules/                              ← Git subtrees
│   ├── acro-td-version-manager/          ← AcroToxExt, AcroVersionExt, AcroVersionManager
│   ├── acro-td-component-creator/        ← Component scaffolding tool
│   ├── acro-td-hotkey-manager/           ← Central hotkey registry
│   ├── acro-td-theme-manager/            ← UI theming
│   ├── acro-td-macros/                   ← Macro framework
│   ├── acro-td-widgets/                  ← Widget framework
│   └── acro-td-mcp/                      ← MCP server + AcroMCP HTTP API
├── docs/                                 ← This documentation site
├── tox/                                  ← External component .tox files
├── AcroCore-VERSION.json                 ← Project version file
└── AcroCore-CHANGELOG.md                 ← Project version history
```

Each module under `modules/` carries its own version file (`<ClassName>-VERSION.json`, e.g. `AcroMacros-VERSION.json`) and changelog (`<ClassName>-CHANGELOG.md`).

## Using as a Template

To start a new project based on this template, use the launcher (the `alpacka` workflow). The launcher reads `template.yml` from this repo and creates a new project with the right folder structure, `.gitignore`, `.mcp.json`, `CLAUDE.md`, and Claude skills already in place. AcroCore itself no longer bootstraps these — the launcher does.

If you're not using the launcher, you can still:

1. Copy this directory to a new location.
2. Save the `.toe` to its new home with **File > Save As**.
3. The project's `onSave` hook refreshes `alpacka.yml` with the new TD version.

## Subtree Management

The project includes git subtrees for each shared module. The `push-subtrees` Claude skill (from this repo's `.claude/skills/`) automates the standard operations.

**Pull latest changes (manual):**

```bash
git subtree pull --prefix=modules/acro-td-version-manager https://github.com/acronym-lol/acro-td-version-manager.git main --squash
git subtree pull --prefix=modules/acro-td-component-creator https://github.com/acronym-lol/acro-td-component-creator.git main --squash
# ... and so on for each module
```

**Push changes upstream (manual):**

```bash
git subtree push --prefix=modules/acro-td-version-manager https://github.com/acronym-lol/acro-td-version-manager.git main
git subtree push --prefix=modules/acro-td-component-creator https://github.com/acronym-lol/acro-td-component-creator.git main
# ... and so on for each module
```

Each module has a corresponding git remote configured in this repo's `.git/config` (`acro-td-version-manager`, `acro-td-component-creator`, etc.) so you can shorten the URLs to just the remote name once they're set up.

## Next Steps

- Read the [Architecture](architecture) page to understand how the modules fit together.
- Learn about [Tox Management](tox-management) and [Version Tracking](version-tracking) — the foundation every module uses.
- Set up [Version Checking](version-checking) for remote update detection.
- Explore the per-module guides: [Component Creator](component-creator), [Hotkey Manager](hotkey-manager), [Theme Manager](theme-manager), [Macros](macros), [Widgets](widgets), and [AcroMCP](tdmcp).
