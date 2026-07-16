---
name: ship
description: Use when work should go live — commit, push, deploy per recipe, cache-busted live verify, smoke, screenshot. Blocks the "shipped" claim on the live check.
---

# op:ship

The release ritual. Steps run in order; a failing step stops the pipeline and reports.

1. **Preflight**: `git status` — summarize what ships. Run the recipe `test` command when present; failures stop here.
2. **Commit**: follow the repo's own style (`git log --oneline -5` first). Stage files by name.
3. **Push**: gated (confirm) unless co-pilot armed; to an existing upstream only.
4. **Deploy**: recipe `deploy` — always confirm, armed or not (production). Missing key → op:project-recipes discovery; never guess a target.
5. **Live verify** (the blocking step): set `BUST` to the current epoch seconds; run recipe `cache_check` with `$URL` and `$BUST` substituted, or fetch `live_url?v=$BUST` and look for a marker from the just-shipped change (new text, version string, asset hash). Stale → report loudly, offer recipe `rollback` when present, and do not use the word "shipped".
6. **Smoke**: every URL in recipe `smoke` answers 200 — `curl -s -o /dev/null -w "%{http_code}" <url>`.
7. **Screenshot** the live page at a desktop width: Playwright MCP when available, else `npx playwright screenshot --viewport-size=1440,900 "$URL" <scratchpad>/ship-<date>.png`.

Proof at end: live URL, screenshot path, status line.
