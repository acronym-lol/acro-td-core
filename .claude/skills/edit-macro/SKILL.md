---
name: edit-macro
description: View and edit a macro's callback code
argument-hint: "[macro-path]"
---

# Edit Macro

View and edit the callback code for a Macros macro.

## Instructions

1. First, list all available macros using `td_execute`:
   ```python
   op.AM.ListMacros()
   ```

2. Display the available macros to the user

3. If the user provided a macro path ($ARGUMENTS), use it. Otherwise, ask which macro to edit.

4. Fetch the current callback code using `td_execute`:
   ```python
   op.AM.GetCallbackCode("macro/path")
   ```

5. Display the current code to the user, formatted nicely

6. Ask what changes the user wants to make

7. Edit the code as requested

8. Save the updated code using `td_execute`:
   ```python
   op.AM.SetCallbackCode("macro/path", '''
   def onInit(info, am, macro):
       # initialization code
       return

   def onTrigger(info, am, macro, comps, args):
       # trigger code
       return
   ''')
   ```

9. Confirm the changes were saved (SetCallbackCode writes to both DAT and disk)

## Callback Template

```python
def onInit(info, am, macro):
    # Called when macro initializes
    # am.Subscribe(macro, 'signal_name')  # subscribe to signals here
    return

def onTrigger(info, am, macro, comps, args):
    # Called when macro is triggered or receives a subscribed signal
    # comps = op.comps (component shortcuts)
    # args = data passed to TriggerMacro or Emit
    return
```

## Tips

- Use `comps.SHORTCUT` to access components with global shortcuts
- Subscribe to signals in `onInit` with `am.Subscribe(macro, 'signal_name')`
- Emit signals with `am.Emit('signal_name', args)` from any macro
