---
name: push-subtrees
description: Push git subtrees to their remote repositories
argument-hint: "[subtree-name]"
disable-model-invocation: true
---

# Push Subtrees

Push all git subtrees to their remote `main` branches, or push a specific subtree.

## Subtree Registry

| Name | Prefix | Remote |
|------|--------|--------|
| acro-td-component-creator | modules/acro-td-component-creator | acro-td-component-creator |
| acro-td-hotkey-manager | modules/acro-td-hotkey-manager | acro-td-hotkey-manager |
| acro-td-mcp | modules/acro-td-mcp | acro-td-mcp |
| acro-td-version-manager | modules/acro-td-version-manager | acro-td-version-manager |
| acro-td-macros | modules/acro-td-macros | acro-td-macros |
| acro-td-widgets | modules/acro-td-widgets | acro-td-widgets |
| acro-td-theme-manager | modules/acro-td-theme-manager | acro-td-theme-manager |

## Instructions

1. **If argument provided ($ARGUMENTS)** — push only that subtree:
   ```bash
   git subtree push --prefix=modules/$ARGUMENTS $ARGUMENTS main
   ```
   Validate the argument matches a known subtree name first.

2. **If no argument** — push all subtrees sequentially:
   ```bash
   git subtree push --prefix=modules/acro-td-component-creator acro-td-component-creator main
   git subtree push --prefix=modules/acro-td-hotkey-manager acro-td-hotkey-manager main
   git subtree push --prefix=modules/acro-td-mcp acro-td-mcp main
   git subtree push --prefix=modules/acro-td-version-manager acro-td-version-manager main
   git subtree push --prefix=modules/acro-td-macros acro-td-macros main
   git subtree push --prefix=modules/acro-td-widgets acro-td-widgets main
   git subtree push --prefix=modules/acro-td-theme-manager acro-td-theme-manager main
   ```

3. **Report results** — For each subtree, report:
   - Success: "acro-td-mcp: pushed to main" or "acro-td-mcp: up-to-date"
   - Failure: "acro-td-mcp: FAILED - [error message]"

4. **Use extended timeout** — Subtree pushes can take 30+ seconds. Use `timeout: 300000` (5 minutes) for each push.

## Notes

- Subtree push computes commit history, which can be slow on large repos
- "Everything up-to-date" means no new commits to push
- New branches will show "Create a pull request" message from GitHub
