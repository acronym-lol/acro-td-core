---
name: list-macros
description: List all Macros macros
---

# List Macros

Display all macros in the Macros system.

## Instructions

1. Fetch all macros using `td_execute`:
   ```python
   op.MC.ListMacros()
   ```

2. Format the output as a clear list showing:
   - Macro path (hierarchical)
   - Comment/description (if set)
   - Any signal subscriptions

3. Optionally, fetch the signal routing table:
   ```python
   op.MC.GetSignals()
   ```

4. Display a summary showing:
   - Total number of macros
   - Macro hierarchy (as a tree if nested)
   - Active signals and their subscribers

## Example Output

```
Macros (5 total):
├── Lighting
│   ├── DimAll — Dims all lights to specified level
│   ├── Blackout — Instant blackout
│   └── Restore — Restore previous state
├── Audio
│   └── FadeOut — Fade audio to silence
└── System
    └── EmergencyStop — Stop all outputs

Signals:
  panic → [Lighting/Blackout, Audio/FadeOut, System/EmergencyStop]
  show_start → [Lighting/Restore]
```
