# Configuration Reference

This is the centralized reference for all parameters, tags, and file formats across the system. For detailed explanations of behavior, see the individual pages for each component.

---

## AcroToxExt -- Component Page Parameters

These parameters are created on the **Component** custom parameter page by `AcroToxExt.__init__()`. Any component that inherits from `AcroToxExt` (directly or through `AcroVersionExt`) will have these parameters.

| Name | Label | Type | Default | Enable Condition | Description |
|------|-------|------|---------|------------------|-------------|
| `Repopath` | Repository Folder | `folder` | `''` | Always enabled | Git repo folder for this component. |
| `Enableexternaltox` | Enable External Tox | `toggle` | `False` | Always enabled | Enable external tox loading. Syncs with TD's built-in `enableexternaltox` via expression binding. |
| `Externaltoxpath` | External Tox Path | `file` | `''` | `me.par.Enableexternaltox` | Path to external tox file on disk. Syncs with TD's built-in `externaltox` via expression binding. |
| `Onsave` | Save on Project Save | `menu` | `off` | `me.par.Enableexternaltox` | Tox save behavior on project save. |
| `Reloadtox` | Reload Tox | `pulse` | N/A | `me.par.Enableexternaltox` | Pulse to reload external tox from disk. |
| `Reloadcustom` | Reload Custom Parameters | `toggle` | `True` | `me.par.Enableexternaltox` | Reload custom parameters when tox is reloaded. |
| `Reloadbuiltin` | Reload Built-In Parameters | `toggle` | `True` | `me.par.Enableexternaltox` | Reload built-in parameters when tox is reloaded. |

### Onsave Menu Values

| Value | Label | Behavior |
|-------|-------|----------|
| `off` | Disabled | Tox is never saved on project save. |
| `prompt` | Prompt to Save | A confirmation dialog is shown before saving. |
| `always` | Always Save | Tox is saved automatically without prompting. |
| `auto` | Auto (In Repo) | Tox is saved automatically only if the project is running from within the component's repository folder. |

---

## AcroVersionExt -- Version Page Parameters

These parameters are created on the **Version** custom parameter page by `AcroVersionExt.__init__()`. Since `AcroVersionExt` inherits from `AcroToxExt`, components using this extension also have the Component page parameters listed above.

| Name | Label | Type | Default | Read Only | Enable Condition | Description |
|------|-------|------|---------|-----------|------------------|-------------|
| `Versionfile` | Version File | `file` | `{project.folder}/{comp.name.lower()}-version.json` | No | Always enabled | Path to the local version JSON file. |
| `Version` | Version | `str` | `1.0.0` | Yes | Always enabled | Semantic version string (Major.Minor.Patch). |
| `Build` | Build | `str` | `0` | Yes | Always enabled | Incremental build number. |
| `Tdversion` | TD Version | `str` | `''` | Yes | Always enabled | TouchDesigner version used for the last build. |
| `Tdbuild` | TD Build | `str` | `''` | Yes | Always enabled | TouchDesigner build number used for the last build. |
| `Lastupdate` | Last Updated | `str` | `''` | Yes | Always enabled | ISO 8601 timestamp of the last version update. |
| `Versionurl` | Remote Version URL | `str` | `''` | No | Always enabled | HTTP URL to a remote version JSON file for update checks. |
| `Usetoken` | Use Auth Token | `toggle` | `False` | No | Always enabled | Enable token-based authentication for remote requests. |
| `Token` | Auth Token | `str` | `''` | No | `me.par.Usetoken` | GitHub personal access token for authenticated requests. |
| `Versioncheckenabled` | Check for Updates | `toggle` | `True` | No | Always enabled | Master toggle for remote version checking. |
| `Autoupdate` | Auto Update | `menu` | `off` | No | `me.par.Versioncheckenabled` | Update behavior when a new version is available. |
| `Reloadonupdate` | Reload Tox on Update | `toggle` | `True` | No | `me.par.Autoupdate != 'off'` | Reload tox from disk after a successful update. |
| `Devmode` | Dev Mode | `menu` | `off` | No | Always enabled | Developer mode setting. |
| `Onlybumpdirty` | Only Bump When Dirty | `toggle` | `True` | No | Always enabled | Skip the version-bump prompt unless the component is dirty. |
| `Forcebump` | Force Version Bump | `pulse` | — | No | Always enabled | Manually trigger the version bump dialog, bypassing dev-mode and dirty checks. |

