---
name: release
description: Use when publishing a version — bump version files, write humanized notes, tag, publish per recipe, verify the published artifact.
---

# op:release

1. Read recipe `release` (`{versions, publish, verify}`). Missing → op:project-recipes discovery.
2. Preflight: clean tree (or arrow-choice to commit first); tests green when recipe `test` exists.
3. Version (arrow-choice): patch / minor / major, computed from the first file in `versions`. Bump every listed file in step; show the diff.
4. Notes: draft from `git log` since the last tag — a lead paragraph, then Added / Changed / Fixed. Offer /rs:hum on the text (skip silently when rs is absent).
5. Commit `chore: release v<version>`, then tag `v<version>` — confirm before tagging.
6. Publish: recipe `publish` — always confirm (irreversible). npm 2FA happens in the user's terminal; say so and wait.
7. Verify: fetch the recipe `verify` URL and confirm the new version string appears. Not there yet → wait 60s, retry twice, report honestly either way.

Proof at end: version, tag, the verify URL with the version visible.
