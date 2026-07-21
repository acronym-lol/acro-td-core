---
name: create-macro
description: Create a new Macros macro
argument-hint: "[MacroName] [parent-path]"
---

# Create Macro

Create a new macro in the Macros system.

## Instructions

1. Parse the arguments ($ARGUMENTS):
   - First word: macro name
   - Second word (optional): parent path for nesting (use "" for root)

2. If no name provided, ask the user:
   - Macro name
   - Parent path (leave empty for root level, or specify like "Lighting" for nesting)

3. List existing macros to show context using `td_execute`:
   ```python
   op.AM.ListMacros()
   ```

4. Create the macro using `td_execute`:
   ```python
   op.AM.CreateMacro("MacroName", "parent_path")  # "" for root
   ```

5. Optionally, set initial callback code. Ask the user what the macro should do, then use:
   ```python
   op.AM.SetCallbackCode("path/to/MacroName", '''
   def onInit(info, am, macro):
       # am.Subscribe(macro, 'signal_name')  # subscribe to signals
       return

   def onTrigger(info, am, macro, comps, args):
       # comps is op.comps (component shortcuts)
       # args is whatever was passed to TriggerMacro or Emit
       print("MacroName triggered!")
       return
   ''')
   ```

6. Confirm creation and show the macro path

## Macro Hierarchy

- Root macros: `CreateMacro("MyMacro", "")` → path is "MyMacro"
- Nested macros: `CreateMacro("SubMacro", "Parent")` → path is "Parent/SubMacro"
