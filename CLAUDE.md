# CLAUDE.md - Project Instructions for AI Agents

## Project Overview

**Acro TD Core** is a TouchDesigner project template providing automated version management, external tox file handling, and component scaffolding. It runs inside TouchDesigner's Python environment (Python 3, bundled with TD).

### Key Scripts

| File | Class | Role |
|------|-------|------|
| `modules/acro-td-version-manager/scripts/AcroToxExt.py` | `AcroToxExt` | Base mixin for external tox file management |
| `modules/acro-td-version-manager/scripts/AcroVersionExt.py` | `AcroVersionExt` | Version tracking mixin (inherits AcroToxExt) |
| `scripts/AcroCore.py` | `AcroCore` | Main project extension (inherits CallbacksExt + AcroVersionExt) |
| `modules/acro-td-version-manager/scripts/AcroVersionManager.py` | `AcroVersionManager` | Central manager for all versioned components |
| `modules/acro-td-component-creator/scripts/AcroComponentCreator.py` | `AcroComponentCreator` | Dialog-based component scaffolding tool |
| `modules/acro-td-hotkey-manager/scripts/AcroHotkeyManager.py` | `AcroHotkeyManager` | Central hotkey management |
| `modules/acro-td-mcp/scripts/AcroMCP.py` | `AcroMCP` | HTTP API bridge for MCP server |
| `modules/acro-td-theme-manager/scripts/AcroThemeManager.py` | `AcroThemeManager` | CSS-based theme application |
| `modules/acro-td-widgets/scripts/AcroWidgets.py` | `AcroWidgets` | Widget discovery + component browser |
| `scripts/AcroColors.py` | `AcroColors` | UI color theming for DAT editors |

### Inheritance Pattern

```
AcroToxExt                       <- External tox file management
    └── AcroVersionExt            <- Version tracking (inherits tox management)

CallbacksExt + AcroVersionExt
    ├── AcroCore                  <- Main project extension
    ├── AcroVersionManager        <- Central version/tox manager (module: acro-td-version-manager)
    ├── AcroComponentCreator      <- Component scaffolding tool (module: acro-td-component-creator)
    ├── AcroHotkeyManager         <- Central hotkey manager (module: acro-td-hotkey-manager)
    ├── AcroMacros                <- Macro framework (module: acro-td-macros)
    ├── AcroMCP                   <- MCP HTTP bridge (module: acro-td-mcp)
    ├── AcroThemeManager          <- Theme system (module: acro-td-theme-manager)
    └── AcroWidgets               <- Widget management (module: acro-td-widgets)
```

## MCP Tools

This project includes an MCP server (`modules/acro-td-mcp/`) that provides tools for interacting with the running TouchDesigner scene. The MCP server wraps the AcroMCP HTTP API as native tools.

Use `td_guide` for curated workflow guides, and `td_help` for official docs on specific operators/classes.

### Architecture

```
Claude Code  →  MCP Server (modules/acro-td-mcp/dist/index.js)  →  AcroMCP HTTP API (localhost:54200-54209)  →  TD Python
```

- **MCP server** (`modules/acro-td-mcp/`): Node.js process with registered MCP tools.
- **AcroMCP** (`/AcroMCP`): TD webserver component (auto-assigned port 54200-54209).
- External projects get a `.mcp.json` pointing to this repo's MCP server (created by `AcroCore.onSave()` via `template.yml`).

### MCP Server Development

```bash
# Build after editing modules/acro-td-mcp/src/
npm run build
```

The MCP server also serves reference docs from `modules/acro-td-mcp/reference/` via the `td_guide` tool.

## Scene Structure

Key operator paths in this project:

| Path | Description | Global Shortcut |
|------|-------------|-----------------|
| `/` | Scene root | — |
| `/AcroCore` | Main project component (file creation, environment) | `op.AC` |
| `/AcroMCP` | HTTP API bridge for MCP server | — |
| `/AcroComponentCreator` | Component scaffolding | `op.ACC` |
| `/AcroHotkeyManager` | Central hotkey management | `op.AHM` |
| `/AcroVersionManager` | Version/tox manager | — |
| `/AcroThemeManager` | Theme manager | `op.ATM` |
| `/AcroWidgets` | Widget management system | `op.AW` |
| `/components` | User components container | — |
| `/AcroMacros` | Macro management | `op.AM` |

