---
name: show
description: Use when a change needs visual proof — serve locally per recipe, screenshot at 14-inch MacBook and mobile viewports, short verdict.
---

# op:show

1. Serve: recipe `serve` in the background; wait until `curl -s localhost:<port>` answers (10 tries, 1s apart). Already running → reuse it.
2. Screenshot: 1512×982 (14" MacBook) and 375×812 (mobile); 768×1024 as an arrow-choice extra. Both color schemes when the site has them (emulate prefers-color-scheme). Playwright MCP when available, else `npx playwright screenshot`.
3. Look at every screenshot before writing a word. Verdict ≤5 bullets: hierarchy, spacing, overflow, contrast, anything broken at either viewport.
4. Offer /rs:vibe for the full scorecard (arrow-choice; skip silently when rs is absent).
5. Stop the server if this command started it.

Proof at end: the screenshot paths, listed.
