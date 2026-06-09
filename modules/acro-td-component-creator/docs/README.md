# Acro TD Component Creator

Dialog-based component scaffolding tool for TouchDesigner.

## What it does

`AcroComponentCreator` (`/AcroComponentCreator`, global shortcut `op.ACC`, extension `ext.AcroComponentCreator`) generates fully wired TouchDesigner components from a settings dict — extension code, callbacks system, parameter pages, optional network protocol DATs.

Open the dialog with **Ctrl+Alt+Shift+N** when focused on a Network Editor pane, or call it programmatically.

## Quick start

```python
# Get default settings
settings = op.ACC.DefaultSettings()

# Configure
settings['Classname'] = 'MyComponent'          # required, UpperCamelCase
settings['Shortcut'] = 'MYCOMP'                # required, 2+ uppercase chars
settings['Opshortcut'] = True                  # enable op.MYCOMP global access
settings['Comptype'] = 'base'                  # 'base' or 'container'
settings['Path'] = '/components'               # where to create
settings['Versionext'] = True                  # include AcroVersionExt mixin
settings['Webserver'] = True                   # include Web Server DAT + callbacks

# Create
op.ACC.CreateComponent(settings)
```

This produces:

- A `MyComponent` baseCOMP at `/components/MyComponent`
- A `scripts/MyComponent.py` extension class file (sync-linked)
- A `MyComponent_callbacks` DAT docked to the parent
- Parameter pages: Controls, Settings, Callbacks, plus protocol-specific pages
- A WebServer DAT inside the comp with parameters bound to the parent

## Features

- **Dialog or API** — Ctrl+Alt+Shift+N for interactive use, `CreateComponent(settings)` for programmatic
- **Jinja2 templates** in `scripts/CallbacksTemplates/` for all generated code
- **Mixin support** — toggle `AcroToxExt` or `AcroVersionExt` to include version tracking + tox management
- **Network protocols built-in** — MQTT, OSC In/Out, TCP Client/Server, UDP In/Out, Web Client, Web Server, WebSocket
- **Validation** — class name must match `^[A-Z]+(?:[A-Za-z0-9]+)*$`, shortcut must match `^[A-Z][A-Z0-9_]+$`
- **Two-tier callbacks** — main callback DAT lives outside the comp (docked to parent); protocol callbacks live inside

## Where to go next

- **[API Reference](api)** — Full DefaultSettings keys, dialog parameter list, validation rules, what's generated and where, Jinja2 template inventory.

## Installation

```bash
git subtree add --prefix=modules/acro-td-component-creator https://github.com/acronym-lol/acro-td-component-creator.git main --squash
```

`setup.ps1` / `setup.sh` register `ACRO_TD_COMPONENT_CREATOR` pointing at the module so the extension can locate its Jinja2 templates via `var('ACRO_TD_COMPONENT_CREATOR')`.