## AcroComponentCreator — Component Scaffolding

The **AcroComponentCreator** (`/AcroComponentCreator`, global shortcut `op.ACC`) provides programmatic component creation with built-in support for extensions, callbacks, and network protocols. Open the creation dialog with **Ctrl+Alt+Shift+N** (when in a network editor pane).

### AcroComponentCreator API

```python
# Get default settings dict
settings = op.ACC.DefaultSettings()

# Modify settings
settings['Classname'] = 'MyComponent'    # REQUIRED - UpperCamelCase
settings['Shortcut'] = 'MYCOMP'          # REQUIRED - UPPERCASE, 2+ chars
settings['Opshortcut'] = True            # Enable op.MYCOMP global access
settings['Comptype'] = 'base'            # 'base' or 'container'
settings['Path'] = '/components'         # Where to create
settings['Posx'] = 400                   # Node position
settings['Posy'] = 0

# Create the component
op.ACC.CreateComponent(settings)
```

### DefaultSettings() Keys

| Key | Default | Description |
|-----|---------|-------------|
| `Classname` | `''` | **Required** — UpperCamelCase (e.g., `MyComponent`) |
| `Shortcut` | `''` | **Required** — UPPERCASE, 2+ chars (e.g., `MYCOMP`) |
| `Docstring` | `''` | Class docstring |
| `Opshortcut` | `False` | Enable `op.SHORTCUT` global access |
| `Comptype` | `'base'` | `'base'` or `'container'` |
| `Samenameasclass` | `True` | Component name = class name |
| `Compname` | `''` | Override name if `Samenameasclass=False` |
| `Toxext` | `False` | Enable external tox management mixin (AcroToxExt) |
| `Versionext` | `False` | Enable version tracking mixin (AcroVersionExt — implies Toxext) |
| `Examples` | `False` | Include example callback code |
| `Path` | `'/'` | Where to create the component |
| `Posx`, `Posy` | `0` | Node position |
| `Mqtt` | `False` | Include MQTT client DAT |
| `Oscin`, `Oscout` | `False` | Include OSC in/out DATs |
| `Tcpclient`, `Tcpserver` | `False` | Include TCP client/server DATs |
| `Udpin`, `Udpout` | `False` | Include UDP in/out DATs |
| `Webclient`, `Webserver` | `False` | Include Web client/server DATs |
| `Websocket` | `False` | Include WebSocket DAT |

### Validation Rules

- `Classname`: Must match `^[A-Z]+(?:[A-Za-z0-9]+)*$` (UpperCamelCase, digits allowed)
- `Shortcut`: Must match `^[A-Z][A-Z0-9_]+$` (2+ uppercase chars, digits/underscores allowed)

## AcroHotkeyManager — Central Hotkey Management

The **AcroHotkeyManager** (`/AcroHotkeyManager`, global shortcut `op.AHM`) provides centralized keyboard shortcut management. Components register hotkey combinations via a simple API, and the manager dispatches callbacks when keys are pressed.

### AcroHotkeyManager API

```python
# Register a hotkey
op.AHM.Register('ctrl+alt+shift+n', callback,
                          description='Open Component Creator')

# Unregister a hotkey
op.AHM.Unregister('ctrl+alt+shift+n')

# Unregister all hotkeys owned by a component
op.AHM.UnregisterOwner('/AcroComponentCreator')

# Get all registered bindings
op.AHM.Bindings  # Returns dict

# Get current modifier state
op.AHM.Modifiers  # {'ctrl': bool, 'alt': bool, 'shift': bool}

# Enable/disable a hotkey without removing it
op.AHM.SetEnabled('ctrl+alt+shift+n', False)

# Print all hotkeys to textport
op.AHM.PrintHelp()
```

### Hotkey String Format

- **Case-insensitive**: `'Ctrl+Alt+N'` = `'ctrl+alt+n'`
- **Order-insensitive**: `'alt+ctrl+n'` = `'ctrl+alt+n'`
- **Modifiers**: `ctrl`, `alt`, `shift`
- **Keys**: single characters (`n`, `s`) or special keys (`f1`, `space`, `enter`, `esc`, `tab`)

