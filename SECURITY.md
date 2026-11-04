# Security Policy

## Reporting a vulnerability

Please don't open a public issue. Report it privately on this repo's **Security** tab with **Report a vulnerability**, and we'll reply there. The module repos (acro-td-mcp and the rest) take reports too, so use whichever repo the problem is in.

## Supported versions

Fixes go into the latest release on `main`. Older versions don't get patches.

## Scope

Two parts of Acro TD Core accept network requests:

- **AcroMCP** runs any Python it's sent. It only accepts requests from the same machine, with no `Origin` header, carrying the per-session token from the instance registry. A way around any of these checks is a vulnerability.
- **The Macros REST API** is off by default. When on, it requires an API key, refuses other machines unless `Allowremote` is on, and refuses browser origins that aren't listed in `Alloworigins`. A way around the key check is a vulnerability.

A secret that ends up in a saved `.toe`/`.tox` or another committed file is also in scope.

Anything already running as the same user on the same machine can read the instance registry, and the AcroMCP token in it. That's by design, not a vulnerability.
