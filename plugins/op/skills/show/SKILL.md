---
name: show
description: Use when a change needs visual proof — serve locally per recipe, screenshot the standard responsive breakpoints (mobile, tablet, desktop), short verdict.
---

# op:show

1. Serve: recipe `serve` in the background; wait until `curl -s localhost:<port>` answers (10 tries, 1s apart). Already running → reuse it.
2. Screenshot the standard breakpoints: 375×812 (mobile), 768×1024 (tablet), 1440×900 (desktop). Offer 320, 1920, and 1512×982 (14" MacBook) as arrow-choice extras, or take whatever widths the request names. Both color schemes when the site has them (emulate prefers-color-scheme). Playwright MCP when available, else `npx playwright screenshot`.
3. Look at every screenshot before writing a word. Verdict ≤5 bullets: hierarchy, spacing, overflow, contrast, anything broken at any viewport.
4. Offer /rs:vibe for the full scorecard (arrow-choice; skip silently when rs is absent).
5. Stop the server if this command started it.

Proof at end: the screenshot paths, listed.
