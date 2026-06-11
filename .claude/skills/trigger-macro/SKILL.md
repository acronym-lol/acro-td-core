---
name: trigger-macro
description: Trigger a Macros macro
argument-hint: "[macro-path] [args]"
---

# Trigger Macro

Trigger an existing macro in the Macros system.

## Instructions

1. First, list all available macros using `td_execute`:
   ```python
   op.AM.ListMacros()
   ```

2. Display the available macros to the user with their paths and comments

3. If the user provided arguments ($ARGUMENTS):
   - First word/path: macro path to trigger
   - Remaining words: arguments to pass to the macro

   If no arguments provided, ask which macro to trigger.

4. Trigger the macro using `td_execute`:
   ```python
   op.AM.TriggerMacro("macro/path", {"key": "value"})  # or just args as needed
   ```

   If no args needed:
   ```python
   op.AM.TriggerMacro("macro/path")
   ```

5. Confirm the macro was triggered

## Notes

- Macro paths are hierarchical: "Parent/Child/GrandChild"
- Arguments are passed to the `onTrigger` callback as the `args` parameter
- You can also use `op.AM.Emit("signal_name", args)` to broadcast to all macros subscribed to that signal