### Registering Hotkeys in Components

Components should register hotkeys during initialization:

```python
class MyComponent(CallbacksExt):
    def __init__(self, ownerComp):
        # ... existing init code ...
        self._registerHotkeys()

    def _registerHotkeys(self):
        hk = op.AHM
        if hk:
            hk.Register('ctrl+alt+m', self.MyMethod,
                        description='Do something')
```

### Conflict Handling

- Last-registered wins by default (`force=True`) — re-registering a hotkey replaces the existing binding. This is required so components can re-register cleanly when their synced extension reloads.
- Pass `force=False` to defer to an existing binding — the registration is rejected with a warning and `Register()` returns `False`.

## AcroMacros — Macro Management System

The **AcroMacros** component (`/AcroMacros`, global shortcut `op.AM`) is a macro management framework. Macros are hierarchical units with callback code (`onInit`, `onTrigger`) stored on disk in `macros/main/`. They can be triggered directly or via signal subscriptions.

### AcroMacros API Quick Reference

| Method | Returns | Purpose |
|--------|---------|---------|
| `ListMacros()` | `list[dict]` | List all macros with metadata |
| `GetMacroInfo(path)` | `dict \| None` | Full info for a macro by path |
| `GetCallbackCode(path)` | `str \| None` | Read callback Python code |
| `SetCallbackCode(path, code)` | `dict` | Write callback code and save to disk |
| `CreateMacro(name, path)` | `None` | Create a new macro (path = parent path, `""` for root) |
| `DeleteMacro(path)` | `None` | Delete a macro by path |
| `TriggerMacro(path, args)` | `None` | Execute a macro |
| `Emit(signal, args)` | `None` | Broadcast signal to subscribers |
| `SetMacroComment(path, comment)` | `dict` | Set macro comment |
| `GetSignals()` | `dict` | Get signal routing table |
| `RenameMacroUUID(uuid, name)` | `None` | Rename a macro by UUID |

### Macro Callback Template

```python
def onInit(info, am, macro):
    # am.Subscribe(macro, 'signal_name')  # subscribe to signals here
    return

def onTrigger(info, am, macro, comps, args):
    # comps is op.comps (component shortcuts)
    # args is whatever was passed to TriggerMacro or Emit
    return
```

## AcroWidgets — Widget System

**AcroWidgets** (`/AcroWidgets`, global shortcut `op.AW`) is a widget management system for building custom user interfaces in TouchDesigner. It provides widget discovery, component inspection, and clipboard operations.

### AcroWidgetContainer — CRITICAL COMPONENT

**AcroWidgetContainer** is the fundamental building block of the AcroWidgets UI system. Think of it like HTML's `<div>` element.

**Key characteristics:**
- Can exist **anywhere** in the scene hierarchy
- Can be **nested** many levels deep (widget containers inside widget containers)
- Contains exactly one widget from the widget library at a time
- Supports drag/drop, copy/paste, and undo operations

**IMPORTANT: Modification Guidelines**

The AcroWidgetContainer extension (`modules/acro-td-widgets/scripts/AcroWidgetContainer.py`) requires extreme caution when modifying:

1. **Global references are intentional**: The `op.AW` reference must point to the central AcroWidgets registry regardless of where the widget container lives in the scene. Do NOT replace with relative paths. PopMenu uses TouchDesigner's built-in `op.TDResources.PopMenu`.

2. **Small changes only**: Any modifications should be isolated to single features so they can be tested individually before proceeding.

3. **Always ask first**: Before making ANY changes to AcroWidgetContainer, ask the user for approval and explain the specific change.

4. **Test thoroughly**: Widget containers can be nested arbitrarily deep and interact with each other through copy/paste/drag/drop operations.

### Widget Discovery

Widgets are discovered via tags:
- `widgetFolder` — Container for widget collections
- `widget` or `TDBasicWidget` — Individual widgets

```python
# Get all widget folders and their contents
op.AW.UpdateWidgets()
print(op.AW.Widgets)  # Dict of folders → widgets
```

