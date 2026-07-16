# op — personal operator plugin

- Date: 2026-07-16
- Author: Artem Iagovdik <artyom.yagovdik@gmail.com>
- License: MIT
- Home: `rapid-stack/plugins/op/` (second plugin in the existing marketplace)
- Status: design approved in session; implementation plan pending

## Goal

Carry the operator disciplines of y1-superpowers into personal project work, without the agency machinery. No Jira, no Bitbucket, no offers, no timesheets, no bilingual output, no company branding. One plugin, eight commands, one always-on constitution, per-project recipes. Target weight ~1,500–2,000 lines including tests (y1-superpowers is ~10,000+).

## Evidence base

Built from three analyses run on 2026-07-16: a distillation of y1-superpowers 1.17.0, an audit of rapid-stack 1.3.0, and a mining pass over 504 Claude Code sessions (600 real user messages) across sonto-news, sonto-space, ktulu, file-viewer, druck, artttj-de, cthulhu, llama-cthulhu, y1-radar.

What the sessions show:

- Two working modes: autonomous build (spec → subagent execution → per-file review → commit → push live) and an iterative design loop (build → "show me locally" → art-director feedback → deploy → live check).
- Recurring typed rituals: "yes commit sync repo push live to ssh wolton do smoke test", "pull db, images, data, feed from ssh wolton to localhost", "show me locally", design-polish passes, npm/marketplace releases.
- Top recurring pain: stale content after deploy (cache). Second: renders breaking on the 14" MacBook viewport and mobile.
- The spec gate must scale down: "i dont need plans though, all fixes implement, code review, visual check and deploy live" — while big builds demonstrably run the full gate (cthulhu: zero typed messages mid-build).

## Shape

**Wrap, don't vendor.** y1-superpowers forks superpowers because an agency pins its own copy. Here superpowers and rs are already installed, so op only adds what exists nowhere else:

- the router and the gate trio (spec/plan/build)
- the ops verbs (ship/sync/show/release)
- the constitution skill, injected by a SessionStart hook
- `lib/status_line.py` (git status line with `gh` PR lookup)

Deep disciplines are called by name from superpowers (brainstorming, systematic-debugging, test-driven-development, subagent-driven-development, writing-plans, verification-before-completion), each with a short inline fallback — the same pattern rs `/dbg` uses. Review and polish delegate to rs (`/cr`, `/trim`, `/vibe`, `/hum`).

Layout:

```
plugins/op/
├── .claude-plugin/plugin.json      name op, author Artem Iagovdik
│                                   <artyom.yagovdik@gmail.com>, MIT,
│                                   version 1.0.0 at first release
├── commands/                       go, spec, plan, build, ship, sync,
│                                   show, release (thin entrypoints)
├── skills/
│   ├── using-op/                   constitution, injected at session start
│   │   └── lib/status_line.py      + pytest tests
│   ├── one skill per command/      orchestrators, delegate weight outward
│   └── project-recipes/            discovery + .claude/op.json access
└── hooks/
    ├── hooks.json                  SessionStart → inject using-op
    └── session-start               de-branded port of the y1 49-line hook
```

marketplace.json gains a second `plugins[]` entry. rs stays untouched in behavior.

## Commands

Every command is a thin entrypoint to a skill. Every command ends with proof — command output, screenshot, or live URL — plus the git status line whenever the tree changed.

### /op:go — front door

Classifies the ask and confirms the route as an arrow-choice (a misjudgment costs one keypress):

- **bug** (existing behavior broken, error output in hand) → superpowers systematic-debugging, with the circling checkpoint (3 disproven hypotheses or 20 min without new evidence → stop, restate, fan out)
- **small fix** (single surface, no new interface, roughly ≤2 files) → direct build: implement + review + verify, no docs
- **feature** (new behavior, new surface, multi-file) → the gate: spec → plan → build

Before heavy steps it suggests raising effort (xhigh/max or ultracode) and lets the user decide. All other commands remain directly callable; the router is convenience, not a wall.

### /op:spec

Short clarifying Q&A (arrow-choices preferred) → writes `docs/specs/<slug>/spec.md` in the target repo:

```
---
status: draft | approved | implemented
approved: <date, when approved>
---
# <title>
## Goal
## Behavior
## Architecture
## Tests
## Out of scope
## Open questions
```

Self-approval is one keypress (the user is the PO). On approval, offers to chain into /op:plan.

### /op:plan

Runs on the strong model ("think expensive, execute cheap"). Writes `docs/specs/<slug>/plan.md` with frontmatter pinning:

```
---
spec: docs/specs/<slug>/spec.md
spec-version: <sha256 of spec body, first 12 hex>
status: draft | signed-off
---
```

Ordered tasks with file paths and test expectations. Sign-off gate is an arrow-choice. Re-runnable: regenerating the plan never touches the spec.

### /op:build

Preconditions when a plan exists: `status: signed-off` and spec-version hash matches the current spec body; mismatch blocks with an arrow-choice (re-plan or consciously proceed). Then: branch/worktree choice → execution (subagent-driven for multi-task plans, inline TDD otherwise) → agent code review (rs `/cr` when present, generic review subagent otherwise; capped at 3 rounds) → verification-before-completion → diff stat + test output as proof. Direct mode (routed small fixes) skips docs but keeps review + verify.

### /op:ship

The one-line ritual, hardened into a pipeline with the cache pain solved as a blocking step:

