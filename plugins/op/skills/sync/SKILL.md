---
name: sync
description: Use when localhost should match prod — pulls db, images, feed, data per the recipe sync map. One direction only: prod → local.
---

# op:sync

1. Read recipe `sync` (a map of part → command). Missing → op:project-recipes discovery.
2. Arrow-choice which parts to pull (all preselected).
3. Confirm before overwriting local state — list exactly what gets replaced.
4. Run each part; a failing part reports and the rest continue.
5. Hard stop: this command never pushes local state to prod. That is /op:ship's lane.

Proof at end: per part — what moved, its size (`du -sh`), the local path.
