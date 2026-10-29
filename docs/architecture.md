---
last_reviewed: 2026-08-27
---

# Architecture

## Overview

The system is built on a **mixin inheritance pattern** where functionality is composed through Python multiple inheritance. Two tag-based discovery systems allow central management of components.

## Class Hierarchy

```
AcroToxExt                      ← External tox file management
    └── AcroVersionExt           ← Version tracking (inherits tox management)

CallbacksExt                  ← Event callback system (from TD)

CallbacksExt + AcroVersionExt
    ├── AcroCore                ← Main project extension
    ├── AcroVersionManager      ← Central version/tox manager
    ├── AcroComponentCreator    ← Component scaffolding tool
    ├── AcroHotkeyManager       ← Central hotkey registry
    ├── AcroThemeManager        ← UI theming (ui.colors / TUIK2 / op shortcuts)
    ├── AcroMCP                 ← MCP HTTP API bridge
    ├── AcroMacros              ← Macro framework
    └── AcroWidgets             ← Widget framework
```

Any extension can inherit from `AcroToxExt` for tox-only management, or `AcroVersionExt` for full version tracking (which includes tox management). Most first-party modules in this project inherit from both `CallbacksExt` and `AcroVersionExt`, so they all carry the standard Component / Version / Callbacks parameter pages and are discoverable via the `tox_managed` and `version_tracking` tags.

## Tag Discovery System

Components are discovered at runtime using TouchDesigner's tag system:

| Tag | Applied By | Purpose |
|-----|-----------|---------|
| `tox_managed` | `AcroToxExt.__init__()` | Identifies components with external tox management |
| `version_tracking` | `AcroVersionExt.__init__()` | Identifies version-tracked components |

The `AcroVersionManager` discovers components using:

```python
# Find all tox-managed components
root.findChildren(tags=['tox_managed'])

# Find all version-tracked components (subset of tox_managed)
root.findChildren(tags=['version_tracking'])
```

Since `AcroVersionExt` inherits from `AcroToxExt`, version-tracked components always have **both** tags.

## Parameter Page Pattern

Each mixin creates its own custom parameter page on the owning component:

| Mixin | Page Name | Key Parameters |
|-------|-----------|---------------|
| `AcroToxExt` | **Component** | Repopath, Enableexternaltox, Externaltoxpath, Onsave, Reloadtox |
| `AcroVersionExt` | **Version** | Version, Build, Versionurl, Tokenenv, Autoupdate, Devmode |

Parameters are created programmatically in `_ensureComponentPage()` and `_ensureVersionPage()` methods. These methods are idempotent — they skip parameters that already exist, so re-initialization is safe.

## TD Parameter Binding

`AcroToxExt` creates custom parameters that **bind** to TouchDesigner's built-in external tox system:

```python
# Our custom parameter controls the value
comp.par.Externaltoxpath = '/path/to/component.tox'

# TD's built-in parameter references ours via expression
comp.par.externaltox.expr = "me.par.Externaltoxpath"
comp.par.externaltox.mode = ParMode.EXPRESSION
```

This means:
- Users interact with our custom parameters (on the Component page)
- TouchDesigner's tox loading system reads the values automatically
- We maintain full control over the values and can add logic around them

## Lifecycle Hooks

The system hooks into TouchDesigner's project lifecycle:

| Event | Handler | What Happens |
|-------|---------|-------------|
| **Project Start** | `AcroCore.onStart()` | Prints the startup banner, copies the playbar into the main menu, hides external links / GPU display, schedules a project-saved check. |
| **Project Start** | `AcroVersionManager.onStart()` | Checks all components for updates (with configurable delay). |
| **Project Start** | `AcroThemeManager.onStart()` | Clones into TUIK2 colors, optionally re-applies the active theme and runs the bundled UI fix-ups. |
| **Project Save** | `AcroCore.onSave()` | Refreshes `alpacka.yml` (the launcher's project metadata file) with the current TD version. |
| **Project Save** | `AcroVersionManager.onSaveStart()` | Finds and saves dirty tox-managed components. |
| **Project Exit** | `AcroCore.onExit()` | Forwards to AcroMCP's `onExit()` to deregister the MCP instance. |

## Persistent Storage

The `AcroVersionManager` uses TouchDesigner's `StorageManager` for data that persists across saves:

| Key | Type | Purpose |
|-----|------|---------|
| `SkippedVersions` | `dict` | Maps component paths to skipped version strings |
| `IgnoredComponents` | `list` | Component paths that should not be checked for updates |

## Enable Expressions

Parameters use `enableExpr` to conditionally gray out based on other parameter values:

```python
# Token variable name only enabled when Usetoken is on
('Tokenenv', ..., 'me.par.Usetoken')

# Autoupdate only enabled when version checking is on
('Autoupdate', ..., 'me.par.Versioncheckenabled')

# Reloadonupdate only enabled when autoupdate is not 'off'
('Reloadonupdate', ..., "me.par.Autoupdate != 'off'")
```

This keeps the parameter UI clean by hiding irrelevant options.