## AcroThemeManager — CSS Theme Application

**AcroThemeManager** (`/AcroThemeManager`, global shortcut `op.ATM`) applies CSS-based theme files to TouchDesigner's `ui.colors`, TUIK2 component parameters, and `op.*` shortcut parameters.

Theme files live in `modules/acro-td-theme-manager/themes/`. See that module's `CLAUDE.md` for the theme-file format, the base template, the protected-color rules, and tips for creating new themes.

## Code Conventions

### TouchDesigner-Specific Patterns

- **Promoted extensions**: Extensions are promoted via `comp.par.ext0promote = True`, making methods/properties accessible as `comp.MethodName`
- **Uppercase public API**: All public methods and properties use UpperCamelCase (e.g., `SaveTox()`, `IsDirty`, `VersionString`). This is a TD convention for promoted extension members.
- **Private methods**: Use `_camelCase` prefix (e.g., `_ensureComponentPage()`, `_isDevActive()`)
- **Pulse handlers**: Named `pulse_Parametername` to match TD's pulse callback convention
- **Sync-to-file**: All extension TextDATs use `syncfile = True`, so TD automatically picks up changes when you edit the `.py` file on disk. You do NOT need to call `reinitextensions` after modifying a script file — TD handles it.
- **Extension reinitialization**: When a synced extension file is edited on disk, the extension automatically reinitializes — `__init__` runs again. Extensions should **never create persistent operators** in `__init__` — use MCP tools to create component structure, and have extensions simply reference existing operators:
  ```python
  # BAD — don't create operators in extensions
  def __init__(self, ownerComp):
      self.helper = ownerComp.create(nullTOP, 'helper')

  # GOOD — reference operators that already exist in the component
  def __init__(self, ownerComp):
      self.helper = ownerComp.op('helper')  # created via MCP, not extension
  ```
- **Frame-sensitive operations**: Some TD operations require frame delays. Creating and destroying an operator in the same frame will crash TouchDesigner. OP Viewer TOPs need 1 frame after setting their path before the image is rendered. Use `run('code', args, delayFrames=1)` to defer operations.
- **Node placement**: Before creating any operator or component, always check existing children and their positions in the target location to avoid placing new nodes on top of existing ones. Query positions first and choose a clear spot.
- **debug() over print()**: TouchDesigner provides a built-in `debug()` function that is superior to `print()`. Always prefer `debug()` because it automatically includes the script location and operator path in the output, making it much easier to track down where messages originate. Use `debug('message')` instead of `print('message')`.

### Callbacks Pattern

Components use a two-tier callbacks system managed by `CallbacksExt`:

**Main component callbacks** (external):
- Live **outside** the component in its parent, docked to the component for visual association
- Named `{ComponentName}_callbacks` (e.g., `MyComponent_callbacks`)
- Created by `AcroComponentCreator.addCallbacks()` which places them in `comp.parent()` and sets `dock = comp`
- Allows easy editing without diving into the component internals

**Backup and auto-creation mechanism**:
- An internal `callbacksBackup` TextDAT stores a copy of the callbacks template
- On component creation, `execute` DAT's `onCreate()` checks if the external callbacks exist
- If missing, it copies `callbacksBackup` to the parent and docks it to the component
- The `opExecCallbacks` DAT watches for component renames and updates the callbacks DAT name to match

**Connection-specific callbacks** (internal):
- Protocol callbacks (`webserver_callbacks`, `mqtt_callbacks`, `oscin_callbacks`, etc.) live **inside** the component
- These are tied to specific connection DATs (WebServer DAT, MQTT DAT, etc.)
- Generated from Jinja2 templates in `modules/acro-td-component-creator/scripts/CallbacksTemplates/`

**Callbacks page parameters**:
- `Callbackdat` — DAT parameter pointing to the external callbacks DAT
- `Editcallbackdat` — Pulse to open the callbacks DAT for editing
- `Printcallbacks` — Toggle for debugging callback execution

### Parameter Conventions

