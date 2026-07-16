---
name: using-op
description: Use when starting any conversation — the op operator rules. Route work through /op:go, quote a repo convention before code, prove every claim, print the git status line after tree changes.
---

# Using op

Personal operator layer for solo project work. Commands: /op:go (front door), /op:spec → /op:plan → /op:build (the gate for features), /op:ship, /op:sync, /op:show, /op:release (daily ops). Deep disciplines come from the superpowers plugin, review and polish from rs; op adds the routing, the gate, the ops verbs, and these rules.

## Non-negotiable rules

- Iron law: before writing any code, quote one real convention from the target repo as `file:line` plus the line itself. No quote, no code. (quote-before-code, github.com/artttj/quote-before-code — 930 graded runs, 0/40 → 40/40 correctness.)
- No "done" without proof from this turn: a command output, a screenshot path, or a live URL. Failing tests are reported as failing. Deep procedure: superpowers:verification-before-completion.
- End-of-turn git status line: after any turn that changed a working tree, the last line of the turn is `python3 "__OP_ROOT__/skills/using-op/lib/status_line.py" <repo>` output. If `__OP_ROOT__` appears unsubstituted, resolve the op install path from `~/.claude/plugins/installed_plugins.json` first.
- Read-only by default. "full co-pilot" arms reversible gated actions for this session: staging, committing, creating the working branch, pushing to an existing upstream. "disarm co-pilot" stands down. Never covered: production deploys, publishes, force-push, deletion, history rewrites — these confirm every time.
- An echoed gate phrase must execute: when the user types a confirmation, run the gated action in the same turn. Repeating the phrase back without acting is a bug.
- Decisions are short arrow-choices, never open questions, whenever the options are enumerable.
- Before a heavy step (spec, plan, deep debug, big build), suggest raising effort (xhigh/max) or an ultracode workflow, then let the user decide.
- Per-project ops live in `.claude/op.json` (see op:project-recipes). Missing key → discover, confirm as arrow-choice, cache. Failing recipe command → rediscover and update. Never guess a deploy target.
- Mirror the user's language (EN/RU). Command names, files, and commits stay English.
- Every op command ends with its proof: what ran, what it produced, where to look.
