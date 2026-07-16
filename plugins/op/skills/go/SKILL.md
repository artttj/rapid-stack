---
name: go
description: Use when any work ask arrives — classifies it (bug / small fix / feature), confirms the route, and hands off to debugging, direct build, or the spec gate.
---

# op:go

The front door. Classify, confirm, hand off — nothing is built here.

## Classify

- **bug**: existing behavior broken — an error, a wrong output, or a repro exists.
- **small fix**: single surface, no new interface, roughly ≤2 files.
- **feature**: new behavior or surface, or a multi-file change.

Ambiguous → resolve with an arrow-choice, not open text.

## Confirm

Present the route as an arrow-choice before acting — `bug → debug / small fix → direct build / feature → spec gate` — with the classification first. One keypress fixes a misroute.

## Route

- bug → superpowers:systematic-debugging (absent → fallback: reproduce first, hypothesize from evidence, change one variable at a time, report root cause). Circling checkpoint: 3 disproven hypotheses or 20 minutes without new evidence → stop, restate what is known, fan out fresh-eyes subagents.
- small fix → op:build direct mode.
- feature → op:spec, which chains into op:plan and op:build, each behind its own gate.

Before a heavy route (feature gate, deep debug), suggest raising effort (xhigh/max) or an ultracode workflow; the user decides.

Proof at end: one line — the route taken and the first artifact produced (repro, test, or spec path).
