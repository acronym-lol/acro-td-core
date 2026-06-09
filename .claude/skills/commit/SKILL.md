---
name: commit
description: Create a git commit with guided best practices
argument-hint: "[message]"
disable-model-invocation: true
---

# Git Commit

Create a well-structured git commit following project conventions.

## Instructions

1. **Check current state** — Run these in parallel:
   ```bash
   git status
   git diff --stat
   git log --oneline -5
   ```

2. **Review changes** — Analyze what's being committed:
   - Summarize the changes (new features, bug fixes, refactors, docs, etc.)
   - Check for any files that shouldn't be committed (.env, credentials, large binaries)
   - Warn if committing unrelated changes that should be separate commits

3. **Stage files** — If there are unstaged changes:
   - Ask user which files to include, or stage all with `git add -A`
   - For partial commits, use `git add <specific files>`

4. **Draft commit message** — Follow these conventions:
   - First line: imperative mood, max 50 chars (e.g., "Add web fallback to td_help")
   - Blank line
   - Body: explain *why* not *what* (the diff shows what)
   - Keep lines under 72 chars
   - Match the style of recent commits in the repo

5. **If user provided a message ($ARGUMENTS)**, use it as the basis but ensure it follows conventions

6. **Create the commit**:
   ```bash
   git commit -m "$(cat <<'EOF'
   Summary line here

   Optional body explaining why this change was made.

   )"
   ```

7. **Verify** — Run `git log --oneline -1` to confirm

## Commit Message Examples

**Good:**
```
Add web fallback to td_help for newer documentation

When offline help lookup fails (e.g., for new POP operators),
fetch from docs.derivative.ca as fallback.
```

**Bad:**
```
Updated help.ts and index.ts files
```

## Safety Rules

- Never commit files containing secrets (.env, credentials, tokens)
- Never use `--force` or `--no-verify` unless explicitly requested
- Never amend commits that have been pushed
- If no changes to commit, inform the user instead of creating empty commit
