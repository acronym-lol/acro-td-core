# Acro TD Component Creator

Dialog-based component scaffolding tool for TouchDesigner.

## Features

- Create components with extensions, callbacks, and network protocols
- Jinja2-based code generation templates
- Support for AcroToxExt and AcroVersionExt mixins
- Network protocol helpers (OSC, MQTT, TCP, UDP, WebSocket, etc.)

## Usage

```python
# Get default settings
settings = op.COMPCREATOR.DefaultSettings()

# Configure component
settings['Classname'] = 'MyComponent'
settings['Shortcut'] = 'MYCOMP'
settings['Opshortcut'] = True
settings['Path'] = '/components'

# Create the component
op.COMPCREATOR.CreateComponent(settings)
```

Or use the keyboard shortcut **Ctrl+Alt+Shift+N** to open the creation dialog.

## Installation

This module is typically installed as a git subtree in the acro-td-core template.

```bash
git subtree add --prefix=modules/acro-td-component-creator https://github.com/acronym-lol/acro-td-component-creator.git main --squash
```
