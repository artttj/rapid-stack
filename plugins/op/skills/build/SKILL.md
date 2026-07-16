---
name: build
description: Use when executing work — a signed-off plan (gate mode) or a routed small fix (direct mode). TDD, capped review, verification, proof.
---

# op:build

## Preconditions (gate mode)

1. `plan.md` has `status: signed-off`.
2. Recompute the spec pin and compare with the plan's `spec-version`:

   `awk 'c==2{print} /^---$/{if(c<2)c++}' docs/specs/<slug>/spec.md | shasum -a 256 | cut -c1-12`

   Mismatch → hard stop, arrow-choice: re-run /op:plan / proceed anyway (the final report then records "pin overridden").

## Steps

1. Iron law first: quote one real convention (file:line) from the repo before any new code.
2. Branch (arrow-choice): current branch / new `feat/<slug>` / isolated worktree via superpowers:using-git-worktrees.
3. Execute:
   - Plan with ≥3 tasks → superpowers:subagent-driven-development over plan.md.
   - Smaller plan → inline, superpowers:test-driven-development per task.
   - Direct mode (no plan, routed small fix): one TDD cycle — failing test, minimal fix, green.
   - superpowers absent → inline fallback: write the failing test, run it, implement minimally, run to green, commit per task.
4. Review, capped at 3 rounds: dispatch the rs `code-reviewer` agent on the diff (rs absent → a fresh general subagent prompted for high-confidence defects only). Fix what is real, push back with a reason on what is not, stop at the cap.
5. Verify: superpowers:verification-before-completion — run the recipe `test` command (or the repo's test command), read the output, report it as it is.
6. Gate-mode close: set spec `status: implemented`, commit the status flip with the work. Offer /op:ship (arrow-choice).

Proof at end: test output, `git diff --stat`, status line.
