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

### Task 1: <name>
- Files: exact paths to create or modify
- Tests: the failing test to write first, named from the spec's Tests section
- Steps: write test → see it fail → implement → see it pass → commit

(one section per task; every spec Behavior maps to a task; every task ends committable)
```

5. Self-check against the spec: every Behavior covered, no placeholders, exact paths. Fix inline.
6. Sign-off gate (arrow-choice): sign off / revise / abandon. On sign-off → `status: signed-off`, commit (`docs: add <slug> plan`), offer /op:build.
7. Re-run: /op:plan on a spec that already has a plan regenerates plan.md fresh (new pin). It never edits the spec.

Proof at end: plan path, pin value, status.
