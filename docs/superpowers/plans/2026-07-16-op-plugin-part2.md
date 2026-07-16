# op Plugin Implementation Plan (part 2 of 2)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or superpowers:executing-plans. Part 1 (`2026-07-16-op-plugin.md`) holds the Global Constraints — they apply to every task here. Command files follow the rs alias pattern: frontmatter `description`, short body, `$ARGUMENTS` last.

---

### Task 6: /op:spec

**Files:**
- Create: `plugins/op/commands/spec.md`
- Create: `plugins/op/skills/spec/SKILL.md`

**Interfaces:**
- Produces: `docs/specs/<slug>/spec.md` with frontmatter `status: draft|approved|implemented` and `approved: <date>`. Tasks 7 and 8 read `status` and hash the body.

- [ ] **Step 1: Write `plugins/op/commands/spec.md`**

```markdown
---
description: Write a feature spec with a self-approval gate via the op:spec skill
---

Use the `op:spec` skill on the request below. Short clarifying arrow-choices, then `docs/specs/<slug>/spec.md`, then the approval gate. No code until approved.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/spec/SKILL.md`**

````markdown
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
````

- [ ] **Step 3: Verify sizes**

Run: `wc -l plugins/op/commands/spec.md plugins/op/skills/spec/SKILL.md`
Expected: command ≤ 10, skill ≤ 55.

- [ ] **Step 4: Commit**

```bash
git add plugins/op/commands/spec.md plugins/op/skills/spec/SKILL.md
git commit -m "feat: add /op:spec command and skill"
```

---

### Task 7: /op:plan

**Files:**
- Create: `plugins/op/commands/plan.md`
- Create: `plugins/op/skills/plan/SKILL.md`

**Interfaces:**
- Consumes: Task 6's spec file and `status: approved`.
- Produces: `docs/specs/<slug>/plan.md` with frontmatter `spec`, `spec-version` (12-hex pin), `status: draft|signed-off`. Task 8 recomputes the pin with the identical command.

- [ ] **Step 1: Write `plugins/op/commands/plan.md`**

```markdown
---
description: Turn an approved spec into a hash-pinned build plan via the op:plan skill
---

Use the `op:plan` skill on the request below (or the newest approved spec when no argument). Suggest max effort before planning. Sign-off gate before any build.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/plan/SKILL.md`**

````markdown
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
````

- [ ] **Step 3: Test the pin command on a fixture**

```bash
mkdir -p /tmp/op-pin-test && printf -- '---\nstatus: approved\n---\n# T\n\nbody line\n' > /tmp/op-pin-test/spec.md
A=$(awk 'c==2{print} /^---$/{if(c<2)c++}' /tmp/op-pin-test/spec.md | shasum -a 256 | cut -c1-12)
B=$(awk 'c==2{print} /^---$/{if(c<2)c++}' /tmp/op-pin-test/spec.md | shasum -a 256 | cut -c1-12)
printf -- '---\nstatus: implemented\n---\n# T\n\nbody line\n' > /tmp/op-pin-test/spec2.md
C=$(awk 'c==2{print} /^---$/{if(c<2)c++}' /tmp/op-pin-test/spec2.md | shasum -a 256 | cut -c1-12)
printf -- '---\nstatus: approved\n---\n# T\n\nchanged body\n' > /tmp/op-pin-test/spec3.md
D=$(awk 'c==2{print} /^---$/{if(c<2)c++}' /tmp/op-pin-test/spec3.md | shasum -a 256 | cut -c1-12)
[ "$A" = "$B" ] && [ "$A" = "$C" ] && [ "$A" != "$D" ] && echo PIN-OK
```

Run the block above.
Expected: `PIN-OK` (stable across runs, frontmatter-insensitive, body-sensitive).

- [ ] **Step 4: Commit**

```bash
git add plugins/op/commands/plan.md plugins/op/skills/plan/SKILL.md
git commit -m "feat: add /op:plan command and skill"
```

---

### Task 8: /op:build

**Files:**
- Create: `plugins/op/commands/build.md`
- Create: `plugins/op/skills/build/SKILL.md`

**Interfaces:**
- Consumes: Task 7's plan frontmatter (`status: signed-off`, `spec-version`), the pin command verbatim, recipe key `test` (Task 5).
- Produces: sets spec `status: implemented` on gate-mode completion.