1. preflight: tree state, tests if the recipe defines them
2. commit (repo commit conventions; nothing auto-pushed unarmed)
3. push (gated unless co-pilot armed)
4. deploy per recipe
5. **live verify**: fetch `live_url` with a cache-buster, run the recipe `cache_check` or compare a content marker against the just-built output; failure here is loud and blocks the "shipped" claim
6. smoke test per recipe (or key pages return 200)
7. screenshot the live page → report: live URL + screenshot + status line

Offers rollback when the recipe defines one.

### /op:sync

Prod → local per recipe (`sync` map: db, images, feed, data dirs). Confirms before overwriting local state. Reports what moved and sizes.

### /op:show

Serve locally per recipe → Playwright screenshots at 1512×982 (14" MacBook) and 375×812 (mobile), 768 optional, both themes when the site has them → short verdict → offers rs `/vibe` for the full scorecard. Screenshot paths are the proof.

### /op:release

Reads the recipe `release` block: version files to bump, publish command, verify URL. Bumps versions in step, writes humanized release notes, tags, publishes, then fetches the published artifact to verify. Generalizes the druck release train; dogfoods on rapid-stack itself.

## Constitution — skills/using-op

~60 lines, injected every session by the SessionStart hook. Rules:

- **Iron law**: no code until one real convention from the target repo is quoted (quote-before-code, attributed: github.com/artttj/quote-before-code, 930 graded runs)
- **No "done" without fresh proof** from this turn: command output, screenshot, or live URL (superpowers verification-before-completion is the deep procedure)
- **End-of-turn git status line** after any turn that changed the tree: `branch — push state — PR url|no PR` via `status_line.py` (`gh pr view`; degrades to local state without gh/remote)
- **Read-only default, co-pilot arming**: "full co-pilot" arms reversible gated actions (stage, commit, branch, push to existing upstream) for the session; "disarm co-pilot" stands down; irreversible actions and production deploys always prompt; an echoed gate phrase must execute in the same turn, never be repeated back idle
- **Arrow-choice decisions**, never open questions when options are enumerable
- **Effort escalation**: suggest xhigh/max or an ultracode workflow before heavy steps; the user decides
- **Recipes**: per-project ops live in `.claude/op.json`; discover, confirm, cache on miss; self-heal on failure
- **Mirror the user's language** (EN/RU); command names and files stay English

## Per-project recipes — .claude/op.json

Committed, non-secret, per repo. Schema (all keys optional; commands refuse gated actions on missing keys instead of guessing):

```json
{
  "serve": "python3 -m http.server 8080",
  "build": "./build.sh",
  "test": "python3 -m pytest -q",
  "deploy": "ssh wolton 'cd /root/workspaces/<proj> && git pull && ./build.sh'",
  "sync": { "db": "<cmd>", "images": "<cmd>", "feed": "<cmd>" },
  "release": { "versions": ["package.json"], "publish": "npm publish", "verify": "<url>" },
  "live_url": "https://sonto.tech",
  "cache_check": "curl -s $URL?v=$BUST | grep <marker>",
  "smoke": ["<url1>", "<url2>"],
  "rollback": "<cmd>"
}
```

`$URL` and `$BUST` are substituted by op at run time (`live_url` and a fresh cache-buster value); they are the only substitutions.

Discovery on first use: read AGENTS.md/CLAUDE.md, scripts/, package.json, existing `.claude/skills` (smith-*, hallmark, druck-release); propose the recipe as an arrow-choice; write the file. On a failing recipe command: rediscover, confirm, update. SSH aliases (wolton) are fine; tokens never enter the file.

## Degradation

- superpowers absent → inline short-procedure fallbacks in each wrapper
- rs absent → generic review subagent instead of `/cr`, skip `/vibe` offers
- no `gh` or no remote → status line reports local branch state, "no PR"
- no recipe key for a gated action → refuse with a clear message, never guess a deploy target
- ship live-verify failure → loud report, offer recipe rollback, never claim shipped
- spec/plan hash mismatch → build blocked, arrow-choice to re-plan or proceed consciously

## Testing

- pytest units for `status_line.py` (pure-function core, injectable git/gh)
- a validate script: every command file has a frontmatter description and its skill dir exists; run locally before release
- pilot: run `/op:show` and `/op:ship` against artttj.de end to end before calling v1 done
- docs: README section in rapid-stack matching its existing terse tone; marketplace.json entry
- dogfood: release op with `/op:release`

## Repo hygiene (same effort, separate commits)

From the 2026-07-16 rapid-stack audit:

- LICENSE copyright still "artttj" → Artem Iagovdik
- `/ui` command references skill `design` from ui-ux-pro-max but resolves to the bundled `design` skill → point at the correct external skill name
- vibe dimensions: README/marketplace say 9, command/skill say 8 → reconcile
- add `.gitignore` (.DS_Store)
- version drift: manifests at 1.3.0 with no tags → reconcile at next release

## Out of scope

plannotator and any browser companion, xlsx/PDF generation, bilingual output, timesheets, Jira/Bitbucket integration, onboarding/map commands, secrets-guard hook (no client tokens on this machine), any vendoring of superpowers skills.

## Decisions log

- Home: sibling plugin in the rapid-stack marketplace — rs keeps its "short aliases" identity; marketplace.json already supports multiple plugins (user choice, 2026-07-16)
- Name: `op` — /op:ship, /op:spec; two keystrokes (user choice)
- Gate: scaled + router — mandatory gate contradicts real usage on small fixes; no gate loses the autonomous-build mode (user choice)
- Wrap over vendor: confirmed in design round 1 (user choice)
