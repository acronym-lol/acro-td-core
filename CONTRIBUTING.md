# Contributing to Acro TD Core

Thanks for helping. This page covers where changes go and what a pull request needs.

## Where things live

acro-td-core holds the template and its seven modules. Each module lives in `modules/<module>/` and is also published to its own repo (acro-td-mcp, acro-td-macros and so on) with `git subtree push`. Those module repos are copies that maintainers update from here.

- **Pull requests go to acro-td-core,** even for module code. Edit the files under `modules/<module>/`. A pull request opened on a module repo can't be merged there.
- **Issues** are welcome here or in the module's own repo. Search both first.

## Branches

- **`dev`** is where work happens. Branch off `dev` and open your pull request against `dev`.
- **`main`** is the released version. Projects check for updates against it and the docs sites publish from it, so it only changes through a release pull request from `dev`.

GitHub suggests `main` as the base when you open a pull request, because it's the default branch. Change the base to `dev`.

## Link an issue

If there's an issue for your change, link it in the pull request description with `Closes #123`, or `Closes acronym-lol/acro-td-mcp#12` for an issue in a module repo. For anything bigger than a small fix, open an issue first so we can agree on the approach before you build it.

## Making the change

- **Setup:** follow [Getting Started](https://acronym-lol.github.io/acro-td-core/#/getting-started), using the TouchDesigner build listed as `td_build` in `AcroCore-VERSION.json`.
- **Python first:** extensions are `.py` files synced into the scene (`scripts/`, `modules/*/scripts/`), so prefer changing those. `.toe` and `.tox` files are binary and can't be merged. Keep scene changes small and describe them in the pull request.
- **Conventions:** public extension methods and properties are UpperCamelCase, private ones `_camelCase`. Use `debug()` instead of `print()`, and don't create operators in an extension's `__init__`. More in [CLAUDE.md](CLAUDE.md#code-conventions).
- **Docs:** when behavior changes, update the page under `docs/` or `modules/<module>/docs/`. Don't edit `_sidebar.md` files; a workflow regenerates them.
- **MCP server:** after changing `modules/acro-td-mcp/src/`, run `npm install && npm run build` at the repo root and commit `modules/acro-td-mcp/dist/`. CI fails if the bundle doesn't match the source.
- **No secrets in parameters:** TouchDesigner saves parameter values into the `.toe`/`.tox`. Keys and tokens come from environment variables (the `Apikeyenv` and `Tokenenv` parameters name them), and `.env` files are git-ignored.
- **Versions:** don't bump version numbers or edit the changelogs. Maintainers do that when releasing.

## Review

A maintainer reviews every pull request. CI runs on pull requests from forks once a maintainer approves it.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