- [ ] **Step 1: Write `plugins/op/commands/build.md`**

```markdown
---
description: Execute a signed-off plan or a small fix via the op:build skill
---

Use the `op:build` skill on the request below. Gate mode needs a signed-off plan with a matching spec pin; direct mode is for routed small fixes. TDD, capped review, verification, proof.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/build/SKILL.md`**

````markdown
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
````

- [ ] **Step 3: Verify sizes**

Run: `wc -l plugins/op/commands/build.md plugins/op/skills/build/SKILL.md`
Expected: command ≤ 10, skill ≤ 55.

- [ ] **Step 4: Commit**

```bash
git add plugins/op/commands/build.md plugins/op/skills/build/SKILL.md
git commit -m "feat: add /op:build command and skill"
```

---

### Task 9: /op:go

**Files:**
- Create: `plugins/op/commands/go.md`
- Create: `plugins/op/skills/go/SKILL.md`

**Interfaces:**
- Consumes: `op:spec` (Task 6), `op:build` direct mode (Task 8), `superpowers:systematic-debugging`.

- [ ] **Step 1: Write `plugins/op/commands/go.md`**

```markdown
---
description: Front door — classify the ask (bug / small fix / feature) and route it
---

Use the `op:go` skill on the request below. Classify, confirm the route as an arrow-choice, hand off. Do not start building here.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/go/SKILL.md`**

````markdown
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
````

- [ ] **Step 3: Verify sizes**

Run: `wc -l plugins/op/commands/go.md plugins/op/skills/go/SKILL.md`
Expected: command ≤ 10, skill ≤ 45.

- [ ] **Step 4: Commit**

```bash
git add plugins/op/commands/go.md plugins/op/skills/go/SKILL.md
git commit -m "feat: add /op:go front-door command and skill"
```

---

### Task 10: /op:ship

**Files:**
- Create: `plugins/op/commands/ship.md`
- Create: `plugins/op/skills/ship/SKILL.md`

**Interfaces:**
- Consumes: recipe keys `test`, `deploy`, `live_url`, `cache_check`, `smoke`, `rollback` (Task 5, exact names); co-pilot arming rules (Task 3).

- [ ] **Step 1: Write `plugins/op/commands/ship.md`**

```markdown
---
description: Commit, deploy, and verify live via the op:ship skill
---

Use the `op:ship` skill on the request below. Run the pipeline in order and stop loudly on the live cache check — never claim shipped without it.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/ship/SKILL.md`**

````markdown
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
7. **Screenshot** the live page: Playwright MCP when available, else `npx playwright screenshot --viewport-size=1512,982 "$URL" <scratchpad>/ship-<date>.png`.

Proof at end: live URL, screenshot path, status line.
````

- [ ] **Step 3: Verify sizes**

Run: `wc -l plugins/op/commands/ship.md plugins/op/skills/ship/SKILL.md`
Expected: command ≤ 10, skill ≤ 40.

- [ ] **Step 4: Commit**

```bash
git add plugins/op/commands/ship.md plugins/op/skills/ship/SKILL.md
git commit -m "feat: add /op:ship command and skill"
```

---

### Task 11: /op:sync and /op:show

**Files:**
- Create: `plugins/op/commands/sync.md`, `plugins/op/commands/show.md`
- Create: `plugins/op/skills/sync/SKILL.md`, `plugins/op/skills/show/SKILL.md`

**Interfaces:**
- Consumes: recipe keys `sync`, `serve` (Task 5).

- [ ] **Step 1: Write `plugins/op/commands/sync.md`**

```markdown
---
description: Pull prod state (db, images, feed) to localhost via the op:sync skill
---

Use the `op:sync` skill on the request below. Prod to local only. Confirm before overwriting local state.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/sync/SKILL.md`**

````markdown
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
````

- [ ] **Step 3: Write `plugins/op/commands/show.md`**

```markdown
---
description: Serve locally and screenshot at 14-inch and mobile viewports via the op:show skill
---

Use the `op:show` skill on the request below. Screenshots first, then a short verdict. Offer /rs:vibe for the full scorecard.

$ARGUMENTS
```

- [ ] **Step 4: Write `plugins/op/skills/show/SKILL.md`**

````markdown
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
````

- [ ] **Step 5: Verify sizes**

