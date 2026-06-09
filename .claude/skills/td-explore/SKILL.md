---
name: td-explore
description: Explore the TouchDesigner scene and save a snapshot
argument-hint: "[depth]"
---

# TD Scene Exploration

Explore the current TouchDesigner scene and save a persistent snapshot.

## Instructions

1. First, check if TD is running using `td_health`

2. Get the current pane/network location with `td_pane`

3. Explore the scene structure:
   - Use `td_children` with `path="/"` and `depth=2` to get top-level structure
   - Use `td_children` on `/AcroCore` with `depth=2` to explore the main project
   - Use `td_children` on `/components` with `depth=2` to explore user components

4. Check for any errors with `td_errors`

5. Create a snapshot file at `td-scene-snapshot.md` in the project root with:
   - TD version and build info
   - Current date/time
   - Scene hierarchy (formatted as a tree)
   - List of components with global shortcuts (op.SHORTCUT)
   - Any active errors or warnings
   - Brief summary of what's in the scene

6. Report a summary to the user

If the user provides a depth argument ($ARGUMENTS), use that depth for exploration instead of the default 2.
