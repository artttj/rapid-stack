---
name: spec
description: Use when a feature needs its spec — short clarifying Q&A, then docs/specs/<slug>/spec.md with a one-keypress self-approval gate.
---

# op:spec

Turn a feature ask into an approved spec. Write for your future executor: behavior and tests, not prose.

## Steps

1. Effort check: for a non-trivial feature, suggest raising to xhigh/max (arrow-choice), continue on answer.
2. Clarify with at most 3 arrow-choice questions (purpose, constraints, success criteria). Skip what the ask already answers. For a genuinely unshaped problem use superpowers:brainstorming first; otherwise stay lean.
3. Derive `<slug>`: kebab-case, 2–4 words, from the feature title.
4. Write `docs/specs/<slug>/spec.md` in the target repo:

```markdown
---
status: draft
---
# <title>

## Goal
One paragraph: what exists after this ships, and why.

## Behavior
One bullet per observable behavior. Edge cases included.

## Architecture
Files to touch, data flow, integration points. Quote one real repo convention (file:line) this will follow.

## Tests
The named tests that prove Behavior.

## Out of scope
What this deliberately does not do.

## Open questions
Empty when approved.
```

5. Present the spec, then the gate (arrow-choice): approve / edit / discard.
   - approve → set `status: approved`, add `approved: <YYYY-MM-DD>`, commit (`docs: add <slug> spec`), offer /op:plan as the next arrow-choice.
   - edit → apply, re-present.
6. Hard stop: no plan and no code for this feature until `status: approved` and Open questions is empty.

Proof at end: the spec path and its frontmatter status.