Run: `wc -l plugins/op/commands/sync.md plugins/op/skills/sync/SKILL.md plugins/op/commands/show.md plugins/op/skills/show/SKILL.md`
Expected: commands ≤ 10 each, skills ≤ 35 each.

- [ ] **Step 6: Commit**

```bash
git add plugins/op/commands/sync.md plugins/op/skills/sync/SKILL.md plugins/op/commands/show.md plugins/op/skills/show/SKILL.md
git commit -m "feat: add /op:sync and /op:show commands and skills"
```

---

### Task 12: /op:release + validate script

**Files:**
- Create: `plugins/op/commands/release.md`
- Create: `plugins/op/skills/release/SKILL.md`
- Create: `plugins/op/scripts/validate.sh`

**Interfaces:**
- Consumes: recipe key `release` = `{versions, publish, verify}` (Task 5).

- [ ] **Step 1: Write `plugins/op/commands/release.md`**

```markdown
---
description: Bump, tag, publish, and verify a release via the op:release skill
---

Use the `op:release` skill on the request below. Confirm before tag and publish. Verify the published artifact before claiming released.

$ARGUMENTS
```

- [ ] **Step 2: Write `plugins/op/skills/release/SKILL.md`**

````markdown
---
name: release
description: Use when publishing a version — bump version files, write humanized notes, tag, publish per recipe, verify the published artifact.
---

# op:release

1. Read recipe `release` (`{versions, publish, verify}`). Missing → op:project-recipes discovery.
2. Preflight: clean tree (or arrow-choice to commit first); tests green when recipe `test` exists.
3. Version (arrow-choice): patch / minor / major, computed from the first file in `versions`. Bump every listed file in step; show the diff.
4. Notes: draft from `git log` since the last tag — a lead paragraph, then Added / Changed / Fixed. Offer /rs:hum on the text (skip silently when rs is absent).
5. Commit `chore: release v<version>`, then tag `v<version>` — confirm before tagging.
6. Publish: recipe `publish` — always confirm (irreversible). npm 2FA happens in the user's terminal; say so and wait.
7. Verify: fetch the recipe `verify` URL and confirm the new version string appears. Not there yet → wait 60s, retry twice, report honestly either way.

Proof at end: version, tag, the verify URL with the version visible.
````

- [ ] **Step 3: Write `plugins/op/scripts/validate.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
for c in commands/*.md; do
  grep -q '^description:' "$c" || { echo "missing description: $c"; fail=1; }
  name=$(basename "$c" .md)
  [ -f "skills/$name/SKILL.md" ] || { echo "missing skill for: $c"; fail=1; }
done
[ -f skills/using-op/SKILL.md ] || { echo "missing using-op skill"; fail=1; }
[ -f skills/project-recipes/SKILL.md ] || { echo "missing project-recipes skill"; fail=1; }
python3 -m json.tool < .claude-plugin/plugin.json > /dev/null || { echo "bad plugin.json"; fail=1; }
python3 -m json.tool < hooks/hooks.json > /dev/null || { echo "bad hooks.json"; fail=1; }
[ "$fail" -eq 0 ] && echo "op validate: OK"
exit "$fail"
```

- [ ] **Step 4: Run the validator and the test suite**

Run: `chmod +x plugins/op/scripts/validate.sh && plugins/op/scripts/validate.sh`
Expected: `op validate: OK`

Run: `cd plugins/op/skills/using-op/lib && python3 -m pytest -q`
Expected: `6 passed`

- [ ] **Step 5: Commit**

```bash
git add plugins/op/commands/release.md plugins/op/skills/release/SKILL.md plugins/op/scripts/validate.sh
git commit -m "feat: add /op:release and the op validate script"
```

---

### Task 13: README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add the op install line**

In the `## Install` section, after the `/plugin install rs@rapid-stack` line, add:

```
/plugin install op@rapid-stack
```

- [ ] **Step 2: Add the op section**

Insert before `## Want them without the /rs: prefix?`:

```markdown
## op — the operator layer

Second plugin in this marketplace. Where rs gives you single-shot aliases, op runs the whole loop: route, spec, plan, build, ship — with proof at the end of every command.

| Command | What it does |
|---|---|
| `/op:go` | Front door. Classifies the ask — bug, small fix, or feature — confirms the route, hands off. |
| `/op:spec` | Feature spec in `docs/specs/<slug>/spec.md`. You approve it with one keypress. |
| `/op:plan` | Build plan pinned to the approved spec by content hash. Think expensive, execute cheap. |
| `/op:build` | Executes the plan: TDD, subagents for big plans, capped code review, verification. |
| `/op:ship` | Commit, push, deploy, cache-busted live check, smoke test, screenshot. |
| `/op:sync` | Pull prod state (db, images, feed) to localhost per the project recipe. |
| `/op:show` | Serve locally, screenshot at 14-inch MacBook and mobile viewports, verdict. |
| `/op:release` | Bump, notes, tag, publish, verify the published artifact. |

op reads per-project ops from `.claude/op.json` — the first run discovers your serve/deploy/sync commands and writes the file. Deep disciplines come from `superpowers`, review and polish from `rs`. Both optional: every wrapper degrades to a short inline fallback.
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: document the op plugin in the README"
```

---

### Task 14: rapid-stack hygiene (four separate commits)

**Files:**
- Modify: `LICENSE`, `plugins/rs/commands/ui.md`, `README.md`, `.claude-plugin/marketplace.json`
- Create: `.gitignore`

- [ ] **Step 1: LICENSE name.** Replace `artttj` in the copyright line with `Artem Iagovdik`. Commit: `git add LICENSE && git commit -m "chore: use real author name in LICENSE"`

- [ ] **Step 2: .gitignore.** Create `.gitignore` containing one line `.DS_Store`. Commit: `git add .gitignore && git commit -m "chore: ignore .DS_Store"`

- [ ] **Step 3: /ui skill reference.** `plugins/rs/commands/ui.md` tells the agent to use the `design` skill "(from the `ui-ux-pro-max` plugin)" — but the external plugin's skill is named `ui-ux-pro-max`, and rs bundles its own `design` skill (used by `/polish`), so the reference resolves to the wrong skill. Read the file, then replace the skill reference sentence so it opens: ``Use the `ui-ux-pro-max` skill on the request below.`` — dropping the parenthetical, leaving the rest of the body and frontmatter unchanged. Commit: `git add plugins/rs/commands/ui.md && git commit -m "fix: point /ui at the ui-ux-pro-max skill, not the bundled design skill"`

- [ ] **Step 4: vibe dimension count.** The skill defines 8 dimensions; README and marketplace say nine/9. Align the marketing on the skill: in `README.md` change `UI scorecard, nine dimensions.` to `UI scorecard, eight dimensions plus an AI-sameness screen.`; in `.claude-plugin/marketplace.json` change `audits UI quality across 9 dimensions and catches AI sameness` to `audits UI quality across eight dimensions and catches AI sameness`. Commit: `git add README.md .claude-plugin/marketplace.json && git commit -m "fix: reconcile vibe dimension count with the skill"`

---

### Task 15: Install verification and pilot (interactive)

This task needs the user present — it reloads plugins and touches a real project. No autonomous deploys.

- [ ] **Step 1: Full local check**

Run: `plugins/op/scripts/validate.sh && cd plugins/op/skills/using-op/lib && python3 -m pytest -q && cd - && plugins/op/hooks/session-start | python3 -m json.tool > /dev/null && echo ALL-OK`
Expected: `op validate: OK`, `6 passed`, `ALL-OK`.

- [ ] **Step 2: User installs and reloads.** Ask the user to run `/plugin install op@rapid-stack` (or re-add the local marketplace) and `/reload-plugins`, then confirm `/op:go` … `/op:release` autocomplete and a fresh session shows the `<op-rules>` injection.

- [ ] **Step 3: Pilot /op:show on artttj.de.** In `/var/www/artttj.de`, run `/op:show`. Expect: recipe discovery writes `.claude/op.json` (serve key), screenshots at both viewports, a verdict. Fix what the pilot surfaces before proceeding.

- [ ] **Step 4: Pilot /op:ship on artttj.de (user-gated).** With a trivial change staged, run `/op:ship`. The deploy and push steps must each ask for confirmation; the live verify must fetch with a cache-buster. This is a real deploy — only with the user's explicit go.

- [ ] **Step 5: Finish the branch.** Offer superpowers:finishing-a-development-branch: merge `feat/op-plugin` to `master` via PR per the house rules, no force-push, no tags yet — the `v1.4.0` tag lands later via `/op:release` as the dogfood run.