### Autoupdate Menu Values

| Value | Label | Behavior |
|-------|-------|----------|
| `off` | Disabled | No automatic updates. |
| `prompt` | Prompt to Update | A confirmation dialog is shown before updating. |
| `always` | Always Update | Updates are applied automatically without prompting. |

### Devmode Menu Values

| Value | Label | Behavior |
|-------|-------|----------|
| `off` | Disabled | No developer features. Updates are checked and applied normally. |
| `auto` | Auto (In Repo) | Developer features activate only when the component is inside its git repository. |
| `always` | Always | Developer features are always active regardless of repository status. |

---

## AcroVersionManager Parameters

These parameters are defined on the `AcroVersionManager` component itself and control the central version management system.

| Name | Type | Description |
|------|------|-------------|
| `Checkonstart` | `toggle` | Check for updates automatically when the project starts. |
| `Startupdelay` | `int` | Delay in frames before the startup version check executes. |
| `Printtotextport` | `toggle` | Print version check results to the textport. |
| `Showpopup` | `toggle` | Show a popup dialog when updates are found. |
| `Automaticupdates` | `toggle` | Enable automatic update functionality for components that support it. |
| `Checkdirtyonsave` | `toggle` | Check for unsaved (dirty) tox-managed components when the project saves. |
| `Callbackdat` | `DAT` | Reference to the callbacks DAT used by the `CallbacksExt` base class. |

### Pulse Parameters

| Name | Action |
|------|--------|
| `Checkall` | Run `CheckAll()` -- scan all versioned components for updates. |
| `Printreport` | Run `PrintReport()` -- print a formatted version status report to the textport. |
| `Clearignored` | Run `ClearIgnored()` -- reset all skipped versions and ignored components. |

---

## AcroCore Parameters

`AcroCore` is the main project extension. It inherits from both `AcroVersionExt` and `CallbacksExt`, so a AcroCore component carries all parameters from both the **Component** page (from `AcroToxExt`) and the **Version** page (from `AcroVersionExt`), plus its own additional parameters.

### Callbacks Page

| Name | Type | Description |
|------|------|-------------|
| `Callbackdat` | `DAT` | Reference to the project callbacks DAT. |
| `Editcallbackdat` | `pulse` | Open the callbacks DAT in the system editor. |
| `Printcallbacks` | `pulse` | Print all registered callbacks to the textport. |

### Additional Pulse Parameters

| Name | Description |
|------|-------------|
| `Editextension` | Open the extension script in the system editor. |
| `Printstartupbanner` | Print the project startup banner to the textport. |
| `Checkforupdates` | Trigger a version check for this component. |

---

## Tag Reference

Tags are applied automatically during extension initialization. They enable runtime discovery of managed components using `root.findChildren(tags=[...])`.

| Tag | Applied By | Purpose |
|-----|------------|---------|
| `tox_managed` | `AcroToxExt.__init__()` | Identifies components with external tox management. |
| `version_tracking` | `AcroVersionExt.__init__()` | Identifies version-tracked components. |

Since `AcroVersionExt` inherits from `AcroToxExt`, every component with the `version_tracking` tag is guaranteed to also have the `tox_managed` tag. The reverse is not true.

```python
# Find all tox-managed components
root.findChildren(tags=['tox_managed'])

# Find all version-tracked components (always a subset of tox_managed)
root.findChildren(tags=['version_tracking'])
```

---

## Version File Format

The version file is a JSON document stored on disk at the path specified by the `Versionfile` parameter. It is created automatically with default values if it does not exist when `AcroVersionExt` initializes.

### Schema

