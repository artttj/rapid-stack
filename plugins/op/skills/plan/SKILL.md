---
name: plan
description: Use when an approved spec needs its build plan — writes docs/specs/<slug>/plan.md pinned to the spec body hash, with a sign-off gate.
---

# op:plan

Think expensive, execute cheap: plan at high effort so the build can run lean.

## Steps

1. Locate the spec: the argument, else the newest `docs/specs/*/spec.md` with `status: approved`. Hard stop if not approved or Open questions is non-empty — route back to /op:spec.
2. Effort check: suggest max for this step (arrow-choice).
3. Compute the spec pin (body = everything after the closing frontmatter `---`):

   `awk 'c==2{print} /^---$/{if(c<2)c++}' docs/specs/<slug>/spec.md | shasum -a 256 | cut -c1-12`

4. Write `docs/specs/<slug>/plan.md`:

```markdown
---
spec: docs/specs/<slug>/spec.md
spec-version: <12-hex pin>
status: draft
---
# <title> — build plan

## Tasks

```