- Custom parameter names use capitalized first letter (e.g., `Externaltoxpath`, `Versionurl`, `Devmode`)
- TD's built-in parameters are lowercase (e.g., `externaltox`, `enableexternaltox`)
- Parameters are created programmatically in `_ensureXxxPage()` methods — these are idempotent (skip params that already exist)
- Enable expressions (`enableExpr`) conditionally gray out parameters based on other values

### Tag-Based Discovery

Components are discovered at runtime using tags:
- `tox_managed` — Applied by `AcroToxExt.__init__()`, identifies components with external tox management
- `version_tracking` — Applied by `AcroVersionExt.__init__()`, identifies version-tracked components

Discovery: `root.findChildren(tags=['tox_managed'])` or `root.findChildren(tags=['version_tracking'])`

### TD Parameter Binding

Custom parameters bind to TD's built-in parameters via expression mode:
```python
comp.par.externaltox.expr = "me.par.Externaltoxpath"
comp.par.externaltox.mode = ParMode.EXPRESSION
```

## Documentation Site

The project uses **Docsify** with the shared [acro-docs-theme](https://github.com/acronym-lol/acro-docs-theme), published on GitHub Pages. There are eight sites: this repo's `docs/` (https://acronym-lol.github.io/acro-td-core/), and one per module, each published from its own repo's `docs/` via the subtree (https://acronym-lol.github.io/acro-td-<module>/).

### Documentation Structure

Project-level docs live in `docs/`; each module ships its own site in `modules/<module>/docs/`. Every site folder has the same shape:

```
docs/                          <- Main site (project-level)
├── .nojekyll                  <- Disables Jekyll on GitHub Pages
├── index.html                 <- Theme shell: name + repo link only. Styling comes from the theme
├── _sidebar.md                <- GENERATED from the folder. Never edit by hand
├── _sidebar.extra.md          <- Hand-written links appended to the sidebar (module sites, core site)
├── _meta.yml                  <- acro-docs metadata; name/summary feed the page header
├── README.md                  <- Home page
├── getting-started.md         <- Setup guide
├── architecture.md            <- System design overview
└── configuration.md           <- All parameters, tags, file formats

modules/<module>/docs/         <- Per-module sites (same files as above)
├── README.md                  <- Module overview
└── *.md                       <- Module reference pages, e.g.:
    acro-td-version-manager/docs/: tox-management.md, version-tracking.md,
        version-manager.md, version-checking.md, dev-workflow.md
    acro-td-theme-manager/docs/: theme-format.md, creating-themes.md,
        base-template.md, protected-colors.md, themes-library.md, theme-manager.md
    acro-td-component-creator/docs/: api.md
    acro-td-hotkey-manager/docs/: api.md
    acro-td-macros/docs/: api.md
    acro-td-widgets/docs/: widgets.md
    acro-td-mcp/docs/: mcp-tools.md, http-api.md
```

### Sidebars are generated

`_sidebar.md` in every site is rebuilt by the theme's generator, and the `.github/workflows/acro-docs-sidebar.yml` workflow regenerates all eight on push. The existing `_sidebar.md` is the author's order: each run rebuilds it from itself.

- **Order**: move lines in `_sidebar.md`; the next run keeps it. New pages are added after the listed ones, and links to deleted pages are dropped. Don't add `sidebar_position` just to set the order.
- **Section labels**: top-level `- **Label**` lines stay where you put them (e.g. **Foundations**, **Workflows** in the version manager).
- **Titles** come from the page: `sidebar_label` in front matter, else `title`, else its first `# ` heading. Editing the link text in `_sidebar.md` does nothing.
- **Links to other sites** go in that site's `_sidebar.extra.md`, appended after a divider.
- Regenerate locally with `npx -p github:acronym-lol/acro-docs-theme#v1 acro-docs-sidebar docs modules/acro-td-*/docs`.
- **Never add the sidebar workflow to a module repo.** Module sidebars are generated here and carried out by `git subtree push`; a bot commit in a module repo would make the next subtree push non-fast-forward.
- Use GitHub-style callouts (`> [!WARNING]`, `> [!TIP]`, ...), not Docsify's `!>` / `?>`.

### Documentation Maintenance Rules

When modifying code in this project, follow these rules to keep documentation in sync:

1. **New feature or modified behavior** — Check if any page in `docs/` needs updating. Look at the relevant page for the class you modified.

2. **New public method, property, or parameter** — Update the relevant doc page's reference table (Properties Reference or Methods Reference section).

3. **New extension class** — Create/update the owning module's `docs/` pages (the sidebar picks new pages up automatically; set `sidebar_position` if order matters); project-level pages only for cross-module concerns.

4. **Modified AcroToxExt, AcroVersionExt, or AcroVersionManager** — Verify the corresponding doc page matches the current code (parameter tables, method signatures, behavior descriptions).

5. **Changed parameter names, defaults, or types** — Update `docs/configuration.md` (the centralized parameter reference).

6. **Changed menu options** — Update both the specific doc page and `docs/configuration.md` with new menu values and labels.

7. **Documentation format** — Uses standard GitHub-flavored markdown (rendered by Docsify). Python code blocks use ` ```python ` fencing.

8. **Verify cross-references** — After renaming a method or parameter, grep across `docs/` to catch stale references:
   ```bash
   grep -r "OldMethodName" docs/
   ```

9. **Keep code examples accurate** — Code snippets in docs should match actual API signatures. If you change a method signature, update all examples that use it.

10. **Version badge** — When bumping the project version, update the version badge in `README.md` and `docs/README.md`.

## Version File Format

```json
{
  "version": "1.10.12",
  "build": 515,
  "last_update": "2026-06-11T10:38:36.567241",
  "td_version": "099",
  "td_build": "2025.32820"
}
```

The main project version file is `AcroCore-VERSION.json`. Individual components have their own version files at `modules/acro-td-<module>/<ClassName>-VERSION.json` (e.g. `modules/acro-td-macros/AcroMacros-VERSION.json`), with changelogs named `<ClassName>-CHANGELOG.md`.

## Project Structure

```
acro-td-core/
├── scripts/                              # Core Python extensions
│   ├── AcroCore.py                       # Main project extension
│   └── AcroColors.py                     # UI color theming
├── modules/                              # Git subtrees (each with its own docs/)
│   ├── acro-td-version-manager/          # Central version/tox management
│   │   ├── scripts/AcroToxExt.py
│   │   ├── scripts/AcroVersionExt.py
│   │   ├── scripts/AcroVersionManager.py
│   │   ├── AcroVersionManager-VERSION.json
│   │   └── AcroVersionManager-CHANGELOG.md
│   ├── acro-td-component-creator/        # Component scaffolding tool
│   │   ├── scripts/AcroComponentCreator.py
│   │   ├── scripts/AcroComponentCreateDialog.py
│   │   ├── scripts/CallbacksTemplates/   # Jinja2 code-gen templates
│   │   ├── AcroComponentCreator-VERSION.json
│   │   └── AcroComponentCreator-CHANGELOG.md
│   ├── acro-td-hotkey-manager/           # Central hotkey management
│   │   ├── scripts/AcroHotkeyManager.py
│   │   ├── AcroHotkeyManager-VERSION.json
│   │   └── AcroHotkeyManager-CHANGELOG.md
│   ├── acro-td-mcp/                      # MCP server + TD bridge
│   │   ├── src/index.ts                  # MCP tool registrations
│   │   ├── src/client.ts                 # Typed HTTP client for AcroMCP
│   │   ├── dist/index.js                 # Built bundle (esbuild)
│   │   ├── scripts/AcroMCP.py            # TD-side HTTP API bridge
│   │   └── reference/                    # TD reference docs (served via td_guide)
│   ├── acro-td-macros/                   # AcroMacros framework
│   ├── acro-td-theme-manager/            # CSS-based theme system
│   └── acro-td-widgets/                  # Widget UI system
├── docs/                                 # Main Docsify documentation site
├── assets/                               # Templates copied into new projects (template.yml)
├── template.yml                          # ALPACKA project-template config
├── AcroCore.toe                          # Main TouchDesigner project file
├── .mcp.json                             # MCP server config (points to modules/acro-td-mcp/dist/index.js)
├── AcroCore-VERSION.json                 # Project version file
└── AcroCore-CHANGELOG.md                 # Version history
```