| Field | Type | Description |
|-------|------|-------------|
| `version` | `string` | Semantic version in `Major.Minor.Patch` format. |
| `build` | `integer` | Incremental build number. |
| `last_update` | `string` | ISO 8601 timestamp of the last version update. |
| `td_version` | `string` | TouchDesigner application version identifier. |
| `td_build` | `string` | TouchDesigner build number string. |

### Example

```json
{
  "version": "1.6.1",
  "build": 294,
  "last_update": "2026-02-19T12:53:32.732217",
  "td_version": "099",
  "td_build": "2025.32280"
}
```

---

## Per-Module Environment Variables

Each module ships with a `setup.ps1` (Windows) and `setup.sh` (macOS / Linux) that registers a per-module OS environment variable pointing at the module's installed path. These are accessible inside TD via the standard `var('NAME')` lookup, so extension code, parameter expressions, and external tox paths can reference modules portably regardless of where the module is checked out.

| Variable | Set By | Points To |
|----------|--------|-----------|
| `ACRO_TD_VERSION_MANAGER` | `modules/acro-td-version-manager/setup.{ps1,sh}` | The version-manager module folder. |
| `ACRO_TD_COMPONENT_CREATOR` | `modules/acro-td-component-creator/setup.{ps1,sh}` | The component-creator module folder. |
| `ACRO_TD_HOTKEY_MANAGER` | `modules/acro-td-hotkey-manager/setup.{ps1,sh}` | The hotkey-manager module folder. |
| `ACRO_TD_THEME_MANAGER` | `modules/acro-td-theme-manager/setup.{ps1,sh}` | The theme-manager module folder. |
| `ACRO_TD_MACROS` | `modules/acro-td-macros/setup.{ps1,sh}` | The macros module folder. |
| `ACRO_TD_WIDGETS` | `modules/acro-td-widgets/setup.{ps1,sh}` | The widgets module folder. |
| `ACRO_TD_MCP` | `modules/acro-td-mcp/setup.{ps1,sh}` | The MCP module folder. |

Run each setup script once per machine (or once per workspace if you check out modules into a custom location). On Windows the variables persist via `[System.Environment]::SetEnvironmentVariable(..., 'User')`; on macOS/Linux they go into the user's shell profile.

### Use Cases

| Purpose | Reference |
|---------|-----------|
| `ComponentCreator` callbacks templates | `var('ACRO_TD_COMPONENT_CREATOR')` in `AcroComponentCreator.py` |
| `Macros` callbacks templates | `var('ACRO_TD_MACROS')` in `AcroMacros.py` |
| External tox path for `AcroToxExt` script in generated components | `var('ACRO_TD_VERSION_MANAGER')` in extension expression |
| External tox path for `AcroVersionExt` script in generated components | `var('ACRO_TD_VERSION_MANAGER')` in extension expression |

### Using in Path Parameters

You can reference these variables in TD's external tox path parameter, file references, or any parameter expression. Example expression for an external tox path:

```python
f"{var('ACRO_TD_VERSION_MANAGER')}/scripts/AcroToxExt.py"
```

This pattern is what `AcroComponentCreator` uses when it scaffolds a component with the tox/version mixins — the generated component points back at the master `AcroToxExt.py` / `AcroVersionExt.py` so updates ripple through automatically.

> **Note:** Earlier versions of this template used a single `SOFTWARE` variable (`C:/Software` on Windows, `~/Software` on macOS) set by `AcroCore.setVarSoftwarePath()`. That has been replaced with per-module variables to allow modules to live anywhere on disk and to remove the implicit dependency on the `Software` directory layout. References to `var('SOFTWARE')` in legacy projects still work if the variable is set, but new projects should use the per-module variables.

---

## Default Folder Structure

The following folders are created by `AcroCore.createDefaultFolders()` during project initialization if they do not already exist:

```
project/
  scripts/       Python scripts and extensions
  content/       Project content files
  tox/           External component .tox files
  macros/main/   Macro definitions
  TDLogs/        Log files
```

These folders establish the conventional directory layout expected by the system. The `tox/` folder is the default save location used by `AcroToxExt.GetToxSavePath()` when no explicit `Externaltoxpath` is configured.
