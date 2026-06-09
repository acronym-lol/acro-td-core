---
name: create-component
description: Create a new TouchDesigner component using ComponentCreator
argument-hint: "[ComponentName]"
---

# Create Component

Scaffold a new TouchDesigner component using the ComponentCreator API.

## Instructions

1. If the user provided a component name ($ARGUMENTS), use it. Otherwise, ask the user:
   - Component class name (UpperCamelCase, e.g., "MyComponent")
   - Shortcut name (UPPERCASE, e.g., "MYCOMP") — optional, can derive from class name

2. Ask the user about optional features they want enabled:
   - `Opshortcut` — Enable `op.SHORTCUT` global access?
   - `Comptype` — "base" or "container"?
   - Network protocols — MQTT, OSC in/out, TCP client/server, UDP in/out, WebSocket, Web client/server?

3. Find an empty position for the new component using `td_find_empty` with `path="/components"`

4. Create the component via `td_execute`:

```python
s = op.COMPCREATOR.DefaultSettings()
s['Classname'] = 'ComponentName'  # UpperCamelCase
s['Shortcut'] = 'COMPNAME'        # UPPERCASE, 2+ chars
s['Opshortcut'] = True            # if user wants op.SHORTCUT access
s['Comptype'] = 'base'            # or 'container'
s['Path'] = '/components'
s['Posx'] = <x from td_find_empty>
s['Posy'] = <y from td_find_empty>
# Set any network protocol flags as needed
op.COMPCREATOR.CreateComponent(s)
```

5. Confirm creation and tell the user how to access it (e.g., `op.COMPNAME`)

## Validation Rules

- `Classname`: Must match `^[A-Z]+(?:[A-Za-z0-9]+)*$` (UpperCamelCase, digits allowed)
- `Shortcut`: Must match `^[A-Z][A-Z0-9_]+$` (2+ uppercase chars, digits/underscores allowed)
